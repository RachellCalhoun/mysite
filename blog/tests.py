from django.test import TestCase
from blog.models import Post, Comment
from django.contrib.auth.models import User
from django.test import Client
from django.utils import timezone
import datetime
# Create your tests here.

class BlogTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='blogposter', email='blogposter@email.com', password='blogpost')
        self.post = Post.objects.create(title="testy title", text="description goes here", author=self.user, published_date=timezone.now())
        self.c = Client()

    def test_post_creation(self):
        """
        tests that we can create a post
        """
       
        self.assertEqual(self.post.title, 'testy title')
        self.assertEqual(self.post.author, self.user)

    def test_user_can_read(self):
        """
        tests that user is allowed to read
        """
        self.c.login(username='blogposter', password='blogpost')
        response = self.c.get('/post/1/')
        self.assertEqual(response.status_code, 200)

    def test_was_published_recently_with_future_post(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.post.published_date <= now

class CommentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='blogposter', email='blogposter@email.com', password='blogpost')
        self.user2 = User.objects.create_user(username='commenter', email='commenter@gmail.com', password="comment")
        self.post = Post.objects.create(title="testy title", text="description goes here", author=self.user, published_date=timezone.now())
        self.comment = Comment.objects.create(
            post=self.post, 
            author=self.user2.username, 
            text='this is a comment', 
            created_date=timezone.now(),
            
             )
        self.c = Client()

    def test_was_comment_author_user(self):
        """
        
        """
        self.assertEqual(self.comment.author, self.user2.username)
        self.assertEqual(self.comment.post, self.post)

    def test_was_comment_approved(self):
        """
        """
        self.assertIs(self.comment.approved_comment, False)
    
    def test_will_comment_be_approved(self):
        """
        """
        self.comment.approve()
        self.assertIs(self.comment.approved_comment, True)