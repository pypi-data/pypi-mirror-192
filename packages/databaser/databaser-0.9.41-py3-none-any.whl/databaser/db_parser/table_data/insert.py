import re


class Insert:

    def __init__(self, table_name: str, data: dict, table_quote: str = "", field_quote: str = "", value_quote: bool = False, schema_name: str = "public"):
        self.table_name = table_name
        self.schema_name = schema_name
        self.fields = []
        self.values = []

        self.table_quote = table_quote
        self.field_quote = field_quote
        self.value_quote = "\'" if value_quote else ""

        if len(data.keys()) == 0:
            raise Exception("There is no data to insert")

        for field in data.keys():
            if data[field] is None:
                self.values.append("NULL")
            else:
                val = "{quote}{value}{quote}".format(quote="\'", value=data[field].replace("'", "''"))
                self.values.append(val)

            self.fields.append(field)

    def get_sql(self):
        fields = self.fields
        values = self.values

        return f"""INSERT INTO {f"{self.table_quote}{self.schema_name}{self.table_quote}." if self.schema_name != '' else ""}{self.table_quote}{self.table_name}{self.table_quote} ({self.field_quote}{f'{self.field_quote}, {self.field_quote}'.join(fields)}{self.field_quote}) VALUES ({f', '.join(values)});"""
