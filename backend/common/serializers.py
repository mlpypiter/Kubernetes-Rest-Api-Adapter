
def serialize_subscription(subscription):
    return {
        "id": subscription.id,
        "customer": subscription.customer,
        "start_date": subscription.start_date,
        "end_date": subscription.end_date,
        "term_subscription": subscription.term_subscription,
        "service_type": subscription.service_type,
        "subscription": subscription.subscription,
        "server_name_prefix": subscription.server_name_prefix,
        "package": subscription.package,
        "trunk_service_provider": subscription.trunk_service_provider,
        "extra_call_record_package": subscription.extra_call_record_package,
        "demo": subscription.demo,
        "extra_duration_package": subscription.extra_duration_package,
    }
