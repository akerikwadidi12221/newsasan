from django.urls import path
from .views import EligibilityCheckView, AccountInfoView

urlpatterns = [
    path('v1/digipay/eligibility-check', EligibilityCheckView.as_view()),
    path('v1/digipay/account', AccountInfoView.as_view()),
]
