import sqlite3

class Model():
    def __init__(self, db, table):
        self.db = db
        self.table = table
        self.connection = sqlite3.connect(db + '.sqlite3')
        self.connection.row_factory = sqlite3.Row

    
    def insert(self, row):
        columns = '({})'.format(','.join(row.keys()))
        values = '("{}")'.format('","'.join(row.values()))
        sql = 'INSERT INTO {} {} VALUES {}'.format(self.table, columns, values)

        try:
            self.connection.execute(sql)
            self.connection.commit()
            print('inserted')
        except sqlite3.OperationalError as e:
            # table doesn't exist
            print('creating table...')
            self.create_table(self.table, columns, row)

    
    def select_all(self):
        sql = 'SELECT * FROM {}'.format(self.table)
        cursor = self.connection.execute(sql)

        return list(map(dict, cursor.fetchall()))

   
    def select_one(self, id):
        sql = 'SELECT * FROM {} WHERE ID={}'.format(self.table, id)
        cursor = self.connection.execute(sql)

        return dict(cursor.fetchone())


    def filter(self, query):
        where = self.build_where(query)
        sql = 'SELECT * FROM {} WHERE {}'.format(self.table, where[:-4])
        cursor = self.connection.execute(sql)

        return list(map(dict, cursor.fetchall()))


    def create_table(self, table, columns, row):
        columns = '(ID INTEGER PRIMARY KEY AUTOINCREMENT,' + columns[1:]
        sql = 'CREATE TABLE IF NOT EXISTS {} {}'.format(table, columns)
        self.connection.execute(sql)
        self.connection.commit()

        # try to insert again
        self.create(row)


    def delete(self, id):
        sql = 'DELETE FROM {} WHERE ID = "{}"'.format(self.table, id)

        cursor = self.connection.execute(sql)
        self.connection.commit()


    def update(self, sets, id):
        sets = '{} = "{}"'.format(sets[0], sets[1])
        sql = 'UPDATE {} SET {} WHERE id = {}'.format(self.table, sets, id)

        try:
            cursor = self.connection.execute(sql)
            self.connection.commit()
            return True
        except Exception as e:
            print(e)
    

    def build_where(self, query):
        where = ''
        for key, value in query.items():
            where += '{}="{}" AND '.format(key, value)

        return where
