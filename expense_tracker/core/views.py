from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from decimal import Decimal
from datetime import datetime
from django.contrib.auth.decorators import login_required
import csv
from django.http import HttpResponse
def register(request):
    if request.method == 'POST':
        User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password'],
            email=request.POST['email'],
            full_name=request.POST['full_name'],
            currency=request.POST['currency']
        )
        return redirect('login')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)

    total = sum(e.amount for e in expenses)

    debts = ExpenseParticipant.objects.filter(user=request.user, status='pending')
    owed = sum(d.pending_amount for d in debts)

    to_receive = ExpenseParticipant.objects.filter(
        expense__user=request.user, status='pending'
    )
    receive_total = sum(x.pending_amount for x in to_receive)

    # highest category
    categories = {}
    for e in expenses:
        categories[e.category] = categories.get(e.category, 0) + float(e.amount)

    highest = max(categories, key=categories.get) if categories else "None"

    return render(request, 'dashboard.html', {
        'total': total,
        'owed': owed,
        'receive': receive_total,
        'debts': debts,
        'highest': highest
    })
@login_required
def add_expense(request):
    users = User.objects.exclude(id=request.user.id)

    if request.method == 'POST':
        amount = Decimal(request.POST['amount'])

        expense = Expense.objects.create(
            user=request.user,
            title=request.POST['title'],
            amount=amount,
            category=request.POST['category'],
            date=request.POST['date'],
            payment_mode=request.POST['payment_mode'],
            notes=request.POST.get('notes', ''),
            is_shared='is_shared' in request.POST
        )

        if expense.is_shared:
            selected_users = request.POST.getlist('participants')

            split = amount / (len(selected_users) + 1)

            # payer
            ExpenseParticipant.objects.create(
                expense=expense,
                user=request.user,
                share_amount=split,
                pending_amount=0,
                status='paid'
            )

            for uid in selected_users:
                u = User.objects.get(id=uid)

                ExpenseParticipant.objects.create(
                    expense=expense,
                    user=u,
                    share_amount=split,
                    pending_amount=split,
                    status='pending'
                )

        return redirect('dashboard')

    return render(request, 'add_expense.html', {'users': users})
@login_required
def expenses(request):
    data = Expense.objects.filter(user=request.user)

    query = request.GET.get('q')
    if query:
        data = data.filter(title__icontains=query)

    category = request.GET.get('category')
    if category:
        data = data.filter(category=category)

    return render(request, 'expenses.html', {'data': data})
@login_required
def repay(request, id):
    p = ExpenseParticipant.objects.get(id=id)

    if request.method == 'POST':
        amt = Decimal(request.POST['amount'])

        if amt <= p.pending_amount:
            p.pending_amount -= amt
            p.paid_amount += amt

            if p.pending_amount == 0:
                p.status = 'completed'

            p.save()

            Repayment.objects.create(
                payer=request.user,
                receiver=p.expense.user,
                amount=amt
            )

    return redirect('dashboard')
@login_required
def budget(request):
    if request.method == 'POST':
        Budget.objects.update_or_create(
            user=request.user,
            category=request.POST['category'],
            month=request.POST['month'],
            defaults={'amount': request.POST['amount']}
        )
        return redirect('budget')

    budgets = Budget.objects.filter(user=request.user)

    return render(request, 'budget.html', {'budgets': budgets})
@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Amount', 'Category'])

    expenses = Expense.objects.filter(user=request.user)

    for e in expenses:
        writer.writerow([e.title, e.amount, e.category])

    return response
@login_required
def shared_expenses(request):
    data = ExpenseParticipant.objects.filter(user=request.user)

    return render(request, 'shared.html', {'data': data})