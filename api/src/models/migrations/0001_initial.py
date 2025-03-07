
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=20,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_name",
                                message="Допускаются только буквы латиницы и кириллицы",
                                regex="^[a-zA-Zа-яА-Я\\s]*$",
                            )
                        ],
                        verbose_name="Категория",
                    ),
                ),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
                "db_table": "category",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Role",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Введите название роли до 20 символов(допускаются только буквы кириллицы и латиницы.",
                        max_length=20,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_name",
                                message="Допускаются только буквы латиницы и кириллицы",
                                regex="^[a-zA-Zа-яА-Я\\s]*$",
                            )
                        ],
                        verbose_name="название",
                    ),
                ),
                (
                    "color",
                    models.CharField(
                        help_text="Введите цвет в формате 6 цифр.",
                        max_length=6,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_color",
                                message="Цвет должен быть в формате RRGGBB",
                                regex="^([A-Fa-f0-9]{6})$",
                            )
                        ],
                        verbose_name="цвет",
                    ),
                ),
            ],
            options={
                "verbose_name": "роль",
                "verbose_name_plural": "роли",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Tags",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="Название")),
                ("slug", models.SlugField(unique=True, verbose_name="Ссылка")),
                (
                    "color",
                    models.CharField(
                        help_text="Введите цвет в формате 6 цифр.",
                        max_length=6,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_color",
                                message="Цвет должен быть в формате RRGGBB",
                                regex="^([A-Fa-f0-9]{6})$",
                            )
                        ],
                        verbose_name="цвет",
                    ),
                ),
            ],
            options={
                "verbose_name": "Тег",
                "verbose_name_plural": "Теги",
            },
        ),
        migrations.CreateModel(
            name="VerifyEmail",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("link", models.CharField(max_length=255, verbose_name="Ссылка")),
                (
                    "email",
                    models.EmailField(
                        max_length=50,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_email",
                                message="Неверный формат email",
                                regex="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                            )
                        ],
                        verbose_name="email",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "expires_at",
                    models.DateTimeField(verbose_name="Дата до которой валидна"),
                ),
            ],
            options={
                "verbose_name": "Подтверждение почты",
                "verbose_name_plural": "Подтверждение почты",
                "db_table": "verify_email",
            },
        ),
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=20,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_name",
                                message="Допускаются только буквы латиницы и кириллицы",
                                regex="^[a-zA-Zа-яА-Я\\s]*$",
                            )
                        ],
                        verbose_name="имя",
                    ),
                ),
                (
                    "surname",
                    models.CharField(
                        max_length=20,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_name",
                                message="Допускаются только буквы латиницы и кириллицы",
                                regex="^[a-zA-Zа-яА-Я\\s]*$",
                            )
                        ],
                        verbose_name="фамилия",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=50,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_email",
                                message="Неверный формат email",
                                regex="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                            )
                        ],
                        verbose_name="email",
                    ),
                ),
                (
                    "password",
                    models.CharField(
                        max_length=150,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_password",
                                message="Пароль должен содержать строчные и заглавные буквы и цифры",
                                regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)[a-zA-Z\\d]{8,}$",
                            )
                        ],
                        verbose_name="пароль",
                    ),
                ),
                (
                    "tg_name",
                    models.CharField(
                        max_length=50,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_name",
                                message="Допускаются только буквы, цифры и спец.символы",
                                regex="^[a-zA-Zа-яА-Я0-9._%+-]+$",
                            )
                        ],
                        verbose_name="tg имя",
                    ),
                ),
                (
                    "tg_nickname",
                    models.CharField(
                        max_length=50,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_name",
                                message="Допускаются только буквы, цифры и спец.символы",
                                regex="^[a-zA-Zа-яА-Я0-9._%+-]+$",
                            )
                        ],
                        verbose_name="tg ник",
                    ),
                ),
                (
                    "google_meet_nickname",
                    models.CharField(
                        max_length=50,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_name",
                                message="Допускаются только буквы, цифры и спец.символы",
                                regex="^[a-zA-Zа-яА-Я0-9._%+-]+$",
                            )
                        ],
                        verbose_name="googlemeet ник",
                    ),
                ),
                (
                    "gitlab_nickname",
                    models.CharField(
                        max_length=50,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_name",
                                message="Допускаются только буквы, цифры и спец.символы",
                                regex="^[a-zA-Zа-яА-Я0-9._%+-]+$",
                            )
                        ],
                        verbose_name="gitlab ник",
                    ),
                ),
                (
                    "github_nickname",
                    models.CharField(
                        max_length=50,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_name",
                                message="Допускаются только буквы, цифры и спец.символы",
                                regex="^[a-zA-Zа-яА-Я0-9._%+-]+$",
                            )
                        ],
                        verbose_name="github ник",
                    ),
                ),
                (
                    "avatar",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="images/avatars/",
                        verbose_name="аватар",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        blank=True,
                        default=False,
                        null=True,
                        verbose_name="активный статус",
                    ),
                ),
                (
                    "is_admin",
                    models.BooleanField(
                        blank=True,
                        default=False,
                        null=True,
                        verbose_name="статус администратора",
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False, verbose_name="суперпользователь"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(default=False, verbose_name="персонал"),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="дата регистрации"
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "пользователь",
                "verbose_name_plural": "пользователи",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="CustomUserList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "registration_date",
                    models.DateField(auto_now_add=True, verbose_name="дата создания"),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "пользовательский список",
                "verbose_name_plural": "пользовательские списки",
            },
        ),
        migrations.CreateModel(
            name="Meet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=20,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Допускаются только буквы и пробел",
                                regex="^[а-яА-ЯёЁa-zA-Z]+(?:\\s[а-яА-ЯёЁa-zA-Z]+)*$",
                            )
                        ],
                        verbose_name="Название",
                    ),
                ),
                (
                    "start_time",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="Дата"
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="author_meets",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Автор",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="models.category",
                        verbose_name="Категория",
                    ),
                ),
                (
                    "responsible",
                    models.ForeignKey(
                        default=models.ForeignKey(
                            null=True,
                            on_delete=django.db.models.deletion.CASCADE,
                            related_name="author_meets",
                            to=settings.AUTH_USER_MODEL,
                            verbose_name="Автор",
                        ),
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="responsible_meets",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Ответственный",
                    ),
                ),
            ],
            options={
                "verbose_name": "Мит",
                "verbose_name_plural": "Миты",
                "db_table": "meets",
                "ordering": ["start_time", "category", "title"],
            },
        ),
        migrations.CreateModel(
            name="MeetParticipant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PRESENT", "Присутствует"),
                            ("ABSENT", "Отсутствует"),
                            ("WARNED", "Предупредил"),
                        ],
                        default="PRESENT",
                        max_length=10,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "custom_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="custom_meets",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Участник",
                    ),
                ),
                (
                    "meet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="models.meet",
                        verbose_name="Мит",
                    ),
                ),
            ],
            options={
                "verbose_name": "Участник мита",
                "verbose_name_plural": "Участники мита",
                "db_table": "custom_user_meet",
                "unique_together": {("meet", "custom_user")},
            },
        ),
        migrations.AddField(
            model_name="meet",
            name="participants",
            field=models.ManyToManyField(
                related_name="meets",
                through="models.MeetParticipant",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Участники",
            ),
        ),
        migrations.CreateModel(
            name="Permission",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="Название"
                    ),
                ),
                (
                    "code",
                    models.IntegerField(
                        choices=[
                            (1, "Чтение"),
                            (2, "Комментирование"),
                            (3, "Редактирование"),
                        ],
                        verbose_name="Код доступа",
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Описание"),
                ),
                (
                    "object_id",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="ID объекта"
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="permissions",
                        to="contenttypes.contenttype",
                        verbose_name="Тип объекта",
                    ),
                ),
            ],
            options={
                "verbose_name": "право",
                "verbose_name_plural": "права",
                "ordering": ["-id"],
                "unique_together": {("code", "content_type", "object_id")},
            },
        ),
        migrations.AddField(
            model_name="meet",
            name="permissions",
            field=models.ManyToManyField(
                blank=True,
                related_name="meets",
                to="models.permission",
                verbose_name="Права",
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="permissions",
            field=models.ManyToManyField(
                blank=True,
                related_name="customuser_permissions",
                to="models.permission",
                verbose_name="права",
            ),
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=20,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Допускаются только буквы и пробел",
                                regex="^[а-яА-ЯёЁa-zA-Z]+(?:\\s[а-яА-ЯёЁa-zA-Z]+)*$",
                            )
                        ],
                        verbose_name="Название",
                    ),
                ),
                ("slug", models.SlugField(unique=True, verbose_name="Ссылка")),
                (
                    "logo",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="project_logos",
                        verbose_name="Логотип",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, max_length=500, null=True, verbose_name="Описание"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("В обсуждении", "В обсуждении"),
                            ("В разработке", "В разработке"),
                            ("В поддержке", "В поддержке"),
                        ],
                        default="В обсуждении",
                        max_length=20,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "date_created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "participants",
                    models.ManyToManyField(
                        related_name="project_participants",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Участники",
                    ),
                ),
                (
                    "responsible",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="projects_responsibles",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Ответственный",
                    ),
                ),
            ],
            options={
                "verbose_name": "Проект",
                "verbose_name_plural": "Проекты",
                "ordering": ["-name"],
            },
        ),
        migrations.AddField(
            model_name="customuser",
            name="role",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="models.role",
                verbose_name="роль",
            ),
        ),
        migrations.CreateModel(
            name="Features",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=50,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Допускаются только буквы и пробел",
                                regex="^[а-яА-ЯёЁa-zA-Z]+(?:\\s[а-яА-ЯёЁa-zA-Z]+)*$",
                            )
                        ],
                        verbose_name="Название",
                    ),
                ),
                ("slug", models.SlugField(unique=True, verbose_name="Ссылка")),
                (
                    "description",
                    models.TextField(
                        blank=True, max_length=10000, null=True, verbose_name="Описание"
                    ),
                ),
                (
                    "importance",
                    models.PositiveIntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MaxValueValidator(
                                limit_value=1000000
                            )
                        ],
                        verbose_name="Важность",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Новая", "Новая"),
                            ("Разработка", "Разработка"),
                            ("Тестирование", "Тестирование"),
                            ("Готов", "Готов"),
                        ],
                        default="Новая",
                        max_length=20,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "date_created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "participants",
                    models.ManyToManyField(
                        related_name="features_participants",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Исполнители",
                    ),
                ),
                (
                    "responsible",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="features_responsibles",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Ответственный",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="features_projects",
                        to="models.project",
                        verbose_name="Проект",
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        related_name="features_tags",
                        to="models.tags",
                        verbose_name="Теги",
                    ),
                ),
            ],
            options={
                "verbose_name": "Фича",
                "verbose_name_plural": "Фичи",
            },
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=50,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Допускаются только буквы и пробел",
                                regex="^[а-яА-ЯёЁa-zA-Z]+(?:\\s[а-яА-ЯёЁa-zA-Z]+)*$",
                            )
                        ],
                        verbose_name="название",
                    ),
                ),
                ("priority", models.IntegerField(verbose_name="приоритет")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Новая", "Новая"),
                            ("Разработка", "Разработка"),
                            ("Тестирование", "Тестирование"),
                            ("Готов", "Готов"),
                        ],
                        default="Новая",
                        max_length=20,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="дата создания"
                    ),
                ),
                (
                    "closed_at",
                    models.DateTimeField(null=True, verbose_name="дата закрытия"),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, max_length=10000, verbose_name="описание"
                    ),
                ),
                (
                    "contributor",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="tasks_contributors",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="автор",
                    ),
                ),
                (
                    "feature",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tasks_features",
                        to="models.features",
                        verbose_name="фича",
                    ),
                ),
                (
                    "responsible",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="tasks_responsibles",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="ответственный",
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        related_name="tasks_tags", to="models.tags", verbose_name="теги"
                    ),
                ),
            ],
            options={
                "verbose_name": "Задача",
                "verbose_name_plural": "Задачи",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "comment",
                    models.TextField(
                        blank=True, max_length=1000, verbose_name="Комментарий"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="дата создания"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comment_user",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="автор",
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comment_task",
                        to="models.task",
                        verbose_name="задача",
                    ),
                ),
            ],
            options={
                "verbose_name": "Коментиарий",
                "verbose_name_plural": "Коментиарии",
            },
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=20,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Допускаются только буквы и пробел",
                                regex="^[а-яА-ЯёЁa-zA-Z]+(?:\\s[а-яА-ЯёЁa-zA-Z]+)*$",
                            )
                        ],
                        verbose_name="Команда",
                    ),
                ),
                (
                    "participants",
                    models.ManyToManyField(
                        related_name="team_participants",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Участники",
                    ),
                ),
            ],
            options={
                "verbose_name": "команда",
                "verbose_name_plural": "команды",
                "ordering": ["name"],
            },
        ),
        migrations.AddField(
            model_name="customuser",
            name="team",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="models.team",
                verbose_name="команда",
            ),
        ),
    ]
