from django.test import TestCase

from trello.forms import WorkerCreationForm

from trello.models import Position


class FormTests(TestCase):
    def test_worker_creation_form_with_additional_parameters(self):
        position = Position.objects.create(name="QA")
        form_data = {
            "position": position,
            "username": "OrdinaryUser",
            "first_name": "Ordinary",
            "last_name": "User",
            "email": "xxx@mail.com",
            "password1": "12121212@A",
            "password2": "12121212@A",

        }

        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
