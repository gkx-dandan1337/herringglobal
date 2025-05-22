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

used_ids = set()

def get_id():
    while True:
        id = randrange(0,100000)
        if id in used_ids:
            continue
        else:
            used_ids.add(id)
            return id



def find_posts(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i, p 



@app.get("/")
async def root():
    return {"message": "Hello hehe"}

@app.get("/posts")
async def get_posts():
    return my_posts

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post : Post):
    post_dict = post.model_dump()
    post_dict['id'] = get_id()
    my_posts.append(post_dict)
    return {"data" : post_dict}

@app.get("/posts/{id}")
async def get_post(id:int, response: Response):
    index, post = find_posts(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="the page was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} was not found"}
    return {"post_detail" : post}

@app.delete("posts/{id}", status_code=status.HTTP_204_NO_CONTENT )
async def delete_posts(id:int):
    index, post = find_posts(id) 
    if index:
        my_posts.pop(index)
        return {"message": f"the post id {id} has been successfully deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"this id does not exist.")
    
