"""Post related all apis."""

from .. import schemas, models, oauth2
from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get('/', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    print(search)
    all_posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return all_posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post_data = post.model_dump()
    new_post = models.Post(owner_id=user_id.id, **post_data)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id:{id} was not found.')
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist.")

    if post.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not authorized to perform requested action')
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.Post)
def update_post(id:int, update_post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist.")
    if post.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not authorized to perform requested action')
    post_query.update(dict(update_post), synchronize_session=False)
    db.commit()

    return post_query.first()
