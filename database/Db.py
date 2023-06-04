import sqlite3


class DB:
    def __init__(self):
        self.db = "./database/data.sqlite"
        self.conn = sqlite3.connect(self.db)
        self.c = self.conn.cursor()
        self.c.execute(
            """
        CREATE TABLE IF NOT EXISTS guild(guild_id INT, welcome_channel INT)
        """
        )
        self.conn.commit()

    # mai bana rha hu , abhi tak ye koi kam ka nhi ha
