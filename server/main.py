from fastapi import FastAPI,status, HTTPException, Response, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from database.database import engine, get_db
from models import models
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

# These are all codes when using only the psycopg2 to run sql codes in order to perform database queries
    
# while True:
    
#     try: 
#         conn = psycopg2.connect(host='localhost',database='fastapi_tut',user = 'postgres', password ='password', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database Connection Successful')
#         break

#     except Exception as error:
#         print('Connection to database failed')
#         print('Error:', error)
#         time.sleep(2)

app = FastAPI()

@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return{"Data": posts}

@app.get('/posts/{id}')
def get_post(id : int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts where id = %s """ , str(id))
    # post = cursor.fetchone()
    # print (post)

    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    return {"Post Detail": post}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(new_post)
    return {"post": new_post}

@app.put('/posts/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):

    # cursor.execute(""" UPDATE posts SET title = %s, content = %s,  published = %s  WHERE id = %s RETURNING *""" , (post.title, post.content, post.published, str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    
    post_q = db.query(models.Post).filter(models.Post.id == id)
    post = post_q.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    post_q.update(updated_post.dict(), synchronize_session = False)
    db.commit()
    return {"Data": post_q.first()}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts where id = %s RETURNING *""", str(id))
    # post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist") 
           
    post.delete(synchronize_session = False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)