import factory
import secrets
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.template.defaultfilters import slugify
from datetime import timedelta
from uuid import uuid4

from src.models.invites import Invite
from src.models.choice_classes import InviteChoices
from src.models.models import CustomUser, Role, Team
from src.models.meets import Category, Meet, MeetParticipant
from src.models.projects import Project, Tags, Features, Task, Comment


class InviteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Invite

    link = factory.LazyFunction(lambda: f"https://example.com/registration/{secrets.token_urlsafe(16)}")
    status = InviteChoices.ACTIVE
    created_at = factory.LazyFunction(timezone.now)
    expires_at = factory.LazyAttribute(lambda o: o.created_at + timedelta(days=7))


class RoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Role

    name = factory.Sequence(lambda n: f"Role {n}")
    color = factory.Iterator(["ff5733", "33ff57", "3357ff", "ff33a8", "33fff5"])


class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team

    name = factory.Sequence(lambda n: f"Team {n}")

    @factory.post_generation
    def participants(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            # Если переданы участники, добавляем их
            for participant in extracted:
                self.participants.add(participant)
        else:
            self.participants.add(
                CustomUserFactory(team=None),
                CustomUserFactory(team=None)
            )


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    # Обязательные поля
    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    password = factory.LazyFunction(lambda: make_password("Password_123"))
    tg_name = factory.Sequence(lambda n: f"tg_name_{n}")
    tg_nickname = factory.Sequence(lambda n: f"tg_nickname_{n}")
    google_meet_nickname = factory.Sequence(lambda n: f"google_meet_{n}")
    gitlab_nickname = factory.Sequence(lambda n: f"gitlab_{n}")
    github_nickname = factory.Sequence(lambda n: f"github_{n}")

    # Необязательные поля
    avatar = factory.django.ImageField(color="blue")
    role = factory.SubFactory(RoleFactory)
    team = factory.SubFactory(TeamFactory)
    is_active = True
    is_admin = False
    is_superuser = False
    is_staff = False
    date_joined = factory.LazyFunction(timezone.now)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")


class MeetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Meet

    title = factory.Sequence(lambda n: f"Meet {n}")
    start_time = factory.LazyFunction(timezone.now)
    category = factory.SubFactory(CategoryFactory)
    author = factory.SubFactory(CustomUserFactory)
    responsible = factory.SubFactory(CustomUserFactory)


class MeetParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MeetParticipant

    meet = factory.SubFactory(MeetFactory)
    custom_user = factory.SubFactory(CustomUserFactory)
    status = "PRESENT"

class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Sequence(lambda n: f"Project {n}")
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    description = factory.Faker("text", max_nb_chars=500)
    responsible = factory.SubFactory(CustomUserFactory)
    status = "DISCUSSION"

class TagsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tags

    name = factory.Sequence(lambda n: f"Tag {n}")
    slug = factory.LazyAttribute(lambda o: slugify(o.name) + "_" + f"{uuid4().hex}")
    color = factory.Faker("hex_color")

class FeaturesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Features

    name = factory.Sequence(lambda n: f"Feature {n}")
    slug = factory.LazyAttribute(lambda o: slugify(o.name) + "_" + f"{uuid4().hex}")
    description = factory.Faker("text", max_nb_chars=10000)
    importance = factory.Faker("random_int", min=0, max=10)
    responsible = factory.SubFactory(CustomUserFactory)
    status = "NEW"
    project = factory.SubFactory(ProjectFactory)

class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    name = factory.Sequence(lambda n: f"Task {n}")
    priority = factory.Faker("random_int", min=1, max=10)
    contributor = factory.SubFactory(CustomUserFactory)
    responsible = factory.SubFactory(CustomUserFactory)
    status = "NEW"
    feature = factory.SubFactory(FeaturesFactory)
    description = factory.Faker("text", max_nb_chars=10000)

class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    user = factory.SubFactory(CustomUserFactory)
    task = factory.SubFactory(TaskFactory)
    comment = factory.Faker("text", max_nb_chars=1000)
