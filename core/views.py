from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import api_view
from .models import Question , Tag , Company , Post , Comment
from .serializers import QuestionSerilizer , TagSerilizer , PostSerializer , UserSerializer
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth.hashers import make_password

@api_view(["GET"])
def get_questions(request):

    offset = int(request.GET.get("offset" , 0))
    limit = int(request.GET.get("limit" , 50))

    questions = Question.objects.all()[offset : limit + offset]
    serial = QuestionSerilizer(questions , many=True)

    return Response(serial.data)

@api_view(["GET" , "POST"])
def get_posts(request):
    if request.method == "GET":

        limit = int(request.GET.get("limit" , 50))
        offset = int(request.GET.get("offset" , 0))


        data = Post.objects.all()[offset : offset + limit]
        serial = PostSerializer(data , many=True , context={"request": request})

        return Response(serial.data , status=status.HTTP_200_OK)
    else:
        serial = PostSerializer(data=request.data)
        if serial.is_valid():
            serial.save()
            return Response({"Message" : "Posted Successfully"} , status=status.HTTP_201_CREATED)
        return Response({"Message" : "Data Not Valid"} , status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def register(request):
    serial = UserSerializer(data=request.data)
    if serial.is_valid():
        serial.save()
        return Response({"message": "User Created Successfully"} , status=status.HTTP_201_CREATED)
    return Response({"message": "Data Not Valid"} , status=status.HTTP_400_BAD_REQUEST)