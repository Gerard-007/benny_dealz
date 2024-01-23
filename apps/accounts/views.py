import random
import re
from datetime import timedelta

from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import generic
from django.views.generic.base import View
from validate_email import validate_email
from apps.accounts.models import User, OTP
from apps.common.views import convert_to_true_or_false_v2, EmailThreading
from apps.dealers.models import Dealer


class RegistrationView(View):
    def get(self, request):
        return render(request, 'accounts/signup.html')

    def post(self, request):
        # get user data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # validate data
        if (
            not User.objects.filter(username=username).exists()
            and not User.objects.filter(email=email).exists()
        ):
            if password == password2:
                if len(password) < 6:
                    return JsonResponse({
                        "status": "warning",
                        "message": "password is too short"
                    })
                # ========== Send OTP to user and activate user status & Send activation email to user ============
                otp = random.randint(000000, 999999)
                print(f"OTP: {otp}")

                # Calculate the expiration date
                current_time = timezone.now()
                expiration_date = current_time + timedelta(hours=24)

                # Create a new token record associated with the user email
                otp, created = OTP.objects.update_or_create(
                    email=email,
                    defaults={'token': otp, 'expiration_date': expiration_date}
                )
                message = "Do not disclose this pin to anyone copy the code below to confirm your registration"
                email_template = render_to_string(
                    'accounts/activation_email.html',
                    {
                        'user': username,
                        'otp': otp.token,
                        'message': message
                    }
                )
                email_message = EmailMultiAlternatives(
                    subject='Benny Dealz Account Activations',
                    body='Activate your Benny Dealz Account',
                    from_email=settings.SUPPORT_EMAIL,
                    to=[email],
                )
                email_message.attach_alternative(email_template, "text/html")
                EmailThreading(email_message).start()
                return JsonResponse({
                    "status": "success",
                    "message": "An OTP was sent to your email copy the pin & paste to activate your account."
                })
            # messages.error(request, "Passwords does not match please check!")
            return JsonResponse({
                "status": "warning",
                "message": "Passwords does not match please check!"
            })
        return render(request, 'accounts/signup.html')


class ActivateAccountView(View):

    def post(self, request):
        # get user data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # dealer_reg = convert_to_true_or_false_v2(request, "dealerReg")

        # get OTP from frontend
        otp_val = request.POST.get("otp")

        # Retrieve the token
        otp = OTP.objects.get(email=email)

        if str(otp_val) == str(otp.token):
            user = User.objects.create_user(
                username=username,
                email=email,
                password=make_password(password)
            )
            user.set_password(password)
            user.is_active = True
            user.save()

            # if dealer_reg or not hasattr(user, 'user_dealer'):
            #     dealer = Dealer.objects.create(
            #         user=user,
            #         business_name=request.POST.get('business_name'),
            #         business_email=request.POST.get('business_email'),
            #         business_phone=request.POST.get('business_phone')
            #     )
            #     dealer.save()
            #     # Update user instance after saving the Dealer instance
            #     user.is_a_dealer = True
            #     user.save()

            # ============== send success message to user =============
            auth.login(request, auth.authenticate(
                email=email,
                password=password,
            ))
            # Delete the used otp
            otp.delete()

            return JsonResponse({
                "status": "success",
                "message": "Account created and login successful!, please update your credentials",
                "user_slug": user.profile.slug
            })

        return JsonResponse({
            "status": "error",
            "message": "OTP error didn't match"
        })


class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get('password')

        if email and password:
            try:
                if user := auth.authenticate(email=email, password=password):
                    # Login in users if user account is active...
                    if user.is_active:
                        auth.login(request, user)
                        return JsonResponse({
                            "status": "success",
                            "message": f"Welcome, {user.username} login was successful..."
                        })
                    return JsonResponse({
                        "status": "error",
                        "message": "Account is not active,please check your email"
                    })
            except AttributeError or ValueError or Exception:
                return JsonResponse({
                    "status": "error",
                    "message": "Invalid credentials, try again!!!."
                })
            return JsonResponse({
                "status": "warning",
                "message": "Invalid credentials, try again!!!."
            })
        return JsonResponse({
            "status": "error",
            "message": "Please fill all fields"
        })


class LogoutView(generic.RedirectView):
    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully Logged out.")
        return super(LogoutView, self).get(request, *args, **kwargs)


class PasswordResetView(View):
    def get(self, request):
        return render(request, "accounts/reset-password.html")

    def post(self, request):
        email = request.POST['email']

        context = {
            'values': request.POST
        }

        if not validate_email(email):
            messages.error(request, "please supply a valid email")
            return render(request, 'accounts/reset-password.html', context)

        # -> getting Domain we are on...
        current_site = get_current_site(request).domain
        user = User.objects.filter(email=email)

        if user.exists():
            uid = urlsafe_base64_encode(force_bytes(user[0].pk))
            token = PasswordResetTokenGenerator().make_token(user[0])
            link = reverse('accounts:reset-user-password', kwargs={'uidb64': uid, 'token': token})
            message = "reset your password"
            # ========== Send activation email to user ============
            email_template = render_to_string('accounts/account_activation_email.html',
                                              {'user': user[0].username, 'domain': current_site, 'link': link,
                                               'message': message})
            send_mail = EmailMessage(
                'Reset your AdieuLane account password',
                email_template,
                settings.SUPPORT_EMAIL,
                [email],
            )
            send_mail.fail_silently = True
            send_mail.send()
            messages.success(request, "We have sent a password reset link to your email")
            return render(request, 'accounts/reset-password.html', context)
        messages.info(request, "Email does not exist")
        return render(request, 'accounts/reset-password.html', context)


class CompletePasswordResetView(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user):
                messages.info(request, "Password link is invalid, please request for a new password")
                return render(request, 'accounts/reset-password.html', context)
        except Exception as ex:
            print(ex)
            return render(request, 'accounts/set-new-password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, "Password do not match.")
            return render(request, 'accounts/set-new-password.html', context)
        if len(password) < 6:
            messages.error(request, "Password is too short.")
            return render(request, 'accounts/set-new-password.html', context)

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successfully, you can login with your new password")
            return redirect('accounts:login')
        except Exception as ex:
            messages.info(request, "Something was wrong...")
            return render(request, 'accounts/set-new-password.html', context)
