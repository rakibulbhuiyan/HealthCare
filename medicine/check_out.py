from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views import View
from .models import Address, Checkout, CartItem
from .serializers import AddressSerializer, CheckoutSerializer


# @method_decorator(login_required, name='dispatch') 
class CheckoutView(APIView):
    def get(self, request, *args, **kwargs):
        # Get user cart
        try:
            cart_items = CartItem.objects.filter(user=request.user)
            if not cart_items.exists():
                return Response({"error": "Cart is empty"}, status=status.HTTP_404_NOT_FOUND)
            
            cart_data = [
                {"id": item.id, "medicine": item.medicine.name, "quantity": item.quantity} 
                for item in cart_items
            ]
            return Response({"cart": cart_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class AddressView(APIView):
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users

    def get(self, request):
        addresses = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Associate the address with the logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)