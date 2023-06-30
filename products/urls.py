from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('admin-panel/', views.admin_login, name='admin_login'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('delete/<int:pk>/',views.product_delete,name='product_delete'),
    path('customer_view/', views.customer_view, name='customer_view'),
    path('add_to_cart/<int:pk>/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('remove_from_cart/<int:pk>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('add_product/', views.add_product, name='add_product'),
    path('product_list/', views.Product_List, name='Product_List'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/update/', views.product_update, name='product_update'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('customers/', views.customer_list_view, name='customer_list'),
    path('customer_product_list/', views.customer_product_list, name='customer_product_list'),
    path('remove_from_cart/<int:pk>/',views.remove_from_cart_view, name='remove_from_cart'),
    path('profile',views.profile,name='profile'),

]
