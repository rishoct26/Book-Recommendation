import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.getenv("SUPABASE_URL")
service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase = create_client(url, service_key)

response = supabase.auth.admin.update_user_by_id(
    "07ea25db-a246-4b2d-8613-0d4ca1876482",
    {"password": "TestPassword123!"}
)

print("Password updated for:", response.user.email)