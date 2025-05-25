import os
from dotenv import load_dotenv
from botocore.credentials import Credentials

load_dotenv()

class Settings:
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY")
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 3))
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
    REDIS_TTL = int(os.getenv("REDIS_TTL", None))
    TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    def get_aws_credentials(self):
        return {
            "region": self.AWS_REGION,
            "access_key":self.AWS_ACCESS_KEY_ID,
            "secret_key":self.AWS_SECRET_ACCESS_KEY,
             }

settings = Settings()
