from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from ob_dj_store.core.stores.models import Cart, Order, OrderHistory, Wallet


@receiver(
    post_save,
    sender=settings.AUTH_USER_MODEL,
    dispatch_uid="create_customer_cart_and_wallet_handler",
)
def create_customer_cart_and_wallet_handler(sender, instance, created, **kwargs):
    if not created:
        return
    cart = Cart(customer=instance)
    cart.save()
    country = getattr(instance, "country", None)
    Wallet.objects.create(user=instance, country=country)


# add receiver to ProductVariant to create inventory


@receiver(
    post_save,
    sender=Order,
    dispatch_uid="create_order_history_handler",
)
def create_order_history_handler(sender, instance, created, **kwargs):
    OrderHistory.objects.create(
        order=instance,
        status=instance.status,
    )
