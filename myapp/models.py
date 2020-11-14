from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from myapp import stock_api


# Create your models here.
class Stock(models.Model):
    symbol = models.CharField(max_length=12, primary_key=True)
    name = models.CharField(max_length=64)
    top_rank = models.IntegerField(null=True)
    price = models.FloatField()
    change = models.FloatField(null=True)
    change_percent = models.FloatField(null=True)
    market_cap = models.FloatField(null=True)
    primary_exchange = models.CharField(null=True, max_length=32)
    last_modified = models.DateTimeField(auto_now=True)

    @classmethod
    def add_to_watchlist(cls, profile, stock_symbol):
        stock = cls.objects.get(symbol=stock_symbol)
        profile.watchlist.add(stock)
        profile.save()

    @classmethod
    def remove_from_watchlist(cls, profile, stock_symbol):
        stock = cls.objects.get(symbol=stock_symbol)
        profile.watchlist.remove(stock)
        profile.save()
    
    @classmethod
    def add_to_db(cls, data):
        cls.objects.create(symbol=data['symbol'], 
                            name=data['companyName'],
                            price=data['latestPrice'],
                            change=data['change'],
                            change_percent=data['changePercent'],
                            market_cap=data['marketCap'],
                            primary_exchange=data['primaryExchange'])

    @classmethod
    def is_needed(cls, stock_symbol):
        stock = cls.objects.filter(symbol=stock_symbol)[:1]
        if not stock.exists():
            return False
        else:
            profiles_using_stock = stock[0].profile_set.all()
            if profiles_using_stock.exists():
                return True
            else:
                return False


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    watchlist = models.ManyToManyField(Stock, blank=True)
    # portfolio = models.ManyToManyField(Stock)

    def __str__(self):
        return f'{self.user.username}'

    @staticmethod
    def add_notification(profile, content):
        Notification.objects.create(title=content['title'],
                                    description=content['description'],
                                    user=profile)

    @staticmethod
    def remove_notification(profile, pk=""):
        if pk:
            Notification.objects.filter(pk=pk, user=profile).delete()
        else:
            Notification.objects.filter(user=profile).delete()

    def get_notifications(self):
        notifications_list = Notification.objects.filter(user__pk=self.pk)
        notifications_dict = {}
        i = 0
        for notification in notifications_list:
            notifications_dict [i] = {'pk': notification.pk,
                                    'title': notification.title,
                                    'description': notification.description,
                                    'time': notification.time,
                                    'link': reverse('index')}   # placeholder for notification.link
            i += 1
        return notifications_dict


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Notification(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)


# https://docs.djangoproject.com/en/3.1/topics/db/examples/many_to_many/
