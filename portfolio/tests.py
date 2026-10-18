from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from .models import CollaborationRequest, Project


class PortfolioTests(TestCase):
    def test_public_pages(self):
        for path in ('/', '/current-work/', '/collaborate/', '/admin-dashboard/'):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)

    def test_invalid_submission_is_not_saved(self):
        response = self.client.post('/collaborate/', {'email': 'invalid'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(CollaborationRequest.objects.count(), 0)

    def test_submission_is_saved_and_shown_on_dashboard(self):
        response = self.client.post('/collaborate/', {
            'name': 'Local Test', 'phone': '+9611234567',
            'email': 'local-test@example.com', 'gender': 'O', 'country': 'LEB',
            'available_online': 'on', 'project_name': 'Local smoke test',
        }, follow=True)
        self.assertRedirects(response, '/collaborate/')
        self.assertContains(response, 'submitted successfully')
        self.assertEqual(CollaborationRequest.objects.count(), 1)
        self.assertContains(self.client.get('/admin-dashboard/'), 'Local smoke test')

    def test_csrf_is_required(self):
        self.assertEqual(Client(enforce_csrf_checks=True).post('/collaborate/', {}).status_code, 403)

    def test_admin_authentication_and_model_pages(self):
        self.assertEqual(self.client.get('/admin/').status_code, 302)
        user = get_user_model().objects.create_superuser(
            username='local-test-admin', email='admin@example.com', password='test-only-password'
        )
        self.client.force_login(user)
        for path in ('/admin/', '/admin/portfolio/project/', '/admin/portfolio/collaborationrequest/'):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)
        project = Project.objects.create(title='Test project', description='Test description')
        self.assertEqual(str(project), 'Test project')
