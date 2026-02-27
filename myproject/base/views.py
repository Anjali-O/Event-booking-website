from django.shortcuts import render, redirect
from .models import Event, CartModel, BookingModel
from django.utils import timezone
from django.db.models import Q, Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import transaction


# -------------------- HOME --------------------

def home(request):

    if request.user.is_authenticated:
        cartproducts_count = CartModel.objects.filter(user=request.user).count()
    else:
        cartproducts_count = 0

    events = Event.objects.filter(event_date__gte=timezone.now())

    nomatch = False

    if 'q' in request.GET:
        q = request.GET['q']
        events = events.filter(Q(title__icontains=q) | Q(location__icontains=q))
        if not events.exists():
            nomatch = True

    elif 'cat' in request.GET:
        cat = request.GET['cat']
        events = events.filter(pcategory=cat)

    category = Event.objects.values_list('pcategory', flat=True).distinct()
    return render(request, 'home.html', {'events': events,'category': category,'nomatch': nomatch,'cartproducts_count': cartproducts_count})


# -------------------- CONTACT --------------------

def contact(request):

    if request.user.is_authenticated:
        cartproducts_count = CartModel.objects.filter(user=request.user).count()
    else:
        cartproducts_count = 0

    return render(request, 'contact.html', {
        'cartproducts_count': cartproducts_count
    })


# -------------------- BOOK PAGE --------------------

def book(request, pk):

    event = Event.objects.filter(id=pk, event_date__gte=timezone.now()).first()

    if not event:
        return redirect('home')

    if request.user.is_authenticated:
        cartproducts_count = CartModel.objects.filter(user=request.user).count()
    else:
        cartproducts_count = 0

    return render(request, 'book.html', {'data': event,'cartproducts_count': cartproducts_count})


# -------------------- ADD TO CART --------------------

# @login_required(login_url='login_')
def addtocart(request, pk):
    if request.user.is_authenticated:
        cartproducts_count=CartModel.objects.filter(user=request.user).count()

        event = Event.objects.get(id=pk)

        if event.total_seats <= 0:
            return render(request, 'book.html', {'noseats': True, 'data': event})

        try:
            cart_item = CartModel.objects.get(user=request.user, event=event)
            if event.total_seats >= cart_item.quantity + 1:
                cart_item.quantity += 1
                cart_item.total_price += event.ticket_price
                cart_item.save()
            else:
                return render(request, 'book.html', {'limit': True, 'data': event})
        except CartModel.DoesNotExist:
            CartModel.objects.create(
                user=request.user,
                event=event,
                quantity=1,
                total_price=event.ticket_price
            )
        else:
            return render(request,'book.html',{'status':True,'data':event,'cartproducts_count':cartproducts_count})
    
    else:
        return redirect('login2_',pk=pk)
    return redirect('cart')
    


# -------------------- CART --------------------

@login_required(login_url='login_')
def cart(request):

    cartproducts = CartModel.objects.filter(user=request.user)
    cartproducts_count = cartproducts.count()

    TA = cartproducts.aggregate(total=Sum('total_price'))['total'] or 0

    return render(request, 'cart.html', {'data': cartproducts,'TA': TA,'cartproducts_count': cartproducts_count})


# -------------------- CART ADD --------------------

@login_required(login_url='login_')
def cadd(request, pk):

    cart_item = CartModel.objects.get(id=pk, user=request.user)
    event = cart_item.event

    if event.total_seats >= cart_item.quantity + 1:
        cart_item.quantity += 1
        cart_item.total_price += event.ticket_price
        cart_item.save()
    else:
        messages.error(request, "No more seats available")

    return redirect('cart')


# -------------------- CART SUB --------------------

@login_required(login_url='login_')
def csub(request, pk):
    cart_item = CartModel.objects.get(id=pk, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.total_price -= cart_item.event.ticket_price
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


# -------------------- REMOVE ITEM --------------------

@login_required(login_url='login_')
def remove(request, pk):
    cart_item = CartModel.objects.get(id=pk, user=request.user)
    cart_item.delete()
    return redirect('cart')


# -------------------- PAYMENT --------------------

@login_required(login_url='login_')
def payment(request):

    cart_items = CartModel.objects.filter(user=request.user)
    if not cart_items.exists():
        return HttpResponse("Cart is empty")
    
    if request.method == "GET":
        for item in cart_items:
            event = item.event  # event linked via ForeignKey
            if event.total_seats < item.quantity:
                return HttpResponse(
                    f"Sorry, only {event.total_seats} seats available for {event.title}"
                )
        return render(request, "payment.html")
    
    elif request.method == "POST":
        upi = request.POST.get("upi")
        if not upi:
            return HttpResponse("Enter UPI ID")
        
        with transaction.atomic():
            for item in cart_items:
                event = Event.objects.select_for_update().get(id=item.event.id)
                if event.total_seats < item.quantity:
                    return HttpResponse(
                        f"Sorry, only {event.total_seats} seats available for {event.title}"
                    )

                booked_count = BookingModel.objects.filter(event=event).aggregate(total=Sum('quantity'))['total'] or 0
                start_seat = booked_count + 1
                seat_numbers = list(range(start_seat, start_seat + item.quantity))

                BookingModel.objects.create(
                    user=request.user,
                    event=event,
                    quantity=item.quantity,
                    total_price=item.total_price,
                    seat_numbers=seat_numbers
                )

                event.total_seats -= item.quantity
                event.save()

            cart_items.delete()

        return render(request, "paysuccess.html")


# -------------------- PAY SUCCESS --------------------

def paysuccess(request):
    return render(request, 'paysuccess.html')


# -------------------- BOOKINGS --------------------

@login_required(login_url='login_')
def booked(request):
    cartproducts_count = CartModel.objects.filter(user=request.user).count()
    bookings = BookingModel.objects.filter(user=request.user,event__event_date__gte=timezone.now())
    return render(request, 'booked.html', {'data': bookings,'cartproducts_count': cartproducts_count})


# -------------------- ABOUT --------------------

def aboutus(request):

    if request.user.is_authenticated:
        cartproducts_count = CartModel.objects.filter(user=request.user).count()
    else:
        cartproducts_count = 0
    return render(request, 'aboutus.html', {
        'cartproducts_count': cartproducts_count
    })

















