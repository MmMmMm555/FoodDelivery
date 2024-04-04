from rest_framework.serializers import ModelSerializer, ValidationError
from django.db import transaction
from django.db.models import F, Count

from datetime import timedelta
from django.contrib.gis.geos import Point, GEOSGeometry
from django.contrib.gis.db.models.functions import Distance

from apps.orders.models import Order, OrderItem, States
from apps.branches.models import Branch
from apps.foods.api_endpoints.foods.serializers import FoodListSerializer


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('food', 'amount', 'comment',)


class OrderItemListSerializer(ModelSerializer):
    food = FoodListSerializer(many=False, read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'food', 'amount', 'total_price', 'comment',)


class OrderSerializer(ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'payment_type', 'location', 'items',)

    def create(self, validated_data):
        with transaction.atomic():

            # Extract necessary data from validated_data
            payment_type = validated_data.pop('payment_type')
            location = validated_data.pop('location')
            order_items_data = validated_data.pop('items')

            # Calculate total price and total cooking time
            total_price = 0
            all_foods_amount = 0
            ordered_foods = []
            for item_data in order_items_data:
                if item_data.get('food').available and item_data.get('food'):
                    food = item_data['food']
                    amount = item_data['amount']
                    ordered_foods.append(food.id)
                    total_price += food.price * amount
                    all_foods_amount += amount
                else:
                    raise ValidationError(
                        {'item': "food", 'info': "Not available food selected"})

            # Find available branches
            available_branches = Branch.objects.filter(
                branch_foods__in=ordered_foods).distinct()
            if not available_branches:
                raise ValidationError(
                    {'item': 'branch', 'info': "available branches not found for given foods"})

            # Find nearest branch
            nearest_branch = available_branches.annotate(distance=Distance(
                F('location'), GEOSGeometry(location))*1,).order_by('distance').first()

            all_cooking_time = Order.objects.filter(state=States.WAITING, branch=nearest_branch).aggregate(
                queue_amount=Count("items__amount"))

            cooking_time = timedelta(
                minutes=all_foods_amount+all_cooking_time['queue_amount'], seconds=15*(all_foods_amount+all_cooking_time['queue_amount']))

            # Calculate delivery time based on distance to nearest branch
            delivery_time = timedelta(minutes=3*nearest_branch.distance)

            # Create the order
            order = Order.objects.create(
                client=self.context['request'].user,
                payment_type=payment_type,
                location=location,
                branch=nearest_branch,
                total_price=total_price,
                delivery_time=delivery_time+cooking_time
            )

            # Create order items
            order_items_for_create = [
                OrderItem(
                    order=order,
                    food=item_data['food'],
                    amount=item_data['amount'],
                    total_price=item_data['food'].price *
                    item_data['amount'],
                    comment=item_data.get('comment', '')
                )
                for item_data in order_items_data
            ]

            OrderItem.objects.bulk_create(order_items_for_create)

            return order


class OrderListSerializer(ModelSerializer):
    items = OrderItemListSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'client', 'total_price', 'payment_type', 'state', 'location',
                  'branch', 'delivery_time', 'cancelled', 'items',)
        read_only_fields = fields


class OrderUpdateWaiterSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'state', 'cancelled',)


class OrderUpdateClientSerializer(ModelSerializer):

    class Meta:
        model = Order
        fields = ('id', 'payment_type', 'location', 'cancelled',)
        extra_kwargs = {
            'longitude': {'required': False},
            'latitude': {'required': False},
        }

    def validate(self, attrs):
        if (attrs['cancelled'] and self.instance.cancelled):
            raise ValidationError({'order': "order already cancelled"})
        if (attrs['cancelled'] in [1, 0]) and self.instance.cancelled:
            raise ValidationError({'order': "reorder is not allowed"})
        if attrs['cancelled'] and (self.instance.state == States.DELIVERING):
            raise ValidationError(
                {'order': "you can not cancel now, order on the way"})

        return super().validate(attrs)
