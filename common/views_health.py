"""
Public health endpoints for uptime probes, load balancers, and demos.

Three endpoints, all public (no auth) so ops tooling needs no credentials:

    POST /api/health/        — combined snapshot (always 200 if process is up)
    POST /api/health/live/   — liveness:   process is running                (200)
    POST /api/health/ready/  — readiness:  DB is reachable                   (200|503)

The split mirrors Kubernetes / standard cloud probe semantics:
- Liveness  = "should the orchestrator restart this pod?"  (only fail on hard crash)
- Readiness = "should the orchestrator route traffic here?" (fail when deps are down)
"""
from __future__ import annotations

import logging

from django.db import connection
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .responses import error_response, success_response

logger = logging.getLogger("carnova.health")


def _probe_database() -> tuple[bool, str | None]:
    """Run a single round-trip; return (ok, error_message)."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return True, None
    except Exception as exc:
        logger.warning("Health DB probe failed: %s", exc)
        return False, str(exc)


class _PublicPostView(APIView):
    http_method_names = ["post"]
    authentication_classes = []
    permission_classes = [AllowAny]


class HealthCheckView(_PublicPostView):
    """Combined snapshot — always returns 200 when the process is alive."""

    def post(self, request):
        db_ok, _ = _probe_database()
        return success_response(
            data={"status": "ok", "database": "ok" if db_ok else "error"},
            message="Service is healthy",
        )


class LivenessView(_PublicPostView):
    """Liveness probe: 200 = the process is alive (no dependency checks)."""

    def post(self, request):
        return success_response(data={"status": "ok"}, message="Service is alive")


class ReadinessView(_PublicPostView):
    """Readiness probe: 200 only when all critical dependencies are healthy.

    A failed DB probe returns HTTP 503 so an orchestrator can stop routing
    traffic to this instance until the dependency recovers.
    """

    def post(self, request):
        db_ok, db_err = _probe_database()
        if not db_ok:
            return error_response(
                message="Service is not ready",
                errors={"database": [db_err or "unreachable"]},
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        return success_response(
            data={"status": "ok", "database": "ok"},
            message="Service is ready",
        )
