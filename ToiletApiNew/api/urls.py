from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'toilets', views.ToiletViewSet)
router.register(r'ratings', views.RatingViewSet)
router.register(r'reports', views.ReportViewSet)
router.register(r'suggestedtoilets', views.SuggestedToiletViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]