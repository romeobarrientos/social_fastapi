from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from . import database, schemas, models, utils


router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(userCredentials: schemas.UserLogin, db: Session = Depends()):
    user = db.query(models.User).filter(models.User.email == userCredentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    
    if not utils.verify(userCredentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
