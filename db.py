import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL,SUPABASE_KEY)

if __name__ == "__main__":
        result = supabase.table("users").select("*").execute()
        print("Connected. Users table returned:", result.data)
        
