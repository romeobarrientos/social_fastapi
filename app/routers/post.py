import models, schemas
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import engine, SessionLocal, get_db
router = APIRouter()
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from schemas import UserCreate

# Get a post
@router.get("/posts", response_model=schemas.PostResponse)
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

# Create a post
@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostBase, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    # newPost = cursor.fetchone()
    # conn.commit()
    
    newPost = models.Post(**post.dict())
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost

# Getting an individual post
@router.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (id,))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)


    if not post:
        raise HTTPException(status_code= 404, detail= f"ID {id} could not be found in the system!")
    return post

# Delete post
@router.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
        # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
        # deletedPost = cursor.fetchone()
        # conn.commit()

       post = db.query(models.Post).filter(models.Post.id == id)
       if post.first() == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Page not found, likely deleted. Please try again :)")
       post.delete(synchronize_session=False)
       db.commit()
       
       return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updatedPost: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, (id,)))
    # updatedPost = cursor.fetchone()
    # conn.commit()

    postQuery = db.query(models.Post).filter(models.Post.id == id)
    post = postQuery.first()
    if post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Page not found, likely deleted. Please try again :)")
    postQuery.update(updatedPost.dict(), synchronize_session=False)
    db.commit()
    return postQuery.first()