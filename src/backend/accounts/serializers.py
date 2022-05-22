from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    email = serializers.EmailField(allow_blank=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            email=validated_data['email'],
            gender=validated_data['gender'],
            website_url=validated_data['website_url'],
            phone_number=validated_data['phone_number'],
            company_id=validated_data['company_id'],
            company_name=validated_data['company_name'],
        )
        user.set_password(validated_data['password'])  # 암호화 저장
        user.save()
        return user

    class Meta:
        model = User
        fields = ['pk', 'username', 'password', 'first_name', 'email', 'gender', 'website_url', 'phone_number', 'company_id', 'company_name']

