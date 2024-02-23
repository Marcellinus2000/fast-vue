from fastapi import FastAPI
from controllers import post, user

app = FastAPI()

@app.get('/')
def hello():
    return{"Welcome": "Message"}

app.include_router(post.router, tags=["POSTS"])
app.include_router(user.router, tags=["USERS"])