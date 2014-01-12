class Whitelist:
    def __init__(self):
        self.tabledata = dict()
        self.tablehandlers = dict()

    def add(self, table, columns, handler=None):
        self.tabledata[table] = columns
        self.tablehandlers[table] = handler

    def known_columns(self, table):
        known_plain = list()
        columns = self.table(table)
        for column in columns:
            if column[0] == '_' and ':' in column:
                function, name = column.split(':', 1)
                known_plain.append(name)
            else:
                known_plain.append(column)
        return known_plain

    def process(self, table):
        known_columns = list()
        columns = self.table(table)
        if self.tabledef(table) == 'nodata':
            return
        for column in columns:
            if column[0] == '_' and ':' in column:
                function, name = column.split(':', 1)
                function = function.lstrip('_')
                known_columns.append((function, name))
            else:
                known_columns.append((None, column))
        return known_columns

    def get_tables(self):
        return [self.name_only(e) for e in self.tabledata.keys() if '_ignore:' not in e]

    def name_only(self, id):
        if id[0] == '_' and ':' in id:
            function, name = id.split(':', 1)
            return name
        return id

    def function_only(self, id):
        if id[0] == '_' and ':' in id:
            function, name = id.split(':', 1)
            function = function.lstrip('_')
            return function

    # Return a table's columns. Useful when handlers and names were combined
    def table(self, table):
        if table in self.tabledata.keys():
            return self.tabledata[table]
        else:
            return False

    # Legacy fetch the table's handlers
    def tabledef(self, table):
        known_tables = self.tabledata.keys()
        if table in known_tables:
            return self.tablehandlers[table]
        else:
            return False

    def columnmap(self, columns):
        plain_columns = map(self.name_only, columns)
        mapped_columns = dict(zip(plain_columns, columns))
        return mapped_columns

    def update(self, table, columns=[], handler='save'):
        table_desc = self.table(self.name_only(table)) #Store the current def
        print table_desc
        del(self.tabledata[table])
        old_columns = self.columnmap(table_desc)
        new_columns = self.columnmap(columns)
        for column, value in new_columns.items():
            old_columns[column] = value
        self.tabledata[table] = old_columns.values()
        if handler != 'save':
            self.tablehandlers[table] = handler
        print self.tabledata[table] 
