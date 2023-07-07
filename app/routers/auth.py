from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
import database, schemas, models, utils, oauth2
from database import get_db

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(userCredentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == userCredentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    
    if not utils.verify(userCredentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    
    # Create a token
    # Return a token

    access_token = oauth2.create_access_token(data= {"user_id"})

    return {"access_token": access_token, "token_type": "bearer"}