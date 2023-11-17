
#from django.utils import timezone

from django.shortcuts import render
from bson.decimal128 import Decimal128

from rest_framework import generics, mixins, status

from decimal import Decimal
from daily_expense.serializers import ExpenseSerializer,CurrentMonthExpenseSerializer,TotalAmountbyCategorySerializer,\
    YearlyReportSerializer,MonthReportSerializer

from daily_expense.models import Expense
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from daily_expense.pagination import StandardResultsSetPagination

from datetime import datetime,timedelta,date
import calendar

from rest_framework import generics
from rest_framework.response import Response
# Create your views here.


class Addexpense(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Expense.objects.all()
    serializer_class=ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        response = self.create(request)
        if response.status_code == status.HTTP_201_CREATED:
            return Response({'message': 'Expense added successfully'}, status=status.HTTP_201_CREATED)
        else:
            return response
        #return self.create(request)



class CurrentMonthExpenseView(APIView):
    serializer_class = CurrentMonthExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        current_month = datetime.now().month
        current_year = datetime.now().year

        expense = Expense.objects.filter(
            user=user,
            date_of_transaction__gte=datetime(current_year, current_month, 1),
            date_of_transaction__lt=datetime(current_year, current_month + 1, 1)
        )
        total_expense=0
        for i in expense:

            total_expense+=Decimal(str(i.amount_spent))

        serializer = CurrentMonthExpenseSerializer({'total_expense': total_expense})
        return Response(serializer.data, status=status.HTTP_200_OK)


class Editexpense(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset=Expense.objects.all()
    serializer_class=ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        return self.retrieve(request)
    def put(self,request,pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Return a success response with a confirmation message
        return Response({'message': 'Expense updated successfully'}, status=status.HTTP_200_OK)
        #return self.update(request)
    def delete(self,request,pk):
        return self.destroy(request)




class ExpenseListfilter(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('category', )
    search_fields = ('expense_name',)


    def get_queryset(self):
        queryset = Expense.objects.filter(user=self.request.user)
        category = self.request.query_params.get('category')
        # Get the start_date and end_date from the query parameters
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                end_date += timedelta(days=1)

            except ValueError:
                return Expense.objects.none()

            #Filter expenses between the specified date range
            queryset = queryset.filter(
                Q(date_of_transaction__gte=start_date) &
                Q(date_of_transaction__lte=end_date)
            )

        if category:
            queryset = queryset.filter(category=category)

        return queryset

class RecentTransactionsView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Expense.objects.filter(user=user).order_by('-date_of_transaction')[:5]


class TotalAmountByCategoryView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = self.request.user
        categories = Expense.objects.filter(user=user)
        total_expenses = {}

        for i in categories:
            if i.category in total_expenses:
                total_expenses[i.category] += Decimal(str(i.amount_spent))
            else:
                total_expenses[i.category]=Decimal(str(i.amount_spent))

        return Response(total_expenses)


class PaginationExpenseListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        return Expense.objects.filter(user=user)



class YearlyExpenseReportsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = self.request.user
        selected_year = self.request.query_params.get('year')  # Get the selected year from the request

        # Check if the selected year is valid (you may want to add further validation)
        if not selected_year:
            return Response({'error': 'Year not specified'}, status=status.HTTP_400_BAD_REQUEST)

        # Initialize a dictionary to store expenses for each month
        monthly_expenses = {
            1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0
        }

        # Get all expenses for the selected year
        expenses = Expense.objects.filter(
            user=user).filter(
            date_of_transaction__year=selected_year)


        # Calculate monthly expenses
        for expense in expenses:
            print(expense)
            month = expense.date_of_transaction.month
            amount_spent = expense.amount_spent

            monthly_expenses[month] +=Decimal(str(amount_spent))

        # Serialize the report data
        report_data = {
            'year': selected_year,
            'monthly_expenses': monthly_expenses
        }

        serializer = YearlyReportSerializer(report_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MonthExpenseReportsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = self.request.user
        selected_year = self.request.query_params.get('year')  # Get the selected year from the request
        selected_month = self.request.query_params.get('month')  # Get the selected month from the request

        # Check if the selected year and month are valid (you may want to add further validation)
        if not selected_year or not selected_month:
            return Response({'error': 'Year and month not specified'}, status=status.HTTP_400_BAD_REQUEST)

        # Parse the selected year and month as integers
        selected_year = int(selected_year)
        selected_month = int(selected_month)

        # Calculate the number of days in the selected month
        days_in_month = calendar.monthrange(selected_year, selected_month)[1]

        # Initialize a dictionary to store expenses for each day
        daily_expenses = {}

        # Get all expenses for the selected month and year
        expenses = Expense.objects.filter(
            user=user).filter(
            date_of_transaction__gte=datetime(selected_year, selected_month, 1),
            date_of_transaction__lt=datetime(selected_year, selected_month + 1, 1)
        )


        # Calculate daily expenses
        for day in range(1, days_in_month + 1):
            daily_expenses[day] = 0

        for expense in expenses:
            day = expense.date_of_transaction.day
            amount_spent = expense.amount_spent

            # Accumulate daily expenses
            daily_expenses[day] += Decimal(str(amount_spent))

        # Serialize the report data
        report_data = {
            'year': selected_year,
            'month': selected_month,
            'daily_expenses': daily_expenses
        }

        serializer = MonthReportSerializer(report_data)
        return Response(serializer.data, status=status.HTTP_200_OK)