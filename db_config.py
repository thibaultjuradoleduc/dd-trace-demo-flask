import os

db_host = os.environ.get('DB_HOST', 'mysql')
db_username = os.environ.get('DB_USERNAME', 'demo')
db_password = os.environ.get('DB_PASSWORD', 'demo')
db_name = os.environ.get('DB_NAME', 'demo')
