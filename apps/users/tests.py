from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class RegisterAccessTests(TestCase):
    """Ro'yxatdan o'tish faqat administratorlarga ochiq bo'lishi kerak."""

    def _payload(self, **overrides):
        data = {
            'username': 'newdoc',
            'first_name': 'Yangi',
            'last_name': 'Shifokor',
            'email': 'new@example.com',
            'role': 'doctor',
            'phone': '',
            'department': '',
            'password1': 'Kuchli-Parol-2026',
            'password2': 'Kuchli-Parol-2026',
        }
        data.update(overrides)
        return data

    def test_anonymous_is_redirected_to_login(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_anonymous_cannot_create_admin_account(self):
        # Regressiya: avval istalgan odam o'zini "admin" roli bilan yarata olardi
        self.client.post(reverse('register'), self._payload(username='hacker', role='admin'))
        self.assertFalse(User.objects.filter(username='hacker').exists())

    def test_regular_user_gets_403(self):
        self.client.force_login(User.objects.create_user('nurse', password='x'))
        self.assertEqual(self.client.get(reverse('register')).status_code, 403)

    def test_staff_can_create_account(self):
        self.client.force_login(User.objects.create_user('boss', password='x', is_staff=True))
        response = self.client.post(reverse('register'), self._payload())
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newdoc', role='doctor').exists())


class ProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('doc', password='Eski-Parol-2026', role='doctor')
        self.client.force_login(self.user)

    def test_profile_update(self):
        response = self.client.post(reverse('profile'), {
            'first_name': 'Aziz', 'last_name': 'Karimov', 'email': 'a@example.com',
            'phone': '+998901234567', 'department': 'Neonatologiya',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.department, 'Neonatologiya')

    def test_profile_cannot_change_role(self):
        self.client.post(reverse('profile'), {
            'first_name': 'Aziz', 'last_name': '', 'email': '', 'phone': '', 'department': '',
            'role': 'admin', 'is_staff': 'on',
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.role, 'doctor')
        self.assertFalse(self.user.is_staff)

    def test_password_change(self):
        response = self.client.post(reverse('password-change'), {
            'old_password': 'Eski-Parol-2026',
            'new_password1': 'Yangi-Parol-2026!',
            'new_password2': 'Yangi-Parol-2026!',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('Yangi-Parol-2026!'))

    def test_login_page_renders_for_anonymous(self):
        self.client.logout()
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, reverse('register'))
