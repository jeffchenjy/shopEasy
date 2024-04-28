from django.contrib.auth import validators
from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.utils import timezone
import uuid as uuid_lib

class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False
    )

    username_validators = UnicodeUsernameValidator()

    username = models.CharField(
        "ユーザ名",
        max_length=150,
        unique=True,
        help_text="※150文字以下の文字や数字、一部の記号で入力したください。",
        validators = [username_validators],
        error_messages={
            "unique": "このユーザー名は既に使用されています。",
        },
    )

    channel_name = models.CharField("チャンネル名", max_length=150, blank=True)
    email = models.EmailField("Eメールアドレス", blank=True)

    is_staff = models.BooleanField(
        "ユーザステータス",
        help_text="ユーザーがこの管理サイトにログインできるかどうかを指定します。",
        default=False,
    )

    is_member = models.BooleanField(
        "会員ステータス", 
        help_text="このユーザが契約しているかを区別します。",
        default=False,
    )

    is_active = models.BooleanField(
        "アクティブユーザ",
        help_text="このユーザーをアクティブとして扱うかどうかを指定します。アカウントを削除する代わりに、これを選択解除してください。",
        default=True,
    )

    date_joined = models.DateTimeField("登録日", default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    groups = models.ManyToManyField(Group, verbose_name='groups', blank=True, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_permissions',
    )

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
