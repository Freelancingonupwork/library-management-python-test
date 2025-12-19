from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods

from .api.serializers import PublicMemberRegistrationSerializer


@require_http_methods(["GET", "POST"])
def login_view(request):
    """HTML login page view"""
    # Allow access even if logged in (user can switch accounts)
    # if request.user.is_authenticated:
    #     return redirect('/library/books/')  # Redirect to books page if already logged in
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if not username or not password:
            return render(request, "accounts/login.html", {
                "error": "Username and password are required."
            })
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get("next", "/library/books/")
            return redirect(next_url)
        else:
            return render(request, "accounts/login.html", {
                "error": "Invalid username or password. Please try again."
            })
    
    return render(request, "accounts/login.html")


@require_http_methods(["GET", "POST"])
def register_view(request):
    """HTML registration page view"""
    # Allow access even if logged in (user can register another account)
    # if request.user.is_authenticated:
    #     return redirect('/library/books/')  # Redirect if already logged in
    
    if request.method == "POST":
        # Get form data
        data = {
            "username": request.POST.get("username"),
            "email": request.POST.get("email"),
            "password": request.POST.get("password"),
            "password_confirm": request.POST.get("password_confirm"),
            "first_name": request.POST.get("first_name", ""),
            "last_name": request.POST.get("last_name", ""),
        }
        
        # Validate using serializer
        serializer = PublicMemberRegistrationSerializer(data=data)
        
        if serializer.is_valid():
            try:
                member = serializer.save()
                messages.success(
                    request, 
                    f"Account created successfully! Welcome, {member.user.username}. Please login."
                )
                return redirect("account-login")
            except Exception as e:
                return render(request, "accounts/register.html", {
                    "error": f"Registration failed: {str(e)}",
                    "form": serializer
                })
        else:
            # Extract field-specific errors for display
            errors = {}
            for field, field_errors in serializer.errors.items():
                if isinstance(field_errors, list):
                    errors[field] = field_errors[0] if field_errors else ""
                else:
                    errors[field] = str(field_errors)
            
            return render(request, "accounts/register.html", {
                "form": serializer,
                "form_errors": errors,
                "error": "Please correct the errors below."
            })
    
    # GET request - show empty form
    return render(request, "accounts/register.html", {
        "form": PublicMemberRegistrationSerializer(),
        "form_errors": {}
    })


@require_http_methods(["GET", "POST"])
def logout_view(request):
    """HTML logout page view"""
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been successfully logged out.")
    return redirect("account-login")

