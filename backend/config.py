import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Supabase Configuration
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
    
    # Data.gov.in Configuration
    GOV_API_KEY = os.environ.get("GOV_API_KEY")
    
    # Flask Configuration
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "gridcast_secret_123")
    DEBUG = os.environ.get("DEBUG", "True").lower() == "true"
    
    # Admin Key for retraining
    ADMIN_SECRET_KEY = os.environ.get("ADMIN_SECRET_KEY", "admin_pass")
