from django.db import models


class MeetStatusChoice(models.TextChoices):
    PRESENT = "present", "Присутствует"
    ABSENT = "absent", "Отсутствует"
    WARNED = "warned", "Предупредил"

    @classmethod
    def get_color(cls, status):
        if status == cls.PRESENT:
            return "green"
        elif status == cls.ABSENT:
            return "red"
        elif status == cls.WARNED:
            return "yellow"
        return "grey"


class ProjectChoices(models.TextChoices):
    DISCUSSION = "В обсуждении", "В обсуждении"
    DEVELOPMENT = "В разработке", "В разработке"
    SUPPORT = "В поддержке", "В поддержке"


class FeatureChoices(models.TextChoices):
    NEW = "Новая", "Новая"
    DEVELOPMENT = "Разработка", "Разработка"
    TESTING = "Тестирование", "Тестирование"
    SUCCESS = "Готов", "Готов"


class TaskChoices(models.TextChoices):
    NEW = "Новая", "Новая"
    DEVELOPMENT = "Разработка", "Разработка"
    TESTING = "Тестирование", "Тестирование"
    SUCCESS = "Готов", "Готов"
    BACKLOG = "Бэклог", "Бэклог"
