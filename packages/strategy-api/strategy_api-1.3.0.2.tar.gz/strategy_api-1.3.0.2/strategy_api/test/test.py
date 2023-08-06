import time
from datetime import datetime

from strategy_api.event.engine import Event, EventEngine, EVENT_TICK, EVENT_BAR, EVENT_ORDER
from strategy_api.tm_api.Binance.futureUsdt import BinanceFutureUsdtGateway
from strategy_api.tm_api.Binance.futureInverse import BinanceFutureInverseGateway
from strategy_api.tm_api.Binance.spotGateway import BinanceSpotGateway
from strategy_api.tm_api.Okex.gateway import OkexGateway

from strategy_api.tm_api.object import Interval, TickData, BarData, OrderData, DataType, PositionSide, Dest, Chain, \
    TransferType

import socket
import socks

# proxy_host = "127.0.0.1"  # 代理地址
# proxy_port = 1080  # 代理端口号
# socks.set_default_proxy(socks.SOCKS5, proxy_host, proxy_port)
# socket.socket = socks.socksocket


def process_tick_event(event: Event):
    tick: TickData = event.data
    print("tick 数据：")
    print(tick)


def process_bar_event(event: Event):
    bar: BarData = event.data
    print("k 线 数据：")
    print(bar)


def process_order_event(event: Event):
    order: OrderData = event.data
    print("订单 数据：")
    print(order)


def init_event():
    event_engine = EventEngine()
    event_engine.start()
    event_engine.register(EVENT_TICK, process_tick_event)
    event_engine.register(EVENT_BAR, process_bar_event)
    event_engine.register(EVENT_ORDER, process_order_event)
    return event_engine


def test_binance_spot_query_orders():
    api_setting = {
        "key": "oZ9EjUvlU5mvwFr2oQARcmsvzP9gQxf6f1gLhg0jmPZ5vy6Qo8NSxtOSg1V2eDng11",
        "secret": "Og2O2hcvobj3KXfa08pdBtO9OY0PRvtAqrCui3RZyoaYmMYznkenHrqYwRJkVJuz11",
        "proxy_host": "127.0.0.1",
        "proxy_port": 8010,
        "Passphrase": "",

        "call_order_switch": False,  # 订单数据回调 开关
        "call_tick_switch": False,  # tick数据回调 开关
        "call_bar_switch": False  # k线数据回调 开关
    }

    event_engine = init_event()
    api = BinanceSpotGateway(event_engine)
    api.connect(api_setting)
    # 杠杆根据标的查询所有订单， 现货标的 改为 BTC-USDT-SPOT
    # orders = api.query_orders("BTC-USDT-MARGIN")
    # for order in orders:
    #     print(f"订单号：{order.orderid} | 订单价：{order.price} | 订单方向: {order.direction} | 订单成交价：{order.traded_price} | 订单累计成交量: {order.traded} | 订单状态: {order.status}")

    # 杠杆现货根据标的 和 订单号 查询订单, 现货标的 改为 BTC-USDT-SPOT
    # order = api.query_order(symbol="BTC-USDT-MARGIN", orderId="web_3e65910cf8c74557910757cf9d893c12")
    # print(f"订单号：{order.orderid} | 订单价：{order.price} | 订单方向: {order.direction} | 订单成交价：{order.traded_price} | 订单累计成交量: {order.traded}" | 订单状态: {order.status})

    # 杠杆现货根据标的 撤销所有订单, 现货标的 改为 BTC-USDT-SPOT
    tag = api.cancel_all_order(symbol="BTC-USDT-MARGIN")
    if tag:
        print("成功撤销")
    else:
        print("撤销失败")

def test_binance_usdt_orders():
    api_setting = {
        "key": "oZ9EjUvlU5mvwFr2oQARcmsvzP9gQxf6f1gLhg0jmPZ5vy6Qo8NSxtOSg1V2eDng",
        "secret": "Og2O2hcvobj3KXfa08pdBtO9OY0PRvtAqrCui3RZyoaYmMYznkenHrqYwRJkVJuz",
        "proxy_host": "127.0.0.1",
        "proxy_port": 8010,
        "Passphrase": "",

        "call_order_switch": False,  # 订单数据回调 开关
        "call_tick_switch": False,  # tick数据回调 开关
        "call_bar_switch": False  # k线数据回调 开关
    }

    event_engine = init_event()
    api = BinanceFutureUsdtGateway(event_engine)
    api.connect(api_setting)
    # 杠杆根据标的查询所有订单
    # orders = api.query_orders("BTC-USDT")
    # for order in orders:
    #     print(f"订单号：{order.orderid} | 订单价：{order.price} | 订单方向: {order.direction} | 订单成交价：{order.traded_price} | 订单累计成交量: {order.traded} | 订单状态: {order.status}")

    # 杠杆现货根据标的 和 订单号 查询订单
    # order = api.query_order(symbol="BTC-USDT", orderId="web_JQvJPw4ySemOXngUZEBj")
    # print(f"订单号：{order.orderid} | 订单价：{order.price} | 订单方向: {order.direction} | 订单成交价：{order.traded_price} | 订单累计成交量: {order.traded} | 订单状态: {order.status}")

    # 杠杆现货根据标的 撤销所有订单
    # tag = api.cancel_all_order(symbol="BTC-USDT")
    # if tag:
    #     print("成功撤销")
    # else:
    #     print("撤销失败")

def test_binance_inverse_orders():
    api_setting = {
        "key": "oZ9EjUvlU5mvwFr2oQARcmsvzP9gQxf6f1gLhg0jmPZ5vy6Qo8NSxtOSg1V2eDng",
        "secret": "Og2O2hcvobj3KXfa08pdBtO9OY0PRvtAqrCui3RZyoaYmMYznkenHrqYwRJkVJuz",
        "proxy_host": "127.0.0.1",
        "proxy_port": 8010,
        "Passphrase": "",

        "call_order_switch": False,  # 订单数据回调 开关
        "call_tick_switch": False,  # tick数据回调 开关
        "call_bar_switch": False  # k线数据回调 开关
    }

    event_engine = init_event()
    api = BinanceFutureInverseGateway(event_engine)
    api.connect(api_setting)
    # 杠杆根据标的查询所有订单， 现货标的 改为 BTC-USDT-SPOT
    # orders = api.query_orders("BTC-USD-PERP")
    # for order in orders:
    #     print(f"订单号：{order.orderid} | 订单价：{order.price} | 订单方向: {order.direction} | 订单成交价：{order.traded_price} | 订单累计成交量: {order.traded} | 订单状态: {order.status}")

    # 杠杆现货根据标的 和 订单号 查询订单, 现货标的 改为 BTC-USDT-SPOT
    # order = api.query_order(symbol="BTC-USD-PERP", orderId="web_XxYYXfx97UgOUVbNpEjV")
    # print(f"订单号：{order.orderid} | 订单价：{order.price} | 订单方向: {order.direction} | 订单成交价：{order.traded_price} | 订单累计成交量: {order.traded} | 订单状态: {order.status}")

    # 杠杆现货根据标的 撤销所有订单, 现货标的 改为 BTC-USDT-SPOT
    tag = api.cancel_all_order(symbol="BTC-USD-PERP")
    if tag:
        print("成功撤销")
    else:
        print("撤销失败")

def test_okex():
    api_setting = {
        "key": "e000bb72-0ff8-488b-a77c-41e32a89fa7a",
        "secret": "43961C6EE31AD226BADF234258EE14DA",
        "proxy_host": "127.0.0.1",
        "proxy_port": 8010,
        "Passphrase": "Test.123",

        "call_order_switch": True,  # 订单数据回调 开关
        "call_tick_switch": True,  # tick数据回调 开关
        "call_bar_switch": True  # k线数据回调 开关
    }
    event_engine = init_event()
    api = OkexGateway(event_engine)
    api.connect(api_setting)
    orders = api.query_orders("BTC-USDT")
    for order in orders:
        print(f"订单号：{order.orderid} | 订单价：{order.price} | 订单方向: {order.direction} | 订单成交价：{order.traded_price} | 订单累计成交量: {order.traded} | 订单状态: {order.status}")
    order = api.query_order("BTC-USDT-SPOT", '5463494692529682458')
    print(f"订单号：{order.orderid} | 订单价：{order.price} | 订单方向: {order.direction} | 订单成交价：{order.traded_price} | 订单累计成交量: {order.traded} | 订单状态: {order.status}")


if __name__ == '__main__':
    print("测试币安 现货 查询 orders")
    test_okex()
