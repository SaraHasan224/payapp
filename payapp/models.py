from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class Currency(models.Model):
    name = models.CharField(max_length=100)
    iso_code = models.CharField(max_length=5)
    code = models.CharField(max_length=5)
    curr_rate = models.DecimalField(max_digits=11, decimal_places=2)


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="assigned_profile",
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="assigned_currency"
    )
    phone = models.CharField(max_length=12, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    @receiver(post_save, sender=CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            profile = Profile.objects.create(user=instance)
            profile.save()

    def __str__(self):
        return self.user.username


class Wallet(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="wallet_user",
    )
    wallet_number = models.CharField(max_length=14, default=0)
    withdrawal_limit = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=11, decimal_places=2, null=True, default=0)
    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="wallet_currency",
        unique=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Payee(models.Model):
    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=True, null=True,
        related_name="payee_sender_id",
        unique=False
    )
    payee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True,
                              related_name="payee_id",
                              unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def __str__(self):
        return str(self.user)



class Transaction(models.Model):
    TRANSACTION_STATUS_OPTIONS = [
        ("1", "Paid"),
        ("0", "Not paid"),
    ]
    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=True,
        null=True,
        related_name="transaction_sender_id"
    )
    sender_curr = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="assigned_sender_currency",
    )
    sender_prev_bal = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    sender_cur_bal = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name="transaction_receiver_id")
    receiver_curr = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="assigned_receiver_currencies",
        unique=False
    )
    receiver_prev_bal = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    receiver_cur_bal = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    requested_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="requested_currency",
        unique=False
    )
    amount_requested = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    sent_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="sent_currency",
        unique=False
    )
    amount_sent = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    comment = models.CharField(max_length=1000, null=True)
    status = models.CharField(
        max_length=1, default="0", choices=TRANSACTION_STATUS_OPTIONS
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def __str__(self):
        return str(self.user)



class Invoice(models.Model):
    STATUS_OPTIONS = [
        ("0", "Draft"),
        ("1", "Sent"),
        ("2", "Processing"),
        ("3", "Processed"),
    ]
    TRANSACTION_STATUS_OPTIONS = [
        ("1", "Paid"),
        ("0", "Not paid"),
    ]
    invoice_no = models.CharField(max_length=255)
    invoice_date = models.DateField(auto_now=True,blank=True)
    transaction_date = models.DateField(blank=True, null=True)
    transaction_status = models.CharField(
        max_length=1, default="0", choices=TRANSACTION_STATUS_OPTIONS
    )
    transaction = models.ForeignKey(
        Transaction, on_delete=models.CASCADE, blank=True, null=True,
        related_name="transaction",
        unique=False
    )
    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=True, null=True,
        related_name="sender_id",
        unique=False
    )
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name="receiver_id",
                                 unique=False)
    status = models.CharField(max_length=1, default="0", choices=STATUS_OPTIONS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def __str__(self):
        return str(self.user)

class RequestResponseLogs(models.Model):
    url = models.TextField(null=True)
    user = models.BigIntegerField(null=True)
    request = models.TextField(null=True)
    response = models.TextField(null=True)
    response_code = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def __str__(self):
        return str(self.user)


class Notification(models.Model):
    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=True, null=True,
        related_name="n_sender",
        unique=False
    )
    receiver = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=True, null=True,
        related_name="n_receiver",
        unique=False
    )
    is_read = models.TextField(null=True)
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, blank=True, null=True,
        related_name="n_invoice",
        unique=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)