from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate

from .forms import RegisterForm
from .models import Customer


def home(request):
    return render(request, "home.html")


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("dashboard")

        return render(
            request,
            "login.html",
            {"error": "Invalid username or password."}
        )

    return render(request, "login.html")


def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.set_password(
                form.cleaned_data["password"]
            )

            user.save()

            Customer.objects.create(
                user=user,
                phone=form.cleaned_data["phone"],
                address=form.cleaned_data["address"],
                aadhaar=form.cleaned_data["aadhaar"]
            )

            return redirect("login")

    else:

        form = RegisterForm()

    return render(
        request,
        "register.html",
        {"form": form}
    )


def logout_view(request):

    logout(request)

    return redirect("login")