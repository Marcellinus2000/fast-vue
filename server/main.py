from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import post, user, auth

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get('/')
def hello():
    return{"Welcome": "Message"}

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)