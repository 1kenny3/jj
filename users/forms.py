from django.forms import Form, CharField, ModelForm, ValidationError, fields
from django.contrib.auth.models import User


class LoginForm(Form):
    username = CharField(required=True)
    password = CharField(required=True)


class RegisterForm(ModelForm):
    repeated_password = CharField(required=True)

    class Meta:
        model = User
        fields = ["username", "password", "repeated_password"]

    def clean_repeated_password(self):
        if self.cleaned_data["password"] != self.cleaned_data["repeated_password"]:
            raise ValidationError(message="repeated password")
        return self.cleaned_data["repeated_password"]

