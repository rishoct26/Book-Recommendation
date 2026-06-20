from fastapi import APIRouter, HTTPException
from api.database import supabase
from api.schemas import ReadingListCreate, ReadingListUpdate, ReadingListResponse

router = APIRouter(prefix="/reading-list", tags=["reading-list"])

@router.post("/")
def add_to_reading_list(entry: ReadingListCreate, user_id: str):
    response = supabase.table("reading_list").insert({
        "user_id": user_id,
        "book_id": entry.book_id,
        "status": entry.status
    }).execute()

    if not response.data:
        raise HTTPException(status_code=400, detail="Could not add to reading list")
    
    return response.data[0]

@router.get("/{user_id}")
def update_reading_list(user_id:str):
    response= supabase.table("reading_list").select("*").eq("user_id",user_id).execute()

    return response.data

@router.put("/{user_id}/{book_id}")
def update_reading_list_status(user_id: str, book_id: int, entry: ReadingListUpdate):
    response = supabase.table("reading_list").update({
        "status":entry.status
    }).eq("user_id",user_id).eq("book_id",book_id).execute()

    if not response.data:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    return response.data[0]

@router.delete("/{user_id}/{book_id}")
def remove_from_reading_list(user_id: str, book_id: int):
    supabase.table("reading_list").delete().eq("user_id",user_id).eq("book_id",book_id).execute()

    return{"message": "Removed from reading list sucessfully"}