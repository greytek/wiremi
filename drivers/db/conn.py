from dotenv import dotenv_values
config = dotenv_values(".env")

db_url = config["DB_SERVER_LIVE"]
db_name = config["DB_NAME_LIVE"]
db_admin = config["DB_USER_LIVE"]
db_pass = config["DB_PASSWORD_LIVE"]

db_url_local = config['DB_SERVER_LOCAL']
db_name_local = config['DB_NAME_LOCAL']

connection_string_live = "Driver={ODBC Driver 17 for SQL Server};" \
                    f"Server={db_url};" \
                    f"Database={db_name};" \
                    f"Uid={db_admin};" \
                    f"Pwd={db_pass};" \
                    "Encrypt=yes;" \
                    "TrustServerCertificate=no;" \
                    "Connection Timeout=30;"

connection_string_local = "Driver={ODBC Driver 17 for SQL Server};" \
                    f"Server={db_name_local};" \
                    f"Database={db_name_local};" \
                    "TrustServerCertificate=Yes;" \
                    "Connection Timeout=30;"
