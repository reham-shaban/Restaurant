# Restaurant
This is an API project from Meta Back-End Developer course.

TODOs:
--------------
roles: managers, customers, delivery crew
registeration & authentication: /api/users/
assign to groups: /api/users/{userId}/groups
------------------------
Manager role:
*add, edit, delete menu-items : /api/menu-items/
*update user role: /api/users/{userId}/groups

*browse, assign orders to delivery person: 
/api/orders
/api/orders/{orderId}

*filter orders:
/api/orders?status=delivered
/api/orders?status=pending

Customer role:
*browse, pagination, filter, search menu-items
*add to cart: /api/users/{userId}/cart/menu-items
*place, view order: /api/orders
*flush cart: /api/users/{userId}/cart

The cart should be emptied when the ordere is made.

Delivery role:
*browse their orders: 
/api/orders
/api/orders/{orderId}
---------------------------

djoser for authentication
Throttling: 5 per minute
comment session class before submission