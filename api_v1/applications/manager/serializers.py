from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from manager.models import ChargePoint, Location, Transaction
from manager.transactions import create_remote_transaction


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = (
            'id',
            'name',
            'city',
            'address1',
            'address2',
            'description',
            'created_at',
            'updated_at',
        )


class ChargePointSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = ChargePoint
        fields = (
            'id',
            'charge_point_id',
            'description',
            'is_enabled',
            'manufacturer',
            'latitude',
            'longitude',
            'serial_number',
            'model',
            'connectors',
            'connectors_count',
            'location',
            'password',
            'websocket_url',
            'created_at',
            'updated_at',
        )

    location = SlugRelatedField(
        slug_field='id',
        queryset=Location.objects.all(),
        required=False,
    )

    def create(self, validated_data):
        # Hash the new password if provided
        password = validated_data.pop('password', None)
        if password:
            validated_data['password_hash'] = make_password(password)

        # Create the ChargePoint object
        charge_point = ChargePoint.objects.create(**validated_data)
        return charge_point

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.password = make_password(password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class ChargePointVerifyPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = ChargePoint
        fields = (
            'id',
            'charge_point_id',
            'description',
            'is_enabled',
            'manufacturer',
            'latitude',
            'longitude',
            'serial_number',
            'model',
            'connectors',
            'location',
            'password',
            'websocket_url',
            'created_at',
            'updated_at',
        )

        read_only_fields = (
            'id',
            'charge_point_id',
            'description',
            'status',
            'manufacturer',
            'latitude',
            'longitude',
            'serial_number',
            'model',
            'connectors',
            'location',
            'websocket_url',
            'created_at',
            'updated_at',
        )

    location = LocationSerializer(read_only=True)

    def create(self, validated_data):
        charge_point = self.context['charge_point']

        if not charge_point.is_enabled:
            raise serializers.ValidationError({'charge_point_id': 'Charge point is disabled'})

        password = validated_data.pop('password', None)
        if not charge_point.check_password(password):
            raise serializers.ValidationError({'password': 'Invalid password'})

        return charge_point


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'transaction_id',
            'tag_id',
            'city',
            'vehicle',
            'address',
            'meter_start',
            'meter_value_raw',
            'meter_stop',
            'charge_point',
            'connector_id',
            'external_id',
            'start_date',
            'end_date',
            'status',

        )

        read_only_fields = (
            'transaction_id',
            'tag_id',
            'meter_start',
            'meter_value_raw',
            'meter_stop',
            'start_date',
            'end_date',
            'status',
        )

    charge_point = SlugRelatedField(
        slug_field='id',
        queryset=ChargePoint.objects.all(),
    )

    connector_id = serializers.IntegerField(
        default=1,
    )

    @transaction.atomic()
    def create(self, validated_data):
        charge_point = validated_data.pop('charge_point')
        connector_id = validated_data.pop('connector_id')

        return create_remote_transaction(
            charge_point=charge_point,
            connector_id=connector_id,
            **validated_data,
        )
