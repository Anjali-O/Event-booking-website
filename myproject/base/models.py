from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    pcategory = models.CharField(max_length=100)
    venue = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    event_date = models.DateTimeField()
    total_seats = models.IntegerField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title


class CartModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"


class BookingModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    seat_numbers = models.JSONField()
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"




















# from django.db import models

# # Create your models here.
# from django.contrib.auth.models import User

# class Event(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     pcategory =models.CharField(max_length=100)
#     venue = models.CharField(max_length=200)
#     location = models.CharField(max_length=200)
#     event_date = models.DateTimeField()
#     total_seats = models.IntegerField()
#     ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
#     # image = models.ImageField(upload_to='event_images/', blank=True, null=True)

#     def __str__(self):
#         return self.title


# class CartModel(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     venue = models.CharField(max_length=200)
#     event_date = models.DateTimeField()
#     total_seats = models.IntegerField()
#     ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
#     totalprice=models.IntegerField()
#     quantity=models.IntegerField()
#     host=models.ForeignKey(User,on_delete=models.CASCADE)


# class BookingModel(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     venue = models.CharField(max_length=200)
#     event_date = models.DateTimeField()
#     ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
#     seat_numbers = models.JSONField()
#     totalprice=models.IntegerField()
#     quantity=models.IntegerField()
#     host=models.ForeignKey(User,on_delete=models.CASCADE)




   