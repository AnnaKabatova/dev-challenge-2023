from django.urls import path

from .views import cell_create_retrieve, sheet_data
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('<sheet_id>/<cell_id>/', cell_create_retrieve, name='cell-create-retrieve'),
    path('<sheet_id>/', sheet_data, name='sheet-data'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

app_name = 'sheets'
