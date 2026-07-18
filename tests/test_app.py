import unittest
import os

os.environ["TESTING"] = "true"

from app import app, mydb, TimelinePost


class AppTestCase(unittest.TestCase):
    def setUp(self):
        if mydb.is_closed():
            mydb.connect()
        mydb.bind([TimelinePost], bind_refs=False, bind_backrefs=False)
        mydb.create_tables([TimelinePost])
        TimelinePost.delete().execute()
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200

        html = response.get_data(as_text=True)
        assert "<title>Sakshyam Sigdel</title>" in html
        assert "About Me" in html
        assert "Work Experience" in html

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json

        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

    def test_timeline_page(self):
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Timeline</title>" in html
        assert "timeline-form" in html

    def test_timeline_post(self):
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "content": "Hello world, I'm John!",
            },
        )
        assert response.status_code == 200
        assert response.is_json

        created = response.get_json()
        assert created["name"] == "John Doe"
        assert created["email"] == "john@example.com"
        assert created["content"] == "Hello world, I'm John!"

        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        posts = response.get_json()["timeline_posts"]
        assert len(posts) == 1
        assert posts[0]["name"] == "John Doe"
        assert posts[0]["email"] == "john@example.com"
        assert posts[0]["content"] == "Hello world, I'm John!"

    def test_malformed_timeline_post(self):
        response = self.client.post(
            "/api/timeline_post",
            data={
                "email": "john@example.com",
                "content": "Hello world, I'm John!",
            },
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "content": "",
            },
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "not-an-email",
                "content": "Hello world, I'm John!",
            },
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
