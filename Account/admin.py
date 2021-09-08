from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from Account.models import Account


class UserCreationForm(forms.ModelForm):
    # password1 : first password input
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    # password2 : second password input
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        # form of the model.
        model = Account
        # fields of the model whihc are needed to be seen when creating an instance of the model.
        fields = ['userid', 'useremail', 'name']

    def clean_password2(self):
        # Checking that the two passwords which are entered do match and are entered.
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Credential Error')
        return password2

    def save(self, commit=True):
        # commit = False gives us the model object but it does not save the instance.
        user = super().save(commit=False)
        # setting the password of the user instance given by the save(commit=False) method.
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    # password can not be changed so that to only see the password's hash value not the original
    # ReadOnlyPasswordHashField() is used.
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = ('userid', 'useremail', 'name', 'is_active', 'is_staff', 'is_admin')

    def clean_password(self):
        return self.initial['password']


class UserAdmin(BaseUserAdmin):
    # form : used update an instance
    form = UserChangeForm
    # add_form : used to create an instance
    add_form = UserCreationForm

    # In all the list of the model instances list_display fields are the columns which will be displayed.
    list_display = ('userid', 'useremail', )
    # this is the filtering showed to the left side of all accounts by which we can filter the instances.
    list_filter = ('is_admin', 'is_staff', )
    # Fieldsets is used to show all the fields which needs to be changed to change the data of an instance.
    # Fields means show all the fields in the admin panel to change the values of the fields.
    # Permissions : Used to show all the permissions you want to change.
    fieldsets = (
        (None, {'fields': ('userid', 'useremail', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    # add_fieldsets is an attribute which is used to show all the fields in the admin panel while adding a new instance.
    # fields : all the fields which need to be added while creating a new instance.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('userid', 'useremail', 'name', 'password1', 'password2'),
        }),
    )
    search_fields = ('userid', )
    # ordering : Arrange all the instances in the admin panel in the order.
    ordering = ('userid', )
    filter_horizontal = ()


admin.site.register(Account, UserAdmin)
admin.site.unregister(Group)
