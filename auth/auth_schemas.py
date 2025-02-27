from datetime import datetime
from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    
class requestdetails(BaseModel):
    email:str
    password:str
        
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

class TokenCreate(BaseModel):
    user_id:str
    access_token:str
    refresh_token:str
    status:bool
    created_date:datetime