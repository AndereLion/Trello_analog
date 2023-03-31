from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from trello.models import Position


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        position = Position(name="PM")
        position.save()
        self.admin_superuser = get_user_model().objects.create_superuser(
            username="AdminUser",
            password="12121212@A",
            first_name="Admin",
            last_name="User",
            email="admin@mail.com",
            position=position,
        )
        self.client.force_login(self.admin_superuser)
        self.ordinary_user = get_user_model().objects.create_superuser(
            username="OrdinaryUser",
            password="12121212@A",
            first_name="Ordinary",
            last_name="User",
            email="norm@mail.com",
            position=position,
        )

    def test_worker_position_listed(self):
        url = reverse("admin:trello_worker_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.ordinary_user.position)

    def test_worker_detail_position_listed(self):
        url = reverse(
            "admin:trello_worker_change",
            args=[self.ordinary_user.id]
        )
        response = self.client.get(url)
        self.assertContains(response, self.ordinary_user.position)
