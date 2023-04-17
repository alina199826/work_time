from django.http import Http404
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from webapp.models import Branch
from webapp.serializers import BranchSerializer
from rest_framework.pagination import PageNumberPagination

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser

class BranchCreateAPIView(CreateAPIView):
    serializer_class = BranchSerializer
    permission_classes = [IsAdminUser]

    def has_permission(self, request, view):
        return request.user.is_staff

class BranchList(ListAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class BranchDetail(APIView):

    def get_object(self, pk):
        try:
            return Branch.objects.get(pk=pk)
        except Branch.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        branch = self.get_object(pk)
        qr_code_svg = branch.get_qr_code_svg()
        data = {
            'id': branch.id,
            'name': branch.name,
            'qr_code_svg': qr_code_svg,
        }
        return Response(data, status=status.HTTP_200_OK)