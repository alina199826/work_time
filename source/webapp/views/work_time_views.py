from django.db.models import Sum
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from webapp.models import WorkTime
from webapp.serializers import WorkTimeSerializer
from accounts.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta


class UserWorkTimeByMonth(APIView):
    def get(self, request, user_id, year, month):
        try:
            user = User.objects.get(id=user_id)
            start_date = datetime(int(year), int(month), 1)
            end_date = start_date.replace(day=1) + timedelta(days=32)
            work_times = WorkTime.objects.filter(
                user=user,
                start_time__gte=start_date,
                start_time__lt=end_date,
            ).annotate(
                duration=Sum('end_time', 'start_time')
            )
            total_hours = round(work_times.aggregate(Sum('duration'))['duration__sum'].total_seconds() / 3600, 2)
            serializer = WorkTimeSerializer(work_times, many=True)
            data = serializer.data
            data.append({'total_hours': total_hours})
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)})


class WorkTimeList(generics.ListCreateAPIView):
    queryset = WorkTime.objects.all()
    serializer_class = WorkTimeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination


class WorkTimeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkTime.objects.all()
    serializer_class = WorkTimeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

