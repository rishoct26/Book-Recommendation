import pandas as pd
from dotenv import load_dotenv
from supabase import create_client
import os
import math

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_ROLE_KEY")
)

books = pd.read_csv("data/books.csv")

rows = []
for _, row in books.iterrows():
    year = row['original_publication_year']
    rows.append({
        "id": int(row['id']),
        "title": str(row['title']),
        "authors": str(row['authors']),
        "original_publication_year": None if math.isnan(year) else float(year),
        "average_rating": float(row['average_rating']),
        "ratings_count": int(row['ratings_count']),
        "image_url": str(row['image_url']),
        "language_code": str(row['language_code']) if pd.notna(row['language_code']) else None
    })

batch_size = 500
total = len(rows)
for i in range(0, total, batch_size):
    batch = rows[i:i+batch_size]
    supabase.table("books").insert(batch).execute()
    print(f"Inserted rows {i+1} to {min(i+batch_size, total)} of {total}")

print("Done! All books loaded.")