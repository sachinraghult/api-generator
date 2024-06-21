import json
from sqlalchemy import create_engine, inspect

# Connection details
USER = 'your_username'
PASSWORD = 'your_password'
SERVER = 'your_server_address'
PORT = 1433  # Default port for SQL Server
DATABASE = 'your_database'

# Create the database URL
DATABASE_URL = f'mssql+pymssql://{USER}:{PASSWORD}@{SERVER}:{PORT}/{DATABASE}'

def serialize_column(column):
    return {
        'name': column['name'],
        'type': str(column['type']),
        'nullable': column['nullable'],
        'default': column['default']
    }

# Create an engine and connect to the database
try:
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
        primary_key = inspector.get_pk_constraint(table).get('constrained_columns', [])
        indexes = inspector.get_indexes(table)

        schema[table] = {
            'columns': [serialize_column(col) for col in columns],
            'primary_key': primary_key,
            'foreign_keys': foreign_keys,
            'indexes': indexes
        }

    # Close the connection
    connection.close()

    # Convert the schema dictionary to a JSON file
    with open('schema.json', 'w') as json_file:
        json.dump(schema, json_file, indent=4)

except Exception as e:
    print(f"Error: {e}")

import json

# Example JSON schema (replace with your schema loading logic)
json_schema = '''
{
    "Table1": {
        "columns": [
            {"name": "id", "type": "INT"},
            {"name": "name", "type": "VARCHAR"},
            {"name": "age", "type": "INT"}
        ],
        "primary_key": ["id"],
        "foreign_keys": [],
        "indexes": []
    },
    "Table2": {
        "columns": [
            {"name": "id", "type": "INT"},
            {"name": "description", "type": "VARCHAR"}
        ],
        "primary_key": ["id"],
        "foreign_keys": [],
        "indexes": []
    }
}
'''

def generate_java_classes(schema):
    java_classes = []

    for table_name, table_info in schema.items():
        # Generate entity class
        entity_class = f'''
import javax.persistence.*;

@Entity
@Table(name = "{table_name}")
public class {table_name.capitalize()} {{
    // Fields
    {"".join(f"@Column\nprivate {col["type"]} {col["name"]};\n" for col in table_info["columns"])}

    // Getters and setters
    {"".join(f"public {col["type"]} get{col["name"].capitalize()}() {{ return {col["name"]}; }}\n" +
             f"public void set{col["name"].capitalize()}({col["type"]} {col["name"]}) {{ this.{col["name"]} = {col["name"]}; }}\n"
             for col in table_info["columns"])}
}}
'''
        java_classes.append(entity_class)

        # Generate repository interface
        repository_class = f'''
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface {table_name.capitalize()}Repository extends JpaRepository<{table_name.capitalize()}, {table_info["columns"][0]["type"]}> {{
    // Additional methods can be added here if needed
}}
'''
        java_classes.append(repository_class)

        # Generate service class
        service_class = f'''
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class {table_name.capitalize()}Service {{

    @Autowired
    private {table_name.capitalize()}Repository repository;

    // Example methods
    public List<{table_name.capitalize()}> getAll{table_name.capitalize()}() {{
        return repository.findAll();
    }}

    public {table_name.capitalize()} get{table_name.capitalize()}ById({table_info["columns"][0]["type"]} id) {{
        return repository.findById(id).orElse(null);
    }}

    public {table_name.capitalize()} create{table_name.capitalize()}({table_name.capitalize()} {table_name.lower()}) {{
        return repository.save({table_name.lower()});
    }}

    public {table_name.capitalize()} update{table_name.capitalize()}({table_info["columns"][0]["type"]} id, {table_name.capitalize()} {table_name.lower()}) {{
        {table_name.lower()}.setId(id);
        return repository.save({table_name.lower()});
    }}

    public void delete{table_name.capitalize()}({table_info["columns"][0]["type"]} id) {{
        repository.deleteById(id);
    }}
}}
'''
        java_classes.append(service_class)

        # Generate controller class
        controller_class = f'''
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/{table_name.lower()}s")
public class {table_name.capitalize()}Controller {{

    @Autowired
    private {table_name.capitalize()}Service {table_name.lower()}Service;

    // CRUD operations
    @GetMapping("/")
    public List<{table_name.capitalize()}> getAll{table_name.capitalize()}s() {{
        return {table_name.lower()}Service.getAll{table_name.capitalize()}();
    }}

    @PostMapping("/")
    public {table_name.capitalize()} create{table_name.capitalize()}(@RequestBody {table_name.capitalize()} {table_name.lower()}) {{
        return {table_name.lower()}Service.create{table_name.capitalize()}({table_name.lower()});
    }}

    @GetMapping("/{table_info["columns"][0]["name"]}")
    public {table_name.capitalize()} get{table_name.capitalize()}ById(@PathVariable {table_info["columns"][0]["type"]} {table_info["columns"][0]["name"]}) {{
        return {table_name.lower()}Service.get{table_name.capitalize()}ById({table_info["columns"][0]["name"]});
    }}

    @PutMapping("/{table_info["columns"][0]["name"]}")
    public {table_name.capitalize()} update{table_name.capitalize()}(@PathVariable {table_info["columns"][0]["type"]} {table_info["columns"][0]["name"]}, @RequestBody {table_name.capitalize()} {table_name.lower()}) {{
        return {table_name.lower()}Service.update{table_name.capitalize()}({table_info["columns"][0]["name"]}, {table_name.lower()});
    }}

    @DeleteMapping("/{table_info["columns"][0]["name"]}")
    public void delete{table_name.capitalize()}(@PathVariable {table_info["columns"][0]["type"]} {table_info["columns"][0]["name"]}) {{
        {table_name.lower()}Service.delete{table_name.capitalize()}({table_info["columns"][0]["name"]});
    }}
}}
'''
        java_classes.append(controller_class)

    return java_classes

def write_java_files(java_classes):
    for index, java_class in enumerate(java_classes):
        with open(f'{index + 1}.java', 'w') as file:
            file.write(java_class)

# Parse JSON schema
schema = json.loads(json_schema)

# Generate Java classes
java_classes = generate_java_classes(schema)

# Write Java files
write_java_files(java_classes)
