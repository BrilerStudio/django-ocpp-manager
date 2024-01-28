from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from manager.models import ChargePoint, Location, Transaction


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = (
            'id',
            'name',
            'city',
            'address1',
            'address2',
            'comment',
        )


class ChargePointSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = ChargePoint
        fields = (
            'id',
            'code',
            'description',
            'status',
            'manufacturer',
            'latitude',
            'longitude',
            'serial_number',
            'comment',
            'model',
            'connectors',
            'password',
            'location',
            'websocket_url',
        )

    location = SlugRelatedField(
        slug_field='id',
        queryset=Location.objects.all(),
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
            'code',
            'description',
            'status',
            'manufacturer',
            'latitude',
            'longitude',
            'serial_number',
            'comment',
            'model',
            'connectors',
            'location',
            'password',
            'websocket_url',
        )

        read_only_fields = (
            'id',
            'code',
            'description',
            'status',
            'manufacturer',
            'latitude',
            'longitude',
            'serial_number',
            'comment',
            'model',
            'connectors',
            'location',
            'websocket_url',
        )

    location = LocationSerializer(read_only=True)

    def create(self, validated_data):
        charge_point = self.context['charge_point']

        password = validated_data.pop('password', None)
        if not charge_point.check_password(password):
            raise serializers.ValidationError({'password': 'Invalid password'})

        return charge_point


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'transaction_id',
            'city',
            'vehicle',
            'address',
            'meter_start',
            'meter_stop',
            'charge_point',
        )

        read_only_fields = (
            'transaction_id',
            'city',
            'vehicle',
            'address',
            'meter_start',
            'meter_stop',
            'charge_point',
        )

    charge_point = SlugRelatedField(
        slug_field='id',
        queryset=ChargePoint.objects.all(),
    )
