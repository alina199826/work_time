from webapp.models import Branch
from webapp.serializers import BranchSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied


class BranchCreateAPIView(CreateAPIView):
    serializer_class = BranchSerializer
    permission_classes = [IsAdminUser]


class BranchList(ListAPIView):
    serializer_class = BranchSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Branch.objects.filter(organization__id=self.request.user.organization.id)
        return queryset


class BranchDetail(RetrieveAPIView):
    serializer_class = BranchSerializer
    lookup_field = 'pk'

    def get_object(self):
        obj = super().get_object()
        if obj.organization.id != self.request.user.organization.id:
            raise PermissionDenied()
        return obj

    def get_queryset(self):
        queryset = Branch.objects.filter(organization__id=self.request.user.organization.id)
        return queryset
