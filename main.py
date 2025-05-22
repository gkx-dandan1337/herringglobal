from fastapi import FastAPI
from fastapi.params import Body, Optional
from pydantic import BaseModel


app = FastAPI()

class Post(BaseModel):
    title: str
    content : str
    published : bool = True
    rating: Optional[int] = None

@app.get("/")
async def root():
    return {"message": "Hello hehe"}

@app.get("/posts")
async def get_posts():
    return {"hello":"hello"}

@app.post("/createposts")
def create_posts(post : Post):
    print(post)
    return {"data" : "new_post"}