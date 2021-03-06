from django.test import TestCase
from django.contrib.auth import get_user_model
from socialapp import models

from rest_framework.test import APIClient
from socialapp import urls

class TestREST(TestCase):

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user1 = User.objects.create_user('user1', 'user1@user.com')
        cls.user3 = User.objects.create_user('user3', 'user2@user.com')

        cls.author1 = models.Author.objects.create(github='https://api.github.com/users/jejewittt',
									localuser=cls.user1,
									displayName='user1',
									image='https://avatars0.githubusercontent.com/u/25070007?v=4', 
									feed='https://api.github.com/users/jejewittt/events') 
        cls.author3 = models.Author.objects.create(github='https://api.github.com/users/jejewittt',
									localuser=cls.user3,
									displayName='user3',
									image='https://avatars0.githubusercontent.com/u/25070007?v=4', 
									feed='https://api.github.com/users/jejewittt/events')
                                                            
        cls.public_post = models.Post.objects.create(author=cls.author1,title='public', 
									source='http://1.1',
									origin='http://1.1',contentType='PUBLIC',
									description='PUBLIC',content='PUBLIC',
									unlisted=False,published='2019-03-13',
									visibility='PUBLIC')

        cls.public_post_comment = models.Comment.objects.create(author=cls.author1,post=cls.public_post,
                                    comment="test",contentType='PUBLIC',published='2019-03-19')

        cls.author1.friends.add(cls.author3)

    def testGetHome(self):
        client = APIClient()
        response = client.get('')
        self.assertEqual(response.status_code, 200)

    def testGetAuthor(self):
        client = APIClient()
        path = self.author1.get_absolute_url()
        response = client.get(path)
        self.assertEqual(response.status_code, 200)

    def testGetPost(self):
        client = APIClient()
        path = self.public_post.get_absolute_url()
        response = client.get(path)
        self.assertEqual(response.status_code, 200)
  
    def testGetPostEdit(self):
        client = APIClient()
        path = self.public_post.get_absolute_url() + "edit"
        response = client.get(path)
        self.assertEqual(response.status_code, 302)

    def testGetPostDelete(self):
        client = APIClient()
        path = self.public_post.get_absolute_url() + "delete"
        response = client.get(path)
        self.assertEqual(response.status_code, 302)
 
    def testGetCommentEdit(self):
        client = APIClient()
        path = self.public_post_comment.get_edit_url()
        response = client.get(path)
        #TODO Investigate
        self.assertEqual(response.status_code, 302)

    def testGetCommentCreate(self):
        client = APIClient()
        path = self.public_post.get_absolute_url()
        path = "/Comment" + path[5:] + "create"
        response = client.get(path)
        self.assertEqual(response.status_code, 200)

    def testGetCommentDelete(self):
        client = APIClient()
        path = self.public_post_comment.get_delete_url()
        response = client.get(path)
        self.assertEqual(response.status_code, 302)

    """
    def testGetAuthorRemoveFriend(self):
        client = APIClient()
        temp1 = self.author3.get_absolute_url()
        path = temp[:8] + "remove-friend/" + temp[8:]
        response = client.get(path)
        self.assertEqual(response.status_code, 200)
    """

    """
    def testGetAuthorSendRequest(self):
        client = APIClient()
        temp = self.author3.get_absolute_url()
        path = temp[:8] + "send-request/" + temp[8:]
        response = client.get(path)
        self.assertEqual(response.status_code, 200)
    """

    """
    def testGetAuthorAcceptRequest(self):
        client = APIClient()
        temp1 = self.author1.get_absolute_url()
        path = temp[:8] + "accept-request/" + temp[8:]
        response = client.get(path)
        self.assertEqual(response.status_code, 200)
    """

    """
    def testGetAuthorDeclineRequest(self):
        client = APIClient()
        temp1 = self.author1.get_absolute_url()
        path = temp[:8] + "decline-request/" + temp[8:]
        response = client.get(path)
        self.assertEqual(response.status_code, 200)
    """

    """
    def testGetPostCreate(self):
        client = APIClient()
        path = "/Post/create/"
        response = client.get(path)
        self.assertEqual(response.status_code, 200)
    """

    """
    def testPostPost(self):
        client = APIClient()
        path = "/Post/create/"

        #author = self.author1
        #title = "test"
        #source = 'http://1.1'
        #origin = 'http://1.1'
        #contentType = 'PUBLIC'
        #description = 'testpostpost'
        #content = 'does it work?'
        #unlisted = False
        #published = '2019-03-19'
        #visibility = 'PUBLIC'

        responce = client.post(path, {'author': 'author1', 'title': 'test', 'source': 'http://1.1', 'origin': 'http://1.1', 
        'contentType': 'PUBLIC', 'description': 'testpostpost', 'content': 'does it work?', 'unlisted': 'False', 
        'published': '2019-03-19', 'visibility': 'PUBLIC'})

        print('\n')
        print(responce)
        print('\n')
    """

    #login = self.client.login(username='user1')

    #print('\n')
    #print(path)
    #print('\n')