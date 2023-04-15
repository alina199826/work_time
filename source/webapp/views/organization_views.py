from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response
from webapp.models import Organization
from webapp.serializers import OrganizationSerializer
from rest_framework.pagination import PageNumberPagination

class OrganizationList(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("Only administrators can create new organizations.")
        serializer.save()


class OrganizationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_destroy(self, instance):
        if not self.request.user.is_staff:
            raise PermissionDenied("Only administrators can delete organizations.")
        instance.delete()

    def put(self, request, *args, **kwargs):
        organization = self.get_object()
        serializer = self.serializer_class(organization, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

