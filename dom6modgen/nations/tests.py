# dom6modgen/nations/tests.py

from unittest import mock

from django.test import TestCase, Client, override_settings
from django.urls import reverse
from .models import Nation
from django.contrib.auth import get_user_model

# the manifest storage needs collectstatic to have run, which it hasn't in tests
PLAIN_STATIC = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

class NationModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        # Create a test nation instance
        self.nation = Nation.objects.create(
            name='Test Nation',
            description='A nation for testing purposes.',
            creator=self.user
        )

    def test_nation_creation(self):
        """Test that a Nation can be created."""
        self.assertEqual(self.nation.name, 'Test Nation')
        self.assertEqual(self.nation.description, 'A nation for testing purposes.')
        self.assertEqual(self.nation.creator, self.user)
        self.assertIsNotNone(self.nation.created_at)
        self.assertIsNotNone(self.nation.updated_at)

    def test_nation_str_method(self):
        """Test the __str__ method of the Nation model."""
        self.assertEqual(str(self.nation), 'Test Nation')

    def test_unique_nation_name(self):
        """Test that nation names must be unique."""
        with self.assertRaises(Exception): # IntegrityError or similar
            Nation.objects.create(
                name='Test Nation',
                description='Another nation with the same name.',
                creator=self.user
            )

@override_settings(STORAGES=PLAIN_STATIC)
class NationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.nation = Nation.objects.create(
            name='Another Test Nation',
            description='Description for another test nation.',
            creator=self.user
        )

    def test_nation_list_view(self):
        """Test the nation list page can be accessed."""
        response = self.client.get(reverse('nations:nation_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nations/nation_list.html')
        self.assertContains(response, 'Another Test Nation')

    def test_nation_detail_view(self):
        """Test the nation detail page can be accessed."""
        response = self.client.get(reverse('nations:nation_detail', args=[self.nation.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nations/nation_detail.html')
        self.assertContains(response, 'Another Test Nation')
        self.assertContains(response, 'Description for another test nation.')

    def test_nation_create_view(self):
        """Test that a new nation can be created via the form."""
        # Log in the client as a user for form submission
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.post(reverse('nations:nation_create'), {
            'name': 'New Created Nation',
            'description': 'This nation was created via a test.'
        })
        self.assertEqual(response.status_code, 302) # Should redirect after successful creation
        self.assertTrue(Nation.objects.filter(name='New Created Nation').exists())

    def test_nation_update_view(self):
        """Test that an existing nation can be updated."""
        # Log in the client as a user for form submission
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('nations:nation_update', args=[self.nation.pk]), {
            'name': 'Updated Nation Name',
            'description': 'This description has been updated.'
        })
        self.assertEqual(response.status_code, 302) # Should redirect
        self.nation.refresh_from_db()
        self.assertEqual(self.nation.name, 'Updated Nation Name')
        self.assertEqual(self.nation.description, 'This description has been updated.')

    def test_nation_delete_view(self):
        """Test that a nation can be deleted."""
        # Log in the client as a user for form submission
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('nations:nation_delete', args=[self.nation.pk]))
        self.assertEqual(response.status_code, 302) # Should redirect
        self.assertFalse(Nation.objects.filter(pk=self.nation.pk).exists())

@override_settings(STORAGES=PLAIN_STATIC)
class NationPermissionTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.owner = User.objects.create_user(username='owner', password='testpassword')
        self.other = User.objects.create_user(username='other', password='testpassword')
        self.nation = Nation.objects.create(name='Owned Nation', description='Mine.', creator=self.owner)

    def test_create_requires_login(self):
        response = self.client.get(reverse('nations:nation_create'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('nations:nation_create')}")

    def test_create_sets_creator(self):
        self.client.login(username='other', password='testpassword')
        self.client.post(reverse('nations:nation_create'), {'name': 'Fresh', 'description': 'New one.'})
        self.assertEqual(Nation.objects.get(name='Fresh').creator, self.other)

    def test_other_user_cannot_edit(self):
        self.client.login(username='other', password='testpassword')
        response = self.client.post(reverse('nations:nation_update', args=[self.nation.pk]), {
            'name': 'Hijacked', 'description': 'Not yours.'
        })
        self.assertEqual(response.status_code, 403)
        self.nation.refresh_from_db()
        self.assertEqual(self.nation.name, 'Owned Nation')

    def test_other_user_cannot_delete(self):
        self.client.login(username='other', password='testpassword')
        response = self.client.post(reverse('nations:nation_delete', args=[self.nation.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Nation.objects.filter(pk=self.nation.pk).exists())

    def test_anonymous_cannot_delete(self):
        response = self.client.post(reverse('nations:nation_delete', args=[self.nation.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Nation.objects.filter(pk=self.nation.pk).exists())

    def test_staff_can_edit(self):
        get_user_model().objects.create_user(username='admin', password='testpassword', is_staff=True)
        self.client.login(username='admin', password='testpassword')
        response = self.client.post(reverse('nations:nation_update', args=[self.nation.pk]), {
            'name': 'Fixed By Admin', 'description': 'Tidied up.'
        })
        self.assertEqual(response.status_code, 302)

    def test_edit_buttons_hidden_from_other_users(self):
        self.client.login(username='other', password='testpassword')
        response = self.client.get(reverse('nations:nation_detail', args=[self.nation.pk]))
        self.assertNotContains(response, 'Edit Nation')

    @mock.patch('nations.views.genai')
    def test_other_user_cannot_run_generation(self, mock_genai):
        self.client.login(username='other', password='testpassword')
        response = self.client.post(reverse('nations:run_generation_step', args=[self.nation.pk]))
        self.assertEqual(response.status_code, 403)
        mock_genai.GenerativeModel.assert_not_called()

    def test_generation_requires_login(self):
        response = self.client.post(reverse('nations:run_generation_step', args=[self.nation.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    @mock.patch.dict('os.environ', {'GEMINI_API_KEY': 'test-key'})
    @mock.patch('nations.views.genai')
    def test_owner_can_run_generation(self, mock_genai):
        mock_genai.GenerativeModel.return_value.generate_content.return_value.text = 'An expanded concept.'
        self.client.login(username='owner', password='testpassword')
        response = self.client.post(reverse('nations:run_generation_step', args=[self.nation.pk]))
        self.assertRedirects(response, reverse('nations:nation_workshop', args=[self.nation.pk]))
        self.nation.refresh_from_db()
        self.assertEqual(self.nation.expanded_description, 'An expanded concept.')
        self.assertEqual(self.nation.generation_status, 'nation_details')
