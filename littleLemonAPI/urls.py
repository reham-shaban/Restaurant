from django.urls import path

from . import views

menu_item_list = views.MenuItemViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

menu_item_detail = views.MenuItemViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

# 'api/'
urlpatterns = [
    path('menu-items', menu_item_list),
    path('menu-items/<int:pk>', menu_item_detail),
    
    path('groups/manager/users', views.ManagerView.as_view()),    
    path('groups/manager/users/<int:userId>', views.ManagerRemoveView.as_view()),    
    path('groups/delivery-crew/users', views.DeliveryView.as_view()),
    path('groups/delivery-crew/users/<int:userId>', views.DeliveryRemoveView.as_view()),
    
    path('cart/menu-items', views.CartView.as_view()),
    path('orders', views.OrderView.as_view()),
    path('orders/<int:pk>', views.SingleOrderView.as_view()),
]