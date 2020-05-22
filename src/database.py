import sqlite3


class Database:
    def __init__(self, env, address):
        self.db_name = env["db_name"] + ".db"
        self.create_battery_table(address, env["drop_table_on_start"])

    def create_battery_table(self, address, drop_table):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            columns = " REAL, ".join(address) + " REAL, time timestamp"
            table_name = "battery"

            if drop_table:
                c.execute("DROP TABLE IF EXISTS %s" % table_name)

            c.execute("CREATE TABLE IF NOT EXISTS %s (%s)" % (table_name, columns))
            conn.commit()

    def write(self, table, values):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            values = ",".join(str(value) for value in values)
            query = "INSERT INTO %s VALUES (%s, datetime('now'))" % (table, values)
            c.execute(query)
            conn.commit()
