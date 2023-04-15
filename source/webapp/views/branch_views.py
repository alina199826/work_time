from django.http import Http404
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from webapp.models import Branch
from webapp.serializers import BranchSerializer


class BranchList(ListAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

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
            # Добавьте дополнительные поля филиала, если нужно
        }
        return Response(data, status=status.HTTP_200_OK)