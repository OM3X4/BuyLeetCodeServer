from rest_framework import serializers
from core.models import Question , Tag , Company , Post , Comment


class QuestionSerilizer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'


class TagSerilizer(serializers.ModelSerializer):

    class Meta:
        model = Tag
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
