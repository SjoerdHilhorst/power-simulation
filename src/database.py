import sqlite3


class Database:
    def __init__(self, env, address):
        self.conn = sqlite3.connect(env["db_name"] + ".db")
        self.c = self.conn.cursor()
        self.create_battery_table(address, env["drop_table_on_start"])

    def create_battery_table(self, address, drop_table):
        columns = " REAL, ".join(address) + "REAL, time timestamp"
        tableName = "battery"

        if drop_table:
            self.c.execute("DROP TABLE IF EXISTS %s" % tableName)

        self.c.execute("CREATE TABLE IF NOT EXISTS %s (%s)" % (tableName, columns))
        self.conn.commit()

    def write(self, table, values):
        values = ",".join(str(value) for value in values)
        query = "INSERT INTO %s VALUES (%s, datetime('now'))" % (table, values)
        self.c.execute(query)
        self.conn.commit()

