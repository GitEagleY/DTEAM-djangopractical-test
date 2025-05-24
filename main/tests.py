from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework import status
import json

from .models import ModelCV, validate_list_of_strings, validate_dict_of_strings,RequestLog
from .serializers import CVSerializer
from django.utils.timezone import now

class RequestLogTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_middleware_logs_request(self):
        # This should trigger the middleware and log the request
        self.client.get("/")
        log = RequestLog.objects.last()

        self.assertIsNotNone(log)
        self.assertEqual(log.http_method, "GET")
        self.assertEqual(log.path, "/")

    def test_recent_requests_view_displays_logs(self):
        # Create a log manually
        RequestLog.objects.create(http_method="GET", path="/test/", timestamp=now())
        response = self.client.get(reverse("recent_requests"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/test/")
        self.assertTemplateUsed(response, "main/request_log_list.html")

    def test_admin_url_does_not_log(self):
        self.client.get("/admin/")
        self.assertFalse(RequestLog.objects.exists())

    def test_url_patterns_resolve(self):
        response = self.client.get(reverse("template_list"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("api-cv-list"))
        self.assertEqual(response.status_code, 200)

        # Assuming pk=1 exists or you handle 404 gracefully
        response = self.client.get(reverse("api-cv-detail", kwargs={"pk": 1}))
        self.assertIn(response.status_code, [200, 404])
class ModelCVTestCase(TestCase):
    """Test cases for ModelCV model"""
    
    def setUp(self):
        """Set up test data"""
        self.valid_cv_data = {
            'firstname': 'John',
            'lastname': 'Doe',
            'bio': 'Software developer with 5 years of experience',
            'skills': ['Python', 'Django', 'JavaScript'],
            'projects': [
                {'name': 'E-commerce Site', 'description': 'Built with Django'},
                {'name': 'Mobile App', 'description': 'React Native app'}
            ],
            'contacts': {
                'email': 'john.doe@example.com',
                'phone': '+1234567890',
                'linkedin': 'linkedin.com/in/johndoe'
            }
        }
    
    def test_create_cv_success(self):
        """Test creating a CV with valid data"""
        cv = ModelCV.objects.create(**self.valid_cv_data)
        self.assertEqual(cv.firstname, 'John')
        self.assertEqual(cv.lastname, 'Doe')
        self.assertEqual(cv.bio, 'Software developer with 5 years of experience')
        self.assertEqual(len(cv.skills), 3)
        self.assertEqual(len(cv.projects), 2)
        self.assertEqual(len(cv.contacts), 3)
    
    def test_cv_str_method(self):
        """Test the string representation of CV"""
        cv = ModelCV.objects.create(**self.valid_cv_data)
        self.assertEqual(str(cv), 'John Doe')
    
    def test_cv_fields_max_length(self):
        """Test maximum length constraints"""
        # Test firstname max length
        long_name = 'a' * 101
        cv_data = self.valid_cv_data.copy()
        cv_data['firstname'] = long_name
        
        cv = ModelCV(**cv_data)
        with self.assertRaises(ValidationError):
            cv.full_clean()
    
    def test_empty_required_fields(self):
        """Test validation with empty required fields"""
        cv = ModelCV()
        with self.assertRaises(ValidationError):
            cv.full_clean()


class ValidationHelpersTestCase(TestCase):
    """Test cases for validation helper functions"""
    
    def test_validate_list_of_strings_success(self):
        """Test validate_list_of_strings with valid data"""
        valid_lists = [
            ['Python', 'Django'],
            ['JavaScript', 'React', 'Node.js'],
            ['Single item']
        ]
        
        for valid_list in valid_lists:
            try:
                validate_list_of_strings(valid_list)
            except ValidationError:
                self.fail(f"validate_list_of_strings raised ValidationError for {valid_list}")
    
    def test_validate_list_of_strings_failures(self):
        """Test validate_list_of_strings with invalid data"""
        invalid_cases = [
            "not a list",
            123,
            ['valid', 123, 'mixed'],  # mixed types
            ['valid', ''],  # empty string
            ['valid', '   '],  # whitespace only
            []  # empty list is valid though
        ]
        
        for invalid_case in invalid_cases[:-1]:  # exclude empty list
            with self.assertRaises(ValidationError):
                validate_list_of_strings(invalid_case)
    
    def test_validate_dict_of_strings_success(self):
        """Test validate_dict_of_strings with valid data"""
        valid_dicts = [
            {'email': 'test@example.com', 'phone': '123456789'},
            {'linkedin': 'linkedin.com/profile'},
            {'key': 'value'}
        ]
        
        for valid_dict in valid_dicts:
            try:
                validate_dict_of_strings(valid_dict)
            except ValidationError:
                self.fail(f"validate_dict_of_strings raised ValidationError for {valid_dict}")
    
    def test_validate_dict_of_strings_failures(self):
        """Test validate_dict_of_strings with invalid data"""
        invalid_cases = [
            "not a dict",
            ['list', 'instead'],
            {123: 'numeric key'},
            {'': 'empty key'},
            {'   ': 'whitespace key'},
            {'key': 123},  # non-string value
            {'key': ''},  # empty value
            {'key': '   '}  # whitespace value
        ]
        
        for invalid_case in invalid_cases:
            with self.assertRaises(ValidationError):
                validate_dict_of_strings(invalid_case)


class CVSerializerTestCase(TestCase):
    """Test cases for CVSerializer"""
    
    def setUp(self):
        """Set up test data"""
        self.valid_data = {
            'firstname': 'Jane',
            'lastname': 'Smith',
            'bio': 'Frontend developer',
            'skills': ['HTML', 'CSS', 'JavaScript'],
            'projects': [{'name': 'Portfolio', 'description': 'Personal website'}],
            'contacts': {'email': 'jane@example.com'}
        }
        
        self.cv = ModelCV.objects.create(**self.valid_data)
    
    def test_serializer_serialize(self):
        """Test serializing a CV instance"""
        serializer = CVSerializer(self.cv)
        data = serializer.data
        
        self.assertEqual(data['firstname'], 'Jane')
        self.assertEqual(data['lastname'], 'Smith')
        self.assertEqual(data['bio'], 'Frontend developer')
        self.assertEqual(data['skills'], ['HTML', 'CSS', 'JavaScript'])
    
    def test_serializer_deserialize_valid(self):
        """Test deserializing valid data"""
        serializer = CVSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        
        cv = serializer.save()
        self.assertEqual(cv.firstname, 'Jane')
        self.assertEqual(cv.lastname, 'Smith')
    
    def test_serializer_deserialize_invalid(self):
        """Test deserializing invalid data"""
        invalid_data = self.valid_data.copy()
        del invalid_data['firstname']  # Remove required field
        
        serializer = CVSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('firstname', serializer.errors)


class CVViewsTestCase(TestCase):
    """Test cases for CV views (HTML views)"""
    
    def setUp(self):
        """Set up test data and client"""
        self.client = Client()
        self.cv_data = {
            'firstname': 'Test',
            'lastname': 'User',
            'bio': 'Test bio',
            'skills': ['Skill1', 'Skill2'],
            'projects': [{'name': 'Project1', 'description': 'Description1'}],
            'contacts': {'email': 'test@example.com'}
        }
        self.cv = ModelCV.objects.create(**self.cv_data)
    
    def test_cv_list_view(self):
        """Test CV list view"""
        url = reverse('template_list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test User')
        self.assertIn('cvs', response.context)
        self.assertEqual(len(response.context['cvs']), 1)
    
    def test_cv_detail_view(self):
        """Test CV detail view"""
        url = reverse('template_detail', kwargs={'pk': self.cv.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test User')
        self.assertContains(response, 'Test bio')
        self.assertIn('cv', response.context)
        self.assertEqual(response.context['cv'].pk, self.cv.pk)
    
    def test_cv_detail_view_not_found(self):
        """Test CV detail view with non-existent CV"""
        url = reverse('template_detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)


class CVAPITestCase(APITestCase):
    """Test cases for CV API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.cv_data = {
            'firstname': 'API',
            'lastname': 'Test',
            'bio': 'API test bio',
            'skills': ['Python', 'Django'],
            'projects': [{'name': 'API Project', 'description': 'Testing API'}],
            'contacts': {'email': 'api@test.com', 'phone': '123456789'}
        }
        self.cv = ModelCV.objects.create(**self.cv_data)
        self.list_url = reverse('api-cv-list')
        self.detail_url = reverse('api-cv-detail', kwargs={'pk': self.cv.pk})
    
    def test_get_cv_list(self):
        """Test GET request to CV list endpoint"""
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['firstname'], 'API')
    
    def test_create_cv_via_api(self):
        """Test POST request to create CV via API"""
        new_cv_data = {
            'firstname': 'New',
            'lastname': 'User',
            'bio': 'New user bio',
            'skills': ['Vue.js', 'Node.js'],
            'projects': [{'name': 'New Project', 'description': 'New project desc'}],
            'contacts': {'email': 'new@user.com'}
        }
        
        response = self.client.post(self.list_url, new_cv_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ModelCV.objects.count(), 2)
    
    def test_get_cv_detail_via_api(self):
        """Test GET request to CV detail endpoint"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['firstname'], 'API')
        self.assertEqual(response.data['lastname'], 'Test')
    
    def test_update_cv_via_api(self):
        """Test PUT request to update CV via API"""
        updated_data = self.cv_data.copy()
        updated_data['bio'] = 'Updated bio'
        
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cv.refresh_from_db()
        self.assertEqual(self.cv.bio, 'Updated bio')
    
    def test_delete_cv_via_api(self):
        """Test DELETE request to remove CV via API"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ModelCV.objects.count(), 0)
    
    def test_create_cv_invalid_data(self):
        """Test POST request with invalid data"""
        invalid_data = {
            'firstname': '',  # Empty required field
            'lastname': 'Test',
            'bio': 'Test bio'
        }
        
        response = self.client.post(self.list_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CVIntegrationTestCase(TestCase):
    """Integration tests for CV functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
    
    def test_full_cv_workflow(self):
        """Test complete CV workflow from creation to deletion"""
        # Create CV
        cv_data = {
            'firstname': 'Integration',
            'lastname': 'Test',
            'bio': 'Full workflow test',
            'skills': ['Python', 'Testing'],
            'projects': [{'name': 'Test Project', 'description': 'Integration test'}],
            'contacts': {'email': 'integration@test.com'}
        }
        
        cv = ModelCV.objects.create(**cv_data)
        self.assertEqual(ModelCV.objects.count(), 1)
        
        # Test list view shows CV
        list_response = self.client.get(reverse('template_list'))
        self.assertEqual(list_response.status_code, 200)
        self.assertContains(list_response, 'Integration Test')
        
        # Test detail view shows CV details
        detail_response = self.client.get(reverse('template_detail', kwargs={'pk': cv.pk}))
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, 'Full workflow test')
        
        # Test CV can be updated
        cv.bio = 'Updated workflow test'
        cv.save()
        cv.refresh_from_db()
        self.assertEqual(cv.bio, 'Updated workflow test')
        
        # Test CV can be deleted
        cv.delete()
        self.assertEqual(ModelCV.objects.count(), 0)
    
    def test_multiple_cvs_handling(self):
        """Test handling multiple CVs"""
        # Create multiple CVs
        cv1 = ModelCV.objects.create(
            firstname='First', lastname='User', bio='First bio',
            skills=['Skill1'], projects=[{'name': 'P1', 'description': 'D1'}],
            contacts={'email': 'first@test.com'}
        )
        cv2 = ModelCV.objects.create(
            firstname='Second', lastname='User', bio='Second bio',
            skills=['Skill2'], projects=[{'name': 'P2', 'description': 'D2'}],
            contacts={'email': 'second@test.com'}
        )
        
        # Test list view shows both CVs
        response = self.client.get(reverse('template_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First User')
        self.assertContains(response, 'Second User')
        self.assertEqual(len(response.context['cvs']), 2)
        
        # Test individual detail views
        detail1 = self.client.get(reverse('template_detail', kwargs={'pk': cv1.pk}))
        detail2 = self.client.get(reverse('template_detail', kwargs={'pk': cv2.pk}))
        
        self.assertEqual(detail1.status_code, 200)
        self.assertEqual(detail2.status_code, 200)
        self.assertContains(detail1, 'First bio')
        self.assertContains(detail2, 'Second bio')


class CVEdgeCasesTestCase(TestCase):
    """Test edge cases and error conditions"""
    
    def test_cv_with_empty_json_fields(self):
        """Test CV with empty JSON fields"""
        cv = ModelCV.objects.create(
            firstname='Empty',
            lastname='JSON',
            bio='Test with empty JSON fields',
            skills=[],
            projects=[],
            contacts={}
        )
        
        self.assertEqual(len(cv.skills), 0)
        self.assertEqual(len(cv.projects), 0)
        self.assertEqual(len(cv.contacts), 0)
        self.assertEqual(str(cv), 'Empty JSON')
    
    def test_cv_with_unicode_characters(self):
        """Test CV with unicode characters"""
        cv = ModelCV.objects.create(
            firstname='José',
            lastname='García',
            bio='Développeur avec expérience en 中文',
            skills=['Python', '中文编程'],
            projects=[{'name': 'Proyecto', 'description': 'Descripción'}],
            contacts={'email': 'josé@example.com'}
        )
        
        self.assertEqual(cv.firstname, 'José')
        self.assertEqual(cv.lastname, 'García')
        self.assertEqual(str(cv), 'José García')
    
    def test_cv_with_large_json_data(self):
        """Test CV with large JSON data"""
        large_skills = [f'Skill_{i}' for i in range(100)]
        large_projects = [
            {'name': f'Project_{i}', 'description': f'Description_{i}'}
            for i in range(50)
        ]
        large_contacts = {f'contact_{i}': f'value_{i}' for i in range(20)}
        
        cv = ModelCV.objects.create(
            firstname='Large',
            lastname='Data',
            bio='CV with large JSON data',
            skills=large_skills,
            projects=large_projects,
            contacts=large_contacts
        )
        
        self.assertEqual(len(cv.skills), 100)
        self.assertEqual(len(cv.projects), 50)
        self.assertEqual(len(cv.contacts), 20)