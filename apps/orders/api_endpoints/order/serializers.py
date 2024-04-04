from rest_framework.serializers import ModelSerializer, ValidationError
from django.db import transaction
from django.db.models import Sum, ExpressionWrapper, DurationField, F, Count, FloatField

from datetime import timedelta
from geopy.distance import geodesic
from django.contrib.gis.geos import GEOSGeometry, Point
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
        fields = ('id', 'payment_type', 'longitude',
                  'latitude', 'items',)

    def create(self, validated_data):
        with transaction.atomic():

            # Extract necessary data from validated_data
            payment_type = validated_data.pop('payment_type')
            longitude = validated_data.pop('longitude')
            latitude = validated_data.pop('latitude')
            order_items_data = validated_data.pop('items')

            # Find nearest branch
            nearest_branch = Branch.objects.annotate(distance=Distance(
                F('location'),Point(latitude, longitude, srid=4326))*1,).order_by('distance').first()

            # for branch in Branch.objects.all():
            #     p2 = (branch.latitude, branch.longitude)
            #     p2 = GEOSGeometry(
            #         f"SRID=4326;POINT({branch.latitude} {branch.longitude})")
            #     distance = p1.distance(p2) * 100
            #     # geodesic(p1, p2).kilometers
            #     if nearest_branch is None or distance < nearest_distance:
            #         nearest_branch = branch
            #         nearest_distance = distance

            # Calculate total price and total cooking time
            total_price = 0
            all_foods_amount = 0
            for item_data in order_items_data:
                if item_data.get('food').available and item_data.get('food') in nearest_branch.branch_foods.all():
                    food = item_data['food']
                    amount = item_data['amount']
                    food_price = food.price
                    total_price += food_price * amount
                    all_foods_amount += amount
                else:
                    raise ValidationError(
                        {'item': "food", 'info': "Not available food selected"})

            all_cooking_time = Order.objects.filter(state=States.WAITING, branch=nearest_branch).aggregate(
                queue_amount=Count("items__amount"))

            cooking_time = timedelta(
                minutes=all_foods_amount+all_cooking_time['queue_amount'], seconds=15*(all_foods_amount+all_cooking_time['queue_amount']))

            # Calculate delivery time based on distance to nearest branch
            delivery_time = timedelta(minutes=3*nearest_branch.distance)
            print(nearest_branch.distance)
            print(delivery_time)
            # Create the order
            order = Order.objects.create(
                client=self.context['request'].user,
                payment_type=payment_type,
                longitude=longitude,
                latitude=latitude,
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
        fields = ('id', 'client', 'total_price', 'payment_type', 'state', 'longitude',
                  'latitude',
                  'branch', 'delivery_time', 'cancelled', 'items',)
        read_only_fields = fields


class OrderUpdateWaiterSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'state', 'cancelled',)


class OrderUpdateClientSerializer(ModelSerializer):

    class Meta:
        model = Order
        fields = ('id', 'payment_type', 'longitude',
                  'latitude', 'cancelled',)
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

   # def create(self, validated_data):
    #     with transaction.atomic():
    #         payment_type = validated_data.pop('payment_type')
    #         longitude = validated_data.pop('longitude')
    #         latitude = validated_data.pop('latitude')

    #         order_items = validated_data.pop('items')

    #         total_price = 0
    #         all_foods_amount = 0
    #         for item in order_items:
    #             item_food = Food.objects.get(id=item.get('food').id)
    #             if item_food.available:
    #                 all_foods_amount += item.get('amount')
    #                 total_price += item.get('amount')*item_food.price
    #             else:
    #                 raise ValidationError(
    #                     {'item': "food", 'info': "Not available food selected"})

    #         p1 = (latitude, longitude)
    #         near_branch = {}
    #         for branch in Branch.objects.all():
    #             p2 = (branch.latitude, branch.longitude)
    #             distance = geodesic(p1, p2).kilometers
    #             print(geodesic(p1, p2).kilometers)
    #             print(geodesic(p1, p2).km)
    #             if not near_branch:
    #                 near_branch['branch'] = branch
    #                 near_branch['distance'] = distance
    #             elif distance < near_branch['distance']:
    #                 near_branch['distance'] = distance
    #                 near_branch['branch'] = branch

    #         order = Order.objects.create(
    #             client=self.context['request'].user,
    #             payment_type=payment_type,
    #             longitude=longitude,
    #             latitude=latitude,
    #             branch=near_branch['branch'],
    #         )

    #         delivery_time = timedelta(minutes=3*near_branch['distance'])
    #         cooking_time = timedelta(
    #             minutes=1*all_foods_amount, seconds=15*all_foods_amount)

    #         order.total_price = total_price
    #         order.cooking_time = cooking_time
    #         order.delivery_time = delivery_time
    #         order.save()

    #         order_items_for_create = []
    #         for item in order_items:
    #             item_food = Food.objects.get(id=item.get('food').id)
    #             if item_food.available:
    #                 order_items_for_create.append(
    #                     OrderItem(order=order, food=item.get('food'), amount=item.get(
    #                         'amount'), total_price=item_food.price*item.get(
    #                         'amount'), comment=item.get('comment'))
    #                 )

    #         OrderItem.objects.bulk_create(order_items_for_create)

    #         return order
