"""
URL configuration for restintern1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path

from rest_framework_simplejwt import views as jwt_views
from app1 import views
from daily_expense import views as dviews

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('',views.Studentlist.as_view(),name="studentlist"),
    path('',views.Userregistration.as_view()),
    path('change_password/',views.change_password.as_view(), name='change_password'),


    path('addexpense/',dviews.Addexpense.as_view()),
    path('expenseinmonth/',dviews.CurrentMonthExpenseView.as_view()),
    path('editexpense/<int:pk>',dviews.Editexpense.as_view()),
    path('expensefilter/', dviews.ExpenseListfilter.as_view(),),
    path('recenttransaction/', dviews.RecentTransactionsView.as_view()),
    path('total-amount-by-category/', dviews.TotalAmountByCategoryView.as_view()),
    path('paginationexpenselist/', dviews.PaginationExpenseListView.as_view(),),
    path('yearly-report/', dviews.YearlyExpenseReportsView.as_view(),),
    path('monthly-report/',dviews.MonthExpenseReportsView.as_view(),),
    #path('expenses/<int:pk>/', views.ExpenseDetail.as_view(), name='expense-detail'),


    path('api/token/',jwt_views.TokenObtainPairView.as_view(),name ='token_obtain_pair'),
    path('api/token/refresh/',jwt_views.TokenRefreshView.as_view(),name ='token_refresh'),
    # path('', include('app.urls')),
]





