from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATUS = (
    ("STARTED","STARTED"),
    ("PENDING","PENDING"),
    ("SUCCESS","SUCCESS"),
    ("FAILED","FAILED"),
)

class PaymentRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=20, unique=True)
    request_status = models.CharField(max_length=50, choices=STATUS)
    description = models.TextField()
    amount = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            last_transaction = PaymentRequest.objects.order_by('-id').first()
            last_counter = 0
            if last_transaction:
                last_counter = int(last_transaction.transaction_id[5:])  # Extract numeric portion
            new_counter = last_counter + 1
            self.transaction_id = f"ENTXN{new_counter:06d}"
        super().save(*args, **kwargs)