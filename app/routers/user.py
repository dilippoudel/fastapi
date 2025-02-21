
"""User related all apis."""

from .. import schemas, models, utils
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter


router = APIRouter(prefix='/users', tags=['Users'])
from .. database import get_db
@router.post('/',
          status_code=status.HTTP_201_CREATED,
          response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Creating a new user with an email and password."""
    # hash the passord
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    post_user = user.model_dump()
    new_user = models.User(**post_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} could not found')
    return user

