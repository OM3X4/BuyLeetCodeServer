from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import api_view
from .models import Question , Tag , Company , Post , Comment
from .serializers import QuestionSerilizer , TagSerilizer , PostSerializer , UserSerializer , DetailPostSerializer , CommentSerializers
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404

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
        serial = PostSerializer(data=request.data , author=request.user)
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


@api_view(["POST"])
def upVote(request , pk):
    post = get_object_or_404(Post , pk=pk)
    if request.user in post.upvoters.all():
        post.upvoters.remove(request.user)
        return Response({"Message": "Deleted Up Vote"} , status=status.HTTP_202_ACCEPTED)

    post.upvoters.add(request.user)

    return Response({"Message" : "Upvoted Successfully"} , status=status.HTTP_202_ACCEPTED)

@api_view(["GET" , "POST"])
def comments(request , pk):
    post = get_object_or_404(Post.objects.prefetch_related("comments"), pk=pk)

    if request.method == "GET":
        serial = DetailPostSerializer(post , context={"request": request})
        return Response(serial.data)

    else:
        data = request.data.copy()  # Create a mutable copy of request data
        data["author"] = request.user.id  # Assign current user as author
        data["post"] = post.id  # Assign post ID


        serial = CommentSerializers(data=data)
        if serial.is_valid():
            serial.save(author=request.user , post=post)
            return Response({"Message" : "Done"} , status=status.HTTP_201_CREATED)
        return Response({"Message": "In Valid Data" , "errors": serial.error_messages} , status=status.HTTP_400_BAD_REQUEST)


