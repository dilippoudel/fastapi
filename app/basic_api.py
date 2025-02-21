from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException

from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='1234', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connection was successful.")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("error: ", error)
        time.sleep(2)




my_posts = [
    {"title": "Rock Star", "content": "Content of post 1", "id": 1},
    {"title": "Favourite Food", "content": "Content of post 1", "id": 2}
]
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

@app.get("/")
def root():
    return {
        "message": "Welcome to my API, Please log in first."
    }

@app.get('/posts')
def get_posts():
    cursor.execute("""SELECT * FROM posts  """)
    posts = cursor.fetchall()
    return {
        "data": posts
    }

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
        (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {
        "data": new_post
    }


@app.get("/post/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id:{id} was not found.')
    return {"post_detail": post}


# deleting a post
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            print(p)
            return i

@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE from posts where id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/post/{id}')
def update_post(id:int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s where id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()


    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist.")

    return {'data': updated_post}
