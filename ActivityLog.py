from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import uuid
from datetime import datetime

# Step 1: Connect to Cassandra
cluster = Cluster(['127.0.0.1'])  # Replace with your Cassandra server IP
session = cluster.connect()

# Step 2: Create keyspace
session.execute("""
CREATE KEYSPACE IF NOT EXISTS activity_logs 
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
""")

# Step 3: Use the keyspace
session.set_keyspace('activity_logs')

# Step 4: Create a table
session.execute("""
CREATE TABLE IF NOT EXISTS user_activity (
    user_id UUID,
    activity_time TIMESTAMP,
    action TEXT,
    metadata MAP<TEXT, TEXT>,
    PRIMARY KEY (user_id, activity_time)
) WITH CLUSTERING ORDER BY (activity_time DESC)
""")

# Step 5: Insert data
user_id = uuid.uuid4()  # Simulate a user
activities = [
    {"action": "play", "metadata": {"movie_id": "123", "title": "Inception"}},
    {"action": "pause", "metadata": {"movie_id": "123", "time_position": "10:00"}},
    {"action": "stop", "metadata": {"movie_id": "123", "reason": "network_error"}},
]

for activity in activities:
    session.execute(
        """
        INSERT INTO user_activity (user_id, activity_time, action, metadata)
        VALUES (%s, %s, %s, %s)
        """,
        (user_id, datetime.now(), activity["action"], activity["metadata"])
    )

# Step 6: Query data
print("Fetching activity logs for user...")
query = SimpleStatement("""
    SELECT activity_time, action, metadata FROM user_activity WHERE user_id=%s
""", fetch_size=10)  # Fetch limited rows per iteration

rows = session.execute(query, (user_id,))
for row in rows:
    print(f"Time: {row.activity_time}, Action: {row.action}, Metadata: {row.metadata}")

# Close the connection
cluster.shutdown()
