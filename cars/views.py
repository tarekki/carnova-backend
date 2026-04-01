from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Car
from .permissions import user_is_admin
from .serializers import CarSerializer


class CarListCreateView(generics.ListCreateAPIView):
    """
    GET: list cars (own cars, or all if admin).
    POST: create a car; owner is always request.user.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CarSerializer

    def get_queryset(self):
        qs = Car.objects.select_related("owner").order_by("-created_at")
        user = self.request.user
        if user_is_admin(user):
            return qs
        return qs.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CarDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET/PATCH/DELETE a single car.
    queryset is scoped like list: non-admins only see their cars (else 404).
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CarSerializer

    def get_queryset(self):
        qs = Car.objects.select_related("owner")
        user = self.request.user
        if user_is_admin(user):
            return qs
        return qs.filter(owner=user)
