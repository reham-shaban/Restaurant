from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group, User
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission

from .models import MenuItem, Order, OrderItem, Cart
from .serializers import MenuItemSerializer, UserSerializer, OrderSerializer, CartSerializer

# Create your views here.

# permissions
class ManagerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Manager').exists()
   
      
# Manger views   
class ManagerView(APIView):
    serializer_class = UserSerializer
    permission_classes = [ManagerPermission]
    
    def get(self, request, *args, **kwargs):
        queryset = User.objects.filter(groups__name='Manager')
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data) 
        username = serializer.initial_data.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': f'User "{username}" does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        group = Group.objects.get(name='Manager')
        group.user_set.add(user)     
        return Response({'message': f'{user} added to Manager group successfully'}, status=status.HTTP_200_OK)
       
class ManagerRemoveView(APIView):
    def delete(self, request, userId):
        user = get_object_or_404(User, pk=userId)
        group = Group.objects.get(name='Manager')
        group.user_set.remove(user)
        return Response({'message' : f'{user} removed from Manager group succefully'}, status=status.HTTP_200_OK)  
      
        
# Delivery views
class DeliveryView(APIView):
    serializer_class = UserSerializer
    permission_classes = [ManagerPermission]
    
    def get(self, request, *args, **kwargs):
        queryset = User.objects.filter(groups__name='Delivery crew')
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data) 
        username = serializer.initial_data.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': f'User "{username}" does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        group = Group.objects.get(name='Delivery crew')
        group.user_set.add(user)     
        return Response({'message': f'{user} added to Delivery crew group successfully'}, status=status.HTTP_200_OK)
       
class DeliveryRemoveView(APIView):
    def delete(self, request, userId):
        user = get_object_or_404(User, pk=userId)
        group = Group.objects.get(name='Delivery crew')
        group.user_set.remove(user)
        return Response({'message' : f'{user} removed from Delivery crew group succefully'}, status=status.HTTP_200_OK)  
  
           
# Menu views
class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'category']
    filterset_fields = ['price', 'featured']
    search_fields = ['title', 'category__title']
    
    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [ManagerPermission]
        return [permission() for permission in permission_classes]


# Cart views
class CartView(APIView):
    def get(self, request):
        queryset = Cart.objects.filter(user=self.request.user)
        serializer = CartSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        request.data['user'] = self.request.user.id
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        queryset = Cart.objects.filter(user=self.request.user)
        queryset.delete()
        return Response({"message": "cart flushed"}, status=status.HTTP_400_BAD_REQUEST)


# Order views
class OrderView(APIView):
    def get(self, request):
        user = self.request.user
        # filtering based on user role
        if user.groups.filter(name='Manager').exists():
            queryset = Order.objects.all()
        elif user.groups.filter(name='Delivery crew').exists():
            queryset = Order.objects.filter(delivery_crew=user)
        else:
            queryset = Order.objects.filter(user=user)
        
        # filtering based on status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset.filter(status=status_filter)
            
        # serialize and return queryset
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # create an order of all the cart items of user
    def post(self, request):
        user = self.request.user
        cart_items = Cart.objects.filter(user=user)
        order = Order.objects.create(user=user, total=0)
        total_cart = 0
        
        # put each cart item as an order item
        for cart in cart_items:
            OrderItem.objects.create(
                order=order,
                menuitem=cart.menuitem, 
                quantity=cart.quantity,
                unit_price=cart.unit_price,
                price=cart.price
            )
            total_cart = total_cart + cart.price
            cart.delete()
            
        # update total price
        order.total = total_cart
        order.save()
        
        return Response({"message": "order created succesfully"}, status=status.HTTP_201_CREATED)
            
class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    
    def get_permissions(self):
        method = self.request.method
        if method == 'DELETE':
            permission_classes = [ManagerPermission]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        
        # filtering based on user role
        if user.groups.filter(name='Manager').exists():
            queryset = Order.objects.all()
        elif user.groups.filter(name='Delivery crew').exists():
            queryset = Order.objects.filter(delivery_crew=user)
        else:
            queryset = Order.objects.filter(user=user)
            
        return queryset

