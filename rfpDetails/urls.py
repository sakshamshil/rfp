from django.urls import path, include
from .views import *

urlpatterns = [
    path('rfplist/', RFPListView.as_view(), name='rfp_list'),
    path('createrfp/', RFPCreateView.as_view(), name='create_rfp'),
    path('updaterfp/', UpdateRFPView.as_view(), name='update_rfp'),
    path('rfp/getrfp-id/<int:id>/', RFPDetailsByRFP.as_view(), name='get_rfp_by_rfp'),
    path('rfp/getrfp-user/<int:id>/', RFPDetailsByUser.as_view(), name='get_rfp_by_user'),
    path('rfp/closerfp/<int:rfp_id>/', CloseRFPView.as_view(), name='close_rfp'),

]
