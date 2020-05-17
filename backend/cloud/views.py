from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import SubscriptionCreateSerializer, ServerStatusSerializer, ChangeServerSerializer, \
    UpdateServiceSerializer, GetbrokenSubscriptionsSerializer
from .models import Subscription, Server, ServerType, IpgServer, WebcmServer
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
                        server = Server(server_type=ServerType.objects.get(name=server), action='Stop', subscription=subscription_a)
                        server.save()
                        if server.server_type.name == "IpgServer":
                            ipg = IpgServer()
                            ipg.server = server
                            ipg.save()
                        elif server.server_type.name == "WebcmServer":
                            webcm = WebcmServer()
                            webcm.server = server
                            webcm.save()
                        Servers.append(server.server_type.name)
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


class UpdateServiceDetail(GenericAPIView):
    serializer_class = UpdateServiceSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        subscription = serializer.validated_data['subscription']
        print(subscription.id)
        subscription_list = []

        servers = request.data.get('servers')
        ipgserver_input = servers['IpgServer']
        ipgserver_object_id = Server.objects.filter(subscription=subscription).values_list('id', flat=True)[0]
        ipgserver = IpgServer.objects.get(server=ipgserver_object_id)
        ipgserver.cpu = ipgserver_input['cpu']
        ipgserver.ram = ipgserver_input['ram']
        ipgserver.disc = ipgserver_input['disc']
        ipgserver.widea_address = ipgserver_input['widea_address']
        ipgserver.local_ip = ipgserver_input['local_ip']
        ipgserver.internal_ip = ipgserver_input['internal_ip']
        ipgserver.external_ip = ipgserver_input['external_ip']
        ipgserver.server_name = ipgserver_input['server_name']
        ipgserver.state = ipgserver_input['state']
        ipgserver.fqdn = ipgserver_input['fqdn']
        ipgserver.save()

        webcmServer_input = servers['WebcmServer']
        webcmserver_object_id = Server.objects.filter(subscription=subscription).values_list('id', flat=True)[1]
        webcmserver = WebcmServer.objects.get(server=webcmserver_object_id)
        webcmserver.address = webcmServer_input['address']
        webcmserver.local_ip = webcmServer_input['local_ip']
        webcmserver.internal_ip = webcmServer_input['internal_ip']
        webcmserver.server_name = webcmServer_input['server_name']
        webcmserver.state = webcmServer_input['state']
        webcmserver.fqdn = webcmServer_input['fqdn']
        webcmserver.save()

        return Response(
            {
                "result": True,
                "subscription": subscription.id,
                "service": "Ipg",
                "servers": {
                    "IpgServer": {
                        "cpu": ipgserver.cpu,
                        "ram": ipgserver.ram,
                        "disc": ipgserver.disc,
                        "widea_address": ipgserver.widea_address,
                        "local_ip": ipgserver.local_ip,
                        "internal_ip": ipgserver.internal_ip,
                        "external_ip": ipgserver.external_ip,
                        "server_name": ipgserver.server_name,
                        "server_id": ipgserver.server.id,
                        "state": ipgserver.state,
                        "fqdn": ipgserver.fqdn,
                    },
                    "WebcmServer": {
                        "address": webcmserver.address,
                        "local_ip": webcmserver.local_ip,
                        "internal_ip": webcmserver.internal_ip,
                        "server_name": webcmserver.server_name,
                        "server_id": webcmserver.server.id,
                        "state": webcmserver.state,
                        "fqdn": webcmserver.fqdn,
                    }
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
        server.server_type = serializer.validated_data['server_type']
        server.save()

        return Response(
            {
                "result": True,
                "subscriptions": {
                    "status": server.status,
                    "server_id": server.id,
                    "server_type": server.server_type.name,
                }
            },
            status=status.HTTP_200_OK
        )


class GetbrokenSubscriptionsView(GenericAPIView):
    serializer_class = GetbrokenSubscriptionsSerializer

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
                        server = Server(server_type=ServerType.objects.get(name=server), action='Stop', subscription=subscription_a)
                        server.save()
                        if server.server_type.name == "IpgServer":
                            ipg = IpgServer()
                            ipg.server = server
                            ipg.save()
                        elif server.server_type.name == "WebcmServer":
                            webcm = WebcmServer()
                            webcm.server = server
                            webcm.save()
                        Servers.append(server.server_type.name)
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
