from django.db.models import Count
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response

from .models import Server
from .serializers import ServerSerializer


class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()

    def list(self, request):
        by_category = request.query_params.get("category")
        by_qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        by_server_id = request.query_params.get("by_server_id")
        with_num_members = request.query_params.get("with_num_members") == "true"

        if by_user or by_server_id and not request.user.is_authenticated:
            raise AuthenticationFailed()

        # Filtering servers by category
        if by_category:
            self.queryset = self.queryset.filter(category__name=by_category)

        # Filtering servers by user
        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)

        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("members"))
        # Return servers by quantity
        if by_qty:
            self.queryset = self.queryset[: int(by_qty)]

        if by_server_id:
            try:
                self.queryset = self.queryset.filter(id=by_server_id)
                if not self.queryset.exists():
                    raise ValidationError(detail=f"Server with ID {by_server_id} does not exist.")
            except ValueError:
                # TODO: check the value error exception
                # server does not exist and nothing is returned
                raise ValidationError(detail="Server with ID {by_server_id} does not exist.")
        # Pass variable with context to modify its serialization with conditions.
        serializer = ServerSerializer(self.queryset, many=True, context={"num_members": with_num_members})
        return Response(serializer.data)
