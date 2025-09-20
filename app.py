import redis
import mysql.connector
import json

# ------------------------
# Redis Cloud connection
# ------------------------
redis_client = redis.StrictRedis(
    host="",     # e.g. redis-12345.c1.ap-south-1-1.ec2.cloud.redislabs.com
    port=17479,                 # Redis port
    password="",
    decode_responses=True       # decode bytes to str
)

# ------------------------
# MySQL connection
# ------------------------
mysql_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="test",
    database="testdb"
)
cursor = mysql_conn.cursor(dictionary=True)

# ------------------------
# Function to get user by ID
# ------------------------
def get_user(user_id):
    cache_key = f"user:{user_id}"

    # 1. Check if key exists
    if redis_client.exists(cache_key):
        # Check key type
        key_type = redis_client.type(cache_key)
        if key_type != "string":
            # Delete wrong-type key
            print(f"⚠️ Key '{cache_key}' has wrong type '{key_type}'. Deleting...")
            redis_client.delete(cache_key)

    # 2. Try fetching from cache
    cached_data = redis_client.get(cache_key)
    if cached_data:
        print("✅ Cache hit")
        return json.loads(cached_data)

    # 3. If not in cache, fetch from MySQL
    print("❌ Cache miss - fetching from MySQL")
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    row = cursor.fetchone()

    if row:
        # Store in Redis cache (expire in 60 seconds)
        redis_client.setex(cache_key, 60, json.dumps(row))
        return row
    return None

# ------------------------
# Example Usage
# ------------------------
if __name__ == "__main__":
    user = get_user(1)
    print(user)

    # Call again -> should come from cache
    user = get_user(1)

    print(user)
