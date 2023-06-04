from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
app = FastAPI()
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import models, schemas, utils
from schemas import UserCreate
from routers import post, user

#ORM import
from sqlalchemy.orm import Session


from database import engine, SessionLocal, get_db
@app.on_event("startup")
async def on_startup():
    models.Base.metadata.create_all(bind=engine)

# Code for connecting to database using psycopg
while True:

    try:
        conn = psycopg2.connect(host='localhost', database='advento', user='postgres', password='661284Product', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connecting to Database failed")
        print("Error: ", error)
        time.sleep(2)    
# Array that stores post content
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content": "I like pizza", "id": 2}]

# For loop that searches for ID and returns it to find_post function
def find_post(id):
    for p in my_posts:
        if p["id"] ==  id:
            return p

# Find index of post
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

app.include_router(post.router)
app.include_router(user.router)

# Home page
@app.get("/")
def root():
    return{"message": "Welcome to my API"}
