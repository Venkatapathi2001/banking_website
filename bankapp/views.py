from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib import messages
import random
import string
from .models import Account,Transaction  # Assuming you have an Account model
from .models import reg_details
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
User = get_user_model()

# Login view
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('home')  # Redirect to the home page after login
        else:
            
            messages.error(request, 'Invalid login credentials!')
            return redirect('login')
    return render(request, 'login.html')

# Registration view
def reg(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if username or email already exists
        if reg_details.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('reg')
        if reg_details.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('reg')

        # Save into your custom table
        reg = reg_details.objects.create(
            username=username,
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=password,
        )
        reg.save()

        # Save into Django User model also
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = firstname
        user.last_name = lastname
        user.save()

        messages.success(request, "Your account has been successfully created.")
        return redirect('login')

    return render(request, 'reg.html')

# Home view after login
def home(request):
    account = None
    if hasattr(request.user, 'account'):
        account = request.user.account
    return render(request, 'home.html', {'account': account})
# Withdraw view
@login_required
def withdraw(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')

        try:
            amount = float(amount)
            if amount <= 0:
                messages.error(request, "Withdraw amount must be positive.")
                return redirect('withdraw')
        except ValueError:
            messages.error(request, "Invalid amount entered.")
            return redirect('withdraw')

        # Check if the user has an account
        if not hasattr(request.user, 'account'):
            messages.error(request, "Account not found. Please create an account first.")
            return redirect('create_account')

        account = request.user.account

        if account.balance < amount:
            messages.error(request, "Insufficient balance.")
            return redirect('withdraw')

        account.balance -= amount
        account.save()
        Transaction.objects.create(account=account, type='Withdraw', amount=amount)

        messages.success(request, f"${amount} successfully withdrawn.")
        return redirect('home')

    return render(request, 'withdraw.html')



@login_required
def deposit(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')

        try:
            amount = float(amount)
            if amount <= 0:
                messages.error(request, "Deposit amount must be positive.")
                return redirect('deposit')
        except ValueError:
            messages.error(request, "Invalid amount entered.")
            return redirect('deposit')

        # Check if user has an associated account
        if not hasattr(request.user, 'account'):
            messages.error(request, "Account not found. Please create an account first.")
            return redirect('create_account')

        # Deposit
        account = request.user.account
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, type='Deposit', amount=amount)

        messages.success(request, f"${amount} successfully deposited.")
        return redirect('home')

    return render(request, 'deposit.html')


# Check Balance view
def check_balance(request):
    context = {}
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        try:
            account = Account.objects.get(account_number=account_number)
            context['account'] = account
        except Account.DoesNotExist:
            messages.error(request, "Account not found.")
            return redirect('check_balance')
    return render(request, 'check_balance.html', context)


# Transaction History view
def transaction_history(request):
    # Check if the user has an account
    if not hasattr(request.user, 'account'):
        messages.error(request, "You don't have an account yet.")
        return redirect('create_account')

    account = request.user.account
    transactions = account.transactions.all().order_by('-date')  # Optional: newest first

    return render(request, 'transaction_history.html', {
        'transactions': transactions,
        'account_number': account.account_number
    })
def logout_view(request):
    logout(request)
    return render(request, 'logout.html')
@login_required
def create_account(request):
    if hasattr(request.user, 'account'):
        messages.info(request, "Account already exists.")
        return redirect('home')

    account_number = ''.join(random.choices(string.digits, k=10))

    account = Account.objects.create(
        user=request.user,
        account_number=account_number,
        balance=0.0
    )

    messages.success(request, f"Account created successfully! Account Number: {account_number}")
    return redirect('home')
