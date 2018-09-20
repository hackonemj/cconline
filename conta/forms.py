from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db.models import Q

from .models import User


class UserCreationForm(forms.ModelForm):
    user_type = forms.ChoiceField(label="Tipo de usuário",
                                  choices=((None, ''), ('Supervisor', 'Supervisor'), ('Condutor', 'Condutor')))
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirmação de Senha', widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'funcionario_id']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('A confirmação não está correta')
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        User.objects.filter(email=email).count()
        if email and User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError(u'Este email já foi registrado.')
        return email

    def save(self, commit=True):
        user_type = self.cleaned_data.get("user_type")
        user = super(UserCreationForm, self).save(commit=False)
        if user_type == 'Supervisor':  # Se o utilizador for supervisor terá as permissões de Supervisor
            user.is_supervisor = True
            user.is_staff = True
        else:  # O utilizador terá as permissões de condutor
            user.is_condutor = True
            user.is_staff = False
            user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'funcionario_id')


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'E-mail/Utilizador/Nº do Funcionário'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Palavra-passe'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user_qs_final = User.objects.filter(
            Q(username__iexact=username) |
            Q(email__iexact=username) | Q(funcionario_id__iexact=username)
        ).distinct()
        if not user_qs_final.exists() and user_qs_final.count != 1:
            raise forms.ValidationError("*Dados inválidos ou utilizador não existe")
        user_obj = user_qs_final.first()
        if not user_obj.check_password(password):
            raise forms.ValidationError("*Dados inválidos ou utilizador não existe")
        self.cleaned_data["user_obj"] = user_obj
        return super(UserLoginForm, self).clean(*args, **kwargs)
