import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from trello.forms import WorkerCreationForm, TaskForm

from trello.models import Position, TaskType, Tag, Project


class FormTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="QA")
        self.user_data = {
            "position": self.position,
            "username": "OrdinaryUser",
            "first_name": "Ordinary",
            "last_name": "User",
            "email": "xxx@mail.com",
            "password1": "12121212@A",
            "password2": "12121212@A",
        }

    def test_worker_creation_form_with_additional_parameters(self):
        form = WorkerCreationForm(data=self.user_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.user_data)

    def test_task_form_valid_data(self):
        tag = Tag.objects.create(name="Test Tag")
        project = Project.objects.create(name="Test Project")
        worker = get_user_model().objects.create_user(
            self.user_data
        )
        form_data = {
            "name": "Test Task",
            "description": "This is a test task",
            "deadline": datetime.date(2023, 4, 30),
            "is_completed": False,
            "priority": "L",
            "task_type": TaskType.objects.create(name="Test Task Type"),
            "title": "Test Task",
            "assignees": [worker.id],
            "tags": [tag.id],
            "projects": [project.id],
        }

        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data.get("name"),
            form_data.get("name")
        )
        self.assertEqual(
            form.cleaned_data.get("deadline"),
            form_data.get("deadline")
        )

    def test_task_form_blank_data(self):
        form = TaskForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)
