from django.test import TestCase
from django.contrib.auth import get_user_model

from trello.models import (
    Position,
    TaskType,
    Project,
    Team,
    Task
)


class ModelsTests(TestCase):
    def setUp(self):
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

    def test_position_str(self):
        position = self.position
        self.assertEqual(
            str(position),
            f"{position.name}"

        )

    def test_worker_str(self):
        worker = self.worker
        self.assertEqual(
            str(worker),
            f"{worker.username} "
            f"({worker.first_name} "
            f"{worker.last_name})"
        )

    def test_task_type_str(self):
        task_type = TaskType.objects.create(
            name="Refactoring"
        )
        self.assertEqual(str(task_type), task_type.name)

    def test_tag_str(self):
        tag = TaskType.objects.create(
            name="Charity"
        )
        self.assertEqual(str(tag), tag.name)

    def test_project_str(self):
        project = Project.objects.create(
            name="Charity",
            description="Good one"
        )
        self.assertEqual(str(project), project.name)

    def test_team_str(self):
        team = Team.objects.create(
            name="Best",
            description="Good one"
        )
        self.assertEqual(str(team), team.name)

    def test_task_str(self):
        task_type = TaskType.objects.create(name="QA")
        task = Task.objects.create(
            name="Best",
            description="Good one",
            deadline="2024-04-05",
            is_completed=False,
            task_type=task_type,

        )
        self.assertEqual(str(task), task.name)
