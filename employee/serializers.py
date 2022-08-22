from rest_framework.serializers import ModelSerializer
from .models import TestFile
class TestSerializer(ModelSerializer):
    class Meta:
        model = TestFile
        fields = "__all__"