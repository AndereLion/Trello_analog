from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from trello.models import Task, TaskType, Position, Project

TASK_URL = reverse("trello:tasks-list")
MANUFACTURER_URL_WITH_SEARCHING_BY_NAME = reverse(
    "trello:tasks-list"
) + "?name=3"
HOME_URL = reverse("trello:index")


def get_test_worker():
    position = Position.objects.create(name="Test")
    return get_user_model().objects.create_user(
        username="AdminUser",
        password="12121212@A",
        first_name="Admin",
        last_name="User",
        email="admin@mail.com",
        position=position,
    )


class PublicTaskTests(TestCase):
    def test_login_required(self):
        response = self.client.get(TASK_URL)
        self.assertEqual(response.status_code, 302)


class PrivateTaskTests(TestCase):
    def setUp(self) -> None:
        self.task_type = TaskType.objects.create(name="QA")
        self.worker = get_test_worker()
        self.client.force_login(self.worker)

    def test_retrieve_tasks(self):
        task_queryset = Task.objects.all()
        response = self.client.get(TASK_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_list"]),
            list(task_queryset)
        )
        self.assertTemplateUsed(response, "trello/task_list.html")

    def test_retrieve_manufacturers_after_searching_by_name(self):
        task_queryset = Task.objects.filter(name__icontains="3")
        response = self.client.get(MANUFACTURER_URL_WITH_SEARCHING_BY_NAME)

        self.assertEqual(
            list(response.context["task_list"]),
            list(task_queryset)
        )
        self.assertTemplateUsed(response, "trello/task_list.html")

    def test_create_task(self):
        task_data = {
            "name": "Test Task",
            "description": "This is a test task",
            "deadline": "2024-04-05",
            "is_completed": False,
            "priority": "L",
            "task_type": self.task_type,

        }
        task = Task.objects.create(**task_data)
        self.assertEqual(task, Task.objects.get(id=task.id))
        self.assertEqual(Task.objects.count(), 1)


class PublicHomeTests(TestCase):
    def test_login_required(self):
        response = self.client.get(HOME_URL)
        self.assertEqual(response.status_code, 302)


class WorkerTests(TestCase):
    def test_worker_create(self):
        worker = get_test_worker()

        self.assertEqual(worker, get_user_model().objects.get(id=worker.id))
        response = self.client.get(HOME_URL)
        self.assertEqual(response.status_code, 302)
        self.client.force_login(worker)
        response = self.client.get(HOME_URL)
        self.assertEqual(response.status_code, 200)


class ProjectTests(TestCase):
    def setUp(self) -> None:
        self.worker = get_test_worker()
        self.client.force_login(self.worker)

    def test_project_create(self):
        project_data = {
            "name": "Test Project",
            "description": "This is a test project",
        }
        project = Project.objects.create(**project_data)
        self.assertEqual(project, Project.objects.get(id=project.id))
        self.assertEqual(Project.objects.count(), 1)
