from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
app = FastAPI()
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# Base Model schema for post creation format
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

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


# Home page
@app.get("/")
def root():
    return{"message": "Welcome to my API"}

# Get a post
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}

# Create a post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    newPost = cursor.fetchone()
    conn.commit()
    return {"data": newPost}

# Getting an individual post
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code= 404, detail= f"ID {id} could not be found in the system!")
    return{"post detail": post}

# Delete post
@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
        cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
        deletedPost = cursor.fetchone()
        conn.commit()

       
        if deletedPost == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Page not found, likely deleted. Please try again :)")
        
        return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, (id,)))
    updatedPost = cursor.fetchone()
    conn.commit()
    if updatedPost == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Page not found, likely deleted. Please try again :)")
    return{"data": updatedPost}
