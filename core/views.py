from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import api_view
from .models import Question , Tag , Company , Post , Comment
from .serializers import CreatePostSerializer , QuestionSerializer , DetailQuestionSerializer , TagSerializer , PostSerializer , UserSerializer , DetailPostSerializer , CommentSerializers , CompanySerializer
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count

@api_view(["GET"])
def get_questions(request):

    offset = int(request.GET.get("offset" , 0))
    limit = int(request.GET.get("limit" , 50))

    questions = Question.objects.all()[offset : limit + offset]
    serial = QuestionSerializer(questions , many=True)

    return Response(serial.data)


@api_view(["GET"])
def get_question(request , pk):
    data = get_object_or_404(Question , pk=pk)
    serial = DetailQuestionSerializer(data)
    return Response(serial.data , status=status.HTTP_200_OK)

@api_view(["GET" , "POST"])
def get_posts(request):
    if request.method == "GET":

        limit = int(request.GET.get("limit" , 50))
        offset = int(request.GET.get("offset" , 0))


        # data = Post.objects.order_by().prefetch_related()[offset : offset + limit]
        data = (
    Post.objects.annotate(upvotes_count=Count("upvoters"))
    .select_related("author")  # Optimizes ForeignKey lookup
    .prefetch_related("upvoters")  # Optimizes ManyToMany lookup
    .order_by("-upvotes_count", "-created_at")  # Orders by upvotes first, then date
)[offset : offset + limit]
        serial = PostSerializer(data , many=True , context={"request": request})

        return Response(serial.data , status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def new_post(request):
    serial = CreatePostSerializer(data=request.data)
    if serial.is_valid():
        serial.save(author=request.user)  # Pass author explicitly when saving
        return Response({"Message": "Posted Successfully"}, status=status.HTTP_201_CREATED)
    return Response({"Message": "Data Not Valid"}, status=status.HTTP_400_BAD_REQUEST)




@api_view(["POST"])
def register(request):
    serial = UserSerializer(data=request.data)
    if serial.is_valid():
        user = serial.save() # Save the user and get the user instance.
        refresh = RefreshToken.for_user(user) # Generate refresh and access tokens
        return Response({
            "message": "User Created Successfully",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serial.error_messages, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
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

@api_view(["GET"])
def get_companies(request):
    data = Company.objects.all()
    serial = CompanySerializer(data, many=True)
    return Response(serial.data , status=status.HTTP_200_OK)

@api_view(["GET"])
def get_tags(request):
    data = Tag.objects.all()
    serial = TagSerializer(data, many=True)
    return Response(serial.data , status=status.HTTP_200_OK)



