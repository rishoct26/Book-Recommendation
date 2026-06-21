from fastapi import APIRouter, HTTPException
from api.database import supabase
from api.schemas import ActivityFeedResponse

router = APIRouter(tags=["social"])

@router.post("/follows/{user_id}")
def follow_user(user_id: str, follower_id: str):
    response = supabase.table("follows").insert({
        "follower_id": follower_id,
        "following_id": user_id
    }).execute()

    if not response.data:
        raise HTTPException(status_code=400, detail="Could not follow user")
    
    return{"message": "User followed successfully"}

@router.delete("/follows/{user_id}")
def unfollow_user(user_id: str, follower_id: str):
    supabase.table("follows").delete().eq("follower_id",follower_id).eq("following_id",user_id).execute()
    return{"message": "User unfollowed sucessfully"}

@router.get("/follows/{user_id}/followers")
def get_followers(user_id: str):
    response = supabase.table("follows").select("*").eq("following_id",user_id).execute()
    return response.data

@router.get("/follows/{user_id}/following")
def get_following(user_id: str):
    response = supabase.table("follows").select("*").eq("follower_id",user_id).execute()
    return response.data

@router.get("/feed/{user_id}")
def get_feed(user_id: str):
    response = supabase.table("activity_feed").select("*").eq("user_id",user_id).order("created_at", desc=True).execute()
    return response.data