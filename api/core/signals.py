from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save)
def protect_order(Order, **kwargs):
    print('running signal')
    raise Exception()
