from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.http import HttpResponse
# Create your views here.


def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        expenses = Expense.objects.filter(
            amount__istartswith = search_str, owner= request.user) | Expense.objects.filter(
            date__istartswith = search_str, owner= request.user) | Expense.objects.filter(
            description__icontains = search_str, owner= request.user) | Expense.objects.filter(
            category__icontains = search_str, owner= request.user)
        
        data = expenses.values()
        return JsonResponse(list(data), safe= False )





@login_required(login_url='/authentication/login')
def index(request):
    expenses = Expense.objects.filter(owner = request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
            'expenses': expenses,
            'page_obj': page_obj,
            
        }
    return render(request, 'expenses/index.html',context)

@login_required(login_url='/authentication/login')
def add_expense(request):
    categories = Category.objects.all()
    context = {
            'categories': categories,
            'values': request.POST
        }
    
    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        amount =request.POST['amount']
        date =request.POST['expense_date']
        category =request.POST['category']
        description =request.POST['description']

        if not amount:
            messages.error(request, 'Amount is required!')
            return render(request, 'expenses/add_expense.html', context)

        if not description:
            messages.error(request, 'Description is required!')
            return render(request, 'expenses/add_expense.html', context)
        
        if not category:
            messages.error(request, 'Category is required!')
            return render(request, 'expenses/add_expense.html', context)
        
        if not date:
            messages.error(request, 'Date is required!')
            return render(request, 'expenses/add_expense.html', context)

        Expense.objects.create(owner= request.user ,amount=amount , date = date , category= category , description = description)
        messages.success(request, 'Expense saved successfully!')
    return redirect('expenses')


def expense_edit(request, id):
    expense = Expense.objects.get( pk = id )
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories':categories,
    }
    if request.method== 'GET':
        return render(request, 'expenses/edit-expense.html', context)
    
    if request.method== 'POST':
        amount =request.POST['amount']
        date =request.POST['expense_date']
        category =request.POST['category']
        description =request.POST['description']

        if not amount:
            messages.error(request, 'Amount is required!')
            return render(request, 'expenses/edit_expense.html', context)

        if not description:
            messages.error(request, 'Description is required!')
            return render(request, 'expenses/edit_expense.html', context)
        
        if not category:
            messages.error(request, 'Category is required!')
            return render(request, 'expenses/edit_expense.html', context)
        
        if not date:
            messages.error(request, 'Date is required!')
            return render(request, 'expenses/edit_expense.html', context)

        
        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description
        expense.save()

        messages.success(request, 'Expense Updated successfully!')
        return redirect('expenses')

# def delete_expense(request, id):
#     expense= Expense.objects.get(pk = id)
#     expense.delete()
#     messages.success(request, 'Expense removed!')
#     return redirect('expenses')

def delete_expense(request, id):
    if request.method == 'POST':
        expense = Expense.objects.get(pk=id)
        expense.delete()
        messages.success(request, 'Expense removed!')
        return redirect('expenses')
    else:
        expense = Expense.objects.get(pk=id)
        return render(request, 'expenses/delete_expense.html', {'expense': expense})
