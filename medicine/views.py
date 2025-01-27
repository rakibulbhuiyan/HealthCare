from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.views import APIView
from .models import CartItem,Category,Medicine,Subcategory,DietCategory
from .serializers import (CategorySerializer,CategoryCreateSerializer, SubCategorySerializer, MedicineSerializer,
                    SubcategoryCreateSerializer, CartItemSerializer, CartItemCreateSerializer, DietCategorySerializer)
from .nagad_payment import NagadPayment
from .bkash_payment import BkashPayment

# Create your views here.

class CategoryListView(APIView):

    def get(self,request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = CategoryCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,pk):
        try:
            categories = Category.objects.get(pk=pk)
        except categories.DoesNotExist:
            return Response({'errors':'Category not dound'},status=status.HTTP_400_BAD_REQUEST)
        
        serializer=CategorySerializer(categories,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,pk):
        try:
            categories = Category.objects.get(pk=pk)
        except categories.DoesNotExist:
            return Response({'errors':'Category not dound'},status=status.HTTP_400_BAD_REQUEST)
        
        serializer=CategorySerializer(categories,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            categories = Category.objects.get(pk=pk)
            categories.delete()
            return Response({"message": "Category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

         
class SubCategoryListView(APIView):

    def get(self, request, category_id):
        subcategories = Subcategory.objects.filter(category_id=category_id)
        serializer = SubCategorySerializer(subcategories, many=True)
        return Response(serializer.data)
    
    def post(self, request, category_id):
        data = request.data.copy()
        data['category'] = category_id  # Here Dynamically assign category_ID
        serializer = SubcategoryCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,sub_category_id,pk):
        try:
            subcategory = Subcategory.objects.get(category_id=category_id, pk=pk)
        except subcategory.DoesNotExist:
            return Response({'errors':'SubCategory not dound'},status=status.HTTP_400_BAD_REQUEST)
        
        serializer=SubCategorySerializer(subcategory,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,sub_category_id,pk):
        try:
            subcategory = Subcategory.objects.get(category_id=category_id, pk=pk)
        except subcategory.DoesNotExist:
            return Response({'errors':'SubCategory not dound'},status=status.HTTP_400_BAD_REQUEST)
        
        serializer=SubCategorySerializer(subcategory,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, category_id, pk):
        # Delete a subcategory
        try:
            subcategory = Subcategory.objects.get(category_id=category_id, pk=pk)
            subcategory.delete()
            return Response({"message": "Subcategory deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Subcategory.DoesNotExist:
            return Response({'error': 'Subcategory not found'}, status=status.HTTP_404_NOT_FOUND)
        

class MedicineListView(APIView):

    def get(self, request, sub_category_id):
        medicines = Medicine.objects.filter(sub_category_id=sub_category_id) 
        serializer = MedicineSerializer(medicines, many=True)
        return Response(serializer.data)
    # for Create category data
    def post(self,request,sub_category_id):
        # Dynamically assign sub_category_id to the request data
        data=request.data.copy()
        data['sub_category']=sub_category_id
        serializer = MedicineSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Update for full data
    def put(self,request,sub_category_id,pk):
        try:
            medicines = Medicine.objects.get(pk=pk,sub_category_id=sub_category_id)
        except medicines.DoesNotExist:
            return Response({'errors':'Medicine not dound'},status=status.HTTP_400_BAD_REQUEST)
        
        serializer=MedicineSerializer(medicines,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #partial update
    def patch(self,request,sub_category_id,pk):
        try:
            medicine = Medicine.objects.get(pk=pk, sub_category_id=sub_category_id)
        except Medicine.DoesNotExist:
            return Response({'error': 'Medicine not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MedicineSerializer(medicine, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete category data
    def delete(self,request,sub_category_id,pk):
        try:
            medicine = Medicine.objects.get(pk=pk, sub_category_id=sub_category_id)
            medicine.delete()
            return Response({"message": "Medicine deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Medicine.DoesNotExist:
            return Response({'error': 'Medicine not found'}, status=status.HTTP_404_NOT_FOUND)




class MedicneSearchView(APIView):
    
    def get(self,request):
        query = request.query_params.get('q',None)
        medicines = Medicine.objects.all()

        # search medicine name and description here
        if query:
            medicines = medicines.filter(Q(name__icontains=query) | Q(description__icontains=query))
        
        serializer = MedicineSerializer(medicines,many=True)
        return Response(serializer.data)


class CartView(APIView):
    def get(self, request):
        cart_items = CartItem.objects.all()  
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data) 
    
    def post(self,request):
        serializer = CartItemCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,pk):
        try:
            cart_item = CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer=CartItemSerializer(cart_item,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK, partial=True)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,pk):
        try:
            cart_item = CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer=CartItemSerializer(cart_item,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk):
        try:
            cart_item = CartItem.objects.get(pk=pk)
            cart_item.delete()
            return Response({"message": "Item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

#   Nagad Payment Views

class InitializePaymentView(APIView):
    def post(self, request):
        order_id = request.data.get('order_id')
        if not order_id:
            return Response({"error": "Order ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        nagad = NagadPayment()
        response = nagad.initialize_checkout(order_id)
        return Response(response, status=status.HTTP_200_OK)

class CompletePaymentView(APIView):
    def get(self, request, payment_reference_id):
        nagad = NagadPayment()
        response = nagad.complete_checkout(payment_reference_id)
        return Response(response, status=status.HTTP_200_OK)

class VerifyPaymentView(APIView):
    def get(self, request, payment_reference_id):
        nagad = NagadPayment()
        response = nagad.verify_payment(payment_reference_id)
        return Response(response, status=status.HTTP_200_OK)

# Bkash Payment View

class Bkash_InitializePaymentView(APIView):
    def post(self,request):
        amount = request.data.get('amount')
        invoice_number = request.data.get('invoice_number')
        if not amount or not invoice_number:
            return Response({"error": "Amount and Invoice Number are required"}, status=status.HTTP_400_BAD_REQUEST)

        bkash = BkashPayment()
        response = bkash.initialize_checkout(amount, invoice_number)
        return Response(response, status=status.HTTP_200_OK)


class Bkash_ExecutePaymentView(APIView):
    def get(self,request, payment_id):
        bkash = BkashPayment()
        response = bkash.execute_payment(payment_id)
        return Response(response, status = status.HTTP_200_OK)

class Bkash_VerifyPaymentView(APIView):
    def get(self, request, payment_id):
        bkash = BkashPayment()
        response = bkash.verify_payment(payment_id)
        return Response(response, status=status.HTTP_200_OK)




class DietCategoryView(APIView):
    
    def get(self,request,pk=None):
        if pk:  # Retrieve a single category
            try:
                category = DietCategory.objects.prefetch_related('plans').get(pk=pk)
                serializer = DietCategorySerializer(category)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except DietCategory.DoesNotExist:
                return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        else:  # Retrieve all categories
            categories = DietCategory.objects.prefetch_related('plans').all()
            serializer = DietCategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        serializer = DietCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,pk):
        try:
            category = DietCategory.objects.get(pk=pk)
            serializer = DietCategorySerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except DietCategory.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):  
        try:
            category = DietCategory.objects.get(pk=pk)
            category.delete()
            return Response({"message": "Category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except DietCategory.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)


class DietPlanView(APIView):
    def get(self, request, pk=None):
        if pk:  # Retrieve a single diet plan
            try:
                plan = DietPlan.objects.get(pk=pk)
                serializer = DietPlanSerializer(plan)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except DietPlan.DoesNotExist:
                return Response({"error": "Plan not found"}, status=status.HTTP_404_NOT_FOUND)
        else:  # Retrieve all diet plans
            plans = DietPlan.objects.all()
            serializer = DietPlanSerializer(plans, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request): 
        serializer = DietPlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):  # Update diet plan
        try:
            plan = DietPlan.objects.get(pk=pk)
            serializer = DietPlanSerializer(plan, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except DietPlan.DoesNotExist:
            return Response({"error": "Plan not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            plan = DietPlan.objects.get(pk=pk)
            plan.delete()
            return Response({"message": "Plan deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except DietPlan.DoesNotExist:
            return Response({"error": "Plan not found"}, status=status.HTTP_404_NOT_FOUND)

