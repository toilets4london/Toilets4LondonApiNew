from rest_framework_gis.serializers import GeoFeatureModelSerializer
from api.models import Toilet, SuggestedToilet, Report, Rating
from rest_framework import serializers
from rest_framework.reverse import reverse


class ToiletSerializer(GeoFeatureModelSerializer):
    date_created = serializers.DateTimeField(format="%d/%m/%Y", required=False, read_only=True)
    date_modified = serializers.DateTimeField(format="%d/%m/%Y", required=False, read_only=True)

    class Meta:
        model = Toilet
        fields = '__all__'
        geo_field = 'location'


class SuggestedToiletSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = SuggestedToilet
        fields = '__all__'
        geo_field = 'location'


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = '__all__'
