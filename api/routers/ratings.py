from fastapi import APIRouter, HTTPException, Depends
from api.dependencies import get_current_user
from api.database import supabase
from api.schemas import RatingCreate, RatingUpdate, RatingResponse

router = APIRouter(prefix="/ratings", tags=["ratings"])

@router.post("/")
def create_rating(rating: RatingCreate, user_id: str = Depends(get_current_user)):
    response = supabase.table("user_ratings").insert({
        "user_id": user_id,
        "book_id": rating.book_id,
        "rating": rating.rating
    }).execute()

    if not response.data:
        raise HTTPException(status_code=400, detail="Could not create rating")

    return response.data[0]

@router.get("/{user_id}")
def get_ratings(user_id: str):
    response = supabase.table("user_ratings").select("*").eq("user_id", user_id).execute()

    return response.data

@router.put("/{book_id}")
def update_rating(book_id: int, rating: RatingUpdate, user_id: str = Depends(get_current_user)):
    response = supabase.table("user_ratings").update({
        "rating": rating.rating
    }).eq("user_id", user_id).eq("book_id", book_id).execute()

    if not response.data:
        raise HTTPException(status_code=404, detail="Rating not found")

    return response.data[0]

@router.delete("/{book_id}")
def delete_rating(book_id: int, user_id: str = Depends(get_current_user)):
    supabase.table("user_ratings").delete().eq("user_id", user_id).eq("book_id", book_id).execute()

    return {"message": "Rating deleted successfully"}