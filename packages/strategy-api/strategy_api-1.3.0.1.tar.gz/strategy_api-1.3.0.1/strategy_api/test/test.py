import time

from strategy_api.event.engine import Event, EventEngine, EVENT_TICK, EVENT_BAR, EVENT_ORDER
from strategy_api.tm_api.Binance.futureUsdt import BinanceFutureUsdtGateway
from strategy_api.tm_api.Binance.futureInverse import BinanceFutureInverseGateway
from strategy_api.tm_api.Binance.spotGateway import BinanceSpotGateway
from strategy_api.tm_api.Okex.gateway import OkexGateway

from strategy_api.tm_api.object import Interval, TickData, BarData, OrderData, DataType, PositionSide, Dest, Chain, \
    TransferType

api_setting = {
    "key": "",
    "secret": "",
    "proxy_host": "127.0.0.1",
    "proxy_port": 8010,
    "Passphrase": "Test1.123",

    "call_order_switch": True,  # 订单数据回调 开关
    "call_tick_switch": True,  # tick数据回调 开关
    "call_bar_switch": True  # k线数据回调 开关
}


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

# # ---------------------------币安api---------------------------

#
# event_engine = EventEngine()
# event_engine.start()
# event_engine.register(EVENT_TICK, process_tick_event)
# event_engine.register(EVENT_BAR, process_bar_event)
# event_engine.register(EVENT_ORDER, process_order_event)
# #
# api = BinanceFutureUsdtGateway(event_engine)
# # api = BinanceFutureInverseGateway(event_engine)
# # # # 链接api
# api.connect({
#     "key": "",
#     "secret": "",
#     "proxy_host": "127.0.0.1",
#     "proxy_port": 8010,
#     "Passphrase": "",
#     "call_order_switch": False,  # 订单数据回调 开关
#     "call_tick_switch": False,  # tick数据回调 开关
#     "call_bar_switch": False  # k线数据回调 开关
# })
# # time.sleep(5)
# history_kline = api.query_history(symbol="BTC-USDT", interval=Interval.MINUTE, minutes=20)
# print(len(history_kline))
# print(history_kline)
# print(len(history_kline))
# #
# # 订阅 1 分钟 K 线 行情
# api.subscribe(symbol="BTCUSD_PERP", data_type=DataType.BAR, interval=Interval.MINUTE)

# 订阅 tick 行情
# api.subscribe(symbol="BTCUSDT", data_type=DataType.TICK)

# 下单
# api.buy(symbol="BTCUSDT", volume=0.01, price=9999, maker=True, stop_loss=False, stop_profit=False)
#
# # 撤销订单
# api.cancel_order(orderid="xl_1111111", symbol="BTCUSDT")
# # -------------------------------------------------------------
# ---------------------------Okex api---------------------------


# 订阅 1 分钟 K 线 行情
# api.subscribe(symbol="BTC-USDT", interval=Interval.MINUTE)

# # 订阅 tick 行情



event_engine = EventEngine()
event_engine.start()
event_engine.register(EVENT_TICK, process_tick_event)
event_engine.register(EVENT_BAR, process_bar_event)
event_engine.register(EVENT_ORDER, process_order_event)

api = OkexGateway(event_engine)

# 链接api
api.connect(api_setting)
time.sleep(10)
# 查询历史K线数据
send_tag = api.query_depth(symbol="BTC-USDT-SPOT", limit=10)
print(send_tag)
# print(history_kline)
# api.subscribe(symbol="BTC-USDT-SWAP", data_type=DataType.BAR, interval=Interval.MINUTE)

# api.subscribe(symbol="BTC-USDT-SWAP", data_type=DataType.TICK)
# 市价单下单
# api.short(symbol="SOL-USDT-SWAP", volume=1, price=9999, maker=False, stop_loss=False, stop_profit=False, position_side=PositionSide.TWOWAY)
# 限价单下单
# api.buy(symbol="SOL-USD-SWAP", volume=1, price=10, maker=False, stop_loss=False, stop_profit=False)
# print(orderid)
# # 撤销订单
# api.cancel_order(orderid="230104211950000001", symbol="SOL-USDT-SWAP")
# -------------------------------------------------------------
