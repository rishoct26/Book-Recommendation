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

class RatingCreate(BaseModel):
    book_id: int
    rating: float

class RatingUpdate(BaseModel):
    rating: float

class RatingResponse(BaseModel):
    id: str
    user_id: str
    book_id: int
    rating: float
    created_at: datetime

class ReadingListCreate(BaseModel):
    book_id:int
    status:str

class ReadingListUpdate(BaseModel):
    status: str

class ReadingListResponse(BaseModel):
    id:str
    user_id:str
    book_id:int
    status:str
    added_at:datetime

class ReviewCreate(BaseModel):
    book_id: int
    title: Optional[str]=None
    body: str
    rating: Optional[float]=None
    has_spoiler: bool = False 

class ReviewUpdate(BaseModel):
    title: Optional[str]=None
    body: Optional[str]=None
    rating: Optional[float]=None
    has_spoiler: Optional[bool]=None

class ReviewResponse(BaseModel):
    id:str
    user_id: str
    book_id:int
    title:Optional[str]=None
    body:str
    rating:Optional[float]=None
    has_spoiler:bool
    created_at:datetime
    updated_at:datetime

class ActivityFeedResponse(BaseModel):
    id:str
    user_id:str
    action_type:str
    book_id: Optional[int]=None
    review_id: Optional[str]=None
    created_at:datetime

class RecommendationRequest(BaseModel):
    user_id: int
    n: int = 10

class ColdStartRequest(BaseModel):
    genres: list[str]
    n: int = 10

class RecommendationResponse(BaseModel):
    book_id: int 
    score: float