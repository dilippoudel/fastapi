from fastapi import FastAPI
from . import models
from .database import engine
from .routers import user, post, auth, vote
from fastapi.middleware.cors import CORSMiddleware


# models.Base.metadata.create_all(bind=engine) this is done by alembic now.

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "Running server into Ubuntu"}


# origins = ["https://www.google.com"] ==> only the google can access our backend api
origins = ["*"] # if we want to give an access for our api to all domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



