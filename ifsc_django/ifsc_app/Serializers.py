from rest_framework import serializers

class IFSCSerializer(serializers.Serializer):
    bank = serializers.CharField()
    ifsc = serializers.CharField()
    micr_code = serializers.CharField()
    branch = serializers.CharField()
    district = serializers.CharField()
    address = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()

class ApiHistorySerializer(serializers.Serializer):
    ifsc = serializers.CharField()
    timestamp = serializers.DateTimeField()

    