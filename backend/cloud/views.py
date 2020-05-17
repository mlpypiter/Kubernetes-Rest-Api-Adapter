from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import SubscriptionCreateSerializer, ServerStatusSerializer, ChangeServerSerializer
from .models import Subscription, Server, ServiceType
from common.serializers import serialize_subscription


class SubscriptionCreateView(GenericAPIView):
    serializer_class = SubscriptionCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        subscriptions = serializer.data.get('subscriptions')
        subscription_list = []
        if subscriptions:
            for subscription in subscriptions:
                subscription_a = Subscription(
                    customer=subscription['customer'],
                    start_date=subscription['start_date'],
                    end_date=subscription['end_date'],
                    term_subscription=subscription['term_subscription'],
                    service_type=subscription['service_type'],
                    subscription=subscription['subscription'],
                    server_name_prefix=subscription['server_name_prefix'],
                    package=subscription['package'],
                    trunk_service_provider=subscription['trunk_service_provider'],
                    extra_call_record_package=subscription['extra_call_record_package'],
                    demo=subscription['demo'],
                    extra_duration_package=subscription['extra_duration_package'],
                    state="Initializing"
                )
                subscription_a.save()
                servers = subscription['servers']
                Servers = []
                if servers:
                    for server in servers:
                        server = Server(service_type=ServiceType.objects.get(name=server), action='Stop', subscription=subscription_a)
                        server.save()
                        Servers.append(server.service_type.name)
                subscription_list.append({
                    **serialize_subscription(subscription_a),
                    "servers": Servers
                })

        return Response(
            {
                "result": True,
                "subscriptions": subscription_list

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
        server.server_type = serializer.validated_data['server_type']
        server.save()

        return Response(
            {
                "result": True,
                "subscriptions": {
                    "id": server.id,
                    "action": server.action,
                    "server_type": server.server_type.name,
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
        server.status = serializer.data.get('status')
        server.service_type = serializer.validated_data['server_type']
        server.save()

        return Response(
            {
                "result": True,
                "subscriptions": {
                    "status": server.status,
                    "server_id": server.id,
                    "server_type": server.service_type.name,
                }
            },
            status=status.HTTP_200_OK
        )


class GetbrokenSubscriptionsView(GenericAPIView):

    def get(self, request):
        subscriptions = Subscription.objects.all()
        subscriptions_list = []
        for subscription in subscriptions:
            subscriptions_list.append({
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
            })

        return Response(
            {
                "result": True,
                "subscriptions": subscriptions_list,
            },
            status=status.HTTP_200_OK
        )
