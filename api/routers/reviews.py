from fastapi import APIRouter, HTTPException
from api.database import supabase
from api.schemas import ReviewCreate, ReviewUpdate, ReviewResponse

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/")
def create_review(review: ReviewCreate, user_id: str):
    response = supabase.table("reviews").insert({
        "user_id": user_id,
        "book_id": review.book_id,
        "title": review.title,
        "body": review.body,
        "rating": review.rating,
        "has_spoiler": review.has_spoiler
    }).execute()

    if not response.data:
        raise HTTPException(status_code=400, detail="Could not create review")
    return response.data[0]

@router.get("/book/{book_id}")
def get_reviews_by_book(book_id: str):
    response = supabase.table("reviews").select("*").eq("book_id", book_id).execute()

    return response.data

@router.get("/user/{user_id}")
def get_reviews_by_user(user_id: str):
    response = supabase.table("reviews").select("*").eq("user_id",user_id).execute()

    return response.data

@router.put("/{review_id}")
def update_review(review_id: str, review: ReviewUpdate):
    update_data = review.model_dump(exclude_none=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    response = supabase.table("reviews").update(update_data).eq("id",review_id).execute()

    if not response.data:
        raise HTTPException(status_code = 404, detail="Review not found")
    return response.data[0]

@router.delete("/{review_id}")
def delete_review(review_id: str):
    supabase.table("reviews").delete().eq("id",review_id).execute()
    return{"message": "Review deleted successfully"}

@router.post("/{review_id}/like")
def like_review(review_id: str, user_id: str):
    response = supabase.table("review_likes").insert({
        "user_id": user_id,
        "review_id": review_id
    }).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Could not like review")
    return{"message": "Review liked successfully"}

@router.delete("/{review_id}/like")
def unlike_review(review_id:str, user_id: str):
    supabase.table("review_likes").delete().eq("user_id",user_id).eq("review_id", review_id).execute()
    return{"message": "Review unliked successfully"}

@router.post("/{review_id}/comments")
def add_comment(review_id: str, user_id: str, body: str):
    response = supabase.table("review_comments").insert({
        "user_id": user_id,
        "review_id": review_id,
        "body": body
    }).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Could not add comment")
    return response.data[0]

@router.get("/{review_id}/comments")
def get_comments(review_id: str):
    response = supabase.table("review_comments").select("*").eq("review_id",review_id).execute()
    return response.data

@router.delete("/{review_id}/comments/{comment_id}")
def delete_comment(review_id: str, comment_id: str):
    supabase.table("review_comments").delete().eq("id",comment_id).execute()
    return{"message": "Comment deleted sucessfully"}