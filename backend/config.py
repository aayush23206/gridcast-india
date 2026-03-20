import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
    DATA_GOV_API_KEY = os.environ.get("DATA_GOV_API_KEY")
    ADMIN_SECRET = os.environ.get("ADMIN_SECRET")
    DEBUG = os.environ.get("FLASK_ENV") != "production"
