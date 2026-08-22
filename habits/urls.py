# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import HabitViewSet, public_habits_list
#
# router = DefaultRouter()
# router.register(r'habits', HabitViewSet, basename='habit')
#
#
# urlpatterns = [
#     path('public/', public_habits_list, name='public-habits'),
#     path('', include(router.urls)),
# ]


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet

router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habit')

urlpatterns = [
    path('', include(router.urls)),
]
