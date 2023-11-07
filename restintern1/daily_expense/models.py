from app1.models import CustomUser

from django.db import models
from djongo import models
from django.db.models import Sum, F
from django.utils import timezone

# from django.contrib.auth import get_user_model
# User=get_user_model()




class Expense(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    expense_name = models.CharField(max_length=255, help_text="Expense name/description")
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount spent")
    date_of_transaction = models.DateTimeField(auto_now=True, help_text="Date of transaction",editable=True)

    EXPENSE_CATEGORIES = [
        ('Food', 'Food'),
        ('Transportation', 'Transportation'),
        ('Entertainment', 'Entertainment'),
        ('Other', 'Other'),
    ]
    category = models.CharField(max_length=20, choices=EXPENSE_CATEGORIES, help_text="Category of expense")

    def __str__(self):
        return self.expense_name



