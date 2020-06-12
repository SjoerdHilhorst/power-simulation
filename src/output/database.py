import sqlite3


class Database:
    def __init__(self, env, address):
        self.db_name = env["db_name"] + ".db"
        self.table_name = "server"
        self.create_battery_table(address, env["drop_table_on_start"])

    def create_battery_table(self, address, drop_table):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            columns = "time timestamp, " + " REAL, ".join(address) 

            if drop_table:
                c.execute("DROP TABLE IF EXISTS %s" % self.table_name)

            c.execute("CREATE TABLE IF NOT EXISTS %s (%s)" % (self.table_name, columns))
            conn.commit()

    def write(self, values):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            values = ",".join(str(value) for value in values)
            query = "INSERT INTO %s VALUES (datetime('now'), %s)" % (self.table_name, values)
            c.execute(query)
            conn.commit()
