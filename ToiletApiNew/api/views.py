from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_gis.filters import InBBoxFilter, DistanceToPointFilter
from api.models import Toilet, Rating, Report, SuggestedToilet
from api.serialisers import ToiletSerializer, RatingSerializer, ReportSerializer, SuggestedToiletSerializer
from rest_framework.permissions import IsAdminUser, SAFE_METHODS
from api.throttling import PostAnonymousRateThrottle, GetAnonymousRateThrottle
from rest_framework_gis.pagination import GeoJsonPagination


class IsAdminUserOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin


class ToiletViewSet(viewsets.ModelViewSet):
    serializer_class = ToiletSerializer
    queryset = Toilet.objects.filter(is_open=True)
    pagination_class = GeoJsonPagination
    filter_backends = (InBBoxFilter, DistanceToPointFilter)
    throttle_classes = [GetAnonymousRateThrottle]
    permission_classes = [IsAdminUserOrReadOnly]
    bbox_filter_field = 'location'  # eg: /toilets/?in_bbox=-1,50,1,52
    distance_filter_field = 'location'
    distance_ordering_filter_field = 'location'
    bbox_filter_include_overlapping = True

    # Note that the tile address start in the upper left, not the lower left origin used by some implementations.

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    throttle_classes = [GetAnonymousRateThrottle, PostAnonymousRateThrottle]
    serializer_class = RatingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        toilet = serializer.validated_data['toilet']
        num_ratings = toilet.num_ratings + 1
        toilet.num_ratings = num_ratings
        if toilet.rating and num_ratings > 1:
            toilet.rating = (toilet.rating * (num_ratings - 1) + serializer.validated_data['rating']) / num_ratings
        else:
            toilet.rating = serializer.validated_data['rating']
        toilet.save()

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    throttle_classes = [GetAnonymousRateThrottle, PostAnonymousRateThrottle]
    serializer_class = ReportSerializer


class SuggestedToiletViewSet(viewsets.ModelViewSet):
    queryset = SuggestedToilet.objects.all()
    throttle_classes = [GetAnonymousRateThrottle, PostAnonymousRateThrottle]
    serializer_class = SuggestedToiletSerializer
