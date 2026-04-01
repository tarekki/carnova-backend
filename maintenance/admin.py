from django.contrib import admin

from .models import MaintenanceAppointment, MaintenanceRecord, MileageLog


@admin.register(MileageLog)
class MileageLogAdmin(admin.ModelAdmin):
    list_display = ("id", "car", "mileage", "recorded_at")
    search_fields = ("car__plate_number", "car__brand", "car__model")
    list_filter = ("recorded_at",)


@admin.register(MaintenanceAppointment)
class MaintenanceAppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "car", "owner", "mechanic", "service_type", "appointment_date", "status", "created_at")
    search_fields = ("car__plate_number", "owner__email", "mechanic__email", "service_type")
    list_filter = ("status", "appointment_date", "created_at")


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "car", "appointment", "mechanic", "service_done", "cost", "service_date", "created_at")
    search_fields = ("car__plate_number", "mechanic__email", "service_done")
    list_filter = ("service_date", "created_at")
