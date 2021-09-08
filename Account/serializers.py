from rest_framework import serializers

from Account.models import Account

""" (((^^^NOTE^^^))) :- To update only one or lesser than total no of fields you have to enter ^^^partial=True^^^ in 
    instantiating serializer of a model instance who already exists. """


class SmallDataAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['userid', 'name']


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['userid', 'useremail', 'name']


class RegistrationSerializer(serializers.ModelSerializer):
    # Another password attribute for two time password verification.
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        # Model to be serialized
        model = Account
        # fields of the serializer.
        fields = ['userid', 'useremail', 'name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        # Getting an instance of the model with validated data.
        account = Account(
            userid=self.validated_data['userid'],
            useremail=self.validated_data['useremail'],
            name=self.validated_data['name']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        # Checking whether the two passwords match.
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        # Setting the password if two passwords match
        account.set_password(password)
        # Saving the instance to the database, and return it.
        account.save()
        return account
