import json

import psycopg2


# DB operations
class DBConnection:
    def __init__(self, service_uri, topic_name):
        self.service_uri = service_uri
        self.topic_name = topic_name
        self.connection = None

    def create_table(self):
        """
        Creates table if not exist
        """
        cursor = self.connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS {} (id SERIAL PRIMARY KEY, status INTEGER, response_time FLOAT, title VARCHAR);".format(self.topic_name))
        cursor.close()

    def open(self):
        """
        Creates new connections to database
        """
        if self.connection is None:
            print("Open new connection with DB: {}".format(self.service_uri))
            self.connection = psycopg2.connect(self.service_uri)
        print("Create new database if not exist: {}".format(self.topic_name))
        self.create_table()

    def close(self):
        """
        Closes and commits open connection
        """
        if self.connection:
            self.connection.commit()
            self.connection.close()

    def insert_message(self, message):
        """
        Insert new messages into DB

          args:
            message (dict): json object from kafka consumer
        """
        parsed = json.loads(message)
        cursor = self.connection.cursor()

        cursor.execute(
          "INSERT INTO monitoring (status, response_time, title) VALUES (%s, %s, %s)",
          (parsed['status_code'], parsed['response_time'], parsed['page_title'])
        )

        cursor.close()
        print("Successfully inserted: {}".format(message.decode('utf-8')))

    def fetchAll(self):
        """
        Fetches all the data from the main table and prints to STDOUT
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM {};".format(self.topic_name))

        result = cursor.fetchall()
        print("Print All Results:\n {}".format(result))
