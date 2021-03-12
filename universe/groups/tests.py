from django.test import TestCase
from groups.models import Group, MyBlog, Message
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

# Create your tests here.


class GroupTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="zues", password="somepasssword")
        self.userb = User.objects.create_user(username="mike", password="somepasssw")
        Group.objects.create(group_name="welcome", description="whatever", owner=self.userb)
        Group.objects.create(group_name="welcome", description="whatever", owner=self.userb)
        Group.objects.create(group_name="welcome", description="whatever", owner=self.userb)
        Group.objects.create(group_name="welcome", description="whatever", owner=self.userb)
        Group.objects.create(group_name="welcome3", description="4 u", owner=self.userb)
        Group.objects.create(group_name="welcome4", description="whatever2", owner=self.user)
        self.current_count = Group.objects.all().count()

    def test_user_created(self):
        self.assertEqual(self.user.username,  "zues")

    def test_group_create(self):
            group = Group.objects.create(
                group_name="Harvard", description="Will never leave", owner_id=self.user.id)
            self.assertEqual(group.id, 7)
            self.assertEqual(group.owner, self.user)

    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password="somepasssword")
        return client

    def get_client2(self):
        client2 = APIClient()
        client2.login(username=self.userb.username, password="somepasssw")
        return client2

    def test_api_login(self):
        client = APIClient()
        client.login(username=self.user.username, password="somepasssword")
        return client

    def test_Group_list(self):
        client = self.get_client()
        response = client.get("/Group/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 6)

    def test_create_group(self):
        client = self.get_client()
        data = {"group_name": "Hello Python",
                "description": "Welcome to the santinuary of the lord!", "owner": self.user}
        response = client.post("/Group/create", data)
        self.assertEqual(response.status_code, 201)

    def test_group_action_join(self):
        client = self.get_client()
        response = client.post("/Group/action", {"id_": 1, "action": "join"})
        #print(response.json())
        self.assertEqual(response.status_code, 200)

    def test_group_action_follow(self):
        client = self.get_client()
        response = client.post("/Group/action", {"id_": 2, "action": "follow"})
        self.assertEqual(response.status_code, 200)
        #print(response.json())
        likes = response.json().get("follower")
        self.assertEqual(likes, 1)

    def test_action_follow(self):
        client = self.get_client()
        response = client.post("/Group/action", {"id_": 3, "action": "unfollow"})
        self.assertEqual(response.status_code, 200)
        #print(response.json())
        likes = response.json().get("follower")
        self.assertEqual(likes, 0)

    def test_action_exit(self):
        client = self.get_client()
        response = client.post("/Group/action", {"id_": 4, "action": "exit"})
        self.assertEqual(response.status_code, 200)
        #print(response.json())
        likes = response.json().get("users")
        self.assertEqual(likes, 0)

    def test_followers_list(self):
        client = self.get_client2()
        response = client.get("/Group/1/followerslist")
        self.assertEqual(response.status_code, 403)
        follows = response.json().get("follower")
        self.assertEqual(follows, 0)

    def test_users_list(self):
        client = self.get_client2()
        response = client.get("/Group/1/userlist")
        self.assertEqual(response.status_code, 403)
        user = response.json().get("users")
        self.assertEqual(user, 0)

    def test_admin_list(self):
        client = self.get_client2()
        response = client.get("/Group/1/adminlist")
        self.assertEqual(response.status_code, 403)
