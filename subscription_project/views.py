from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from subscriptions.models import Subscription, Video
from django.utils.timezone import now
from datetime import timedelta

def home(request):
    videos = Video.objects.all()  # Includes banner images by default
    subscription_status = None

    if request.user.is_authenticated:
        try:
            subscription = Subscription.objects.get(user=request.user)
            subscription_status = subscription.is_approved
        except Subscription.DoesNotExist:
            subscription_status = None

    context = {
        'videos': videos,
        'subscription_status': subscription_status,
    }
    return render(request, "home.html", context)



@login_required
def video_view(request, video_id):
    try:
        subscription = Subscription.objects.get(user=request.user)
        if subscription.is_active():
            video = Video.objects.get(id=video_id)
            return render(request, 'video.html', {'video': video})  # Play video
        else:
            return redirect('buy_subscription')  # Redirect to subscription page
    except Subscription.DoesNotExist:
        return redirect('buy_subscription')  # Redirect to subscription page


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from subscriptions.models import Subscription, Video
from django.utils.timezone import now
from datetime import timedelta

@login_required
def buy_subscription(request):
    if request.method == "POST":
        payment_id = request.POST.get('payment_id')
        payment_screenshot = request.FILES.get('payment_screenshot')

        # Create or update the subscription
        Subscription.objects.update_or_create(
            user=request.user,
            defaults={
                'start_date': now(),
                'end_date': now() + timedelta(days=30),
                'payment_id': payment_id,
                'payment_screenshot': payment_screenshot,
                'is_approved': False,  # Admin approval pending
            }
        )
        messages.info(request, "Your payment is under review. Please wait for admin approval.")
        return redirect('home')
    return render(request, 'buy_subscription.html')




from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def user_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        messages.success(request, "Registration successful. Please login.")
        return redirect('login')

    return render(request, 'register.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login')

    return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')
