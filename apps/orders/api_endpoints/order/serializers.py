from rest_framework.serializers import ModelSerializer, ValidationError
from django.db import transaction
from django.db.models import Sum, ExpressionWrapper, DurationField, F

from datetime import timedelta
from geopy.distance import geodesic

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
        fields = ('id', 'payment_type', 'longitude', 'latitude', 'items',)

    def create(self, validated_data):
        with transaction.atomic():

            # Extract necessary data from validated_data
            payment_type = validated_data.pop('payment_type')
            longitude = validated_data.pop('longitude')
            latitude = validated_data.pop('latitude')
            order_items_data = validated_data.pop('items')

            # Calculate total price and total cooking time
            total_price = 0
            all_foods_amount = 0
            for item_data in order_items_data:
                if item_data.get('food').available:
                    food = item_data['food']
                    amount = item_data['amount']
                    food_price = food.price
                    total_price += food_price * amount
                    all_foods_amount += amount
                else:
                    raise ValidationError(
                        {'item': "food", 'info': "Not available food selected"})
            all_cooking_time = Order.objects.filter(state=States.PREPARING).aggregate(
                total_cooking_time=Sum(ExpressionWrapper(F("cooking_time"), output_field=DurationField())))

            cooking_time = timedelta(
                minutes=all_foods_amount, seconds=15*all_foods_amount)
            if all_cooking_time['total_cooking_time']:
                cooking_time += all_cooking_time['total_cooking_time']

            # Find nearest branch
            p1 = (latitude, longitude)
            nearest_branch = None
            nearest_distance = None
            for branch in Branch.objects.all():
                p2 = (branch.latitude, branch.longitude)
                distance = geodesic(p1, p2).kilometers
                if nearest_branch is None or distance < nearest_distance:
                    nearest_branch = branch
                    nearest_distance = distance

            # nearest_branch = Branch.objects.annotate(
            #                                     distance=geodesic(p1, (F('latitude'), F('longitude'))).km
            #                                 ).order_by('distance').first()

            # Calculate delivery time based on distance to nearest branch
            delivery_time = timedelta(minutes=3 * nearest_distance)

            # Create the order
            order = Order.objects.create(
                client=self.context['request'].user,
                payment_type=payment_type,
                longitude=longitude,
                latitude=latitude,
                branch=nearest_branch,
                total_price=total_price,
                cooking_time=cooking_time,
                delivery_time=delivery_time
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
        fields = ('id', 'client', 'total_price', 'payment_type', 'state',
                  'branch', 'delivery_time', 'cooking_time', 'cancelled', 'items',)
        read_only_fields = fields


class OrderUpdateWaiterSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'state',  'cancelled',)


class OrderUpdateClientSerializer(ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'payment_type', 'longitude',
                  'latitude', 'items', 'cancelled',)

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
