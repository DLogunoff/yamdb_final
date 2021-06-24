from rest_framework import serializers

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'role',
                  'bio', 'first_name', 'last_name']
        lookup_field = 'username'


class EmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100)
    confirmation_code = serializers.CharField(
        max_length=100,
        allow_null=True,
        allow_blank=True
    )

    class Meta:
        model = User
        fields = ['email', 'confirmation_code']

    def create(self, validated_data):
        validated_data['username'] = validated_data['email']
        user = User.objects.create(**validated_data)
        user.save()
        return user
