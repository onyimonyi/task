from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import (RegisterSerializer, UserLoginSerializer, TaskSerializer)
from .models import (Task)
#GGgg
# Create your views here.

@api_view(['POST'])
def registeration_view(request, *args, **kwargs):
    serializer = RegisterSerializer(data=request.data, context={'request': request})
    data = {}
    if serializer.is_valid():
        account = serializer.save()
        data['message'] = "Account created successfully"
        data['email'] = account.email
        refresh = RefreshToken.for_user(account)
        data['token'] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token), }
        # send_otp_via_email(account.email)
        return Response(data, status=201)
    data = serializer.errors
    return Response(data, status=400)


class UserLoginAPIView(GenericAPIView):
    """
    An endpoint to authenticate existing users using their email and password.
    """

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serializer = UserLoginSerializer(user)
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Task_create_view(request, *args, **kwargs):
    serializer = TaskSerializer(data=request.data, context={'request': request})
    data = {}
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        data['message'] = "Task created successfully"
        return Response(data, status=201)
    data = serializer.errors
    return Response(data, status=400)




class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class AllTaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    partial = True


class TaskDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        data['message'] = "Task deleted successfully"
        return Response(data, status=404)