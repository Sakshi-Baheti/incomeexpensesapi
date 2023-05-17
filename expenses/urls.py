from django.urls import path, include
from .views import ExpenseDetailView, ExpenseListView

urlpatterns = [
    path('', ExpenseListView.as_view(), name='expenses'),
    path('<int:id>', ExpenseDetailView.as_view(), name='expense'),
]