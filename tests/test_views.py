from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from trello.models import (
    Task,
    TaskType,
    Team,
    Position,
    Tag,
    Project
)

TASK_URL = reverse("trello:tasks-list")
MANUFACTURER_URL_WITH_SEARCHING_BY_NAME = reverse(
    "trello:tasks-list"
) + "?name=3"
HOME_URL = reverse("trello:index")


# CAR_URL_WITH_SEARCHING_BY_MODEL = reverse("taxi:car-list") + "?model=mi"
# DRIVER_URL = reverse("taxi:driver-list")
# DRIVER_URL_WITH_SEARCHING_BY_USERNAME = reverse(
#     "taxi:driver-list"
# ) + "?username=an"


class PublicTaskTests(TestCase):

    def test_login_required(self):
        response = self.client.get(TASK_URL)
        self.assertEqual(response.status_code, 302)


class PrivateTaskTests(TestCase):
    def setUp(self) -> None:
        task_type = TaskType.objects.create(name="QA")
        task1 = Task.objects.create(
            name="Best",
            description="Good one",
            deadline="2024-04-05",
            is_completed=False,
            task_type=task_type,

        )
        task2 = Task.objects.create(
            name="Best2",
            description="Good one",
            deadline="2024-04-05",
            is_completed=False,
            task_type=task_type,

        )
        task3 = Task.objects.create(
            name="Best3",
            description="Good one",
            deadline="2024-04-05",
            is_completed=False,
            task_type=task_type,

        )
        self.position = Position.objects.create(
            name="Test"
        )
        self.worker = get_user_model().objects.create_user(

            username="AdminUser",
            password="12121212@A",
            first_name="Admin",
            last_name="User",
            email="admin@mail.com",
            position=self.position,
        )
        self.client.force_login(self.worker)

    def test_retrieve_tasks(self):
        task_queryset = Task.objects.all()
        response = self.client.get(TASK_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(
                response.context["task_list"]
            ), list(task_queryset)
        )
        self.assertTemplateUsed(response, "trello/task_list.html")

    def test_retrieve_manufacturers_after_searching_by_name(self):
        task_queryset = Task.objects.filter(
            name__icontains="3"
        )
        response = self.client.get(MANUFACTURER_URL_WITH_SEARCHING_BY_NAME)

        self.assertEqual(
            list(
                response.context["task_list"]
            ), list(task_queryset)
        )
        self.assertTemplateUsed(response, "trello/task_list.html")


class PublicHomeTests(TestCase):

    def test_login_required(self):
        response = self.client.get(HOME_URL)
        self.assertEqual(response.status_code, 302)
