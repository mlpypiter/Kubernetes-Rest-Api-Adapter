from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import SubscriptionCreateSerializer
from .models import Subscription


class SubscriptionCreateView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    serializer_class = SubscriptionCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subscription = Subscription()
        subscription.customer = serializer.data.get('customer')
        subscription.start_date = serializer.data.get('start_date')
        subscription.end_date = serializer.data.get('end_date')
        subscription.term_subscription = serializer.data.get('term_subscription')
        subscription.service_type = serializer.validated_data['service_type']
        subscription.subscription = serializer.data.get('subscription')
        subscription.server_name_prefix = serializer.data.get('server_name_prefix')
        subscription.package = serializer.data.get('package')
        subscription.trunk_service_provider = serializer.data.get('trunk_service_provider')
        subscription.extra_call_record_package = serializer.data.get('extra_call_record_package')
        subscription.demo = serializer.data.get('demo')
        subscription.extra_duration_package = serializer.data.get('extra_duration_package')
        subscription.save()

        return Response(
            {
                "result": True,
                "subscriptions": {
                    "customer": subscription.customer,
                    "start_date": subscription.start_date,
                    "end_date": subscription.end_date,
                    "term_subscription": subscription.term_subscription,
                    "service_type": subscription.service_type.type,
                    "subscription": subscription.subscriptio,
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
