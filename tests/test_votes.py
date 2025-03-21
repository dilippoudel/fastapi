import pytest
from app import models
@pytest.fixture()
def test_vote(test_posts, session, test_user):
    """This fixture is for creating a vote for one of the assigned post."""
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, test_posts):
    """Test for voting succesfully on post."""
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir":1})
    assert res.status_code == 201

def test_vote_twice_post(authorized_client, test_posts, test_vote):
    """Test for decline to vote twice on the same post."""
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir":1})
    assert res.status_code == 409

def test_delete_vote(authorized_client, test_posts, test_vote):
    """Test for deleting vote from post."""
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id,"dir": 0})
    assert res.status_code == 201

def test_delete_vote_non_exit(authorized_client, test_posts):
    """Test for deleting non exist vote."""
    res = authorized_client.post("/vote/", json={"post_id": test_posts[2].id,"dir": 0})
    assert res.status_code == 404

def test_vote_post_non_exist(authorized_client, test_posts):
    """Test for avoiding voting for non exist post."""
    res = authorized_client.post("/vote/", json={"post_id":200, "dir": 1})
    assert res.status_code == 404

def test_vote_unauthorized_user(client, test_posts):
    """Test to avoid voting for not authorized user."""
    res = client.post("/vote/", json={"post_id":test_posts[3].id, "dir": 1})
    assert res.status_code == 401