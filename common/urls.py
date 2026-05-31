from django.urls import path

from .views_health import HealthCheckView, LivenessView, ReadinessView

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path("health/live/", LivenessView.as_view(), name="health-live"),
    path("health/ready/", ReadinessView.as_view(), name="health-ready"),
]
