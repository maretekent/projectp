from rest_framework import serializers
from app_dir.api.models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = (
            'id',
            'msisdn',
            'first_name',
            'middle_name',
            'last_name',
            'trans_time',
            'trans_id',
            'trans_amount',
            'org_account_balance',
            'invoice_number',
            'bill_ref_number',
            'third_party_transid',
            'business_short_code',
            'transaction_type',
            'status'
        )