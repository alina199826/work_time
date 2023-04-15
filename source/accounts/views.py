from django.http import Http404
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework import status, generics
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from .models import User
from .serializers import UserSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        search_query = request.query_params.get('search')
        if search_query:
            queryset = self.queryset.filter(
                Q(name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(login__icontains=search_query)
            )
        else:
            queryset = self.queryset.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)





class UserDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_mail(
                'Подтвердите свой адрес электронной почты',
                f'Перейдите по ссылке для подтверждения регистрации: '
                f'{settings.FRONTEND_URL}/verify-email?token={user.email_verification_token}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    def get(self, request, token):
        try:
            user = User.objects.get(email_verification_token=token)
            user.email_verified = True
            user.save()
            return Response({'message': 'Email успешно подтвержден'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'Неверный токен'}, status=status.HTTP_400_BAD_REQUEST)
