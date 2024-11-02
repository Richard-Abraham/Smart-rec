from django.conf import settings
from dotenv import load_dotenv
import os

def get_env_settings():
    """Load environment variables and return settings"""
    # Load .env file
    load_dotenv()
    
    return {
        'SUPABASE_URL': os.getenv('SUPABASE_URL'),
        'SUPABASE_KEY': os.getenv('SUPABASE_KEY'),
        'SUPABASE_JWT_SECRET': os.getenv('SUPABASE_JWT_SECRET'),
    } 