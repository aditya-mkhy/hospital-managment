from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyUserManager(BaseUserManager):
    def create_user(self, email, username,  first_name, last_name, password):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username,  first_name, last_name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            password=password,

        )
        user.is_admin = True
        user.is_verified=True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email Address',
        max_length=255,
        unique=True,
    )

    username = models.CharField(max_length = 50, verbose_name = "username", unique=True)

    first_name = models.CharField(max_length = 20, verbose_name = "First Name", blank=False)
    last_name  = models.CharField(max_length = 20, verbose_name = "Last Name", blank=False)


    is_admin = models.BooleanField(default=False, verbose_name="Is Admin")
    is_doctor = models.BooleanField(default=False, verbose_name="Is Doctor")
    auth_token = models.CharField(max_length=200,blank=True)
    auth_token_time = models.CharField(max_length=50 ,default="None")
    propath = models.CharField(max_length = 100, verbose_name = "Profile", null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name",'last_name', 'username']


    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



class Address(models.Model):
    line1 = models.CharField(verbose_name="Line1", max_length=200)
    city = models.CharField(verbose_name="City", max_length=50)
    state = models.CharField(verbose_name="State", max_length=40)
    pin_code = models.CharField(verbose_name="Pin code", max_length=8)

    user = models.ForeignKey(MyUser, verbose_name="User", on_delete=models.SET_NULL, null=True)


    def __str__(self) -> str:
        return f"{self.user}-{self.city}"

class Catgory(models.Model):
    blog_catgory = models.CharField(verbose_name="Catogray", max_length=30)

    def __str__(self) -> str:
        return self.blog_catgory


class Blog(models.Model):
    user = models.ForeignKey(MyUser, verbose_name="User", on_delete=models.SET_NULL, null=True)
    catgory = models.ForeignKey(Catgory, verbose_name="Catgory", on_delete=models.SET_NULL, null=True)
    title = models.CharField(verbose_name="Tile", max_length=200)
    summary = models.CharField(verbose_name="Summary", max_length=500)
    content = models.TextField(verbose_name="Content")
    updated = models.DateTimeField(verbose_name="Time")
    file = models.CharField(verbose_name="Image", max_length=100, null=True)
    is_draft = models.BooleanField(verbose_name="Is_Draft",  default=False)

    def __str__(self) -> str:
        return f"{self.title}-{self.user}"

    @property
    def get_summary(self):
        summary = str(self.summary).split(" ")
        short = []
        count = 0

        for word in summary:
            if len(word) > 0:
                short.append(word)
                count += 1

                if count >= 15:
                    short.append("......")
                    break

        return " ".join(short)




