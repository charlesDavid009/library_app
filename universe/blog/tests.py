from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import (Blog, BlogLikes, Comment, CommentLikes, SubComment, SubCommentLikes)
from rest_framework.test import APIClient

User = get_user_model()
# Create your tests here.


class BlogTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(first_name = "david", last_name = "zues", email= "example@gmail.com", date_of_birth = "1997-5-21" ,username="zues", password="somepasssword")
        self.userb = User.objects.create_user(
            first_name = 'david', last_name = 'zues', email= 'example1@gmail.com', date_of_birth = '1997-05-21', username="mike", password="somepasssword")
        Blog.objects.create(
            title="welcome", content="whatever", user=self.user)
        Blog.objects.create(
            title="welcome2", content="whatever2", user=self.user)
        Blog.objects.create(
            title="welcome2", content="whatever2", user=self.user)
        Blog.objects.create(
            title="welcome2", content="whatever2", user=self.user)
        Comment.objects.create(blog_id=2, text="Hello", user=self.userb)
        Comment.objects.create(blog_id=3, text="Jesus", user=self.userb)
        Comment.objects.create(blog_id=4, text="welcome", user=self.userb)
        Comment.objects.create(blog_id=1, text="williams", user=self.userb)
        Comment.objects.create(blog_id=2, text="welcome", user=self.userb)
        Comment.objects.create(blog_id=3, text="Helo", user=self.userb)
        Comment.objects.create(blog_id=4, text="Whatever", user=self.userb)
        Comment.objects.create(blog_id=1, text="Jesus", user=self.userb)
        SubComment.objects.create(blog_id=2, text="Hello", user=self.user)
        SubComment.objects.create(blog_id=3, text="Jesus", user=self.user)
        SubComment.objects.create(blog_id=4, text="welcome", user=self.user)
        SubComment.objects.create(blog_id=1, text="williams", user=self.user)
        SubComment.objects.create(blog_id=4, text="welcome", user=self.userb)
        SubComment.objects.create(blog_id=1, text="williams", user=self.userb)
        SubComment.objects.create(blog_id=2, text="welcome", user=self.userb)
        SubComment.objects.create(blog_id=3, text="Helo", user=self.userb)
        self.current_count = Blog.objects.all().count()

    def test_user_created(self):
        self.assertEqual(self.user.username,  "zues")

    def test_blog_create(self):
        blog = Blog.objects.create(
            title="welcome3", content="whatever3", user=self.user)
        self.assertEqual(blog.id, 5)
        self.assertEqual(blog.user, self.user)

    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password="somepasssword")
        return client

    def get_client2(self):
        client2 = APIClient()
        client2.login(username=self.userb.username, password="somepasssword")
        return client2

    def test_api_login(self):
        client = APIClient()
        client.login(username=self.user.username, password="somepasssword")
        return client
"""
    def test_blog_list(self):
        client = self.get_client()
        response = client.get("/Blog/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)

    def test_blog_action_report(self):
        client = self.get_client()
        response = client.post("/Blog/action", {"id": 1, "action": "report"})
        #print(response.json())
        report = response.json().get("reports")
        self.assertEqual(report, 1)
        self.assertEqual(response.status_code, 200)

    def test_blog_action_like(self):
        client = self.get_client()
        response = client.post("/Blog/action", {"id": 1, "action": "like"})
        self.assertEqual(response.status_code, 200)
        #print(response.json())
        likes = response.json().get("likes")
        self.assertEqual(likes, 1)

    def test_action_unlike(self):
        client = self.get_client()
        response = client.post("/Blog/action", {"id": 2, "action": "unlike"})
        self.assertEqual(response.status_code, 200)
        #print(response.json())
        likes = response.json().get("likes")
        self.assertEqual(likes, 0)

    def test_action_reblog(self):
        client = self.get_client()
        response = client.post("/Blog/action", {"id": 3, "action": "reblog"})
        self.assertEqual(response.status_code, 201)
        #print(response.json())
        data = response.json()
        new_blog_id = data.get("id")
        self.assertNotEqual(3, new_blog_id)
        self.assertEqual(len(response.json()), 10)

    def test_action_reblog_with_content(self):
        client = self.get_client()
        currentcount = self.current_count
        response = client.post(
            "/Blog/action", {"id": 4, "action": "reblog", "add": "thank you lord"})
        self.assertEqual(response.status_code, 201)
        #print(response.json())
        data = response.json()
        new_blog_id = data.get("id")
        self.assertNotEqual(4, new_blog_id)
        self.assertEqual(len(response.json()), 10)
        self.assertEqual(currentcount + 1, new_blog_id)

    def test_create_blog_post(self):
        client = self.get_client()
        data = {"title": "You are Yahew",
                "content": "Welcome to the santinuary of the lord!", "user_id": self.user.id}
        response = client.post("/Blog/create", data)
        response_data = response.json()
        new_id = response_data.get("id")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.current_count + 1, new_id)
        #print(response.json())

    def test_detail_blog(self):
        client = self.get_client()
        response = client.get("/Blog/4/detail")
        data = response.json()
        _id = data.get("id")
        self.assertEqual(_id, 4)
        #print(response.json())
        self.assertEqual(response.status_code, 200)

    def test_delete_blog(self):
        client = self.get_client()
        response = client.delete("/Blog/2/detail")
        data = response.json()
        print(data)
        _id = data.get("pk")
        self.assertNotEqual(_id, 2)
        self.assertEqual(response.status_code, 200)

    def test_unathorized_delete_blog(self):
        client = self.get_client2()
        response = client.delete("/Blog/2/detail")
        data = response.json()
        _id = data.get("pk")
        self.assertNotEqual(_id, 2)
        self.assertEqual(response.status_code, 403)

    def test_comment_list(self):
        client = self.get_client()
        response = client.get("/Comment/2/")
        #print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_create_comment(self):
        client = self.get_client()
        data = {"blog_id": 2,
                "text": "Welcome to the santinuary", "user_id": self.userb.id}
        response = client.post("/Comment/create",data)
        response_data = response.json()
        new_id = response_data.get("id")
        self.assertEqual(response.status_code, 201)
        #print(response.json())

    def test_comment_detail(self):
        client = self.get_client()
        response = client.get("/Blog/Comment/2/detail/")
        data = response.json()
        _id = data.get("pk")
        self.assertEqual(_id, 2)
        #print(response.json())
        self.assertEqual(response.status_code, 200)

    def test_delete_comment(self):
        client = self.get_client2()
        response = client.delete("/Blog/Comment/2/detail")
        data = response.json()
        print(data)
        _id = data.get("pk")
        self.assertNotEqual(_id, 2)
        self.assertEqual(response.status_code, 204)

    def test_unathorized_delete_comment(self):
        client = self.get_client()
        response = client.delete("/Blog/Comment/5/detail/")
        data = response.json()
        print(data)
        _id = data.get("pk")
        self.assertEqual(_id, 5)
        self.assertEqual(response.status_code, 401)

    def test_comment_action_like(self):
        client = self.get_client()
        response = client.post("/Blog/Comment/action", {"id": 3, "action": "like"})
        self.assertEqual(response.status_code, 200)
        #print(response.json())
        likes = response.json().get("like")
        self.assertEqual(likes, 1)

    def test_comment_action_unlike(self):
        client = self.get_client()
        response = client.post("/Blog/Comment/action",{"id": 5, "action": "unlike"})
        self.assertEqual(response.status_code, 200)
        #print(response.json())
        likes = response.json().get("like")
        self.assertEqual(likes, 0)

    def test_comment_like_list(self):
        client = self.get_client2()
        response = client.get("/Blog/Comment/3/likes")
        #print(response.json())
        self.assertEqual(response.status_code, 200)

    def test_blog_like_list(self):
        client = self.get_client()
        response = client.get("/Blog/2/likes ")
        print(response.json())
        self.assertEqual(response.status_code, 200)

    def test_create_subcomment(self):
        client = self.get_client()
        data = {"blog_id": 2,
                "text": "Welcome to the santinuary", "user_id": self.userb.id}
        response = client.post("/SubComment/create", data)
        response_data = response.json()
        new_id = response_data.get("id")
        self.assertEqual(response.status_code, 201)
        #print(response.json())

    def test_subcomment_detail(self):
        client = self.get_client()
        response = client.get("/Blog/SubComment/2/detail/")
        self.assertEqual(response.status_code, 200)

    def test_delete_subcomment(self):
        client = self.get_client()
        response = client.delete("/Blog/SubComment/4/detail")
        data = response.json()
        print(data)
        _id = data.get("pk")
        self.assertNotEqual(_id, 4)
        self.assertEqual(response.status_code, 204)

    def test_unathorized_delete_subcomment(self):
        client = self.get_client2()
        response = client.delete("/Blog/SubComment/5/detail/")
        data = response.json()
        print(data)
        _id = data.get("pk")
        self.assertEqual(_id, 5)
        self.assertEqual(response.status_code, 401)

    def test_subcomment_action_like(self):
        client = self.get_client()
        response = client.post("/Blog/SubComment/action", {"id": 3, "action": "like"})
        self.assertEqual(response.status_code, 200)
        #print(response.json())
        likes = response.json().get("like")
        self.assertEqual(likes, 1)

    def test_subcomment_action_unlike(self):
        client = self.get_client()
        response = client.post("/Blog/SubComment/action", {"id": 5, "action": "unlike"})
        self.assertEqual(response.status_code, 200)
        #print(response.json())
        likes = response.json().get("like")
        self.assertEqual(likes, 0)

    def test_subcomment_like_list(self):
        client = self.get_client2()
        response = client.get("/Blog/SubComment/3/likes")
        #print(response.json())
        self.assertEqual(response.status_code, 200)
"""