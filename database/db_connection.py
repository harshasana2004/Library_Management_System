import mysql.connector
import configparser
import os


def connect():
    """ Connect to the MySQL database server """
    try:
        # Create a path to the config file from the current script's location
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_dir, 'config.ini')

        parser = configparser.ConfigParser()
        parser.read(config_path)

        db_config = dict(parser.items('database'))

        conn = mysql.connector.connect(**db_config)
        return conn
    except Exception as err:
        print(f"Database connection failed: {err}")
        return None