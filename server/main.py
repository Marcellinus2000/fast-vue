from fastapi import FastAPI,status, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

while True:
    
    try: 
        conn = psycopg2.connect(host='localhost',database='fastapi_tut',user = 'postgres', password ='password', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database Connection Successful')
        break

    except Exception as error:
        print('Connection to database failed')
        print('Error:', error)
        time.sleep(2)

app = FastAPI()

@app.get('/posts')
def get_posts():
    cursor.execute("""SELECT * from posts""")
    posts = cursor.fetchall()
    
    return{"Post": posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
  
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    
    new_post = cursor.fetchone()

    conn.commit()
    print(new_post)
    return {"post": new_post}



@app.get('/posts/{id}')
def get_post(id : str):
    cursor.execute(""" SELECT * FROM posts where id = %s """ , (id))
    post = cursor.fetchone()
    print (post)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    return {"Post Detail": post}



@app.put('/posts/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):

    cursor.execute(""" UPDATE posts SET title = %s, content = %s,  published = %s  WHERE id = %s RETURNING *""" , (post.title, post.content, post.published, str(id)))
    post = cursor.fetchone()
    conn.commit()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    print(post)
    return {"Data": post}



@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    
    cursor.execute(""" DELETE FROM posts where id = %s RETURNING *""", str(id))
    post = cursor.fetchone()
    conn.commit()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")        
    return {"Message": "Post Deleted successfully"}