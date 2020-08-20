from django.urls import path

from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('itemdetails/<slug>', views.ItemDetailsView.as_view(), name='itemdetails'),
    path('item-list/<subid>', views.ItemListView.as_view(), name='item-list'),
    path('category-items/<catid>', views.CategoryItemView.as_view(), name='category-items'),
    path('add-to-cart/<slug>', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>', views.remove_from_cart, name='remove-from-cart'),
    path('remove-single-item-from-cart/<slug>', views.remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('add_to_cart_demo/', views.add_to_cart_demo, name='add_to_cart_demo'),
    path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('order-complete/', views.OrderCompleteView.as_view(), name='order-complete'),
    path('cattle-shop/', views.CattleshopView.as_view(), name='cattle-shop'),
    path('quick-view/<slug>', views.QuickView.as_view(), name='quick-view'),
    path('cart-item-view/', views.CartItemView.as_view(), name='cart-item-view'),
    path('get-cart-items/', views.get_cart_items, name='get-cart-items'),
    path('cart_demo/', views.cart_demo, name='cart_demo'),
    path('about_us/', views.about_us, name='about_us'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('place-order/', views.plcae_order, name='place-order'),
    path('delivery-status/', views.delivery_status, name='delivery-status'),
    path('user_login/', views.user_login, name='user_login'),
    path('monthly_shopping/', views.monthly_shopping, name='monthly_shopping'),
    path('place_monthly_order/', views.place_monthly_order, name='place_monthly_order'),
    path('monthly_order_invoice/<orderid>', views.monthly_order_invoice,name='order-monthly_order_invoice'),
]
