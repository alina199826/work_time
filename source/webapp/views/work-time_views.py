from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from webapp.models import WorkTime
from webapp.serializers import WorkTimeSerializer


class WorkTimeList(generics.ListCreateAPIView):
    queryset = WorkTime.objects.all()
    serializer_class = WorkTimeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WorkTimeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkTime.objects.all()
    serializer_class = WorkTimeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)