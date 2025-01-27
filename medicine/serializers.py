from rest_framework import serializers
from .models import  (Category, Subcategory, Medicine, CartItem, Address, Checkout,
                    DietPlan,DietCategory)

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Subcategory
        fields= ['id', 'name', 'description']


class SubcategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subcategory
        fields=['category', 'name', 'description']


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)
    class Meta:
        model=Category
        fields='__all__'


class CategoryCreateSerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)
    class Meta:
        model=Category
        fields=['id', 'name', 'description', 'subcategories']


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model=Medicine
        fields='__all__'


class CartItemSerializer(serializers.ModelSerializer):
    medicine=MedicineSerializer()
    class Meta:
        model=CartItem
        fields='__all__'


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['medicine', 'quantity']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = '__all__'
    
    def validate(self,data):
        calculated_total=(
            data['sub_total']
            + data['shipping_fee']
            - data['discount']
            - data['coupon_voucher']
            + data['tax']
        )
        if calculated_total != data['total']:
            raise serializers.ValidationError("Total does not match calculated total.")
        return data


class DietPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietPlan
        fields = ['id', 'file_or_image', 'diet_category']

class DietCategorySerializer(serializers.ModelSerializer):
    plans = DietPlanSerializer(many=True, read_only=True)

    class Meta:
        model = DietCategory
        fields = ['id', 'name', 'description', 'image', 'plans']