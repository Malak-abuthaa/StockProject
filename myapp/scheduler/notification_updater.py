from myapp.models import Stock, ChangeStatusRule, Notification, ChangeThresholdRule, PriceThresholdRule
from myapp import stock_api
from django.urls import reverse

CHANGE_STATUS_RULE_THREAD_INT = 1  # one minute interval
CHANGE_THRESHOLD_RULE_THREAD_INT = 1  # one minute interval
PRICE_THRESHOLD_RULE_THREAD_INT = 1  # one minute interval


def change_status_rule():
    rules = ChangeStatusRule.get_rules()
    for rule in rules:
        if not rule.fired:
            num_of_days = rule.num_of_days
            if num_of_days < 5:
                time_range = '5d'
            elif num_of_days < 20:
                time_range = '1m'
            elif num_of_days < 60:
                time_range = '3m'
            elif num_of_days < 120:
                time_range = '6m'
            elif num_of_days < 240:
                time_range = '1y'
            else:
                time_range = '2y'
            days = stock_api.get_stock_historic_prices(symbols=rule.watched_stock.stock.symbol, time_range=time_range,
                                                       chart_interval=1, filter=("changePercent", "date"))
            if num_of_days < len(days):
                for day in days[:-num_of_days - 1:-1]:
                    if rule.status == 'N':
                        if day['changePercent'] > 0:
                            break  # indicating no sequential negative change value through <num_of_days> days
                    if rule.status == 'P':
                        if day['changePercent'] < 0:
                            break  # indicating no sequential positive change value through <num_of_days> days
                else:
                    # indicating there is sequential change through <num_of_days> days,
                    # here we need to insert a notification to user in DB
                    title = f"Sequential {'Positive' if rule.status == 'P' else 'Negative'} Change"
                    description = f"sequential {'Positive' if rule.status == 'P' else 'Negative'} change" \
                                  f" in the past {num_of_days} days for {rule.watched_stock.stock.name}"
                    Notification.objects.create(user=rule.watched_stock.profile, title=title,
                                                description=description,
                                                link=reverse("single_stock", args=(rule.watched_stock.stock.symbol,)))
                    rule.fired = True
                    rule.save()


def change_threshold_rule():
    rules = ChangeThresholdRule.get_rules()
    for rule in rules:
        if not rule.fired:
            data = stock_api.get_stock_info(symbol=rule.watched_stock.stock.symbol, filter=("changePercent",))
            if "changePercent" in data:
                if rule.when == "B" and rule.percentage_threshold > data['changePercent']:
                    title = f"Blow Threshold value Reached for {rule.watched_stock.stock.name}"
                    description = f"the change value percentage " \
                                  f"{data['changePercent']}% reached below the threshold {rule.percentage_threshold}%"
                    Notification.objects.create(user=rule.watched_stock.profile, title=title, description=description,
                                                link=reverse("single_stock", args=(rule.watched_stock.stock.symbol,)))
                    rule.fired = True
                    rule.save()
                elif rule.when == 'A' and rule.percentage_threshold < data['changePercent']:
                    title = f"Above Threshold value Reached for {rule.watched_stock.stock.name}"
                    description = f"the change value percentage " \
                                  f"{data['changePercent']}% reached above the threshold {rule.percentage_threshold}%"
                    Notification.objects.create(user=rule.watched_stock.profile, title=title, description=description,
                                                link=reverse("single_stock", args=(rule.watched_stock.stock.symbol,)))
                    rule.fired = True
                    rule.save()
                elif rule.when == 'O' and rule.percentage_threshold == data['changePercent']:
                    title = f"On Threshold value Reached for {rule.watched_stock.stock.name}"
                    description = f"the change value percentage reached the threshold" \
                                  f" {rule.percentage_threshold}%"
                    Notification.objects.create(user=rule.watched_stock.profile, title=title, description=description,
                                                link=reverse("single_stock", args=(rule.watched_stock.stock.symbol,)))
                    rule.fired = True
                    rule.save()


def price_threshold_rule():
    rules = PriceThresholdRule.get_rules()
    for rule in rules:
        if not rule.fired:
            data = stock_api.get_stock_info(symbol=rule.watched_stock.stock.symbol, filter=("latestPrice",))
            if "latestPrice" in data:
                if rule.when == "B" and rule.price_threshold > data['latestPrice']:
                    title = f"Blow Threshold value Reached for {rule.watched_stock.stock.name}"
                    description = f"the price value {data['latestPrice']} reached below the threshold" \
                                  f" {rule.price_threshold}"
                    Notification.objects.create(user=rule.watched_stock.profile, title=title, description=description,
                                                link=reverse("single_stock", args=(rule.watched_stock.stock.symbol,)))
                    rule.fired = True
                    rule.save()
                elif rule.when == 'A' and rule.price_threshold < data['latestPrice']:
                    title = f"Above Threshold value Reached for {rule.watched_stock.stock.name}"
                    description = f"the price value {data['latestPrice']} reached above the threshold" \
                                  f" {rule.price_threshold}"
                    Notification.objects.create(user=rule.watched_stock.profile, title=title, description=description,
                                                link=reverse("single_stock", args=(rule.watched_stock.stock.symbol,)))
                    rule.fired = True
                    rule.save()
                elif rule.when == 'O' and rule.price_threshold == data['latestPrice']:
                    title = f"Threshold value Reached for {rule.watched_stock.stock.name}"
                    description = f"the price value reached the threshold" \
                                  f" {rule.price_threshold}"
                    Notification.objects.create(user=rule.watched_stock.profile, title=title, description=description,
                                                link=reverse("single_stock", args=(rule.watched_stock.stock.symbol,)))
                    rule.fired = True
                    rule.save()

# TODO: add testing
# TODO: add script for migrating previous watched-stocks properly