from rest_framework import serializers
from core.models import Question , Tag , Company , Post , Comment
from django.contrib.auth.models import User


class DetailQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'

class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    upvoted = serializers.SerializerMethodField()
    upvotes = serializers.SerializerMethodField()
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = ["id" , "upvotes" , "title" , "content" , "author" , "author_name" , "upvoted" , "created_at"]

    def get_upvoted(self , obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return obj.upvoters.filter(id=user.id).exists()
        return False

    def get_upvotes(self , obj):
        return obj.upvoters.count()

class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title" , "content"]


class DetailPostSerializer(serializers.ModelSerializer):
    comments = CommentSerializers(many=True)

    class Meta:
        model = Post
        fields = ["id" , "title" , "content" , "created_at" , "author" , "comments"]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id" , "title" ,"difficulty" , "url"]


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields ="__all__"

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