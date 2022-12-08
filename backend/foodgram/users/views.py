from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from djoser.views import UserViewSet

from .models import User, Follow

from api.serializers import FollowSerializer
from api.pagination import LimitPageNumberPagination


class CastomUserViewSet(UserViewSet):
    pagination_class = LimitPageNumberPagination

    @action(detail=True, permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        """Subscribe to the author"""
        user = request.user
        author = User.get_object_or_404(User, id=id)

        if user == author:
            return Response({
                'errors': "You can't subscribe to yourself."
            }, status=status.HTTP_400_BAD_REQUEST)
        if Follow.objects.filter(user=user, author=author).exists():
            return Response({
                'errors': "You have already subscribed to this author."
            }, status=status.HTTP_400_BAD_REQUEST)
        follow = Follow.objects.create(user=user, author=author)
        serializer = FollowSerializer(
            follow, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def del_subscribe(self, request, id=None):
        """Deleting a subscription to the author."""
        user = request.user
        author = User.get_object_or_404(User, id=id)

        if user == author:
            return Response({
                'errors': "You can't subscribe to yourself."
            }, status=status.HTTP_400_BAD_REQUEST)
        follow = Follow.objects.create(user=user, author=author)

        if follow.exists():
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
                'errors': "You have already unsubscribed."
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        """Returns the users that the current user is subscribed to.
           Recipes are added to the output."""
        user = request.user
        pages = self.paginate_queryset(Follow.objects.filter(user=user))
        serialiser = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serialiser.data)
