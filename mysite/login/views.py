import logging
import uuid
from django.contrib import auth
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from apiclient import errors
from smtplib import SMTPException
from .models import User
from mysite import const
from mysite import helper

logger = logging.getLogger(const.LOGGER_NAME)


def login(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    if not request.POST:
        return render(request, 'login.html', {'type': 'login'})

    username = request.POST.get('email', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username=username, password=password)
    has_user = User.objects.filter(username=username).count() > 0

    if not has_user:
        error_msg = "Don't have this account."
    elif user is None:
        error_msg = "Your password was incorrect."
    elif not user.verified:
        error_msg = "The account not verified yet."
    elif not user.is_active:
        error_msg = "The account has been disabled."
    else:
        auth.login(request, user)
        logger.info("User name: {username} login successful".format(username=username))
        return redirect(settings.LOGIN_REDIRECT_URL)

    messages.error(request, error_msg)

    return render(request, 'login.html', {'type': 'login'})


def signup(request):
    username = request.POST.get('email', '')
    password = request.POST.get('password', '')
    confirm_password = request.POST.get('confirm_password', '')

    has_user = User.objects.filter(username=username).count() > 0

    if has_user:
        error_msg = "Already had this account."
    elif password != confirm_password:
        error_msg = "Password not matching."
    else:
        try:

            verify_uuid = str(uuid.uuid4())
            verify_url = "{scheme}://{host}{verify_url}?verify_uuid={uuid}".format(
                scheme=request.scheme,
                host=request.get_host(),
                verify_url=settings.VERIFY_URL,
                uuid=verify_uuid
            )

            mail_content = settings.EMAIL_CONTEXT.format(
                verify_url=verify_url
            )
            gmail_service = helper.get_gmail_service()
            message = helper.create_message(
                sender=settings.EMAIL_HOST_USER,
                to=username,
                subject=settings.EMAIL_SUBJECT,
                msgplain=mail_content
            )
            helper.send_message_internal(
                service=gmail_service,
                user_id="me",
                message=message
            )

            messages.success(request, "Sent verify email success.")

            user = User.objects.create_user(
                username=username,
                email=username,
                password=password,
                verified=False,
                verify_uuid=verify_uuid
            )

            user.save()

        except (SMTPException, errors.HttpError) as err:
            logger.error("Username: {username}, Error: {err}".format(
                username=username,
                err=err
            ))
            messages.error(request, "Sent verify email fail.")

        return render(request, 'login.html', {'type': 'login'})

    messages.error(request, error_msg)

    return render(request, 'login.html', {'type': 'signup'})


def logout(request):
    auth.logout(request)
    return redirect(settings.LOGIN_REDIRECT_URL)


def verify(request):
    verify_uuid = request.GET.get('verify_uuid', '')
    user = User.objects.filter(verify_uuid=verify_uuid).first()

    if user.verified:
        return redirect(settings.LOGIN_URL)

    user.verified = True
    user.save()

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    auth.login(request, user)

    return redirect(settings.LOGIN_REDIRECT_URL)


def success(request):
    return render(request, 'success.html')
