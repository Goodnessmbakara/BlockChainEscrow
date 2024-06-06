
from rest_framework import serializers
from .models import Invoice, InvoiceItem, Order
from user_auth.models import CustomUser

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'invoice', 'importer', 'exporter', 'order_status', 'created_at', 'delivery_date', 'total')

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ('id', 'product_name', 'quantity', 'price', 'total')

class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = ('id', 'invoiceID', 'created_at', 'creator', 'sent_to', 'amount', 'issued_at', 'current_status', 'items', 'total')

    def get_total(self, obj):
        items = obj.items.all()
        total = sum(item.total for item in items)
        return total

    def create(self, validated_data):
        items_data = self.context.get('view').request.data.get('items')
        invoice = Invoice.objects.create(**validated_data)

        for item_data in items_data:
            quantity = item_data.get('quantity')
            price = item_data.get('price')
            total = quantity * price
            InvoiceItem.objects.create(
                invoice=invoice,
                product_name=item_data.get('product_name'),
                quantity=quantity,
                price=price,
                total=total
            )

        importer_email = self.context.get('view').request.data.get('importer_email')
        if importer_email:
            try:
                user = CustomUser.objects.get(email=importer_email)
                invoice.sent_to = user
                invoice.save()
            except CustomUser.DoesNotExist:
                pass

        return invoice