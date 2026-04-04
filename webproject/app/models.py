from django.db import models

from django.db import models

# 🔹 Booking Model
class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    CITY_CHOICES = [
        ('Pune', 'Pune'),
        ('Ahmedabad', 'Ahmedabad'),
        ('Goa', 'Goa'),
        ('Bengaluru', 'Bengaluru'),
    ]

    city = models.CharField(max_length=50, choices=CITY_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# 🔹 Payment Model
class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

    amount = models.IntegerField()
    payment_id = models.CharField(max_length=200, blank=True, null=True)
    order_id = models.CharField(max_length=200, blank=True, null=True)

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Success', 'Success'),
        ('Failed', 'Failed'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking.name} - {self.status}"