import factory
import secrets
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta

from src.models.invites import Invite
from src.models.choice_classes import InviteChoices
from src.models.models import CustomUser, Role, Team
from src.models.meets import Category, Meet, MeetParticipant


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
