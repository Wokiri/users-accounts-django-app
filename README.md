# Customizing Django's Auth User



This a working pluggable user app for django projects.

Django comes with its authentication system in an initial default configuration. This default offers a generally impressive authentication and authorization functionalities.

In certain situations however, it becomes necessary to perfom a few customizations on the User object-- depending on the specific needs of the project.




<br>
<br>

Django's default User object inherits from AbstractUser object of which class and associated attributes and methods are shown below: 


```python

class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

```



<br>
<br>
<br>
<br>


## Case 1: Extending the attributes of django's default User
### Code available in Branch: `Case1_ExtendingDefaultUser`


As you can see, the primary attributes of the default User (AbstractUser) are:
- username
- password
- email
- first_name
- last_name

Of these, the **`username`** and **`password`** are mndatory fields and must be filled during creation.

Now, also available at default configurations is the room to extend the existing User model. According to the official (v3.2) documentation,

>you can create a proxy model based on User. This allows for any of the features offered by proxy models including default ordering, custom managers, or custom model methods.


If say we were building a Library Management System with the option of interacting differently with different system users-- e.g. if we wanted our system to know whether the user is an administrator, a librarian or a student we would simply create a proxy model based on the default User.


```python

from django.contrib.auth.models import User

class LibraryUser(models.Model):

    class Sections(models.TextChoices):
        ADVENTURE = 'ADV', _('Adventure')
        REALITY = 'REAL', _('Real')
        EDUCATION = 'EDU', _('Education')


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_section = models.CharField(max_length=5, choices=Sections.choices)
    is_administrator = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)

```

Users created in this manner will have both User and LibraryUser models. The two are related and information from one model can be accessed like:

```python

>>> u = User.objects.get(username='some_user1')
>>> some_user1_favorite_section = u.libraryuser.favorite_section

```

The LibraryUser, having a one-to-one relation with the User model, is called a profile model because it might store non-auth related information about a site user, e.g `favorite_section`, `is_administrator`, `is_librarian`, `is_student`.



<br>
<br>
<br>
<br>

## Case 2: