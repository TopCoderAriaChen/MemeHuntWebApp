import unittest
from flask import current_app, url_for
from app import create_app, db
import config  # Import the config module
from models.user import UserModel, RoleModel
from models.post import PostModel, CommentModel, BoardModel
from blueprints.cms import bp

class CmsBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config.TestingConfig)  # Use testing configuration
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_index_route(self):
        response = self.client.get(url_for('cms.index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('CMS Home Page', response.get_data(as_text=True))

    def test_staff_list_route(self):
        response = self.client.get(url_for('cms.staff_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Staff List', response.get_data(as_text=True))

    def test_add_staff_route(self):
        with self.client:
            response = self.client.post(url_for('cms.add_staff'), data={
                'email': 'test@example.com',
                'role': 1
            })
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, url_for('cms.staff_list', _external=True))
    
    def test_edit_staff_route(self):
        test_user = UserModel(username='test', email='test@example.com', password='password')
        db.session.add(test_user)
        db.session.commit()
        
        with self.client:
            response = self.client.post(url_for('cms.edit_staff', user_id=test_user.id), data={
                'is_staff': True,
                'role': 2
            })
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, url_for('cms.staff_list', _external=True))
            
    def test_dele_staff_route(self):
        test_user = UserModel(username='test', email='test@example.com', password='password')
        db.session.add(test_user)
        db.session.commit()
        
        with self.client:
            response = self.client.post(url_for('cms.dele_staff', user_id=test_user.id))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, url_for('cms.staff_list', _external=True))
    
    def test_user_list_route(self):
        response = self.client.get(url_for('cms.user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('User List', response.get_data(as_text=True))
    
    def test_active_user_route(self):
        test_user = UserModel(username='test', email='test@example.com', password='password')
        db.session.add(test_user)
        db.session.commit()
        
        with self.client:
            response = self.client.post(url_for('cms.active_user', user_id=test_user.id), data={
                'is_active': 1
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', response.get_data(as_text=True))
    
    def test_post_list_route(self):
        response = self.client.get(url_for('cms.post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Post List', response.get_data(as_text=True))
    
    def test_active_post_route(self):
        test_post = PostModel(title='Test Post', content='This is a test post')
        db.session.add(test_post)
        db.session.commit()
        
        with self.client:
            response = self.client.post(url_for('cms.active_post', post_id=test_post.id), data={
                'is_active': 1
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', response.get_data(as_text=True))
    
    def test_comment_list_route(self):
        response = self.client.get(url_for('cms.comment_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Comment List', response.get_data(as_text=True))
    
    def test_active_comment_route(self):
        test_comment = CommentModel(content='Test Comment')
        db.session.add(test_comment)
        db.session.commit()
        
        with self.client:
            response = self.client.post(url_for('cms.active_comment', comment_id=test_comment.id), data={
                'is_active': 1
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', response.get_data(as_text=True))
    
    def test_board_list_route(self):
        response = self.client.get(url_for('cms.board_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Board List', response.get_data(as_text=True))
    
    def test_edit_board_route(self):
        test_board = BoardModel(name='Test Board')
        db.session.add(test_board)
        db.session.commit()
        
        with self.client:
            response = self.client.post(url_for('cms.edit_board'), data={
                'board_id': test_board.id,
                'name': 'Updated Board'
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', response.get_data(as_text=True))
    
    def test_active_board_route(self):
        test_board = BoardModel(name='Test Board')
        db.session.add(test_board)
        db.session.commit()
        
        with self.client:
            response = self.client.delete(url_for('cms.active_board', board_id=test_board.id), data={
                'is_active': True
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
