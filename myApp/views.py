from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from datetime import datetime, timedelta, time, date
import calendar
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django import http


# Create your views here.


class EventView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        self.is_not_used()
        duration = request.GET.get('q', '')
        today_min = datetime.combine(datetime.now(), time.min)

        if duration == 'all':
            fetchedData = models.Event.objects.filter(date__gte=today_min)
        elif duration == 'today':
            today_max = datetime.combine(date.today(), time.max)
            fetchedData = models.Event.objects.filter(date__range=(today_min, today_max))
        elif duration == 'tomorrow':
            tomorrow_min = datetime.combine(date.today() + timedelta(1), time.min)
            tomorrow_max = datetime.combine(date.today() + timedelta(1), time.max)
            fetchedData = models.Event.objects.filter(date__range=(tomorrow_min, tomorrow_max))
        elif duration == 'week':
            days_left = 6 - date.today().weekday()
            week_max = datetime.combine(date.today() + timedelta(days_left), time.max)
            fetchedData = models.Event.objects.filter(date__range=(today_min, week_max))
        else:
            days_left = calendar.monthrange(datetime.now().year, datetime.now().month)[1] - datetime.now().day
            month_max = datetime.combine(date.today() + timedelta(days_left), time.max)
            fetchedData = models.Event.objects.filter(date__range=(today_min, month_max))

        detail = [
            {
                "name": detail.eventName,
                "type": detail.eventType,
                "venue": detail.venue,
                "price": detail.price,
                "detail": detail.detail,
                "date": detail.date.strftime("%d %b, %Y ( %A )")
            }
            for detail in fetchedData
        ]
        return Response(detail)

    def is_not_used(self):
        pass


class ActivityView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        self.is_not_used()
        duration = request.GET.get('q', '')

        today_min = datetime.combine(datetime.now(), time.min)

        if duration == 'all':
            fetchedData = models.Activity.objects.filter(date__gte=today_min)
        elif duration == 'today':
            today_max = datetime.combine(date.today(), time.max)
            fetchedData = models.Activity.objects.filter(date__range=(today_min, today_max))
        elif duration == 'tomorrow':
            tomorrow_min = datetime.combine(date.today() + timedelta(1), time.min)
            tomorrow_max = datetime.combine(date.today() + timedelta(1), time.max)
            fetchedData = models.Activity.objects.filter(date__range=(tomorrow_min, tomorrow_max))
        elif duration == 'week':
            days_left = 6 - date.today().weekday()
            week_max = datetime.combine(date.today() + timedelta(days_left), time.max)
            fetchedData = models.Activity.objects.filter(date__range=(today_min, week_max))
        else:
            days_left = calendar.monthrange(datetime.now().year, datetime.now().month)[1] - datetime.now().day
            month_max = datetime.combine(date.today() + timedelta(days_left), time.max)
            fetchedData = models.Activity.objects.filter(date__range=(today_min, month_max))

        detail = [
            {
                "name": detail.activityName,
                "type": detail.activityType,
                "venue": detail.venue,
                "price": detail.price,
                "detail": detail.detail,
                "date": detail.date.strftime("%d %b, %Y ( %A )")
            }
            for detail in fetchedData
        ]
        return Response(detail)

    def is_not_used(self):
        pass


class TripView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        fetchedData = 0
        self.is_not_used()
        duration = request.GET.get('q', '')
        today_min = datetime.combine(datetime.now(), time.min)

        if duration == 'all':
            fetchedData = models.Trip.objects.filter(date__gte=today_min)
        elif duration == 'today':
            today_max = datetime.combine(date.today(), time.max)
            fetchedData = models.Trip.objects.filter(date__range=(today_min, today_max))
        elif duration == 'tomorrow':
            tomorrow_min = datetime.combine(date.today() + timedelta(1), time.min)
            tomorrow_max = datetime.combine(date.today() + timedelta(1), time.max)
            fetchedData = models.Trip.objects.filter(date__range=(tomorrow_min, tomorrow_max))
        elif duration == 'week':
            days_left = 6 - date.today().weekday()
            week_max = datetime.combine(date.today() + timedelta(days_left), time.max)
            fetchedData = models.Trip.objects.filter(date__range=(today_min, week_max))
        elif duration == 'month':
            days_left = calendar.monthrange(datetime.now().year, datetime.now().month)[1] - datetime.now().day
            month_max = datetime.combine(date.today() + timedelta(days_left), time.max)
            fetchedData = models.Trip.objects.filter(date__range=(today_min, month_max))

        detail = [
            {
                "destination": detail.destination,
                "nights": detail.nights,
                "price": detail.price,
                "detail": detail.detail,
                "date": detail.date.strftime("%d %b, %Y ( %A )")
            }
            for detail in fetchedData
        ]
        return Response(detail)

    def is_not_used(self):
        pass


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        self.is_not_used()
        registerSerializer = UserSerializer(data=request.data)

        try:
            registerSerializer.is_valid(raise_exception=True)
        except serializers.ValidationError as err:
            errors = ''.join([str(v[0]) for k, v in err.args[0].items()])
            return http.HttpResponseBadRequest(errors)
        else:
            registerSerializer.validated_data['password'] = make_password(registerSerializer.validated_data['password'])
            user = registerSerializer.save()
            refresh = RefreshToken.for_user(user)
            refresh = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response(refresh)

    def is_not_used(self):
        pass


class UserDetailsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        self.is_not_used()
        user = models.User.objects.get(email=request.user.email)
        userSerializer = UserSerializer(user, context={"request": request})
        return Response(userSerializer.data)

    def is_not_used(self):
        pass
