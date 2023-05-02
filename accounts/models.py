from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class MyAccountManager(BaseUserManager):
    """
    Account manager.
    """
    def create_user(self, email, username, password):
        """
        Method for creating a user.
        :param email: The email address of the user.
        :param username: The username for the user.
        :param password: The users password.
        :return: The user who gets created.
        """
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a username.")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates a superuser.
        :param email: The email address of the user.
        :param username: The username for the user.
        :param password: The users password.
        :return: The superuser who gets created.
        """
        print('Creating super user')
        print(email)
        print(username)
        print(password)
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


def get_profile_image_filepath(self, filename):
    """
    Method for retrieving the profile image of the user.
    :param self:
    :param filename: The file name of the profile image.
    :return: The profile image.
    """
    return 'profile_images/' + str(self.pk) + '/"profile_image.png'


def get_default_profile_image():
    """
    Gets the default image for a profile.
    :return: The default profile image.
    """
    return 'img/default_user_img.png'


class Account(AbstractBaseUser):
    """
    Model for the account.
    """
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(max_length=255, upload_to=get_default_profile_image,
                                      null=True, default=get_default_profile_image)
    hide_email = models.BooleanField(default=True)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        """
        Creates a new account.
        :return: The new users name.
        """
        return self.username

    def get_profile_image_filename(self):
        """
        Gets the file name of the users profile image.
        :return: The file name of the users profile image.
        """
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]

    def has_perm(self, perm, obj=None):
        """
        Indicates if the user is an admin user.
        :param perm:
        :param obj:
        :return: A boolean indicating if the user is an admin.
        """
        return self.is_admin

    def has_module_perms(self, app_label):
        """
        Indicates if the user has module permissions.
        :param app_label:
        :return: A boolean indicating if the user has module permissions.
        """
        return True

