from .views import ExpenseSummaryStatsView, IncomeSourceSummaryStatsView
from django.urls import path

urlpatterns = [
    path('expense_category_data', ExpenseSummaryStatsView.as_view(), name='expense-category-data'),
    path('income_source_data', IncomeSourceSummaryStatsView.as_view(), name='income-source-data'),

]