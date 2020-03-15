"""Получаем по определённым запросам данные на счёт продавца
"""
from webpanel.models.order import Order
from webpanel.models.seller_bill import SellerBill


def get_seller_order_by_number(order_number: int) -> dict:
    """Получить сгруппированные данные по счёту продавца
    Возвращает данные:
        order_data, bill_data
    """
    if Order.objects.filter(order_number=order_number):
        order_data = Order.objects.filter(order_number=order_number)
        if SellerBill.objects.filter(order_number=order_number):
            bill_data = SellerBill.objects.filter(order_number=order_number)
            return order_data, bill_data
        return order_data, None
    return None, None