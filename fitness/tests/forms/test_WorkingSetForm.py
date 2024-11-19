# Django
from django.test import TestCase

# App
from core.models import CustomUser
from fitness.forms import WorkingSetForm


class WorkingSetFormTest(TestCase):
    """Test WorkingSetForm"""
    def setUp(self):
        """Pre-set up for testing the form"""
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@mail.com",
            password="password123"
        )
        self.valid_data_as_weight = {
            'type': 'working',
            'weight': '100',
            'repetitions': '10',
            'distance': None,
            'time': None
        }
        self.valid_data_as_distance = {
            'type': 'working',
            'weight': None,
            'repetitions': None,
            'distance': '10',
            'time': '100'
        }
        self.invalid_data_type = {
            'type': 'training',
            'weight': '100',
            'repetitions': '10',
            'distance': None,
            'time': None
        }
        self.invalid_data_weight = {
            'type': 'working',
            'weight': 'abc',
            'repetitions': None,
            'distance': None,
            'time': None
        }
        self.invalid_data_repetitions = {
            'type': 'working',
            'weight': '100',
            'repetitions': 'abc',
            'distance': None,
            'time': None
        }
        self.invalid_data_distance = {
            'type': 'working',
            'weight': None,
            'repetitions': None,
            'distance': 'abc',
            'time': None
        }
        self.invalid_data_time = {
            'type': 'working',
            'weight': None,
            'repetitions': None,
            'distance': '100',
            'time': 'abc'
        }
        self.invalid_data_none = {
            'type': 'working',
            'weight': None,
            'repetitions': None,
            'distance': None,
            'time': None
        }

    def test_form_is_valid_weight(self):
        """Test if form is valid with correct data as weight"""
        form = WorkingSetForm(data=self.valid_data_as_weight)
        self.assertTrue(form.is_valid())

    def test_form_is_valid_distance(self):
        """Test if form is valid with correct data as distance"""
        form = WorkingSetForm(data=self.valid_data_as_distance)
        self.assertTrue(form.is_valid())

    def test_form_is_invalid_type(self):
        """Test if form is valid with incorrect data as type"""
        form = WorkingSetForm(data=self.invalid_data_type)
        self.assertFalse(form.is_valid())
    
    def test_form_is_invalid_weight(self):
        """Test if form is valid with incorrect data as weight value"""
        form = WorkingSetForm(data=self.invalid_data_weight)
        self.assertFalse(form.is_valid())
    
    def test_form_is_invalid_value_repetitions(self):
        """Test if form is valid with incorrect data as repetitions value"""
        form = WorkingSetForm(data=self.invalid_data_repetitions)
        self.assertFalse(form.is_valid())

    def test_form_is_invalid_value_distance(self):
        """Test if form is valid with incorrect data as distance value"""
        form = WorkingSetForm(data=self.invalid_data_distance)
        self.assertFalse(form.is_valid())
    
    def test_form_is_invalid_value_time(self):
        """Test if form is valid with incorrect data as time value"""
        form = WorkingSetForm(data=self.invalid_data_time)
        self.assertFalse(form.is_valid())

    def test_form_is_valid_value_none(self):
        """Test if form is valid with correct data as none values"""
        form = WorkingSetForm(data=self.invalid_data_none)
        self.assertTrue(form.is_valid())

        