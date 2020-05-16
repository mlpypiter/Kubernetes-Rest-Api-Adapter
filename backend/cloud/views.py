from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import SubscriptionCreateSerializer, ServerStatusSerializer, ChangeServerSerializer
from .models import Subscription, ServiceType, Server, IpgServer, WebcmServer


class SubscriptionCreateView(GenericAPIView):
    serializer_class = SubscriptionCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subscription = Subscription()
        subscription.customer = serializer.data.get('customer')
        subscription.start_date = serializer.data.get('start_date')
        subscription.end_date = serializer.data.get('end_date')
        subscription.term_subscription = serializer.data.get('term_subscription')
        subscription.service_type = serializer.validated_data['serviceType']
        subscription.subscription = serializer.data.get('subscription')
        subscription.server_name_prefix = serializer.data.get('server_name_prefix')
        subscription.package = serializer.data.get('package')
        subscription.trunk_service_provider = serializer.data.get('trunk_service_provider')
        subscription.extra_call_record_package = serializer.data.get('extra_call_record_package')
        subscription.demo = serializer.data.get('demo')
        subscription.extra_duration_package = serializer.data.get('extra_duration_package')
        subscription.state = "Initializing"
        subscription.save()

        return Response(
            {
                "result": True,
                "subscriptions": {
                    "id": subscription.id,
                    "customer": subscription.customer,
                    "start_date": subscription.start_date,
                    "end_date": subscription.end_date,
                    "term_subscription": subscription.term_subscription,
                    "service_type": subscription.service_type.name,
                    "subscription": subscription.subscription,
                    "server_name_prefix": subscription.server_name_prefix,
                    "package": subscription.package,
                    "trunk_service_provider": subscription.trunk_service_provider,
                    "extra_call_record_package": subscription.extra_call_record_package,
                    "demo": subscription.demo,
                    "extra_duration_package": subscription.extra_duration_package,
                }

            },
            status=status.HTTP_200_OK
        )


class ControlServerView(GenericAPIView):
    serializer_class = ServerStatusSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        server = serializer.validated_data['server']
        server.action = serializer.data.get('action')
        server.server_type = serializer.data.get('server_type')
        server.save()

        return Response(
            {
                "result": True,
                "subscriptions": {
                    "id": server.id,
                    "action": server.action,
                    "server_type": server.server_type,
                }
            },
            status=status.HTTP_200_OK
        )


class ChangeServerView(GenericAPIView):
    serializer_class = ChangeServerSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        server = serializer.validated_data['server']
        server.action = serializer.data.get('status')
        server.server_type = serializer.data.get('server_type')
        server.save()

        return Response(
            {
                "result": True,
                "subscriptions": {
                    "id": server.id,
                    "status": server.action,
                    "server_type": server.server_type,
                }
            },
            status=status.HTTP_200_OK
        )
