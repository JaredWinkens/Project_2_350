from cassandra.cluster import Cluster
import uuid

# Connect to Cassandra
cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

# Create a keyspace and use it
session.execute("""
CREATE KEYSPACE IF NOT EXISTS company_keyspace 
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
""")
session.set_keyspace('company_keyspace')

# Create a table for employees
session.execute("""
CREATE TABLE IF NOT EXISTS employees (
    emp_id UUID PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    position TEXT,
    salary DECIMAL
)
""")

# Define reusable Python functions

def add_employee(session, first_name, last_name, position, salary):
    """
    Inserts a new employee into the employees table.
    """
    emp_id = uuid.uuid4()
    session.execute("""
    INSERT INTO employees (emp_id, first_name, last_name, position, salary)
    VALUES (%s, %s, %s, %s, %s)
    """, (emp_id, first_name, last_name, position, salary))
    print(f"Employee {first_name} {last_name} added successfully with ID: {emp_id}")


def get_employees_by_position(session, position):
    """
    Retrieves and prints all employees with a specific position.
    """
    rows = session.execute("""
    SELECT first_name, last_name, salary 
    FROM employees 
    WHERE position = %s 
    ALLOW FILTERING
    """, (position,))
    print(f"\nEmployees with position: {position}")
    for row in rows:
        print(f"Name: {row.first_name} {row.last_name}, Salary: ${row.salary}")

# Use the functions

# Add employees
add_employee(session, "Alice", "Johnson", "Engineer", 75000.00)
add_employee(session, "Bob", "Smith", "Manager", 85000.00)
add_employee(session, "Charlie", "Brown", "Engineer", 70000.00)

# Retrieve employees with the position "Engineer"
get_employees_by_position(session, "Engineer")

# Close the connection
cluster.shutdown()
