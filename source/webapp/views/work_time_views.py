from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from webapp.models import WorkTime
from webapp.serializers import WorkTimeSerializer
from accounts.models import User
from rest_framework.views import APIView
from datetime import datetime, time, timedelta
from django.db.models import Sum, Case, When
from rest_framework.response import Response
from django.db import models


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



# подсчет штрафов. Начало работы в 8,00.
# для проверки за определенный месяц /main/work-time-stats/1/?month=4
# за весь период /main/work-time-stats/1/

class WorkTimeStatsView(generics.RetrieveAPIView):
    def get(self, request, user_id, month=None):
        work_times = WorkTime.objects.filter(user_id=user_id)
        if month:
            work_times = work_times.filter(start_time__month=month)

        # Считаем количество опозданий и количество приходов вовремя
        late_count = work_times.filter(start_time__time__gt=time(8)).count()
        on_time_count = work_times.filter(start_time__time__lte=time(8)).count()

        # Считаем количество опозданий и штрафы
        penalties = work_times.annotate(
            is_late=Case(
                When(start_time__time__gt=time(8), then=1),
                default=0,
                output_field=models.IntegerField(),
            ),
            penalty=Case(
                When(start_time__time__gt=time(8), then=200),
                default=0,
                output_field=models.IntegerField(),
            ),
        ).aggregate(
            late_count=Sum('is_late'),
            total_penalty=Sum('penalty'),
        )

        return Response({
            'Вовремя': late_count,
            'Опозданий': on_time_count,
            'Штрафы': penalties['total_penalty'],
        }, status=status.HTTP_200_OK)
