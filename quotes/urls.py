from django.urls import path
from .views import *

urlpatterns = [
    path('rfp/apply/<int:rfp_id>', ApplyRFPView.as_view(), name = 'apply_rfp'),
    path('rfp/quotes/<int:rfp_id>', QuotesListView.as_view(), name = 'quotes_list'),
    path('rfp/quotes/', ListAllQuotesView.as_view(), name = 'all_quotes_list'),
]