import logging
import psycopg2
from db.config import config
from db.DbClass import DbClass

# setup logging
my_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=my_format)

class PostgresDB(object):
    """
    Context manager isolating DB concerns
    """
    def __init__(self) -> object:
        """
        Connect to the DB on context initialization
        use the settings read form config.ini
        """
        try:
            params = config()
            self.conn = psycopg2.connect(**params)
            logging.debug('DB connection established')
            self.cur = self.conn.cursor()

            logging.debug('PosgreSQL database version')
            self.cur.execute('SELECT version()')

            logging.debug(self.cur.fetchone())
            
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)


    def __enter__(self) -> object:
        """
        Create the DB when entering the context 
        (if it does not exists)
        """
        try:
            command = (
                """
                CREATE TABLE IF NOT EXISTS video_data (
                    clip_id SERIAL PRIMARY KEY,
                    clip_name VARCHAR(255) NOT NULL,
                    clip_file_extension VARCHAR(5) NOT NULL,
                    clip_duration INTEGER NOT NULL,
                    clip_location VARCHAR(255) NOT NULL,
                    insert_timestamp TIMESTAMP NOT NULL
                );
                """
            )
            self.cur.execute(command)
            self.conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)

        return self


    def __exit__(self, ctx_type, ctx_value, ctx_traceback) -> None:
        """Close the cursor an connection when exiting the context"""
        try:
            self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
        finally:
            if self.conn is not None:
                self.conn.close()
            logging.debug('Databse connection closed.')


    def insert_record(self, name:str, extension:str, duration:int, location:str) -> int:
        clip_id = None
        """Insert the data safely into the DB"""
        command = """INSERT INTO video_data (clip_name, clip_file_extension, clip_duration, clip_location, insert_timestamp)
                     VALUES(%s, %s, %s, %s, now()) RETURNING clip_id;"""

        try:
            self.cur.execute(command, (name, extension, duration, location))
            clip_id = self.cur.fetchone()[0]
            logging.debug(f"Inserted clip: {clip_id}")
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
        
        return clip_id
