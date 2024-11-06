from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import redirect
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone

from src.models.choice_classes import (
    FeaturesChoices,
    ProjectChoices,
    TaskChoices,
)

from src.domain.validators.validators import ModelValidator

User = get_user_model()


class Project(models.Model):
    """Модель проекты"""

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ["-name"]

    name = models.CharField(
        max_length=20,
        verbose_name="Название",
        unique=True,
        validators=[ModelValidator.validate_letters_space_only()]
    )

    slug = models.SlugField(unique=True, verbose_name="Ссылка")
    logo = models.ImageField(
        upload_to="project_logos",
        verbose_name="Логотип",
        blank=True,
        null=True,
    )
    description = models.TextField(
        max_length=500, verbose_name="Описание", blank=True, null=True
    )
    participants = models.ManyToManyField(
        to=User,
        related_name="project_participants",
        verbose_name="Участники",
    )
    responsible = models.ForeignKey(
        to=User,
        related_name="projects_responsibles",
        on_delete=models.CASCADE,
        verbose_name="Ответственный",
    )
    status = models.CharField(
        max_length=20,
        choices=ProjectChoices,
        default=ProjectChoices.DISCUSSION,
        verbose_name="Статус",
    )

    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Генерируем `slug` только если его нет
        if not self.slug:
            base_slug = slugify(self.name)
            unique_slug = base_slug
            counter = 1

            while Project.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}_{counter}"
                counter += 1

            self.slug = unique_slug

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            viewname="projects:update_project", kwargs={"slug": self.slug}
        )


class Tags(models.Model):
    """Модель тегов"""

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    name = models.CharField(max_length=50, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="Ссылка")
    color = models.IntegerField(
        verbose_name="Цвет",
        help_text="Введите цвет в формате 6 цифр.",
        validators=[ModelValidator.validate_color()],
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) + "_" + f"{uuid4().hex}"
        return super().save()

    def get_absolute_url(self):
        return redirect(
            reverse(viewname="projects:update_tag", kwargs={"slug": self.slug})
        )


class Features(models.Model):
    """Модель фичи"""

    class Meta:
        verbose_name = "Фича"
        verbose_name_plural = "Фичи"

    name = models.CharField(
        max_length=50,
        verbose_name="Название",
        unique=True,
        validators=[ModelValidator.validate_letters_space_only()]
    )
    slug = models.SlugField(unique=True, verbose_name="Ссылка")
    description = models.TextField(
        max_length=10000, verbose_name="Описание", null=True, blank=True
    )
    importance = models.PositiveIntegerField(
        default=0,
        verbose_name="Важность",
        validators=[ModelValidator.validate_max_value()]
    )
    tags = models.ManyToManyField(
        to=Tags,
        related_name="features_tags",
        verbose_name="Теги",
    )
    participants = models.ManyToManyField(
        to=User,
        related_name="features_participants",
        verbose_name="Исполнители",
    )
    responsible = models.ForeignKey(
        to=User,
        related_name="features_responsibles",
        on_delete=models.CASCADE,
        verbose_name="Ответственный",
    )
    status = models.CharField(
        max_length=20,
        choices=FeaturesChoices,
        default=FeaturesChoices.NEW,
        verbose_name="Статус",
    )

    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        editable=False
    )

    project = models.ForeignKey(
        to=Project,
        related_name="features_projects",
        on_delete=models.CASCADE,
        verbose_name="Проект",
        default=None,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) + "_" + f"{uuid4().hex}"
        return super().save()

    def get_absolute_url(self):
        return redirect(
            reverse(
                viewname="projects:detail_features", kwargs={"slug": self.slug}
            )
        )

