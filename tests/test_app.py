"""
Basic tests for Tiraz application
"""
import unittest
from app import create_app, db
from app.models import Item


class TirazTestCase(unittest.TestCase):
    """Test cases for Tiraz application"""

    def setUp(self):
        """Set up test client and database"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        """Test that the app exists"""
        self.assertIsNotNone(self.app)

    def test_app_is_testing(self):
        """Test that the app is in testing mode"""
        self.assertTrue(self.app.config['TESTING'])

    def test_home_page(self):
        """Test that the home page loads"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Tiraz', response.data)

    def test_about_page(self):
        """Test that the about page loads"""
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)

    def test_items_list_page(self):
        """Test that the items list page loads"""
        response = self.client.get('/items/')
        self.assertEqual(response.status_code, 200)

    def test_create_item_page(self):
        """Test that the create item page loads"""
        response = self.client.get('/items/create')
        self.assertEqual(response.status_code, 200)

    def test_create_item(self):
        """Test creating a new item"""
        response = self.client.post('/items/create', data={
            'name': 'Test Item',
            'description': 'Test Description',
            'style': 'Modern'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Check that item was created
        item = Item.query.filter_by(name='Test Item').first()
        self.assertIsNotNone(item)
        self.assertEqual(item.description, 'Test Description')
        self.assertEqual(item.style, 'Modern')

    def test_view_item(self):
        """Test viewing a single item"""
        # Create an item
        item = Item(name='Test Item', description='Test', style='Classic')
        db.session.add(item)
        db.session.commit()
        
        # View the item
        response = self.client.get(f'/items/{item.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Item', response.data)

    def test_edit_item(self):
        """Test editing an item"""
        # Create an item
        item = Item(name='Original Name', description='Original', style='Original')
        db.session.add(item)
        db.session.commit()
        
        # Edit the item
        response = self.client.post(f'/items/{item.id}/edit', data={
            'name': 'Updated Name',
            'description': 'Updated Description',
            'style': 'Updated Style'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Check that item was updated
        updated_item = Item.query.get(item.id)
        self.assertEqual(updated_item.name, 'Updated Name')
        self.assertEqual(updated_item.description, 'Updated Description')
        self.assertEqual(updated_item.style, 'Updated Style')

    def test_delete_item(self):
        """Test deleting an item"""
        # Create an item
        item = Item(name='To Delete', description='Delete me', style='Any')
        db.session.add(item)
        db.session.commit()
        item_id = item.id
        
        # Delete the item
        response = self.client.post(f'/items/{item_id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Check that item was deleted
        deleted_item = Item.query.get(item_id)
        self.assertIsNone(deleted_item)

    def test_item_model(self):
        """Test the Item model"""
        item = Item(name='Model Test', description='Testing model', style='Test')
        self.assertEqual(str(item), '<Item Model Test>')
        
        # Test to_dict method
        item_dict = item.to_dict()
        self.assertEqual(item_dict['name'], 'Model Test')
        self.assertEqual(item_dict['description'], 'Testing model')
        self.assertEqual(item_dict['style'], 'Test')


if __name__ == '__main__':
    unittest.main()
