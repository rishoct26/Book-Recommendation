from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProfileUpdate(BaseModel):
    username: Optional[str]=None
    bio: Optional[str]=None
    avatar_url: Optional[str]=None
    is_public: Optional[bool]=None
    selected_genres: Optional[list[str]]=None
    onboarding_complete: Optional[bool]=None

class ProfileResponse(BaseModel):
    id:str
    username: str
    bio: Optional[str]=None
    avatar_url: Optional[str]=None
    is_public:bool
    selected_genres: Optional[list[str]]=None
    onboarding_complete:bool
    created_at:datetime