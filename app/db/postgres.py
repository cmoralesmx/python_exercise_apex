from datetime import datetime
import logging
import psycopg2
from .config import config

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
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            raise RuntimeError('Could not initialize DB')

    def initialize(self) -> bool:
        """
        Create the DB when entering the context
        (if it does not exists)
        """
        try:
            command = """
                CREATE TABLE IF NOT EXISTS video_data (
                    video VARCHAR(255) NOT NULL,
                    clip_name VARCHAR(255) NOT NULL,
                    clip_file_extension VARCHAR(5) NOT NULL,
                    clip_duration FLOAT4 NOT NULL,
                    clip_location VARCHAR(255) NOT NULL,
                    insert_timestamp TIMESTAMP NOT NULL,
                    PRIMARY KEY(video, clip_name)
                );
                """
            logging.debug('PosgreSQL database initialization')
            self.cur.execute('SELECT version()')

            logging.debug(self.cur.fetchone())
            self.cur.execute(command)
            self.conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)

    def __enter__(self) -> object:
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

    def insert_record(
        self,
        video: str,
        clip_name: str,
        extension: str,
        duration: float,
        location: str,
    ) -> datetime:
        insert_timestamp: datetime = None
        """Insert the data safely into the DB"""
        command = """INSERT INTO video_data (video, clip_name,
                     clip_file_extension, clip_duration,
                     clip_location, insert_timestamp)
                     VALUES(%s, %s, %s, %s, %s, now())
                     RETURNING insert_timestamp;"""

        try:
            logging.debug(
                f'{video=},v{clip_name=}, {extension=}, {duration=}, {location=}'
            )

            self.cur.execute(
                command, (video, clip_name, extension, duration, location)
            )
            self.conn.commit()
            insert_timestamp = self.cur.fetchone()[0]
            logging.debug(f'Inserted clip: {clip_name} @ {insert_timestamp}')
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)

        return insert_timestamp
