import unittest
from flask import url_for
from app import create_app, db
import config
from models.user import UserModel
from models.post import PostModel, CommentModel, BoardModel

class CmsBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config.TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

        # Create a unique test user for relationships
        self.test_user = UserModel(username=f'testuser_{self._testMethodName}', email=f'testuser_{self._testMethodName}@example.com', password='password')
        db.session.add(self.test_user)
        db.session.commit()

        self.login_test_user()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login_test_user(self):
        with self.client:
            # Simulate the login logic. Update this to match your app's login route.
            response = self.client.post('/user/login', data=dict(
                email=self.test_user.email,
                password='password'
            ), follow_redirects=True)
            self.assertTrue(response)

    def test_index_route(self):
        response = self.client.get(url_for('cms.index'))
        self.assertTrue(response)

    def test_staff_list_route(self):
        response = self.client.get(url_for('cms.staff_list'))
        self.assertTrue(response)

    def test_add_staff_route(self):
        response = self.client.post(url_for('cms.add_staff'), data={
            'email': f'newstaff_{self._testMethodName}@example.com',  # Ensure a unique email
            'role': 1,
            'csrf_token': self.get_csrf_token()
        })
        self.assertTrue(response)

    def test_edit_staff_route(self):
        test_user = UserModel(username=f'testedit_{self._testMethodName}', email=f'testedit_{self._testMethodName}@example.com', password='password')
        db.session.add(test_user)
        db.session.commit()

        response = self.client.post(url_for('cms.edit_staff', user_id=test_user.id), data={
            'is_staff': True,
            'role': 2,
            'csrf_token': self.get_csrf_token()
        })
        self.assertTrue(response)

    def test_dele_staff_route(self):
        test_user = UserModel(username=f'testdelete_{self._testMethodName}', email=f'testdelete_{self._testMethodName}@example.com', password='password')
        db.session.add(test_user)
        db.session.commit()

        response = self.client.post(url_for('cms.dele_staff', user_id=test_user.id), data={
            'csrf_token': self.get_csrf_token()
        })
        self.assertTrue(response)

    def test_user_list_route(self):
        response = self.client.get(url_for('cms.user_list'))
        self.assertTrue(response)

    def test_active_user_route(self):
        test_user = UserModel(username=f'testactive_{self._testMethodName}', email=f'testactive_{self._testMethodName}@example.com', password='password')
        db.session.add(test_user)
        db.session.commit()

        response = self.client.post(url_for('cms.active_user', user_id=test_user.id), data={
            'is_active': 1,
            'csrf_token': self.get_csrf_token()
        })
        self.assertTrue(response)

    def test_post_list_route(self):
        response = self.client.get(url_for('cms.post_list'))
        self.assertTrue(response)

    def test_active_post_route(self):
        test_post = PostModel(title='Test Post', content='This is a test post', author_id=self.test_user.id)
        db.session.add(test_post)
        db.session.commit()

        response = self.client.post(url_for('cms.active_post', post_id=test_post.id), data={
            'is_active': 1,
            'csrf_token': self.get_csrf_token()
        })
        self.assertTrue(response)

    def test_comment_list_route(self):
        response = self.client.get(url_for('cms.comment_list'))
        self.assertTrue(response)

    def test_active_comment_route(self):
        test_comment = CommentModel(content='Test Comment', author_id=self.test_user.id)
        db.session.add(test_comment)
        db.session.commit()

        response = self.client.post(url_for('cms.active_comment', comment_id=test_comment.id), data={
            'is_active': 1,
            'csrf_token': self.get_csrf_token()
        })
        self.assertTrue(response)

    def test_board_list_route(self):
        response = self.client.get(url_for('cms.board_list'))
        self.assertTrue(response)

    def test_edit_board_route(self):
        test_board = BoardModel(name='Test Board')
        db.session.add(test_board)
        db.session.commit()

        response = self.client.post(url_for('cms.edit_board'), data={
            'board_id': test_board.id,
            'name': 'Updated Board',
            'csrf_token': self.get_csrf_token()
        })
        self.assertTrue(response)

    def test_active_board_route(self):
        test_board = BoardModel(name='Test Board')
        db.session.add(test_board)
        db.session.commit()

        response = self.client.delete(url_for('cms.active_board', board_id=test_board.id), data={
            'is_active': True,
            'csrf_token': self.get_csrf_token()
        })
        self.assertTrue(response)

    def get_csrf_token(self):
        response = self.client.get(url_for('cms.index'))  # Updated to match correct endpoint
        token = response.headers.get('csrf-token')
        return token

if __name__ == '__main__':
    unittest.main()
