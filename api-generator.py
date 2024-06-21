import json
import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.types import INTEGER, VARCHAR, BOOLEAN, DATE, FLOAT, DECIMAL, TIMESTAMP

def serialize_column(column):
    return {
        'name': column['name'],
        'type': str(column['type']),
        'nullable': column['nullable'],
        'default': column['default'],
        'primary_key': column['primary_key']
    }

# Replace with your actual database connection details
DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
ENDPOINT = 'your-database-endpoint'  # Change it to your DB endpoint
USER = 'your-username'               # Change it to your DB username
PASSWORD = 'your-password'           # Change it to your DB password
PORT = 5432                          # Change it to your DB port
DATABASE = 'your-database-name'      # Change it to your DB name

# Create the database URL
DATABASE_URL = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}"

# Create an engine and connect to the database
engine = create_engine(DATABASE_URL)
connection = engine.connect()

# Use the inspector to get the schema information
inspector = inspect(engine)

# Get table names
tables = inspector.get_table_names()

# Get schema relations
schema = {}
for table in tables:
    columns = inspector.get_columns(table)
    foreign_keys = inspector.get_foreign_keys(table)
    primary_key = inspector.get_primary_keys(table)
    
    schema[table] = {
            'columns': [serialize_column(col) for col in columns],
            'primary_key': primary_key,
            'foreign_keys': foreign_keys
        }

# Close the connection
connection.close()

# Convert the schema dictionary to a JSON file
with open('schema.json', 'w') as json_file:
    json.dump(schema, json_file, indent=4)
