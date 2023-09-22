from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils import timezone
from django.utils.timesince import timesince

class CustomUserManager(UserManager):
    def _create_user(self, firstname, lastname, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, firstname=firstname,lastname=lastname, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_user(self, firstname=None, lastname=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(firstname, lastname, email, password, **extra_fields)
    
    def create_superuser(self, firstname=None, lastname=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(firstname, lastname, email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=255, blank=True, null=True, default='')
    lastname = models.CharField(max_length=255, blank=True, null=True, default='')
    birthday = models.DateField(null=True, blank=True)
    tel = models.CharField(max_length=50, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    
    friends = models.ManyToManyField('self')
    friends_count = models.IntegerField(default=0)
    
    posts_count = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        else:
            return '/media/profile.png'


class FriendshipRequest(models.Model):
    SENT = 'sent'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    STATUS_CHOICES = (
        (SENT, 'Sent'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    )

    created_for = models.ForeignKey(User, related_name='received_friendshiprequests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_friendshiprequests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=SENT)
    
    def created_at_formatted(self):
       return timesince(self.created_at)


