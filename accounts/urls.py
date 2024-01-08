from django.urls import path
from .views import (
    UserBaseViewSet, RefreshViewSet,
)

urlpatterns = [
    path('register/', UserBaseViewSet.as_view({'post': 'create'})),
    path('login/', UserBaseViewSet.as_view({'post': 'login'})),
    path('refresh/', RefreshViewSet.as_view({'post': 'post'}), name='token_refresh'),
    
    path('me/', UserBaseViewSet.as_view({'get': 'me'})),
    path('me/<str:id>/', UserBaseViewSet.as_view({'put': 'update'})),
]