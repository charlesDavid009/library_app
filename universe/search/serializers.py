from rest_framework import serializers


class SearchSerailizer(serializers.Serializer):
    query = serializers.Charfield()