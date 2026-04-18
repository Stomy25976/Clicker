from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserSerializer, ProfileSerializer
from .models import Profile
from rest_framework.response import Response
from rest_framework.decorators import api_view

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        profile = request.user.profile
        profile.clicks += profile.click_power
        profile.save()
        return Response({'clicks': profile.clicks})


@api_view(['GET'])
def my_api_page(request):
    data = {
        'message': 'Привет! Это данные с новой страницы API',
        'status': 'success'
    }
    return Response(data)

@api_view(['POST'])
def buy_upgrade(request):
    profile = request.user.profile
    if profile.clicks >= 100: # Цена улучшения
        profile.clicks -= 100
        profile.click_power = 2 # Теперь клик дает 2
        profile.save()
        return Response({'success': True})
    return Response({'error': 'Недостаточно кликов'}, status=400)