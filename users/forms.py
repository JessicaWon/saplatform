from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import *
 # extend Django's built-in UserCreationForm and UserChangeForm to
 # remove the username field (and optionally add any others that are
 # required)

class SkyUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(SkyUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = SkyUser
        fields = '__all__'

class SkyUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(SkyUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = SkyUser
        fields = '__all__'
