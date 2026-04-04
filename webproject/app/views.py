from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import Booking
from django.conf import settings

import random

from django.shortcuts import render
from .models import Booking
from django.db.models import Count

# ---------------- HOME ----------------
def Home_page(request):
    return render(request, 'website/Home.html')


# ---------------- CONTACT + OTP FLOW ----------------
def Conatact_page(request):

    if request.method == "POST":

        # 👉 STEP 1: SEND OTP (ONLY EMAIL)
        if 'send_otp' in request.POST:

            email = request.POST.get('email')

            otp = str(random.randint(1000, 9999))

            # session store
            request.session['otp'] = otp
            request.session['email'] = email

            # EMAIL SEND
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


        # 👉 STEP 3: FINAL SUBMIT (NOW NAME COMES HERE)
        elif 'final_submit' in request.POST:

            if request.session.get('verified'):

                Booking.objects.create(
                    name=request.POST.get('name'),   # 👈 NOW FROM FORM
                    email=request.session.get('email'),
                    phone=request.POST.get('phone'),
                    city=request.POST.get('city')
                )

                request.session.flush()
                return redirect('Home_page')

    return render(request, 'website/Conatact.html')


# ---------------- PAYMENT ----------------
# def pay(request):
#     client = razorpay.Client(auth=("YOUR_KEY", "YOUR_SECRET"))

#     payment = client.order.create({
#         "amount": 50000,
#         "currency": "INR",
#         "payment_capture": "1"
#     })

#     return render(request, "website/pay.html", {"payment": payment})




# --------------------------------DASHBOARD----------------------------------------------------------------------




def dashboard(request):

    # 👉 Total bookings
    total_bookings = Booking.objects.count()

    # 👉 City wise count
    city_data = Booking.objects.values('city').annotate(total=Count('city'))

    # 👉 Latest bookings (last 5)
    latest_bookings = Booking.objects.all().order_by('-id')[:5]

    # 👉 All bookings (table)
    all_bookings = Booking.objects.all().order_by('-id')

    context = {
        'total_bookings': total_bookings,
        'city_data': city_data,
        'latest_bookings': latest_bookings,
        'all_bookings': all_bookings,
    }

    return render(request, 'website/dashboard.html', context)