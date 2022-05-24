from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_blank=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            company_id=validated_data['company_id'],
            company_name=validated_data['company_name'],
        )
        user.set_password(validated_data['password'])  # 암호화 저장
        user.save()
        return user

    class Meta:
        model = User
        fields = ['pk', 'username', 'password', 'email', 'phone_number', 'company_id', 'company_name']

