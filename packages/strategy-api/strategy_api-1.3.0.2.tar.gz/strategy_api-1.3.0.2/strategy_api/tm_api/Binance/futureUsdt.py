# rest api host
import hashlib
import hmac
import json
import time
import urllib
from copy import copy
from enum import Enum
from ssl import SSLError
from threading import Lock
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple, List
from strategy_api.event.engine import EVENT_TIMER, Event, EventEngine
from strategy_api.tm_api.api.rest.rest_client import RestClient, Request, Response
from strategy_api.tm_api.api.websocket.websocket_client import WebsocketClient
from strategy_api.tm_api.base import BaseGateway
from strategy_api.tm_api.object import TickData, BarData, Interval, OrderRequest, OrderData, Direction, OrderType, \
    Offset, Status, CancelRequest, HistoryRequest, PositionSide, DataType, Product, Exchange, DepthData, BidData, \
    AskData, TdMode, PositionData

# http 基础地址
from strategy_api.tm_api.tools import get_order_type, symbol_deal

F_REST_HOST: str = "https://fapi.binance.com"

# ws 基础地址
F_WEBSOCKET_TRADE_HOST: str = "wss://fstream.binance.com/ws/"
F_WEBSOCKET_DATA_HOST: str = "wss://fstream.binance.com/stream"

# sell/buy direction map
DIRECTION_VT2BINANCES: Dict[Direction, str] = {
    Direction.LONG: "BUY",
    Direction.SHORT: "SELL"
}

DIRECTION_BINANCES2VT: Dict[str, Direction] = {v: k for k, v in DIRECTION_VT2BINANCES.items()}

# GTC 成交为止, 一直有效
ORDERTYPE_VT2BINANCES: Dict[OrderType, Tuple[str, str]] = {
    OrderType.LIMIT: ("LIMIT", "GTC"),  # 限价单
    OrderType.MARKET: ("MARKET", "GTC"),  # 市价单
    OrderType.STOP_MARKET: ("STOP_MARKET", "GTC"),  # 止损单
    OrderType.TAKE_PROFIT_MARKET: ("TAKE_PROFIT_MARKET", "GTC")  # 止盈单
}
ORDERTYPE_BINANCES2VT: Dict[Tuple[str, str], OrderType] = {v: k for k, v in ORDERTYPE_VT2BINANCES.items()}

# Order status map
STATUS_BINANCES2VT: Dict[str, Status] = {
    "NEW": Status.NOTTRADED,
    "PARTIALLY_FILLED": Status.PARTTRADED,
    "FILLED": Status.ALLTRADED,
    "CANCELED": Status.CANCELLED,
    "REJECTED": Status.REJECTED,
    "EXPIRED": Status.CANCELLED
}

TIMEDELTA_MAP: Dict[Interval, timedelta] = {
    Interval.MINUTE: timedelta(minutes=1),
    Interval.HOUR: timedelta(hours=1)
}

INTERVAL_VT2BINANCES: Dict[Interval, str] = {
    Interval.MINUTE: "1m",
    Interval.MINUTE_3: "3m",
    Interval.MINUTE_5: "5m",
    Interval.MINUTE_15: "15m",
    Interval.MINUTE_30: "30m",
    Interval.HOUR: "1h",
    Interval.HOUR_2: "2h",
    Interval.HOUR_4: "4h",
    Interval.HOUR_6: "6h",
    Interval.HOUR_8: "8h",
    Interval.HOUR_12: "12h"
}


# 私钥使用枚举
class Security(Enum):
    NONE: int = 0
    SIGNED: int = 1
    API_KEY: int = 2


class BinanceFutureUsdtGateway(BaseGateway):
    default_setting: Dict[str, Any] = {
        "key": "",
        "secret": "",
        "proxy_host": "",
        "proxy_port": 0,
    }
    exchange: Exchange = Exchange.BINANCE
    product: Product = Product.U_FUTURES
    symbolMap: dict = dict()
    SYMBOL_SET: set = set()

    def __init__(self, event_engine: EventEngine, order_switch: bool = False, bar_switch: bool = False,
                 tick_switch: bool = False) -> None:
        """init"""
        super().__init__(event_engine, order_switch, bar_switch, tick_switch)
        self.trade_ws_api: "BinanceUsdtTradeWebsocketApi" = BinanceUsdtTradeWebsocketApi(self)
        self.market_ws_api: "BinanceUsdtDataWebsocketApi" = BinanceUsdtDataWebsocketApi(self)
        self.rest_api: "BinanceUsdtRestApi" = BinanceUsdtRestApi(self)
        self.get_server_time_interval: int = 0

    def connect(self, setting: dict) -> None:
        key: str = setting["key"]
        secret: str = setting["secret"]

        if isinstance(setting["proxy_host"], str):
            proxy_host: str = setting["proxy_host"]
        else:
            proxy_host: str = ""

        if isinstance(setting["proxy_port"], int):
            proxy_port: int = setting["proxy_port"]
        else:
            proxy_port: int = 0

        self.rest_api.connect(key, secret, proxy_host, proxy_port)
        self.market_ws_api.connect(proxy_host, proxy_port)

        if self.order_call_switch:
            self.event_engine.unregister(EVENT_TIMER, self.process_timer_event)
            self.event_engine.register(EVENT_TIMER, self.process_timer_event)

            self.event_engine.unregister(EVENT_TIMER, self.trade_ws_api.ping_pong)
            self.event_engine.register(EVENT_TIMER, self.trade_ws_api.ping_pong)

        self.event_engine.unregister(EVENT_TIMER, self.market_ws_api.ping_pong)
        self.event_engine.register(EVENT_TIMER, self.market_ws_api.ping_pong)

    # 定时任务, 不间断获取服务器时间
    def process_timer_event(self, event: Event) -> None:
        self.rest_api.keep_user_stream()
        self.get_server_time_interval += 1
        if self.get_server_time_interval >= 300:
            self.rest_api.query_time()
            self.get_server_time_interval = 0

    # 多头买进
    def buy(self,
            orderid: str,
            symbol: str,
            volume: float,  # 数量
            price: float = 0,  # 价格
            maker: bool = False,  # 限价单
            stop_loss: bool = False,  # 止损
            stop_loss_price: float = 0,  # 止损价
            stop_profit: bool = False,  # 止盈
            stop_profit_price: float = 0,  # 止盈价
            position_side: PositionSide = PositionSide.ONEWAY,
            tdMode: TdMode = TdMode.CROSS,
            ccy: str = ""
            ):
        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol

        original_req: OrderRequest = OrderRequest(
            symbol=new_symbol,
            direction=Direction.LONG,
            offset=Offset.OPEN,
            type=get_order_type(maker, stop_loss, stop_profit, self.exchange),
            price=price,
            volume=volume,
            positionSide=position_side,
            exchange=self.exchange,
            stop_loss_price=stop_loss_price,
            stop_profit_price=stop_profit_price,
        )
        self.send_order(original_req, orderid)

    # 多头卖出
    def sell(self,
             orderid: str,
             symbol: str,
             volume: float,  # 数量
             price: float = 0,  # 价格
             maker: bool = False,  # 限价单
             stop_loss: bool = False,  # 止损
             stop_loss_price: float = 0,  # 止损价
             stop_profit: bool = False,  # 止盈
             stop_profit_price: float = 0,  # 止盈价
             position_side: PositionSide = PositionSide.ONEWAY,
             tdMode: TdMode = TdMode.CROSS,
             ccy: str = ""
             ):
        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol

        original_req: OrderRequest = OrderRequest(
            symbol=new_symbol,
            direction=Direction.SHORT,
            offset=Offset.CLOSE,
            type=get_order_type(maker, stop_loss, stop_profit, self.exchange),
            price=price,
            volume=volume,
            positionSide=position_side,
            exchange=self.exchange,
            stop_loss_price=stop_loss_price,
            stop_profit_price=stop_profit_price,
        )
        self.send_order(original_req, orderid)

    # 空头买进
    def short(self,
              orderid: str,
              symbol: str,
              volume: float,  # 数量
              price: float = 0,  # 价格
              maker: bool = False,  # 限价单
              stop_loss: bool = False,  # 止损
              stop_loss_price: float = 0,  # 止损价
              stop_profit: bool = False,  # 止盈
              stop_profit_price: float = 0,  # 止盈价
              position_side: PositionSide = PositionSide.ONEWAY,
              tdMode: TdMode = TdMode.CROSS,
              ccy: str = ""
              ):
        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol

        original_req: OrderRequest = OrderRequest(
            symbol=new_symbol,
            direction=Direction.SHORT,
            offset=Offset.OPEN,
            type=get_order_type(maker, stop_loss, stop_profit, self.exchange),
            price=price,
            volume=volume,
            positionSide=position_side,
            exchange=self.exchange,
            stop_loss_price=stop_loss_price,
            stop_profit_price=stop_profit_price,
        )
        self.send_order(original_req, orderid)

    # 空头卖出
    def cover(self,
              orderid: str,
              symbol: str,
              volume: float,  # 数量
              price: float = 0,  # 价格
              maker: bool = False,  # 限价单
              stop_loss: bool = False,  # 止损
              stop_loss_price: float = 0,  # 止损价
              stop_profit: bool = False,  # 止盈
              stop_profit_price: float = 0,  # 止盈价
              position_side: PositionSide = PositionSide.ONEWAY,
              tdMode: TdMode = TdMode.CROSS,
              ccy: str = ""
              ):
        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol

        original_req: OrderRequest = OrderRequest(
            symbol=new_symbol,
            direction=Direction.LONG,
            offset=Offset.CLOSE,
            type=get_order_type(maker, stop_loss, stop_profit, self.exchange),
            price=price,
            volume=volume,
            positionSide=position_side,
            exchange=self.exchange,
            stop_loss_price=stop_loss_price,
            stop_profit_price=stop_profit_price,
        )
        self.send_order(original_req, orderid)

    # 发送订单
    def send_order(self, req: OrderRequest, orderid: str):
        self.rest_api.send_order(req, orderid)

    def query_orders(self, symbol: str) -> List[OrderData]:
        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol
        return self.rest_api.query_orders(new_symbol, s_type=symbol)

    def query_order(self, symbol: str, orderId: str) -> OrderData:
        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol
        return self.rest_api.query_order(new_symbol, orderId, s_type=symbol)

    def cancel_all_order(self, symbol) -> bool:
        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol
        return self.rest_api.cancel_all_order(new_symbol, symbol)

    # 撤销订单
    def cancel_order(self, orderid: str, symbol: str) -> None:
        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol

        req: CancelRequest = CancelRequest(
            orderid=orderid,
            symbol=new_symbol,
            exchange=self.exchange
        )
        self.rest_api.cancel_order(req)

    # 获取历史K线
    def query_history(self,
                      symbol: str,
                      interval: Interval,
                      hour: int = 0,
                      minutes: int = 0,
                      end_time: datetime = None
                      ) -> List[BarData]:
        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol

        if end_time:
            end: datetime = end_time
        else:
            end: datetime = datetime.now()

        if hour:
            start: datetime = end - timedelta(hours=hour)
        elif minutes:
            start: datetime = end - timedelta(minutes=minutes)
        else:
            print("分钟，小时参数都为0, 查询k线失败")
            return []

        req: HistoryRequest = HistoryRequest(
            symbol=new_symbol,
            start=start,
            end=end,
            interval=interval,
            exchange=self.exchange
        )
        return self.rest_api.query_history(req)

    def query_depth(self, symbol: str, limit: int) -> DepthData:
        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol

        depth_data: DepthData = DepthData(
            symbol=symbol,
            bid_data=[],
            ask_data=[]
        )

        if limit not in [5, 10, 20, 50, 100, 500, 1000, 5000]:
            print(f"无该档位: {limit}")
            return depth_data
        return self.rest_api.query_depth(new_symbol, limit, depth_data)

    def query_position(self, symbol: str) -> List[PositionData]:
        """query position"""
        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol
        return self.rest_api.query_position(new_symbol)

    def query_symbol(self, quote_symbol: str, s_type: str = "") -> list:
        return [i.replace(quote_symbol.upper(), "-" + quote_symbol.upper()) for i in self.SYMBOL_SET if
                i.endswith(quote_symbol.upper())]

    # 订阅数据
    def subscribe(self, symbol: str, data_type: DataType, interval: Interval = None) -> None:
        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol

        if data_type == DataType.TICK:
            self.market_ws_api.subscribe(new_symbol)
        elif data_type == DataType.BAR:
            if interval:
                self.market_ws_api.subscribe(new_symbol, interval)
            else:
                print(f"订阅失败，k 线数据未定义间隔时间")
        else:
            print(f"订阅失败，未知数据类型: {data_type}")

    # 关闭
    def close(self) -> None:
        self.rest_api.stop()
        self.trade_ws_api.stop()
        self.market_ws_api.stop()


class BinanceUsdtRestApi(RestClient):

    def __init__(self, gateway: BinanceFutureUsdtGateway) -> None:
        super().__init__()

        self.gateway: BinanceFutureUsdtGateway = gateway

        self.trade_ws_api: BinanceUsdtTradeWebsocketApi = self.gateway.trade_ws_api

        self.key: str = ""
        self.secret: str = ""

        self.user_stream_key: str = ""
        self.keep_alive_count: int = 0
        self.keep_alive_failed_count: int = 0
        self.recv_window: int = 10000
        self.time_offset: int = 0

        self.order_count: int = 1_000_000
        self.order_count_lock: Lock = Lock()
        self.connect_time: int = 0

    # 登录
    def sign(self, request: Request) -> Request:
        security: Security = request.data["security"]
        if security == Security.NONE:
            request.data = None
            return request

        if request.params:
            path: str = request.path + "?" + urllib.parse.urlencode(request.params)
        else:
            request.params = dict()
            path: str = request.path

        if security == Security.SIGNED:
            timestamp: int = int(time.time() * 1000)

            if self.time_offset > 0:
                timestamp -= abs(self.time_offset)
            elif self.time_offset < 0:
                timestamp += abs(self.time_offset)

            request.params["timestamp"] = timestamp

            query: str = urllib.parse.urlencode(sorted(request.params.items()))
            signature: bytes = hmac.new(self.secret, query.encode(
                "utf-8"), hashlib.sha256).hexdigest()

            query += "&signature={}".format(signature)
            path: str = request.path + "?" + query

        request.path = path
        request.params = {}
        request.data = {}

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "X-MBX-APIKEY": self.key,
            "Connection": "close"
        }

        if security in [Security.SIGNED, Security.API_KEY]:
            request.headers = headers
        return request

    # 连接 http api
    def connect(
            self,
            key: str,
            secret: str,
            proxy_host: str,
            proxy_port: int
    ) -> None:
        self.key = key
        self.secret = secret.encode()
        self.proxy_port = proxy_port
        self.proxy_host = proxy_host

        self.connect_time = (
                int(datetime.now().strftime("%y%m%d%H%M%S")) * self.order_count
        )
        self.init(F_REST_HOST, proxy_host, proxy_port)
        self.start()

        # 获取服务器时间
        self.query_contract()
        self.query_time()
        # 保持用户 ws 的链接
        if self.gateway.order_call_switch:
            self.start_user_stream()

    def query_contract(self) -> None:
        data: dict = {
            "security": Security.NONE
        }
        self.add_request(
            method="GET",
            path="/fapi/v1/exchangeInfo",
            callback=self.on_query_contract,
            data=data
        )

    def on_query_contract(self, data: dict, request: Request) -> None:
        for d in data["symbols"]:
            self.gateway.SYMBOL_SET.add(d['symbol'])

    # 查询服务器时间
    def query_time(self) -> None:
        data: dict = {
            "security": Security.NONE
        }

        path: str = "/fapi/v1/time"

        self.add_request(
            "GET",
            path,
            callback=self.on_query_time,
            on_failed=self.on_query_time_failed,
            on_error=self.on_query_time_error,
            data=data
        )

    # 自定义订单号
    def _new_order_id(self) -> int:
        """生成自定义订单ID"""
        with self.order_count_lock:
            self.order_count += 1
            return self.order_count

    def get_order_id(self) -> str:
        orderid: str = "x-cLbi5uMH" + str(self.connect_time + self._new_order_id())
        return orderid

    # 发送订单
    def send_order(self, req: OrderRequest, orderid: str):

        order: OrderData = req.create_order_data(
            orderid,
        )
        self.gateway.on_order(copy(order))

        data: dict = {
            "security": Security.SIGNED
        }
        if req.positionSide == PositionSide.ONEWAY:
            params: dict = {
                "symbol": req.symbol,
                "side": DIRECTION_VT2BINANCES[req.direction],
                "quantity": req.volume,
                "newClientOrderId": orderid,
                "newOrderRespType": "RESULT",
                "recvWindow": self.recv_window
            }
            if req.offset == Offset.CLOSE:
                params['reduceOnly'] = True
        else:
            if (req.direction == Direction.SHORT and req.offset == Offset.OPEN) or (
                    req.direction == Direction.LONG and req.offset == Offset.CLOSE):
                position_side = "SHORT"
            else:
                position_side = "LONG"

            params: dict = {
                "symbol": req.symbol,
                "side": DIRECTION_VT2BINANCES[req.direction],
                "positionSide": position_side,
                "quantity": req.volume,
                "newClientOrderId": orderid,
                "newOrderRespType": "RESULT",
                "recvWindow": self.recv_window
            }

        # 如果订单type = taker，那就是市价单，如果不是，则是限价单
        if req.type == OrderType.MARKET:
            params["type"] = "MARKET"  # 市价单
        elif req.type == OrderType.STOP_MARKET:
            params["type"] = "STOP_MARKET"  # 止损单
            params["stopPrice"] = req.stop_loss_price
        elif req.type == OrderType.TAKE_PROFIT_MARKET:
            params["type"] = "TAKE_PROFIT_MARKET"  # 止赢单
            params["stopPrice"] = req.stop_profit_price
        else:
            order_type, time_condition = ORDERTYPE_VT2BINANCES[req.type]
            params["type"] = order_type
            params["timeInForce"] = time_condition
            params["price"] = req.price

        path: str = "/fapi/v1/order"

        self.add_request(
            method="POST",
            path=path,
            callback=self.on_send_order,
            data=data,
            params=params,
            extra=order,
            on_error=self.on_send_order_error,
            on_failed=self.on_send_order_failed
        )

    # 撤销订单
    def cancel_order(self, req: CancelRequest) -> None:
        """cancel order"""
        data: dict = {
            "security": Security.SIGNED
        }

        params: dict = {
            "symbol": req.symbol,
            "origClientOrderId": req.orderid,
            "recvWindow": self.recv_window
        }

        path: str = "/fapi/v1/order"

        self.add_request(
            method="DELETE",
            path=path,
            callback=self.on_cancel_order,
            params=params,
            data=data,
            on_failed=self.on_cancel_order_failed,
        )

    def cancel_all_order(self, symbol: str, s_type: str = "") -> bool:
        """cancel order"""

        path = "/fapi/v1/allOpenOrders"

        data: dict = {
            "security": Security.SIGNED
        }

        params: dict = {
            "symbol": symbol.upper(),
        }

        resp: Response = self.request(
            method="DELETE",
            path=path,
            params=params,
            data=data,
        )
        if resp.status_code // 100 != 2:
            msg: str = f"撤销 {self.gateway.symbolMap[symbol]} 订单失败, status code：{resp.status_code}，msg：{resp.text}"
            print(msg)
            return False
        else:
            return True

    def query_order(self, symbol: str, orderId: str, s_type: str = "") -> OrderData:
        path = "/fapi/v1/openOrder"
        data: dict = {
            "security": Security.SIGNED,
        }
        params = {
            "symbol": symbol.upper(),
            "origClientOrderId": orderId
        }

        resp: Response = self.request(
            "GET",
            path=path,
            data=data,
            params=params
        )

        if resp.status_code // 100 != 2:
            msg: str = f"查询 {orderId} 订单失败, status code：{resp.status_code}，msg：{resp.text}"
            print(msg)
        else:
            data = resp.json()
            key: Tuple[str, str] = (data["type"], data["timeInForce"])  # 订单类型
            order_type: OrderType = ORDERTYPE_BINANCES2VT.get(key, OrderType.LIMIT)
            order: OrderData = OrderData(
                symbol=self.gateway.symbolMap[symbol],  # 交易对
                orderid=str(data["clientOrderId"]),  # 订单id
                type=order_type,
                direction=DIRECTION_BINANCES2VT[data["side"]],  # 订单方向
                price=float(data['price']),  # 价格
                volume=float(data["origQty"]),  # 订单原始数量
                traded=float(data["executedQty"]),  # 订单累计已成交量
                traded_volume=float('0'),  # 订单末次成交量
                traded_price=float('0'),  # 订单末次成交价格
                status=STATUS_BINANCES2VT.get(data['status'], Status.NOTTRADED),
                datetime=generate_datetime(data["time"]),
            )
            return order

    def query_orders(self, symbol: str, s_type: str = "") -> List[OrderData]:
        buf: List[OrderData] = []
        path = "/fapi/v1/openOrders"
        data: dict = {
            "security": Security.SIGNED
        }
        params = {
            "symbol": symbol.upper()
        }
        resp: Response = self.request(
            "GET",
            path=path,
            data=data,
            params=params
        )
        if resp.status_code // 100 != 2:
            msg: str = f"查询 {self.gateway.symbolMap[symbol]} 所有订单失败, status code：{resp.status_code}，msg：{resp.text}"
            print(msg)
            return []
        else:
            data = resp.json()
            for i in data:
                key: Tuple[str, str] = (i["type"], i["timeInForce"])  # 订单类型
                order_type: OrderType = ORDERTYPE_BINANCES2VT.get(key, OrderType.LIMIT)
                order: OrderData = OrderData(
                    symbol=self.gateway.symbolMap[symbol],  # 交易对
                    orderid=str(i["clientOrderId"]),  # 订单id
                    type=order_type,
                    direction=DIRECTION_BINANCES2VT[i["side"]],  # 订单方向
                    price=float(i['price']),  # 价格
                    volume=float(i["origQty"]),  # 订单原始数量
                    traded=float(i["executedQty"]),  # 订单累计已成交量
                    traded_volume=float('0'),  # 订单末次成交量
                    traded_price=float('0'),  # 订单末次成交价格
                    status=STATUS_BINANCES2VT.get(i['status'], Status.NOTTRADED),
                    datetime=generate_datetime(i["time"]),
                )
                buf.append(order)
            return buf

    # 获取历史K线数据
    def query_history(self, req: HistoryRequest) -> List[BarData]:
        history: List[BarData] = []
        limit: int = 1500

        start_time: int = int(datetime.timestamp(req.start))

        while True:
            params: dict = {
                "symbol": req.symbol,
                "interval": INTERVAL_VT2BINANCES[req.interval],
                "limit": limit,
                "startTime": start_time * 1000
            }

            path: str = "/fapi/v1/klines"
            if req.end:
                end_time = int(datetime.timestamp(req.end))
                params["endTime"] = end_time * 1000

            resp: Response = self.request(
                "GET",
                path=path,
                data={"security": Security.NONE},
                params=params
            )

            # 如果请求失败，将打破 while 循环
            if resp.status_code // 100 != 2:
                msg: str = f"查询历史kline数据失败, status code：{resp.status_code}，msg：{resp.text}"
                print(msg)
                break
            else:
                data: dict = resp.json()
                if not data:
                    msg: str = f"历史K线数据为空，开始时间：{start_time}"
                    print(msg)
                    break

                buf: List[BarData] = []

                for row in data:
                    bar: BarData = BarData(
                        symbol=self.gateway.symbolMap[req.symbol],
                        datetime=generate_datetime(row[0]),
                        endTime=generate_datetime(row[6]),
                        interval=req.interval,
                        volume=float(row[5]),
                        turnover=float(row[7]),
                        open_price=float(row[1]),
                        high_price=float(row[2]),
                        low_price=float(row[3]),
                        close_price=float(row[4]),
                        exchange=self.gateway.exchange
                    )
                    buf.append(bar)

                begin: datetime = buf[0].datetime
                end: datetime = buf[-1].datetime

                history.extend(buf)
                msg: str = f"查询历史kline数据成功, {req.symbol} - {req.interval.value}，{begin} - {end}"
                print(msg)

                if len(data) < limit:
                    break

                start_dt = bar.datetime + TIMEDELTA_MAP[req.interval]
                start_time = int(datetime.timestamp(start_dt))

        return history

    def query_position(self, symbol: str) -> List[PositionData]:
        """query position"""
        pos_l = []
        params = {
            "symbol": symbol
        }
        resp: Response = self.request(
            method="GET",
            path="/fapi/v2/positionRisk",
            data={"security": Security.SIGNED},
            params=params
        )
        if resp.status_code // 100 != 2:
            msg: str = f"查询仓位数据是比, status code：{resp.status_code}，msg：{resp.text}"
            print(msg)
        else:
            data: dict = resp.json()

            for d in data:
                position: PositionData = PositionData(
                    symbol=self.gateway.symbolMap[symbol],
                    exchange=Exchange.BINANCE,
                    volume=float(d["positionAmt"]),
                    price=float(d["entryPrice"]),
                    mark_price=float(d['markPrice']),
                    liquidation_price=float(d['liquidationPrice']),
                    leverage=int(d['leverage']),
                    pnl=float(d["unRealizedProfit"]),
                )

                # if position.volume:
                volume = d["positionAmt"]
                if '.' in volume:
                    position.volume = float(d["positionAmt"])
                else:
                    position.volume = int(d["positionAmt"])
                pos_l.append(position)
            return pos_l

    def query_depth(self, symbol: str, limit: int, depth_data: DepthData) -> DepthData:
        params: dict = {
            "symbol": symbol,
            "limit": limit
        }

        resp: Response = self.request(
            "GET",
            "/fapi/v1/depth",
            data={"security": Security.NONE},
            params=params
        )
        if resp.status_code // 100 != 2:
            msg: str = f"查询depth数据失败, status code：{resp.status_code}，msg：{resp.text}"
            print(msg)
        else:
            data: dict = resp.json()

            for bid in data["bids"]:
                bid_data: BidData = BidData(
                    bid_price=bid[0],
                    bid_volume=bid[1]
                )
                depth_data.bid_data.append(bid_data)

            for ask in data["asks"]:
                ask_data: AskData = AskData(
                    ask_price=ask[0],
                    ask_volume=ask[1]
                )
                depth_data.ask_data.append(ask_data)

        return depth_data

    # 开始ws 交易数据推送
    def start_user_stream(self) -> None:
        """获取ws listen key 帮助重新连接ws """
        data: dict = {
            "security": Security.API_KEY
        }

        path: str = "/fapi/v1/listenKey"

        self.add_request(
            method="POST",
            path=path,
            callback=self.on_start_user_stream,
            on_failed=self.on_start_user_stream_failed,
            on_error=self.on_start_user_stream_error,
            data=data
        )

    # 撤销订单成功回调
    def on_cancel_order(self, data: dict, request: Request) -> None:
        key: Tuple[str, str] = (data.get("type"), data.get("timeInForce"))
        order_type: OrderType = ORDERTYPE_BINANCES2VT.get(key, OrderType.LIMIT)

        traded = float(data.get("executedQty", "0"))
        traded_price = float(data.get('avgPrice', '0'))

        price = float(data["price"])
        if price <= 0 < traded_price:
            price = traded_price

        order: OrderData = OrderData(
            orderid=data.get("clientOrderId"),
            symbol=data.get("symbol"),
            price=price,
            volume=float(data.get("origQty")),
            traded=traded,
            traded_price=traded_price,
            type=order_type,
            direction=DIRECTION_BINANCES2VT.get(data.get("side")),
            status=STATUS_BINANCES2VT.get(data.get("status"), Status.CANCELLED),
            datetime=generate_datetime(float(data.get("updateTime", time.time() * 1000))),
        )
        self.gateway.on_order(order)

    # 撤销订单失败回调
    def on_cancel_order_failed(self, status_code: int, request: Request) -> None:
        self.failed_with_timestamp(request)
        orderid = ""
        if request.extra:
            order: OrderData = copy(request.extra)
            orderid = order.orderid
            order.status = Status.REJECTED
            self.gateway.on_order(copy(order))

        msg = f"撤销订单失败, orderid: {orderid}, status code：{status_code}, msg：{request.response.text}"
        print(msg)

    # 延长ws 数据保持时间
    def keep_user_stream(self) -> None:
        """延长 listenKey 过期时间"""
        self.keep_alive_count += 1
        if self.keep_alive_count < 300:
            return None

        self.keep_alive_count = 0

        data: dict = {
            "security": Security.API_KEY
        }

        params: dict = {
            "listenKey": self.user_stream_key
        }

        path: str = "/fapi/v1/listenKey"

        self.add_request(
            method="PUT",
            path=path,
            callback=self.on_keep_user_stream,
            params=params,
            data=data,
            on_failed=self.on_keep_user_stream_failed,
            on_error=self.on_keep_user_stream_error
        )

    # 查询服务器时间成功回调
    def on_query_time(self, data: dict, request: Request) -> None:
        """查询服务器时间回调"""
        local_time: int = int(time.time() * 1000)
        server_time: int = int(data["serverTime"])
        self.time_offset: int = local_time - server_time

    # 查询服务器时间失败回调
    def on_query_time_failed(self, status_code: int, request: Request):
        self.query_time()

    # 查询服务器时间错误回调
    def on_query_time_error(self, exception_type: type, exception_value: Exception, tb, request: Request) -> None:
        self.query_time()

    # 发送订单成功回调
    def on_send_order(self, data: dict, request: Request) -> None:
        pass

    # 发送订单失败回调
    def on_send_order_failed(self, status_code: int, request: Request) -> None:
        self.failed_with_timestamp(request)
        if request.extra:
            order: OrderData = copy(request.extra)
            order.status = Status.REJECTED
            order.rejected_reason = request.response.text if request.response.text else ""
            self.gateway.on_order(order)

            msg: str = f"发送订单失败, orderid: {order.orderid}, status code：{status_code}, msg：{request.response.text}"
            print(msg)

    # 发送订单错误回调
    def on_send_order_error(
            self, exception_type: type, exception_value: Exception, tb, request: Request
    ) -> None:
        if request.extra:
            order: OrderData = copy(request.extra)
            order.status = Status.REJECTED
            order.rejected_reason = "on_send_order_error"
            self.gateway.on_order(order)

        if not issubclass(exception_type, (ConnectionError, SSLError)):
            self.on_error(exception_type, exception_value, tb, request)

    # 开始获取ws stream 回调
    def on_start_user_stream(self, data: dict, request: Request) -> None:
        """查询listenkey回调，然后连接trade ws"""
        # 成功获取，记录该参数
        self.user_stream_key = data["listenKey"]
        self.keep_alive_count = 0

        url = F_WEBSOCKET_TRADE_HOST + self.user_stream_key
        self.trade_ws_api.connect(url, self.proxy_host, self.proxy_port)

    # 开始获取ws stream 失败处理
    def on_start_user_stream_failed(self, status_code: int, request: Request):
        print("binance 获取 start_user_stream 失败，重新获取")
        self.failed_with_timestamp(request)  # 重新获取服务器时间撮
        self.start_user_stream()  # 再次链接

    # 开始获取ws stream 错误处理
    def on_start_user_stream_error(self, exception_type: type, exception_value: Exception, tb, request: Request):
        print("binance 获取 start_user_stream 错误，重新获取")
        self.start_user_stream()  # 再次链接

    # 延长监听密钥过期时间请求回调
    def on_keep_user_stream(self, data: dict, request: Request) -> None:
        print("binance 保持 start_user_stream 成功")
        self.keep_alive_failed_count = 0

    # 延长监听密钥过期失败回处理
    def on_keep_user_stream_failed(self, status_code: int, request: Request):
        self.failed_with_timestamp(request)
        self.keep_alive_failed_count += 1
        if self.keep_alive_failed_count <= 3:
            print("binance 保持 start_user_stream 失败，重新 发送延长 请求")
            self.keep_alive_count = 1200000
            self.keep_user_stream()
        else:
            print("binance 保持 start_user_stream 失败 次数过多，重新获取，链接交易ws")
            self.keep_alive_failed_count = 0
            self.start_user_stream()

    # 延长监听密钥过期错误回调处理
    def on_keep_user_stream_error(
            self, exception_type: type, exception_value: Exception, tb, request: Request
    ) -> None:
        print("binance 保持 start_user_stream 出现错误，重新获取")
        self.keep_alive_failed_count += 1
        if self.keep_alive_failed_count <= 3:
            self.keep_alive_count = 1200000
            self.keep_user_stream()
        else:
            self.keep_alive_failed_count = 0
            self.start_user_stream()

        if not issubclass(exception_type, TimeoutError):
            self.on_error(exception_type, exception_value, tb, request)

    # 因为时间撮失败
    def failed_with_timestamp(self, request: Request):
        try:
            if request and request.response and request.response.text:
                resp = json.loads(request.response.text)
                if resp.get('code') == -1021:
                    self.query_time()
        except Exception:
            pass


class BinanceUsdtTradeWebsocketApi(WebsocketClient):

    def __init__(self, gateway: BinanceFutureUsdtGateway) -> None:
        super().__init__()

        self.gateway: BinanceFutureUsdtGateway = gateway
        self.ping_max_num = 4 * 60
        self.ping_count = 0

    def connect(self, url: str, proxy_host: str, proxy_port: int) -> None:
        """连接 binance usdt/busd 期货交易 ws"""
        self.init(url, proxy_host, proxy_port)
        self.start()

    def ping_pong(self, event: Event):
        if self.ping_count > self.ping_max_num:
            self.send_packet(send_pong=True)
            self.ping_count = 0
        else:
            self.ping_count += 1

    def on_connected(self) -> None:
        pass

    def on_packet(self, packet: dict) -> None:
        """从 ws 接收数据s"""
        if packet["e"] == "ORDER_TRADE_UPDATE":
            self.on_order(packet)

    def on_exit_loop(self):
        """ws 连接环"""
        self.gateway.rest_api.start_user_stream()

    # 订单ws 推送
    def on_order(self, packet: dict) -> None:
        ord_data: dict = packet["o"]
        key: Tuple[str, str] = (ord_data["o"], ord_data["f"])
        order_type: OrderType = ORDERTYPE_BINANCES2VT.get(key, OrderType.LIMIT)
        price = float(ord_data["p"])  # 订单原始价格
        if price <= 0:
            price = float(ord_data['ap'])  # 订单平均价格

        order: OrderData = OrderData(
            symbol=ord_data["s"],  # 交易对
            exchange=Exchange.BINANCE,
            orderid=str(ord_data["c"]),  # 客户端自定订单ID
            type=order_type,
            direction=DIRECTION_BINANCES2VT[ord_data["S"]],  # 订单方向
            price=price,
            volume=float(ord_data["q"]),  # 订单原始数量
            traded=float(ord_data["z"]),  # 订单累计已成交量
            traded_volume=float(ord_data.get("l", "0")),  # 订单末次成交量
            traded_price=float(ord_data.get("L", "0")),  # 订单末次成交价格
            status=STATUS_BINANCES2VT.get(ord_data["X"], Status.NOTTRADED),
            datetime=generate_datetime(packet["E"]),
        )

        self.gateway.on_order(order)


class BinanceUsdtDataWebsocketApi(WebsocketClient):

    def __init__(self, gateway: BinanceFutureUsdtGateway) -> None:
        """"""
        super().__init__()

        self.gateway: BinanceFutureUsdtGateway = gateway
        self.ticks: Dict[str, TickData] = {}
        self.bars: Dict[str, BarData] = {}
        self.reqid: int = 0

        self.ping_max_num = 4 * 60
        self.ping_count = 0

    def connect(
            self,
            proxy_host: str,
            proxy_port: int,
    ) -> None:
        """连接ws数据"""
        self.init(F_WEBSOCKET_DATA_HOST, proxy_host, proxy_port)
        self.start()

    def ping_pong(self, event: Event):
        if self.ping_count > self.ping_max_num:
            self.send_packet(send_pong=True)
            self.ping_count = 0
        else:
            self.ping_count += 1

    def on_connected(self) -> None:
        channels = []
        for target in self.bars:
            channels.append(target)

        for target in self.ticks:
            channels.append(target)

        if channels:
            req: dict = {
                "method": "SUBSCRIBE",
                "params": channels,
                "id": self.reqid
            }
            self.send_packet(packet=req)

    def subscribe(self, symbol: str, interval: Interval = None) -> None:
        """订阅数据"""
        # 如果间隔参数不为 None, 那么就是订阅K线数据
        if interval:
            target = f"{symbol.lower()}@kline_{interval.value}"
            # 订阅 K线 流程
            if target in self.bars:
                return
            self.reqid += 1
            bar: BarData = BarData(
                symbol=symbol,
                datetime=datetime.now(),
                endTime=datetime.now(),
                interval=interval,
                exchange=self.gateway.exchange,
                product=self.gateway.product
            )
            self.bars[target] = bar

        else:
            target = f"{symbol.lower()}@aggTrade"

            # 订阅tick 数据流程
            if symbol in self.ticks:
                return
            self.reqid += 1
            tick: TickData = TickData(
                symbol=symbol,
                datetime=datetime.now(),
                exchange=self.gateway.exchange,
                product=self.gateway.product
            )
            self.ticks[target] = tick

        req: dict = {
            "method": "SUBSCRIBE",
            "params": [target],
            "id": self.reqid
        }
        self.send_packet(packet=req)

    def on_packet(self, packet: dict):
        stream: str = packet.get("stream", None)
        if not stream:
            return

        data: dict = packet["data"]

        symbol, channel = stream.split("@")
        bar: BarData = self.bars.get(stream)
        tick: TickData = self.ticks.get(stream)

        if channel.startswith("kline_"):
            data = data['k']
            if data['x']:
                bar.volume = float(data['v'])
                bar.turnover = float(data['q'])
                bar.open_price = float(data['o'])
                bar.high_price = float(data['h'])
                bar.low_price = float(data['l'])
                bar.close_price = float(data['c'])
                bar.datetime = generate_datetime(float(data['t']))
                bar.endTime = generate_datetime(float(data['T']))
                self.gateway.on_bar(copy(bar))

        elif channel == "aggTrade":
            # tick.volume = float(data['v'])
            # tick.turnover = float(data['q'])
            # tick.open_price = float(data['o'])
            # tick.high_price = float(data['h'])
            # tick.low_price = float(data['l'])
            tick.last_price = float(data['p'])
            tick.datetime = generate_datetime(float(data['T']))

            if tick.last_price:
                tick.localtime = datetime.now()
                self.gateway.on_tick(copy(tick))


def generate_datetime(timestamp: float) -> datetime:
    """generate time"""
    dt: datetime = datetime.fromtimestamp(timestamp / 1000)
    return dt
