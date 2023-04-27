from webapp.models import Branch
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from webapp.serializers import BranchSerializer


class BranchCreateAPIView(CreateAPIView):
    serializer_class = BranchSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        branch = serializer.save(organization=self.request.user.admin_organization.first())
        branch.get_qr_code_svg()


class BranchList(ListAPIView):
    serializer_class = BranchSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Branch.objects.filter(organization__admin__id=self.request.user.id)
        return queryset


class BranchDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = BranchSerializer
    lookup_field = 'pk'

    def get_object(self):
        obj = super().get_object()
        if obj.organization.admin.first().id != self.request.user.id:
            raise PermissionDenied()
        return obj

    def get_queryset(self):
        queryset = Branch.objects.filter(organization__admin__id=self.request.user.id)
        return queryset

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.get_qr_code_svg()

    def perform_destroy(self, instance):
        instance.qr_code = None
        instance.save()
        super().perform_destroy(instance)
