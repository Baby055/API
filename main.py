from fastapi import FastAPI, Request, HTTPException, status, Response
from fastapi.responses import PlainTextResponse, HTMLResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import List
from pydantic import BaseModel
from datetime import datetime
import secrets

app = FastAPI()
security = HTTPBasic()
posts_storage = []

# Question 1
@app.get("/ping", response_class=PlainTextResponse)
def ping():
    return Response(content="pong", media_type="text/plain")

# Question 2
@app.get("/home", response_class=HTMLResponse)
def home():
    return HTMLResponse(content="<h1>Welcome home!</h1>", status_code=200)

# Question 3
@app.exception_handler(404)
def not_found(request: Request, exc):
    return HTMLResponse(content="<h1>404 NOT FOUND</h1>", status_code=404)

# Question 4
class Post(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: datetime
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_posts: List[Post]):
    posts_storage.extend(new_posts)
    return posts_storage

# Question 5
@app.get("/posts")
def get_posts():
    return posts_storage

# Question 6
@app.put("/posts")
def update_or_add_post(post: Post):
    for i, existing_post in enumerate(posts_storage):
        if existing_post.title == post.title:
            posts_storage[i] = post
            return {"message": "Post updated", "post": post}
    posts_storage.append(post)
    return {"message": "Post added", "post": post}

#Bonus
@app.get("/ping/auth", response_class=PlainTextResponse)
def secure_ping(credentials: HTTPBasicCredentials = security):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "123456")
    if not (correct_username and correct_password):
        return Response(content="Unauthorized", status_code=401, media_type="text/plain")
    return Response(content="pong", media_type="text/plain")