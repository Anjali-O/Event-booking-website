from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    # path('event/',event,name='event'),
    # path('bookings/',bookings,name='bookings'),
    path('contact/',contact,name='contact'),
    path('book/<int:pk>',book,name='book'),
    # path('location/<str:city>/', events_by_location, name='events_by_location'),
    path('addtocart/<int:pk>',addtocart,name='addtocart'),
    path('cart/',cart,name='cart'),
    path('csub/<int:pk>',csub,name='csub'),
    path('cadd/<int:pk>',cadd,name='cadd'),
    path('remove/<int:pk>',remove,name='remove'),
    path('payment/',payment,name='payment'),
    path('paysuccess/',paysuccess,name='paysuccess'),
    path('booked/',booked,name='booked'),
    path('aboutus/',aboutus,name='aboutus'),

]
