from django.urls import path, include
from .views import IncomeDetailView, IncomeListView

urlpatterns = [
    path('', IncomeListView.as_view(), name='incomes'),
    path('<int:id>', IncomeDetailView.as_view(), name='income'),
]