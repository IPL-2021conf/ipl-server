from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Create your models here.

# helper Class for create User
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('Email is empty')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, **extra_fields)
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('super-user must have is_staff=true')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('super-user must have is_superuser=true')
        
        return self._create_user(email, username, password, **extra_fields)

# custom user
class User(AbstractBaseUser, PermissionsMixin):

    objects = UserManager()
    # ID 겸 Eamil !!필수!!
    email = models.EmailField(  
        verbose_name=('Email ID'),
        max_length=50,
        unique=True,
        help_text='Email ID.',
    )
    # 이름
    username = models.CharField(
        verbose_name=('UserName(nickname)'),
        max_length=30,
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('activate'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(
        _('date_joined'),
        default=timezone.now,
    )
    
    # 로그인 시 username을 email로 설정
    EMAIL_FIELD = 'email'
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS = ['username',]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return self.username
    def get_short_name(self):
        return self.email


# ============================================================

class RefreshDBModel(models.Model):
    email = models.EmailField(max_length=50, null=False)
    refresh = models.TextField(null=True, blank=True)