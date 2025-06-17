from django.db import models
from django.conf import settings
from orders.models import Order


class DigipayAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2)
    available_credit = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:  # pragma: no cover
        return f"Digipay {self.user}"


class CreditScoreHistory(models.Model):
    account = models.ForeignKey(DigipayAccount, on_delete=models.CASCADE, related_name="scores")
    score = models.IntegerField()
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.account.user} score {self.score}"


class DigipayTransaction(models.Model):
    account = models.ForeignKey(DigipayAccount, on_delete=models.CASCADE, related_name="transactions")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:  # pragma: no cover
        return f"Tx {self.id} {self.amount}"


class Installment(models.Model):
    transaction = models.ForeignKey(DigipayTransaction, on_delete=models.CASCADE, related_name="installments")
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self) -> str:  # pragma: no cover
        return f"Installment {self.amount} on {self.due_date}"
