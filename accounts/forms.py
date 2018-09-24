from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, forms



class RegistrationForm(UserCreationForm):
    user_type=forms.ModelChoiceField(queryset=Group.objects.all())
    class Meta:
        model = User
        fields = ('first_name','last_name',"username", "email", "password1", "password2")
