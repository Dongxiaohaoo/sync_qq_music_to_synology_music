import sqlite3


class DB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        sql = "CREATE TABLE IF NOT EXISTS " + table_name + " ("
        for column in columns:
            sql += column + " TEXT, "
        sql = sql[:-2] + ")"
        self.cursor.execute(sql)
        self.conn.commit()

    def insert_data(self, table_name, data):
        sql = "INSERT INTO " + table_name + " VALUES ("
        for value in data:
            if isinstance(value, int):
                sql += str(value) + ", "
                continue
            if isinstance(value, str):
                sql += "\"" + value + "\", "
                continue
            raise ValueError("Invalid data type")
        sql = sql[:-2] + ")"
        # print(sql)
        self.cursor.execute(sql)
        self.conn.commit()

    def select_data(self, table_name, column_name, condition):
        sql = "SELECT " + column_name + " FROM " + table_name + " WHERE " + condition
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def update_data(self, table_name, column_name, new_value, condition):
        sql = "UPDATE " + table_name + " SET " + column_name + " = '" + new_value + "' WHERE " + condition
        self.cursor.execute(sql)
        self.conn.commit()

    def delete_data(self, table_name, condition):
        sql = "DELETE FROM " + table_name + " WHERE " + condition
        self.cursor.execute(sql)
        self.conn.commit()
