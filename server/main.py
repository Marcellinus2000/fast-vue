from fastapi import FastAPI
from controllers import post, user, auth

app = FastAPI()

@app.get('/')
def hello():
    return{"Welcome": "Message"}

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)