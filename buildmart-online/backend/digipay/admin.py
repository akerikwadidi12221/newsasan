from django.contrib import admin
from .models import DigipayAccount, DigipayTransaction, Installment, CreditScoreHistory

admin.site.register(DigipayAccount)
admin.site.register(DigipayTransaction)
admin.site.register(Installment)
admin.site.register(CreditScoreHistory)
