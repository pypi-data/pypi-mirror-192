from typing import List

import function as function

from databaser.engine.engine import DatabaseEngine
from databaser.db_parser.table_structure.create_table import TableField
from databaser.pgsql import Query

class DataModel:
    table_name = None
    fields: List[TableField] = []

    def __init__(self, schema_name: str = "public", conn_string: dict = {}, server_name: str = "pgsql"):
        self.server_name = server_name

        self.__sql = []
        self.schema_name = schema_name
        self.conn_string = conn_string


    def __get_fields(self):
        fields = []
        for field in self.fields:
            fields.append(field.name)

        return fields

    def count(self):
        sql = Query(self.server_name).count(self.table_name, self.schema_name)
        self.__sql.append(sql)
        return self

    def get(self, fields: List = None, condition: dict = {}, joins: dict = {},
                 group_by: list = [], order_by: dict = {}, limit: int = 0, skip: int = 0):

        if fields is None:
            # fields = self.__get_fields()
            fields = None

        sql = Query(
            self.server_name
        ).find(self.table_name, fields, condition, joins, group_by, order_by, limit, skip, schema_name=self.schema_name).get_sql()
        self.__sql.append(sql)
        return self

    def get_one(self, fields: List[str] = None, condition: dict = {}, joins: dict = {}, group_by: list = [], order_by: dict = {}):
        sql = Query(
            self.server_name
        ).find(self.table_name, fields, condition, joins, limit=1, schema_name=self.schema_name, group_by=group_by, order_by=order_by).get_sql()

        self.__sql.append(sql)

        return self

    def insert(self, data: dict, value_quote: bool = True):
        self.on_insert()

        sql = Query(
            self.server_name
        ).insert(self.table_name, data=data, value_quote=value_quote, schema_name=self.schema_name).get_sql()
        self.__sql.append(sql)
        return self

    def update(self, data: dict, conditions: dict, value_quote: bool = True):
        self.on_update()

        sql = Query(
            self.server_name
        ).update(self.table_name, data=data, conditions=conditions, value_quote=value_quote, schema_name=self.schema_name).get_sql()
        self.__sql.append(sql)
        return self

    def delete(self, data: dict, conditions: dict, value_quote: bool = True):
        self.on_delete()

        sql = Query(
            self.server_name
        ).delete(self.table_name, conditions=conditions, value_quote=value_quote, schema_name=self.schema_name).get_sql()
        self.__sql.append(sql)
        return self

    def get_transactions(self):
        return self.__sql

    def add_transaction(self, sql: str):
        self.__sql.append(sql)
        return self

    def show(self, fetch_one: bool = False):
        return DatabaseEngine(**self.conn_string).execute(self.__sql, has_return=True, return_many=(not fetch_one))

    def commit(self):
        res = DatabaseEngine(**self.conn_string).execute(self.__sql, transaction=True)
        self.on_commit()
        return res

    def set_schema_name(self, schema_name: str = "public"):
        self.schema_name = schema_name
        return self.schema_name

    def get_schema_name(self) -> str:
        return self.schema_name

    def on_insert(self, func: function = None):
        if func:
            func()
        return self

    def on_update(self, func: function = None):
        if func:
            func()
        return self

    def on_commit(self, func: function = None):
        if func:
            func()
        return self

    def on_delete(self, func: function = None):
        if func:
            func()
        return self
