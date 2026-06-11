from fastapi import APIRouter, HTTPException, Header
from api.database import supabase
from api.schemas import ProfileUpdate, ProfileResponse
from typing import Optional

router = APIRouter(prefix="/profiles", tags=["profiles"])

@router.get("/{username}", response_model=ProfileResponse)
def get_profiles(username:str):
    response=supabase.table("profiles").select("*").eq("username",username).single().execute()

    if not response.data:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return response.data

@router.put("/{user_id}")
def update_profile(user_id: str,profile:ProfileUpdate):
    update_data=profile.model_dump(exclude_none=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    response = supabase.table("profiles").update(update_data).eq("id",user_id).execute()

    if not response.data:
        raise HTTPException(status_code=404, detail="Profile not found")
    return response.data[0]

@router.delete("/{user_id}")
def delete_profile(user_id:str):
    response = supabase.table("profiles").delete().eq("id",user_id).execute()

    return{"message": "Profile deleted successfully"}