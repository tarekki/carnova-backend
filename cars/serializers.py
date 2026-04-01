from datetime import date

from rest_framework import serializers

from .models import Car


class CarSerializer(serializers.ModelSerializer):
    """All car fields; owner is set by the view on create, not by the client."""

    class Meta:
        model = Car
        fields = (
            "id",
            "owner",
            "brand",
            "model",
            "year",
            "plate_number",
            "color",
            "mileage",
            "created_at",
        )
        read_only_fields = ("id", "owner", "created_at")

    def validate_year(self, value: int) -> int:
        current = date.today().year
        if value < 1900:
            raise serializers.ValidationError("Year must be 1900 or later.")
        if value > current + 1:
            raise serializers.ValidationError(
                f"Year cannot be greater than {current + 1}."
            )
        return value

    def validate_mileage(self, value: int) -> int:
        if value > 2_000_000:
            raise serializers.ValidationError("Mileage value is unrealistically high.")
        return value
