import random

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from tasks.models import Category, Note, Priority, SubTask, Task

STATUSES = ["Pending", "In Progress", "Completed"]


class Command(BaseCommand):
    help = "Seed Priority/Category and generate fake Task, Note and SubTask data."

    def add_arguments(self, parser):
        parser.add_argument("--tasks", type=int, default=10, help="How many fake tasks to create")

    def handle(self, *args, **options):
        fake = Faker()

        for name in ["High", "Medium", "Low", "Critical", "Optional"]:
            Priority.objects.get_or_create(name=name)
        for name in ["Work", "School", "Personal", "Finance", "Projects"]:
            Category.objects.get_or_create(name=name)

        priorities = list(Priority.objects.all())
        categories = list(Category.objects.all())

        for _ in range(options["tasks"]):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                status=fake.random_element(elements=STATUSES),
                category=random.choice(categories),
                priority=random.choice(priorities),
            )
            for _ in range(random.randint(1, 3)):
                SubTask.objects.create(
                    parent_task=task,
                    title=fake.sentence(nb_words=4),
                    status=fake.random_element(elements=STATUSES),
                )
            for _ in range(random.randint(0, 2)):
                Note.objects.create(task=task, content=fake.paragraph(nb_sentences=2))

        self.stdout.write(self.style.SUCCESS(f"Created {options['tasks']} tasks with subtasks and notes."))
