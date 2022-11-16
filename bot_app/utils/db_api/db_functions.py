from asgiref.sync import sync_to_async
from clients.models import OrderRequest, Day, Client


@sync_to_async
def is_free(time: str, date: str, children_amount: int):
    start_time = time.split("-")[0].split(":")[0]
    end_time = time.split("-")[1].split(":")[0].split(":")[0]
    children = children_amount
    orders = OrderRequest.objects.filter(date=Day.objects.get(date=date))
    total_children = [order.children_amount for order in orders if
                      abs(int(order.start_time.hour) - int(start_time)) < 4]
    if sum(total_children) + children <= 10:
        return True, 1
    else:
        return False, 10 - sum(total_children)


@sync_to_async
def write_to_db(*args):
    order = OrderRequest(
        start_time=args[0].split("-")[0].strip(),
        end_time=args[0].split("-")[1].strip(),
        date=Day.objects.get(date=args[1]),
        children_amount=args[2],
        client=Client.objects.get(telegram_id=args[3])
    )
    order.save()


@sync_to_async
def delete_from_db(*args):
    order = OrderRequest.objects.filter(
        start_time=args[0].split("-")[0].strip(),
        end_time=args[0].split("-")[1].strip(),
        date=Day.objects.get(date=args[1]),
        children_amount=args[2],
        client=Client.objects.get(telegram_id=args[3])
    ).delete()
    return True
