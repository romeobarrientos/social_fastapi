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

# Delete post
@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    
        index = find_index_post(id)
        if index == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Page not found, likely deleted. Please try again :)")
        my_posts.pop(index)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Page not found, likely deleted. Please try again :)")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return{"data": post_dict}
