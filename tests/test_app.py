import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_1_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Logan Hoogendijk's Portfolio</title>" in html
        assert "<link rel=\"stylesheet\" href=\"../static/styles/main.css\">" in html
        assert "<p class=\"title is-5\">About Me</p>" in html

    
    def test_2_empty_timeline(self):
        response = self.client.get("api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

    def test_3_timeline(self):
        get_response = self.client.get("api/timeline_post")
        assert get_response.status_code == 200
        assert get_response.is_json
        json = get_response.get_json()
        assert "timeline_posts" in json
        post_amt_before = len(json["timeline_posts"])
        post_response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "john@example.com", "content": "Hello world, I'm John!"})
        get_response = self.client.get("api/timeline_post")
        json = get_response.get_json()
        assert post_response.status_code == 200
        assert len(json["timeline_posts"]) == (post_amt_before + 1)
        first_post = json["timeline_posts"][0]
        assert "name" in first_post
        assert first_post['name'] == "John Doe"
        assert "email" in first_post
        assert first_post['email'] == "john@example.com"
        assert "content" in first_post
        assert first_post['content'] == "Hello world, I'm John!"
        # Timeline page
        timeline_response = self.client.get("timeline")
        assert timeline_response.status_code == 200
        html = timeline_response.get_data(as_text=True)
        assert "<button type=\"submit\">Submit</button>" in html
        assert "<script>" in html

    def test_4_malformed_timeline_post(self):
        response = self.client.post("/api/timeline_post", data={"email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html

        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html






        
