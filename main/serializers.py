from rest_framework import serializers
from .models import ModelCV


class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelCV
        fields = '__all__'  #all fields from the ModelCV model