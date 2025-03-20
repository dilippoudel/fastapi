import pytest
from typing import List
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    """Test to get all posts by authorised user."""
    res = authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostOut(**post)
    assert res.status_code == 200
    assert len(res.json()) == 4



def test_unauthorized_user_get_all_posts(client, test_posts):
    """Test to not get post by unauthorize user."""
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    """Test for not authirze user to block post."""
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exit(authorized_client, test_posts):
    """Test to get single post by authorized user."""
    res = authorized_client.get(f"/posts/888")

    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    """Test for authorize client to get a single post."""
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())

    assert post.post.id == test_posts[0].id
    assert post.post.content == test_posts[0].content

@pytest.mark.parametrize("title, content, published", [
    ("new title","about javascript",True),
    ("new title","about javascript",True),
    ("new title","about javascript",True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']

def test_create_post_with_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title": "title is from me", "content":"New content"})
    created_post = schemas.Post(**res.json())
    assert created_post.title == "title is from me"
    assert created_post.published == True


def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post("/posts/", json={"title": "arbitary title","content":"content for arbitary"})
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_successfully_deleting_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f'/posts/{test_posts[0].id}')
    assert response.status_code == 204
    current_posts = authorized_client.get("/posts")
    assert len(current_posts.json()) == 3

def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f'/posts/5')
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f'/posts/{test_posts[3].id}')
    res.status_code == 403

def test_updating_post(authorized_client, test_user, test_posts):
    data = {
        "title":"Updated title",
        "content": "updated Content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f'/posts/{test_posts[0].id}', json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']

def test_updating_other_post_user(authorized_client, test_user, test_user_two, test_posts):
    data = {
        "title":"Updated title",
        "content": "updated Content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f'/posts/{test_posts[3].id}', json=data)
    assert res.status_code == 403

