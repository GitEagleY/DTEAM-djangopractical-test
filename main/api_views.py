from rest_framework import generics
from drf_spectacular.utils import extend_schema

from .models import ModelCV
from .serializers import CVSerializer


class CVAPIView(generics.ListCreateAPIView):
    """API view for listing and creating CVs"""
    queryset = ModelCV.objects.all()
    serializer_class = CVSerializer

    @extend_schema(
        summary="List all CVs",
        description="Retrieves a paginated list of all CVs in the system.",
        responses={
            200: CVSerializer(many=True),
            400: {"description": "Bad request"},
            500: {"description": "Internal server error"}
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Create CV",
        description="Creates a new CV with personal information, skills, projects, and contacts.",
        request=CVSerializer,
        responses={
            201: CVSerializer,
            400: {"description": "Invalid data provided"},
            500: {"description": "Internal server error"}
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CVDetailedAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API view for retrieving, updating and deleting individual CVs"""
    queryset = ModelCV.objects.all()
    serializer_class = CVSerializer

    @extend_schema(
        summary="Get CV details",
        description="Retrieves details of a specific CV.",
        responses={
            200: CVSerializer,
            404: {"description": "CV not found"},
            500: {"description": "Internal server error"}
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update CV",
        description="Updates an existing CV.",
        request=CVSerializer,
        responses={
            200: CVSerializer,
            400: {"description": "Invalid data provided"},
            404: {"description": "CV not found"}
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Delete CV",
        description="Deletes a specific CV.",
        responses={
            204: None,
            404: {"description": "CV not found"}
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
