from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('products/', views.product_list, name='product_list'),
    path('products/<str:category>/', views.product_list, name='product_list_by_category'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('feature/', views.feature, name='feature'),
    path('fashion/', views.fashion, name='fashion'),
    path('appliances/', views.appliances, name='appliances'),
    path('computer/' , views.computer, name='computer'),
    path('games/', views.games, name='games'),
    path('office/', views.office, name='office'),
    path('explore/', views.explore, name='explore'),
    path('phones/', views.phones, name='phones'),
    path('accessory/', views.accessory, name='accessory'),
    path('products/<int:product_id>/', views.product_details, name='product_details'),
    path('initiate_payment/' , views.initiate_payment, name='initiate_payment'),
    path('verify_payment/', views.verify_payment, name='verify_payment'),
    path('electronics/', views.electronics, name='electronics'),
    path('health/',views.health, name='health'),
    path('supermarket/', views.supermarket, name='supermarket')
    # path('login/', views.CustomLogin, name='login'),
    # path('logout/', views.CustomLogout, name='logout'),
    # ... other URLs ...
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('products/', views.product_list, name='product_list'),
#     path('products/<str:category>/', views.product_list, name='product_list'),
#     path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
#     path('cart/', views.cart_detail, name='cart_detail'),
# ]
