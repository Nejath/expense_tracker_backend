from rest_framework import serializers
from bson.decimal128 import Decimal128
from daily_expense.models import Expense

# from django.contrib.auth import get_user_model
# User=get_user_model()


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Expense
        fields=['expense_name','amount_spent','date_of_transaction','category']

    def get(self,request):
        list = Expense.objects.filter(user=request.user)
        return list

    def create(self, validated_data):
        user = self.context['request'].user
        expense = Expense(user=user, **validated_data)
        expense.save()
        return expense



class CurrentMonthExpenseSerializer(serializers.Serializer):
    total_expense=serializers.DecimalField(max_digits=50,decimal_places=2)

class TotalAmountbyCategorySerializer(serializers.Serializer):
    category = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=50, decimal_places=2)

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     # Convert Decimal128 to float for serialization
    #     data['total_amount'] = float(instance['total_amount'])
    #     return data


class YearlyReportSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    monthly_expenses = serializers.DictField(
        child=serializers.DecimalField(max_digits=10, decimal_places=2)
    )

class MonthReportSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    daily_expenses = serializers.DictField(
        child=serializers.DecimalField(max_digits=10, decimal_places=2)
    )



