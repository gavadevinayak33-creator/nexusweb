from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt

from .models import Booking, Payment

import random
import razorpay


# ---------------- HOME ----------------
def Home_page(request):
    return render(request, 'website/Home.html')


# ---------------- CONTACT + OTP FLOW ----------------
def Conatact_page(request):

    if request.method == "POST":

        # 👉 STEP 1: SEND OTP
        if 'send_otp' in request.POST:

            email = request.POST.get('email')
            otp = str(random.randint(1000, 9999))

            request.session['otp'] = otp
            request.session['email'] = email

            send_mail(
                subject='Your OTP Code',
                message=f'Your OTP is {otp}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

            return render(request, 'website/Conatact.html', {'otp_sent': True})


        # 👉 STEP 2: VERIFY OTP
        elif 'verify_otp' in request.POST:

            user_otp = request.POST.get('otp')
            session_otp = request.session.get('otp')

            if user_otp == session_otp:
                request.session['verified'] = True
                return render(request, 'website/Conatact.html', {'verified': True})

            else:
                return render(request, 'website/Conatact.html', {
                    'otp_sent': True,
                    'error': 'Wrong OTP'
                })


        # 👉 STEP 3: FINAL SUBMIT → BOOKING + PAYMENT REDIRECT
        elif 'final_submit' in request.POST:

            if request.session.get('verified'):

                booking = Booking.objects.create(
                    name=request.POST.get('name'),
                    email=request.session.get('email'),
                    phone=request.POST.get('phone'),
                    city=request.POST.get('city')
                )

                request.session.flush()

                # 🔥 IMPORTANT CHANGE
                return redirect('create_payment', booking_id=booking.id)

    return render(request, 'website/Conatact.html')


# ---------------- DASHBOARD ----------------
def dashboard(request):

    total_bookings = Booking.objects.count()
    city_data = Booking.objects.values('city').annotate(total=Count('city'))
    latest_bookings = Booking.objects.all().order_by('-id')[:5]
    all_bookings = Booking.objects.all().order_by('-id')

    context = {
        'total_bookings': total_bookings,
        'city_data': city_data,
        'latest_bookings': latest_bookings,
        'all_bookings': all_bookings,
    }

    return render(request, 'website/dashboard.html', context)


# ---------------- PAYMENT CREATE ----------------
def create_payment(request, booking_id):

    booking = Booking.objects.get(id=booking_id)

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    amount = 500 * 100  # ₹500

    payment = Payment.objects.create(
        booking=booking,
        amount=500,
        status="Pending"
    )

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    payment.order_id = order['id']
    payment.save()

    context = {
        "payment": payment,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": amount,
    }

    return render(request, "website/payment.html", context)


# ---------------- PAYMENT SUCCESS ----------------
@csrf_exempt
def payment_success(request):

    if request.method == "POST":

        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')

        try:
            payment = Payment.objects.get(order_id=order_id)

            payment.payment_id = payment_id
            payment.status = "Success"
            payment.save()

        except Payment.DoesNotExist:
            pass

        return redirect('Home_page')