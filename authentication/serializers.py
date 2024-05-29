from rest_framework import serializers
from .models import User, Dissertation, Comment, Supervision,Course,Department
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'email', 'RegNo', 'password', 'role', 'firstname', 'middlename', 'surname']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            firstname=validated_data['firstname'],
            middlename=validated_data['middlename'],
            surname=validated_data.get('surname'),
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class DissertationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dissertation
        fields = [ 'title', 'student', 'file', 'status']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['student'] = {
            'firstname': instance.student.firstname,
            'surname': instance.student.surname,
            'regno': instance.student.RegNo,
            'course':instance.student.course
        }
        return data

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'dissertation', 'supervisor', 'created_at', 'updated_at']

    

class SupervisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supervision
        fields = ['id', 'student', 'supervisor', 'created_at']



class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid login credentials.")
        else:
            raise serializers.ValidationError("Both 'email' and 'password' are required.")
        data['user'] = user
        return data
    
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [ 'name']

class CourseSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = Course
        fields = [ 'name', 'department', 'year']

class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'department', 'year']
