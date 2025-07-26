import mysql.connector
import configparser
import os


def run_sql_script():
    """
    Connects to MySQL server, creates the database if it doesn't exist,
    and then creates and populates the tables.
    """
    conn = None
    try:
        # --- Read Config ---
        base_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_dir, 'config.ini')

        parser = configparser.ConfigParser()
        parser.read(config_path)
        db_config = dict(parser.items('database'))

        # This script needs to connect without a specific database first
        # to create it. The SQL file handles the CREATE and USE commands.

        # --- Connect to MySQL Server ---
        conn = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conn.cursor()
        print("Successfully connected to MySQL server.")

        # --- Read and Execute the entire SQL file ---
        sql_file_path = os.path.join(base_dir, "database", "setup_database.sql")

        with open(sql_file_path, "r") as file:
            # The SQL file contains multiple commands; execute them one by one
            sql_commands = file.read().split(';')
            for command in sql_commands:
                if command.strip():
                    cursor.execute(command)

        conn.commit()
        print("\n✅ Database setup complete! The library is populated with default books and students.")

    except mysql.connector.Error as err:
        print(f"❌ Database setup failed: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection is closed.")


if __name__ == "__main__":
    run_sql_script()
