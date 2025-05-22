from fastapi import FastAPI, Response , status , HTTPException
from fastapi.params import Body, Optional
from pydantic import BaseModel
from random import randrange


app = FastAPI()

class Post(BaseModel):
    title: str
    content : str
    published : bool = True
    rating: Optional[int] = None

my_posts = [{"title" : " hello", "content": "hi", "id" : 1}]

def find_posts(id):
    for p in my_posts:
        if p["id"] == id:
            return p
         

@app.get("/")
async def root():
    return {"message": "Hello hehe"}

@app.get("/posts")
async def get_posts():
    return my_posts

@app.post("/posts")
async def create_posts(post : Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0,10000)
    my_posts.append(post_dict)
    return {"data" : post_dict}

@app.get("/posts/{id}")
def get_post(id:int, response: Response):
    post = find_posts(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="the page was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} was not found"}
    return {"post_detail" : post}


# @app.delete("/posts")
# async def delete_posts(post: Post)