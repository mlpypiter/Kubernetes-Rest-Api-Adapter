from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from common.exception import CustomException
from .models import Subscription, ServerType, Server


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    subscriptions = serializers.ListField(required=False)

    default_error_messages = {
        'invalid_subscriptions': _('subscriptions is invalid.'),
    }
    class Meta:
        model = Subscription
        fields = ("subscriptions",)

    def validate(self, attrs):
        return attrs


class ServerStatusSerializer(serializers.ModelSerializer):
    server_ids = serializers.IntegerField(required=False)
    action = serializers.CharField(required=False)
    server_type = serializers.CharField(required=False)

    default_error_messages = {
        'invalid_serverid': _('serverid is invalid.'),
        'invalid_action': _('action is not invalid.'),
        'invalid_server_type': _('server_type is invalid.'),
    }

    class Meta:
        model = Subscription
        fields = ("server_ids", "action", "server_type")

    def validate(self, attrs):
        server_ids = attrs.get("server_ids")
        action = attrs.get("action")
        server_type = attrs.get("server_type")

        if not server_ids:
            raise CustomException(code=10, message=self.error_messages['invalid_serverid'])
        if not action:
            raise CustomException(code=11, message=self.error_messages['invalid_action'])
        if not server_type:
            raise CustomException(code=12, message=self.error_messages['invalid_server_type'])

        try:
            server = Server.objects.get(id=server_ids)
            server_type = ServerType.objects.get(name=server_type)
            attrs['server'] = server
            attrs['server_type'] = server_type
            return attrs
        except ObjectDoesNotExist:
            raise CustomException(code=14, message=self.error_messages['invalid_serverid'])


class ChangeServerSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(required=False)
    server_id = serializers.CharField(required=False)
    server_type = serializers.CharField(required=False)

    default_error_messages = {
        'invalid_status': _('status is invalid.'),
        'invalid_server_id': _('server_id is not invalid.'),
        'invalid_server_type': _('server_type is invalid.'),
    }

    class Meta:
        model = Subscription
        fields = ("status", "server_id", "server_type")

    def validate(self, attrs):
        status = attrs.get("status")
        server_id = attrs.get("server_id")
        server_type = attrs.get("server_type")

        if not status:
            raise CustomException(code=10, message=self.error_messages['invalid_status'])
        if not server_id:
            raise CustomException(code=11, message=self.error_messages['invalid_server_id'])
        if not server_type:
            raise CustomException(code=12, message=self.error_messages['invalid_server_type'])

        try:
            server = Server.objects.get(id=server_id)
            server_type = ServerType.objects.get(name=server_type)
            attrs['server'] = server
            attrs['server_type'] = server_type
            return attrs
        except ObjectDoesNotExist:
            raise CustomException(code=14, message=self.error_messages['invalid_server_id'])


class UpdateServiceSerializer(serializers.ModelSerializer):
    subscription = serializers.IntegerField(required=False)
    service = serializers.CharField(required=False)
    servers = serializers.DictField(required=False)

    default_error_messages = {
        'invalid_subscription': _('subscription is invalid.'),
        'invalid_service': _('service is invalid.'),
    }

    class Meta:
        model = Subscription
        fields = ("subscription", "service", "servers")

    def validate(self, attrs):
        subscription = attrs.get("subscription")
        service = attrs.get("service")
        servers = attrs.get("servers")
        print(servers)

        if not subscription:
            raise CustomException(code=10, message=self.error_messages['invalid_subscription'])
        if not service:
            raise CustomException(code=11, message=self.error_messages['invalid_service'])

        try:
            subscription = Subscription.objects.get(subscription=subscription)
            attrs['subscription'] = subscription
        except ObjectDoesNotExist:
            raise CustomException(code=14, message=self.error_messages['invalid_subscription'])

        return attrs


class GetbrokenSubscriptionsSerializer(serializers.ModelSerializer):
    subscriptions = serializers.ListField(required=False)

    default_error_messages = {
        'invalid_subscriptions': _('subscriptions is invalid.'),
    }

    class Meta:
        model = Subscription
        fields = ("subscriptions",)

    def validate(self, attrs):
        return attrs

