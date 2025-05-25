import asyncio
import aioredis
from server.config.config import settings

MAX_RETRIES = 2
INITIAL_RETRY_DELAY = 1  
MAX_RETRY_DELAY = 30 

redis_client = None
retries = 0

# Connect to Redis using aioredis
async def connect_redis():
    global redis_client, retries
    delay = INITIAL_RETRY_DELAY

    while retries < MAX_RETRIES:
        try:
            redis_client = await asyncio.wait_for(
                aioredis.create_redis_pool(
                    (settings.REDIS_HOST, settings.REDIS_PORT),
                    db=settings.REDIS_DB,
                    password=settings.REDIS_PASSWORD
                ),
                timeout=5  # Set a 5 second timeout for each connection attempt
            )

            pong = await redis_client.ping()
            if pong:
                print("Connected to Redis!")
                return True 
            else:
                raise Exception("Failed to ping Redis server.")

        except Exception as err:
            retries += 1
            print(f"Error connecting to Redis: {err}")

            if retries < MAX_RETRIES:
                print(f"Retry attempt {retries} of {MAX_RETRIES}...")
                print(f"Waiting for {delay} seconds before retrying...")
                await asyncio.sleep(delay)

                # Exponential backoff
                delay = min(delay * 2, MAX_RETRY_DELAY)
            else:
                print(f"Failed to connect to Redis after {MAX_RETRIES} attempts.")
                return False

async def set_value(key: str, value: str, ttl: int):
    try:
        result = await redis_client.setex(key, ttl, value)
        print(f"Successfully set {key} with TTL of {ttl} seconds")
        return result
    except Exception as err:
        print(f"Error setting value in Redis: {err}")
        return None

async def get_value(key: str,db :int = settings.REDIS_DB):
    try:
        if db!=settings.REDIS_DB:
            await redis_client.execute('SELECT', db)
        value = await redis_client.get(key)
        if value is None:
            print(f"Key '{key}' not found in Redis.")
        else:
            print(f"Value of key '{key}': {value.decode('utf-8')}")
        return value
    except Exception as err:
        print(f"Error getting value from Redis: {err}")
        return None

async def set_or_increment_value(key: str, value: str, ttl: int, increment_by: int):
    try:
        existing_value = await redis_client.get(key)

        if existing_value is None:
            result = await redis_client.setex(key, ttl, value)
            print(f'Key "{key}" did not exist. Setting it with value: {value} and TTL {ttl}')
            return result
        else:
            # Key exists, increment its value by 'increment_by'
            new_value = await redis_client.incrby(key, increment_by)
            print(f'Key "{key}" exists. Incrementing value by {increment_by}. New value: {new_value}')
            return new_value
    except Exception as err:
        print(f"Error incrementing or setting value in Redis: {err}")
        return None
