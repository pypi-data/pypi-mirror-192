"""
EXPERIMENTAL
Async interface using aiosqlite
"""

import logging
import os
import re
from contextlib import asynccontextmanager

import aiosqlite

from firepit.asyncstorage import AsyncStorage
from firepit.query import Column, Limit, Offset, Order, Projection, Query
from firepit.schemas import INTERNAL_SCHEMAS
from firepit.sqlitestorage import _in_subnet, _match, _match_bin, _like_bin
from firepit.sqlstorage import DB_VERSION
from firepit.validate import validate_name, validate_path


logger = logging.getLogger(__name__)


@asynccontextmanager
async def transaction(db):
    try:
        cursor = await db.execute('BEGIN')
        yield cursor
    finally:
        await db.commit()
        await cursor.close()


class AsyncSqliteStorage(AsyncStorage):
    class Placeholder:
        def __str__(self, _offset=0):
            return '?'

    def __init__(self,
                 connstring: str,
                 session_id: str):
        self.placeholder = '?'
        self.dialect = 'sqlite3'
        self.connstring = connstring
        self.session_id = session_id
        self.conn = None

    async def _create_funcs(self):
        # Create functions for IP address subnet membership checks
        await self.conn.create_function('in_subnet', 2, _in_subnet)

        # Create function for SQL MATCH
        await self.conn.create_function("match", 2, _match)
        await self.conn.create_function("match_bin", 2, _match_bin)
        await self.conn.create_function("like_bin", 2, _like_bin)

    def _create_table_stmt(self, name, schema):
        pass  #TODO: how do we handle constraints?

    async def create(self, ssl_context=None):
        """
        Create a new "session" (sqlite3 file).  Fail if it already exists.
        """
        logger.debug('Creating storage for session %s', self.session_id)
        self.conn = await aiosqlite.connect(self.connstring)
        await self._create_funcs()

        type_map = {'BIGINT': 'INTEGER'}
        async with transaction(self.conn) as cursor:
            # create tables, etc.
            for schema in INTERNAL_SCHEMAS:
                stmt = schema.create_stmt(type_map=type_map)
                logger.debug('%s', stmt)
                await cursor.execute(stmt)
            # Record db version
            await self._set_meta('dbversion', DB_VERSION)

    async def attach(self):
        """
        Attach/connect to an existing session.  Fail if it doesn't exist.
        """
        logger.debug('Attaching to storage for session %s', self.session_id)
        self.conn = await aiosqlite.connect(self.connstring)
        await self._create_funcs()
        #TODO: fail if it doesn't exist

    async def cache(self,
                    query_id: str,
                    bundle: dict):
        """
        Ingest a single, in-memory STIX bundle, labelled with `query_id`.
        """
        #TODO:writer = AsyncSqlWriter(self.conn, session_id=self.session_id)
        #TODO:splitter = AsyncSplitWriter(writer, query_id=str(query_id))
        #TODO:await splitter.init()

        #TODO:for obj in _transform(bundle):
        #TODO:    await splitter.write(obj)
        #TODO:await splitter.close()
        raise NotImplementedError('cache')

    async def tables(self):
        async with self.conn.execute("SELECT name FROM sqlite_master WHERE type='table'") as cursor: #TODO: extract to common location
            rows = await cursor.fetchall()
        return [i['name'] for i in rows
                if not i['name'].startswith('__') and
                not i['name'].startswith('sqlite')]

    async def views(self):
        """Get all view names"""
        async with self.conn.execute('SELECT name FROM __symtable') as cursor: #TODO: extract to common location
            rows = await cursor.fetchall()
        return [row['name'] for row in rows]

    async def table_type(self, viewname):
        """Get the SCO type for table/view `viewname`"""
        validate_name(viewname)
        stmt = 'SELECT "type" FROM "__symtable" WHERE name = ?' #TODO: extract to common location
        async with self.conn.execute(stmt, (viewname,)) as cursor:
            row = await cursor.fetchone()
        return row['type'] if row else None

    async def types(self, private=False):
        stmt = ("SELECT name FROM sqlite_master WHERE type='table'"
                " EXCEPT SELECT name FROM __symtable") #TODO: extract to common location
        async with self.conn.execute(stmt) as cursor:
            rows = await cursor.fetchall()
        if private:
            return [i['name'] for i in rows]
        return [i['name'] for i in rows
                if not i['name'].startswith('__') and
                not i['name'].startswith('sqlite')]

    async def columns(self, viewname):
        """Get the column names (properties) of `viewname`"""
        validate_name(viewname)
        stmt = f'PRAGMA table_info("{viewname}")'
        async with self.conn.execute(stmt) as cursor:
            try:
                mappings = await cursor.fetchall()
                if mappings:
                    result = [e["name"] for e in mappings]
                else:
                    result = []
                logger.debug('%s columns = %s', viewname, result)
            except aiosqlite.OperationalError as e:
                logger.error('%s', e)
                result = []
        return result

    async def schema(self, viewname=None):
        """Get the schema (names and types) of `viewname`"""
        if viewname:
            validate_name(viewname)
            stmt = f'PRAGMA table_info("{viewname}")'
            async with self.conn.execute(stmt) as cursor:
                rows = await cursor.fetchall()
            result = [{k: v for k, v in row.items() if k in ['name', 'type']}
                      for row in rows]
        else:
            result = []
            for obj_type in await self.types(True):
                stmt = f'PRAGMA table_info("{obj_type}")'
                async with self.conn.execute(stmt) as cursor:
                    rows = await cursor.fetchall()
                for row in rows:
                    result.append({
                        'table': obj_type,
                        'name': row['name'],
                        'type': row['type']
                    })
        return result

    async def delete(self):
        """Delete ALL data in this store"""
        await self.conn.close()
        try:
            os.remove(self.connstring)
        except FileNotFoundError:
            pass

    async def set_appdata(self, viewname, data):  #TODO: this is the same as AsyncStorage except for placeholders and the DB execute line
        """Attach app-specific data to a viewname"""
        validate_name(viewname)
        stmt = ('UPDATE "__symtable" SET appdata = ?'
                ' WHERE name = ?')
        async with transaction(self.conn) as cursor:
            await cursor.execute(stmt, (data, viewname))

    async def get_appdata(self, viewname):
        """Retrieve app-specific data for a viewname"""
        validate_name(viewname)
        stmt = 'SELECT appdata FROM "__symtable" WHERE name = ?'
        async with self.conn.execute(stmt, (viewname,)) as cursor:
            row = await cursor.fetchone()
        if not row:
            return None
        if 'appdata' in row:
            return row['appdata']
        return dict(row[0])

    async def get_view_data(self, viewnames=None):
        """Retrieve information about one or more viewnames"""
        if viewnames:
            placeholders = ', '.join(['?'] * len(viewnames))
            stmt = f'SELECT * FROM "__symtable" WHERE name IN ({placeholders});'
            async with self.conn.execute(stmt, tuple(viewnames)) as cursor:
                rows = await cursor.fetchall()
        else:
            stmt = 'SELECT * FROM "__symtable";'
            async with self.conn.execute(stmt) as cursor:
                rows = await cursor.fetchall()
        return [dict(row) for row in rows]

    async def run_query(self, query: Query):
        query_text, query_values = query.render(self.placeholder, self.dialect)
        async with self.conn.execute(query_text, query_values) as cursor:
            rows = await cursor.fetchall()
        return rows

    #TODO? async def fetch(self, query, *args):
    #TODO?    """Passthrough to underlying DB"""

    async def remove_view(self, viewname):
        """Remove view `viewname`"""
        validate_name(viewname)
        async with transaction(self.conn) as cursor:
            await cursor.execute(f'DROP VIEW IF EXISTS "{viewname}"')
            await self._drop_name(cursor, viewname)

    # "Private" API
    # These account for difference between aiosqlite and asyncpg
    async def _get_view_def(self, viewname):
        stmt = ("SELECT sql"
                " FROM sqlite_master"
                " WHERE type = 'view'"
                " AND name = ?")
        async with self.conn.execute(stmt, (viewname,)) as cursor:
            view = await cursor.fetchone()
        if view:
            slct = view['sql']
            return slct.replace(f'CREATE VIEW "{viewname}" AS ', '')

        # Must be a table
        return f'SELECT * FROM "{viewname}"'

    async def _set_meta(self, name, value):
         #TODO: need _placeholders method to make this common?
        stmt = ('INSERT INTO "__metadata" (name, value)'
                f' VALUES ({self.placeholder}, {self.placeholder});')
        await self.conn.execute(stmt, (name, value))
        #await self.commit()

    async def _new_name(self, cursor, name, sco_type):
        stmt = ('INSERT INTO "__symtable" (name, type)'
                f' VALUES ({self.placeholder}, {self.placeholder})'
                ' ON CONFLICT (name) DO UPDATE SET type = EXCLUDED.type')
        await cursor.execute(stmt, (name, sco_type))

    async def _drop_name(self, cursor, name):
        stmt = f'DELETE FROM "__symtable" WHERE name = {self.placeholder}'
        await cursor.execute(stmt, name)

    async def _create_view(self, viewname, select, sco_type, deps=None):
        """Overrides parent"""
        validate_name(viewname)
        is_new = True
        async with transaction(self.conn) as cursor:
            if not deps:
                deps = []
            elif viewname in deps:
                is_new = False
                # Get the query that makes up the current view
                slct = await self._get_view_def(viewname)
                if not self._is_sql_view(viewname):
                    # Must be a table...
                    await cursor.execute(f'ALTER TABLE "{viewname}" RENAME TO "_{viewname}"')
                    slct = slct.replace(viewname, f'_{viewname}')
                # Swap out the viewname for its definition
                select = re.sub(f'FROM "{viewname}"', f'FROM ({slct}) AS tmp', select, count=1)
                select = re.sub(f'"{viewname}"', 'tmp', select)
            await cursor.execute(f'CREATE OR REPLACE VIEW "{viewname}" AS {select}')
            if is_new:
                await self._new_name(cursor, viewname, sco_type)

    async def _is_sql_view(self, name):
        stmt = ("SELECT sql from sqlite_master"
                " WHERE type='view' and name=?")
        async with self.conn.execute(stmt, (name,)) as cursor:
            view = await cursor.fetchone()
        return view is not None
