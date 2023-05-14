from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
app = FastAPI()

# Base Model schema for post creation format
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# Array that stores post content
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content": "I like pizza", "id": 2}]

# For loop that searches for ID and returns it to find_post function
def find_post(id):
    for p in my_posts:
        if p["id"] ==  id:
            return p


# Home page
@app.get("/")
def root():
    return{"message": "Welcome to my API"}

# Get a post
@app.get("/posts")
def get_posts():
    return {"data": my_posts}

# Create a post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data": post_dict}

# Getting an individual post
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    
    post = find_post(id)
    if not post:
        raise HTTPException(status_code= 404, detail= f"ID {id} could not be found in the system!")
    return{"post detail": post}
