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
            end_date = start_date.replace(day=28) + timedelta(days=4)
            end_date = end_date - timedelta(days=end_date.day)
            work_times = WorkTime.objects.filter(user=user, start_time__range=[start_date, end_date])
            total_duration = timedelta()
            for work_time in work_times:
                duration = work_time.end_time - work_time.start_time
                total_duration += duration
            total_hours = round(total_duration.total_seconds() / 3600, 2)
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

