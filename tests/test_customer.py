import unittest
import os
import sys
import requests
from unittest.mock import MagicMock, patch
from faker import Faker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from services.customerService import save, find_all
from models.customer import Customer

def mock_customer_data():
  faker = Faker()
  mock_customer = MagicMock()
  mock_customer.id = 1
  mock_customer.name = faker.name
  mock_customer.email = faker.email
  mock_customer.phone = faker.phone_number
  return mock_customer

def mock_customers_data():
  mock_customer1 = MagicMock(spec=Customer)
  mock_customer1.id = 1
  mock_customer1.name = "Customer 1"
  mock_customer1.email = "customer1@example.com"
  mock_customer1.phone = "1234567890"

  mock_customer2 = MagicMock(spec=Customer)
  mock_customer2.id = 2
  mock_customer2.name = "Customer 2"
  mock_customer2.email = "customer2@example.com"
  mock_customer2.phone = "0987654321"
  return [mock_customer1,mock_customer2]

def customer_save_url():
  data = {
	"name": "Daniel Durant",
    "email": "runedurant@gmail.com",
    "phone": "7852803958"
  }
  response = requests.post('https://advanced-api-deployment.onrender.com/customers/add-customer',json=data)
  return response

def customer_find_all_url():
  response = requests.get('https://advanced-api-deployment.onrender.com/customers/')
  return response

class TestCustomerEndpoints(unittest.TestCase):
  def setUp(self):
    self.app = create_app('DevelopmentConfig')
    self.app_context = self.app.app_context()
    self.app_context.push()

  def tearDown(self):
    self.app_context.pop()

# Services Tests  
  @patch('services.customerService.Session')
  def test_save(self, mock_session):
    mock_session.return_value.__enter__.return_value = mock_session

    customer_data = {
        'name': "Test Customer",
        'email': "test@example.com",
        'phone': "1234567890"
    }

    response = save(customer_data)

    self.assertIsNotNone(response)
    self.assertEqual(response.name, customer_data['name'])
    self.assertEqual(response.email, customer_data['email'])
    self.assertEqual(response.phone, customer_data['phone'])

  @patch('services.customerService.db.session.execute')
  def test_find_all(self, mock_execute):
    mock_customers = mock_customers_data()

    mock_execute.return_value.scalars.return_value.all.return_value = mock_customers

    customers = find_all()

    self.assertEqual(len(customers), 2)
    self.assertEqual(customers[0].name, "Customer 1")
    self.assertEqual(customers[1].name, "Customer 2")

# Endpoint Tests
  @patch('requests.post')
  def test_customer_save_url_success(self, mock_post):
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {'message': 'Customer added successfully'}

    response = customer_save_url()

    mock_post.assert_called_once_with('https://advanced-api-deployment.onrender.com/customers/add-customer',json={"name": "Daniel Durant", "email": "runedurant@gmail.com", "phone": "7852803958"})
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json(), {'message': 'Customer added successfully'})

  @patch('requests.post')
  def test_customer_save_url_failure(self, mock_post):
    mock_post.return_value.status_code = 400
    mock_post.return_value.json.return_value = {'error': 'Bad Request'}

    response = customer_save_url()

    mock_post.assert_called_once_with(
        'https://advanced-api-deployment.onrender.com/customers/add-customer',
        json={"name": "Daniel Durant", "email": "runedurant@gmail.com", "phone": "7852803958"}
    )
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.json(), {'error': 'Bad Request'})


  @patch('requests.get')
  def test_customer_find_all_url_success(self, mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{'customer_id': 1, 'name': 'Daniel Durant', 'email': 'runedurant@gmail.com', 'phone': '7852803958'}]

    response = customer_find_all_url()

    mock_get.assert_called_once_with('https://advanced-api-deployment.onrender.com/customers/')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), [{'customer_id': 1, 'name': 'Daniel Durant', 'email': 'runedurant@gmail.com', 'phone': '7852803958'}])

  @patch('requests.get')
  def test_customer_find_all_url_failure(self, mock_get):
    mock_get.return_value.status_code = 500
    mock_get.return_value.json.return_value = {'error': 'Internal Server Error'}

    response = customer_find_all_url()

    mock_get.assert_called_once_with('https://advanced-api-deployment.onrender.com/customers/')
    self.assertEqual(response.status_code, 500)
    self.assertEqual(response.json(), {'error': 'Internal Server Error'})
      
if __name__ == '__main__':
  unittest.main()