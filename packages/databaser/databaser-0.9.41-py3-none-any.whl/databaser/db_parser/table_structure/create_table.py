from typing import List, Optional

from pydantic import BaseModel

from databaser.db_parser.table_structure.references_fk import ReferencesFK


class TableField(BaseModel):
    name: str
    data_type: str
    not_null: bool = False
    primary_key: bool = False
    context_data_type: Optional[str] = "Unknown"
    constraint: Optional[str] = ""
    default: Optional[str]
    references: Optional[str]


class CreateTable:
    def __init__(self, table_name: str, table_fields: List[TableField], schema_name: str ="public", table_quote: str = "", field_quote: str = ""):
        self.table_name = table_name
        self.schema_name = schema_name

        self.table_quote = table_quote
        self.field_quote = field_quote

        self.fields = table_fields

    def parse_fields(self) -> str:
        fields = ""
        count = len(self.fields)

        primary_keys = list()

        for index, field in enumerate(self.fields):
            not_null = ' NOT NULL' if field.not_null else ' NULL'
            not_null = not_null if field.primary_key is False else ''
            constraint = ' ' + field.constraint if field.primary_key is False else ''
            default = field.default

            if field.primary_key:
                primary_keys.append(field.name)

            fields += f"{self.field_quote}{field.name}{self.field_quote} {field.data_type}{constraint}{not_null} {f' DEFAULT {default}' if default is not None else ''} {field.references if field.references is not None else ''}"
            fields += ",\n"
            if index >= (count - 1):
                fields += f"PRIMARY KEY ({','.join(primary_keys)})"

        return fields

    def get_sql(self):
        fields = self.parse_fields()

        return f"""CREATE TABLE IF NOT EXISTS {self.table_quote}{self.schema_name}{self.table_quote}.{self.table_quote}{self.table_name}{self.table_quote} (
            {fields}
        );"""
