from django.http import request
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ServiceRequest, Review
from .serializers import ServiceRequestSerializer, ReviewSerializer
from accounts.permissions import IsProvider


class ServiceRequestViewSet(viewsets.ModelViewSet):

    serializer_class = ServiceRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user

        if user.role == 'CUSTOMER':
            return ServiceRequest.objects.filter(
                customer=user
            )

        if user.role == 'PROVIDER':
            return ServiceRequest.objects.filter(
                provider__user=user
            )

        return ServiceRequest.objects.none()

    def create(self, request, *args, **kwargs):

        if request.user.role != 'CUSTOMER':
            return Response(
                {
                    'detail': 'Only customers can create service requests.'
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(customer=request.user)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated, IsProvider]
    )
    def accept(self, request, pk=None):

        service_request = self.get_object()

        if service_request.status != 'PENDING':
            return Response(
                {'detail': 'Only pending requests can be accepted.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        service_request.status = 'ACCEPTED'
        service_request.save()

        return Response({
            'message': 'Service request accepted successfully.',
            'status': service_request.status
        })

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated, IsProvider]
    )
    def reject(self, request, pk=None):

        service_request = self.get_object()

        if service_request.status != 'PENDING':
            return Response(
                {'detail': 'Only pending requests can be rejected.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        service_request.status = 'REJECTED'
        service_request.save()

        return Response({
            'message': 'Service request rejected.',
            'status': service_request.status
        })

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated, IsProvider]
    )
    def start(self, request, pk=None):

        service_request = self.get_object()

        if service_request.status != 'ACCEPTED':
            return Response(
                {'detail': 'Only accepted requests can be started.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        service_request.status = 'IN_PROGRESS'
        service_request.save()

        return Response({
            'message': 'Service request is now in progress.',
            'status': service_request.status
        })

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated, IsProvider]
    )
    def complete(self, request, pk=None):

        service_request = self.get_object()

        if service_request.status != 'IN_PROGRESS':
            return Response(
                {'detail': 'Only in-progress requests can be completed.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        service_request.status = 'COMPLETED'
        service_request.save()

        return Response({
            'message': 'Service request completed successfully.',
            'status': service_request.status
        })
    @action(
    detail=True,
    methods=['post'],
    permission_classes=[IsAuthenticated]
    )
    def cancel(self, request, pk=None):

        service_request = self.get_object()

        if request.user.role != 'CUSTOMER':
            return Response(
                {'detail': 'Only customers can cancel requests.'},
                status=status.HTTP_403_FORBIDDEN
        )

        if service_request.status != 'PENDING':
            return Response(
            {
                'detail':
                'Only pending requests can be cancelled.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

        service_request.status = 'CANCELLED'
        service_request.save()

        return Response({
            'message': 'Service request cancelled successfully.',
            'status': service_request.status
        })

class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'CUSTOMER':
            return Review.objects.filter(customer=user)

        if user.role == 'PROVIDER':
            return Review.objects.filter(provider__user=user)

        return Review.objects.none()

    def create(self, request, *args, **kwargs):

        if request.user.role != 'CUSTOMER':
            return Response(
                {
                    'detail': 'Only customers can create reviews.'
                },
                status=status.HTTP_403_FORBIDDEN
            )

        service_request_id = request.data.get('service_request')

        try:
            service_request = ServiceRequest.objects.get(
                id=service_request_id,
                customer=request.user
            )
        except ServiceRequest.DoesNotExist:
            return Response(
                {
                    'detail': 'Service request not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if service_request.status != 'COMPLETED':
            return Response(
                {
                    'detail': 'You can review only completed services.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if Review.objects.filter(
            service_request=service_request
        ).exists():
            return Response(
                {
                    'detail': 'This service request has already been reviewed.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        rating = request.data.get('rating')

        if not rating or int(rating) < 1 or int(rating) > 5:
            return Response(
                {
                    'detail': 'Rating must be between 1 and 5.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        review = Review.objects.create(
            service_request=service_request,
            customer=request.user,
            provider=service_request.provider,
            rating=rating,
            comment=request.data.get('comment', '')
        )

        serializer = self.get_serializer(review)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )