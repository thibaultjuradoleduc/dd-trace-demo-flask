import os

db_host = os.environ.get('DB_HOST', 'localhost')
db_username = os.environ.get('DB_USERNAME', 'admin')
db_password = os.environ.get('DB_PASSWORD', 'password')
db_name = os.environ.get('DB_NAME', 'defaultdb')
