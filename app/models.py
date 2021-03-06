import sqlite3

class Model():
    def __init__(self, db, table, model):
        self.db = db
        self.table = table
        self.model = model
        self.connection = sqlite3.connect(db + '.sqlite3')
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
    
    def insert(self, values):
        columns = '({})'.format(','.join(self.model.columns))
        values = '("{}")'.format('","'.join(values.values()))
        sql = 'INSERT INTO {} {} VALUES {}'.format(self.model.model_name, columns, values)

        try:
            self.cursor.execute(sql)
            self.connection.commit()
            inserted_id = self.cursor.lastrowid
            print('inserted #{}'.format(inserted_id))

            return inserted_id
        except sqlite3.OperationalError as e:
            # table doesn't exist
            print('creating table...')
            self.create_table(self.model.model_name, columns, values)

    
    def select_all(self):
        sql = 'SELECT * FROM {}'.format(self.model.model_name)
        try:
            cursor = self.connection.execute(sql)
            return list(map(dict, cursor.fetchall()))
        except sqlite3.OperationalError as e:
            return False
   
    def select_one(self, id):
        sql = 'SELECT * FROM {} WHERE ID={}'.format(self.model.model_name, id)
        cursor = self.connection.execute(sql)

        return dict(cursor.fetchone())


    def filter(self, query):
        where = self.build_where(query)
        sql = 'SELECT * FROM {} WHERE {}'.format(self.model.model_name, where[:-4])
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
        sql = 'DELETE FROM {} WHERE ID = "{}"'.format(self.model.model_name, id)

        cursor = self.connection.execute(sql)
        self.connection.commit()


    def update(self, new_data, id):
        update = ''
        for key, value in new_data.items():
            update += '{}="{}",'.format(key, value)

        sql = 'UPDATE {} SET {} WHERE id = {}'.format(self.model.model_name, update[:-1], id)

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
