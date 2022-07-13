import unittest
from peewee import *
import os
os.environ['TESTING'] = 'true'
from app import TimelinePost

MODELS = [TimelinePost]

test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_timeline_post(self):
        first_post = TimelinePost.create(name='John Doe', email='john@example.com', content='Hello world, I\'m John!')
        assert first_post.id == 1
        second_post = TimelinePost.create(name='Jane Doe', email='jane@example.com', content='Hello world, I\'m Jane!')
        assert second_post.id == 2
        # call get timeline post function/perform the required functionality
        # assert each value/object of each timeline post is correct
        get_first_post = TimelinePost.select().where(TimelinePost.id == 1)[0]
        assert get_first_post.name == 'John Doe'
        assert get_first_post.email == 'john@example.com'
        assert get_first_post.content == 'Hello world, I\'m John!'
        get_second_post = TimelinePost.select().where(TimelinePost.id == 2)[0]
        assert get_second_post.name == 'Jane Doe'
        assert get_second_post.email == 'jane@example.com'
        assert get_second_post.content == 'Hello world, I\'m Jane!'

# use command python -m unittest -v tests.test_db to run the test