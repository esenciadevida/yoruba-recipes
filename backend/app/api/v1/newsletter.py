import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.core.config import settings

router = APIRouter()

class Subscriber(BaseModel):
    email: EmailStr

@router.post("/subscribe")
def subscribe(data: Subscriber):
    api_key = settings.MAILERLITE_API_KEY
    group_id = settings.MAILERLITE_GROUP_ID

    if not api_key or not group_id:
        raise HTTPException(status_code=500, detail="Newsletter service not configured")
    
    url = "https://connect.mailerlite.com/api/subscribers"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "email": data.email,
        "groups": [group_id]
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return {"message": "Subscription successful", "data": response.json()}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"MailerLite error: {str(e)}")