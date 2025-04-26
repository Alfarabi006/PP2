import psycopg2
from config import config


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE PhoneBook(
            Name VARCHAR(255) NOT NULL,
            Surname VARCHAR(255) NOT NULL,
            Phone Varchar(255) NOT NULL,
            CONSTRAINT unique_name_surname_phone UNIQUE (Name, Surname, Phone)
        )
        """,
        )
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    create_tables()
