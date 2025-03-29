from rest_framework import serializers
from core.models import Question , Tag , Company , Post , Comment
from django.contrib.auth.models import User


class QuestionSerilizer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'


class TagSerilizer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'

class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    has_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id" , "title" , "content" , "author" , "has_liked"]

    def get_has_liked(self , obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return obj.upvoters.filter(id=user.id).exists()
        return False


class DetailPostSerializer(serializers.ModelSerializer):
    comments = CommentSerializers(many=True)

    class Meta:
        model = Post
        fields = ["id" , "title" , "content" , "created_at" , "author" , "comments"]


class DetailQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id" , "title" ,"difficulty" , "url"]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Ensures password isn't returned in response

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']  # Include 'password' in fields

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),  # Email is optional in Django's default User model
            password=validated_data['password']  # Automatically hashes password
        )
        return user