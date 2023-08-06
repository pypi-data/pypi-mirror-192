"""
1. 只支持单币种保证金模式
2. 只支持全仓模式
3. 只支持单向持仓模式
"""
import base64
import hashlib
import hmac
import json
import time
from copy import copy
from datetime import datetime, timedelta
from threading import Lock
from types import TracebackType
from typing import Any, Dict, List, Tuple

# 实盘 API地址
from urllib.parse import urlencode

from strategy_api.event.engine import EventEngine, EVENT_TIMER, Event
from strategy_api.tm_api.api.rest.rest_client import RestClient, Request, Response
from strategy_api.tm_api.api.websocket.websocket_client import WebsocketClient
from strategy_api.tm_api.base import BaseGateway
from strategy_api.tm_api.object import Status, OrderType, Direction, Interval, TickData, BarData, Product, ContractData, \
    Exchange, DataType, HistoryRequest, PositionSide, OrderRequest, Offset, OrderData, CancelRequest, TdMode, \
    WithDrawData, Dest, Chain, TransferType, TransferRequest, DepthData, BidData, AskData, PositionData, BillInterest
from strategy_api.tm_api.tools import get_order_type, symbol_deal

REST_HOST: str = "https://www.okx.com"

# 实盘Websocket API地址
PUBLIC_WEBSOCKET_HOST: str = "wss://ws.okx.com:8443/ws/v5/public"
PRIVATE_WEBSOCKET_HOST: str = "wss://ws.okx.com:8443/ws/v5/private"

# 委托状态映射
STATUS_OKEX2VT: Dict[str, Status] = {
    "live": Status.NOTTRADED,
    "effective": Status.ALLTRADED,
    "partially_filled": Status.PARTTRADED,
    "filled": Status.ALLTRADED,
    "canceled": Status.CANCELLED
}

# 委托类型映射
ORDERTYPE_OKEX2VT: Dict[str, OrderType] = {
    "limit": OrderType.LIMIT,
    "market": OrderType.MARKET,
    "conditional": OrderType.MARKET,
    "oco": OrderType.STOP_LOSS_PROFIT
}
ORDERTYPE_VT2OKEX: Dict[OrderType, str] = {v: k for k, v in ORDERTYPE_OKEX2VT.items()}

# 买卖方向映射
DIRECTION_OKEX2VT: Dict[str, Direction] = {
    "buy": Direction.LONG,
    "sell": Direction.SHORT
}
DIRECTION_VT2OKEX: Dict[Direction, str] = {v: k for k, v in DIRECTION_OKEX2VT.items()}

# 交易模式映射
TDMODE_OKEX2VT: Dict[str, TdMode] = {
    "cross": TdMode.CROSS,
    "isolated": TdMode.ISOLATED
}

TRANSFERTYPE_VT2OKEX: Dict[TransferType, Tuple[str, str]] = {
    TransferType.OKE_CAPITAL_TRADE: ("6", "18"),
    TransferType.OKE_TRADE_CAPITAL: ("18", "6")
}

TDMODE_VT2OKEX: Dict[TdMode, str] = {v: k for k, v in TDMODE_OKEX2VT.items()}

DEST_OKEXVT2OKEX: Dict[str, Dest] = {
    "3": Dest.INTERNAL,
    "4": Dest.CHAIN
}

DEST_VT2OKEX: Dict[Dest, str] = {v: k for k, v in DEST_OKEXVT2OKEX.items()}

# 合约数据全局缓存字典
symbol_contract_map: Dict[str, ContractData] = {}

INTERVAL_VT2OKEX: Dict[Interval, str] = {
    Interval.MINUTE: "1m",
    Interval.MINUTE_3: "3m",
    Interval.MINUTE_5: "5m",
    Interval.MINUTE_15: "15m",
    Interval.MINUTE_30: "30m",
    Interval.HOUR: "1H",
    Interval.HOUR_2: "2H",
    Interval.HOUR_4: "4H",
}


class OkexGateway(BaseGateway):
    """
    vn.py用于对接OKEX统一账户的交易接口。
    """

    default_setting: Dict[str, Any] = {
        "key": "",
        "secret": "",
        "Passphrase": "",
        "proxy_host": "",
        "proxy_port": 0,
    }
    exchange: Exchange = Exchange.OKEX
    product: Product = Product.U_FUTURES
    symbolMap: dict = dict()
    SPOT_SET: set = set()
    MARGIN_SET: set = set()
    SWAP_SET: set = set()

    def __init__(self, event_engine: EventEngine, order_switch: bool = False, bar_switch: bool = False,
                 tick_switch: bool = False) -> None:
        """init"""
        super().__init__(event_engine, order_switch, bar_switch, tick_switch)

        self.market_ws_api: "OkexWebsocketPublicApi" = OkexWebsocketPublicApi(self)
        self.trade_ws_api: "OkexWebsocketPrivateApi" = OkexWebsocketPrivateApi(self)
        self.rest_api: "OkexRestApi" = OkexRestApi(self)

        self.fail_send_order: int = 0

    def connect(self, setting: dict) -> None:
        """连接交易接口"""
        key: str = setting["key"]
        secret: str = setting["secret"]
        passphrase: str = setting["Passphrase"]

        if isinstance(setting["proxy_host"], str):
            proxy_host: str = setting["proxy_host"]
        else:
            proxy_host: str = ""

        if isinstance(setting["proxy_port"], int):
            proxy_port: int = setting["proxy_port"]
        else:
            proxy_port: int = 0

        self.rest_api.connect(
            key,
            secret,
            passphrase,
            proxy_host,
            proxy_port,
        )

        self.market_ws_api.connect(
            proxy_host,
            proxy_port
        )
        if self.order_call_switch:
            self.trade_ws_api.connect(
                key,
                secret,
                passphrase,
                proxy_host,
                proxy_port,
            )

            self.event_engine.unregister(EVENT_TIMER, self.trade_ws_api.ping_pong)
            self.event_engine.register(EVENT_TIMER, self.trade_ws_api.ping_pong)

        self.event_engine.unregister(EVENT_TIMER, self.market_ws_api.ping_pong)
        self.event_engine.register(EVENT_TIMER, self.market_ws_api.ping_pong)

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
            interval=interval
        )
        return self.rest_api.query_history(req)

    def query_orders(self, symbol: str) -> List[OrderData]:
        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol
        return self.rest_api.query_orders(new_symbol, s_type=symbol)

    def query_order(self, symbol: str, orderId: str) -> OrderData:
        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol
        return self.rest_api.query_order(new_symbol, orderId, s_type=symbol)

    def cancel_all_order(self, symbol) -> bool:
        print("OKEX 没有该接口")
        return False

    def query_position(self, symbol: str) -> List[PositionData]:
        """query position"""
        new_symbol = symbol_deal(symbol, self.exchange)
        if "MARGIN" in symbol:
            s_type = "MARGIN"
        elif "PERP" in symbol or "SWAP" in new_symbol:
            s_type = "SWAP"
        else:
            return []
        self.symbolMap[new_symbol] = symbol
        return self.rest_api.query_position(new_symbol, s_type)

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

    def query_symbol(self, quote_symbol: str, s_type: str = "") -> list:
        if s_type == "SPOT":
            return [i for i in self.SPOT_SET if i.endswith(quote_symbol.upper())]
        elif s_type == "MARGIN":
            return [i for i in self.MARGIN_SET if i.endswith(quote_symbol.upper())]
        else:
            quote_symbol += "-SWAP"
            return [i.replace("-SWAP", "") for i in self.SWAP_SET if i.endswith(quote_symbol.upper())]

    def query_rate(self) -> dict:
        return self.rest_api.query_rate()

    def new_order_id(self) -> str:
        return self.rest_api.get_order_id()

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
            reference=symbol,
            ccy=ccy,
            tdMode=tdMode
        )
        return self.send_order(original_req, orderid)

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
            reference=symbol,
            ccy=ccy,
            tdMode=tdMode
        )
        return self.send_order(original_req, orderid)

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
            reference=symbol,
            ccy=ccy,
            tdMode=tdMode
        )
        return self.send_order(original_req, orderid)

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
            reference=symbol,
            ccy=ccy,
            tdMode=tdMode
        )
        return self.send_order(original_req, orderid)

    def withdraw_coin(self, symbol: str,  # 币种
                      amount: float,  # 数量
                      dest: Dest,  # 提币方式
                      toAddress: str,  # 提币地址（手机）
                      fee: float,  # 手续费设置
                      chain: Chain,  # 链
                      areaCode: str = ""  # 手机区号
                      ) -> bool:

        req: WithDrawData = WithDrawData(
            symbol=symbol,
            amount=str(amount),
            dest=dest,
            toAddress=toAddress,
            fee=str(fee),
            chain=chain,
            areaCode=areaCode
        )
        return self.rest_api.withdraw_coin(req)

    def transfer_coin(self, type: TransferType,
                      symbol: str,
                      amount: float,
                      fromSymbol: str = "",
                      toSymbol: str = "",
                      ) -> bool:
        req: TransferRequest = TransferRequest(
            type=type,
            symbol=symbol,
            amount=amount,
            fromSymbol=fromSymbol,
            toSymbol=toSymbol,
        )

        return self.rest_api.transfer_coin(req)

    # 发送订单
    def send_order(self, req: OrderRequest, orderid: str):
        self.fail_send_order = 0
        self.rest_api.send_order(req, orderid)

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

    # 查询账单
    def query_bill(self, symbol: str, start: datetime, end: datetime) -> List[BillInterest]:
        return self.rest_api.query_bill(symbol, start, end)

    def close(self) -> None:
        """关闭连接"""
        self.rest_api.stop()
        self.trade_ws_api.stop()
        self.market_ws_api.stop()


class OkexRestApi(RestClient):
    """"""

    def __init__(self, gateway: OkexGateway) -> None:
        """构造函数"""
        super().__init__()

        self.gateway: OkexGateway = gateway

        self.key: str = ""
        self.secret: str = ""
        self.passphrase: str = ""
        self.simulated: bool = False

        self.order_count: int = 0
        self.connect_time: int = 0

    def sign(self, request: Request) -> Request:
        """生成欧易V5签名"""
        # 签名
        timestamp: str = generate_timestamp()
        request.data = json.dumps(request.data)

        if request.params:
            path: str = request.path + "?" + urlencode(request.params)
        else:
            path: str = request.path

        msg: str = timestamp + request.method + path + request.data
        signature: bytes = generate_signature(msg, self.secret)

        # 添加请求头
        request.headers = {
            "OK-ACCESS-KEY": self.key,
            "OK-ACCESS-SIGN": signature.decode(),
            "OK-ACCESS-TIMESTAMP": timestamp,
            "OK-ACCESS-PASSPHRASE": self.passphrase,
            "Content-Type": "application/json"
        }

        if self.simulated:
            request.headers["x-simulated-trading"] = "1"

        return request

    def connect(
            self,
            key: str,
            secret: str,
            passphrase: str,
            proxy_host: str,
            proxy_port: int,
    ) -> None:
        """连接REST服务器"""
        self.key = key
        self.secret = secret.encode()
        self.passphrase = passphrase

        self.connect_time = int(datetime.now().strftime("%y%m%d%H%M%S"))

        self.init(REST_HOST, proxy_host, proxy_port)
        self.start()
        print("OKEX REST API启动成功")

        self.query_time()
        self.query_contract()

    def query_contract(self):

        self.add_request(
            method="GET",
            path="/api/v5/public/instruments?instType=SPOT",
            callback=self.on_query_spot_contract,
        )

        self.add_request(
            method="GET",
            path="/api/v5/public/instruments?instType=MARGIN",
            callback=self.on_query_margin_contract,
        )

        self.add_request(
            method="GET",
            path="/api/v5/public/instruments?instType=SWAP",
            callback=self.on_query_swap_contract,
        )

    def query_time(self) -> None:
        """查询时间"""
        self.add_request(
            "GET",
            "/api/v5/public/time",
            callback=self.on_query_time
        )

    def query_order(self, symbol: str, orderId: str, s_type: str = "") -> OrderData:
        path = "/api/v5/trade/order"

        params = {
            "instId": symbol.upper(),
            "clOrdId": orderId
        }

        resp: Response = self.request(
            "GET",
            path=path,
            params=params
        )

        if resp.status_code // 100 != 2:
            msg: str = f"查询 {orderId} 订单失败, status code：{resp.status_code}，msg：{resp.text}"
            print(msg)
        else:
            data = resp.json()
            if int(data['code']) != 0:
                msg: str = f"查询 {orderId} 订单失败, status code：{data['code']}，msg：{data['msg']}"
                print(msg)
                return None
            for i in data['data']:
                if i.get("fillPx") == "":
                    fillPx = 0
                else:
                    fillPx = float(i['fillPx'])
                order: OrderData = OrderData(
                    symbol=self.gateway.symbolMap[symbol],  # 交易对
                    orderid=str(i["clOrdId"]),  # 订单id
                    type=ORDERTYPE_OKEX2VT.get(i['ordType'], OrderType.LIMIT),
                    direction=DIRECTION_OKEX2VT[i["side"]],  # 订单方向
                    price=float(i['px']),  # 价格
                    volume=float(i["sz"]),  # 订单原始数量
                    traded=float(i["accFillSz"]),  # 订单累计已成交量
                    traded_volume=float(i['fillSz']),  # 订单末次成交量
                    traded_price=fillPx,  # 订单末次成交价格
                    status=STATUS_OKEX2VT.get(i['state'], Status.NOTTRADED),
                    datetime=generate_datetime(i["cTime"]),
                )
                return order

    def query_orders(self, symbol: str, s_type: str = "") -> List[OrderData]:
        buf: List[OrderData] = []
        path = "/api/v5/trade/orders-pending"

        params = {
            "instId": symbol.upper(),
        }
        resp: Response = self.request(
            "GET",
            path=path,
            params=params
        )
        if resp.status_code // 100 != 2:
            msg: str = f"查询 {self.gateway.symbolMap[symbol]} 所有订单失败, status code：{resp.status_code}，msg：{resp.text}"
            print(msg)
            return []
        else:
            data = resp.json()
            if int(data['code']) != 0:
                msg: str = f"查询 {self.gateway.symbolMap[symbol]} 订单失败, status code：{data['code']}，msg：{data['msg']}"
                print(msg)
                return []

            for i in data['data']:
                if i.get("fillPx") == "":
                    fillPx = 0
                else:
                    fillPx = float(i['fillPx'])
                order: OrderData = OrderData(
                    symbol=self.gateway.symbolMap[symbol],  # 交易对
                    orderid=str(i["clOrdId"]),  # 订单id
                    type=ORDERTYPE_OKEX2VT.get(i['ordType'], OrderType.LIMIT),
                    direction=DIRECTION_OKEX2VT[i["side"]],  # 订单方向
                    price=float(i['px']),  # 价格
                    volume=float(i["sz"]),  # 订单原始数量
                    traded=float(i["accFillSz"]),  # 订单累计已成交量
                    traded_volume=float(i['fillSz']),  # 订单末次成交量
                    traded_price=fillPx,  # 订单末次成交价格
                    status=STATUS_OKEX2VT.get(i['state'], Status.NOTTRADED),
                    datetime=generate_datetime(i["cTime"]),
                )
                buf.append(order)
            return buf

    def query_bill(self, symbol: str, start: datetime, end: datetime) -> List[BillInterest]:
        buf: Dict[datetime, BillInterest] = {}
        limit: int = 100
        start_time: str = str(int(time.mktime(start.timetuple()) * 1000))
        end_time: str = str(int(time.mktime(end.timetuple()) * 1000))
        path: str = "/api/v5/account/bills-archive"

        while True:
            params = {
                "instType": "MARGIN",
                "ccy": symbol,
                "type": "7",
                "limit": limit
            }
            if end_time:
                params['end'] = end_time
            if start_time:
                params['begin'] = start_time

            resp: Response = self.request(
                method="GET",
                path=path,
                params=params
            )
            # 如果请求失败则终止循环
            if resp.status_code // 100 != 2:
                msg = f"获取历史账户失败，状态码：{resp.status_code}，信息：{resp.text}"
                print(msg)
                break
            else:
                data: dict = resp.json()
                if not data["data"]:
                    m = data["msg"]
                    msg = f"获取历史数据为空，{m}"
                    print(msg)
                    break
                for i in data["data"]:
                    bill: BillInterest = BillInterest(
                        exchange=Exchange.OKEX,  # 交易所
                        datetime=generate_datetime(i['ts']),
                        coin=i['ccy'],  # 币种
                        symbol=i['instId'],  # 交易对
                        tdMode=TDMODE_OKEX2VT[i.get('mgnMode')],  # 仓位类型
                        volume=float(i['sz']),  # 数量
                        fee=float(i['fee']),  # 手续费
                        profit=float(i['pnl']),  # 收益
                        posBalanceChange=float(i['posBalChg']),  # 仓位余额变动
                        posBalance=float(i['posBal']),  # 仓位余额
                        accountBalanceChange=float(i['balChg']),  # 账户余额变动
                        accountBalance=float(i['bal']),  # 账户余额
                    )
                    buf[bill.datetime] = bill
                begin: str = data["data"][-1]['ts']
                if len(data) < limit:
                    break
                # # 更新结束时间
                end_time = begin
            time.sleep(0.5)
        index: List[datetime] = list(buf.keys())
        index.sort()

        history: List[BillInterest] = [buf[i] for i in index]
        return history

    def on_query_spot_contract(self, data: dict, request: Request) -> None:
        for d in data["data"]:
            self.gateway.SPOT_SET.add(d['instId'])

    def on_query_margin_contract(self, data: dict, request: Request) -> None:
        for d in data["data"]:
            self.gateway.MARGIN_SET.add(d['instId'])

    def on_query_swap_contract(self, data: dict, request: Request) -> None:
        for d in data["data"]:
            self.gateway.SWAP_SET.add(d['instId'])

    def on_query_time(self, packet: dict, request: Request) -> None:
        """时间查询回报"""
        timestamp: int = int(packet["data"][0]["ts"])
        server_time: datetime = datetime.fromtimestamp(timestamp / 1000)
        local_time: datetime = datetime.now()
        msg: str = f"服务器时间：{server_time}，本机时间：{local_time}"

    def on_error(
            self,
            exception_type: type,
            exception_value: Exception,
            tb: TracebackType,
            request: Request
    ) -> None:
        """触发异常回报"""
        msg: str = f"触发异常，状态码：{exception_type}，信息：{exception_value}"
        print(msg)

    def query_history(self, req: HistoryRequest) -> List[BarData]:
        """
        查询历史数据
        K线数据每个粒度最多可获取最近1440条
        """
        buf: Dict[datetime, BarData] = {}
        start_time: str = str(int(time.mktime(req.start.timetuple()) * 1000))
        end_time: str = str(int(time.mktime(req.end.timetuple()) * 1000))

        limit: int = 300
        path: str = "/api/v5/market/candles"

        while True:
            # 创建查询参数
            params: dict = {
                "instId": req.symbol,
                "bar": INTERVAL_VT2OKEX[req.interval],
                "limit": limit
            }

            if end_time:
                params["after"] = end_time
            if start_time:
                params["before"] = start_time

            # 从服务器获取响应
            resp: Response = self.request(
                "GET",
                path,
                params=params
            )

            # 如果请求失败则终止循环
            if resp.status_code // 100 != 2:
                msg = f"获取历史数据失败，状态码：{resp.status_code}，信息：{resp.text}"
                print(msg)
                break
            else:
                data: dict = resp.json()

                if not data["data"]:
                    m = data["msg"]
                    msg = f"获取历史数据为空，{m}"
                    print(msg)
                    break

                for bar_list in data["data"]:
                    bar: BarData = BarData(
                        symbol=self.gateway.symbolMap[req.symbol],
                        exchange=self.gateway.exchange,
                        volume=float(bar_list[5]),
                        turnover=float(bar_list[7]),
                        open_price=float(bar_list[1]),
                        high_price=float(bar_list[2]),
                        low_price=float(bar_list[3]),
                        close_price=float(bar_list[4]),
                        datetime=generate_datetime(bar_list[0]),
                        endTime=generate_datetime(bar_list[0])
                    )
                    bar.endTime = None
                    buf[bar.datetime] = bar

                begin: str = data["data"][-1][0]
                end: str = data["data"][0][0]
                msg: str = f"获取历史数据成功，{req.symbol} - {req.interval.value}，{generate_datetime(begin)} - {generate_datetime(end)}"
                if len(data) < limit:
                    break
                # # 更新结束时间
                end_time = begin
            time.sleep(0.5)

        index: List[datetime] = list(buf.keys())
        index.sort()

        history: List[BarData] = [buf[i] for i in index]
        return history

    def query_position(self, symbol: str, s_type: str) -> List[PositionData]:
        """query position"""
        pos_l = []

        params = {
            "instType": s_type,
            "instId": symbol
        }
        resp: Response = self.request(
            method="GET",
            path="/api/v5/account/positions",
            params=params
        )
        if resp.status_code // 100 != 2:
            msg: str = f"查询仓位数据是比, status code：{resp.status_code}，msg：{resp.text}"
            print(msg)
        else:
            data: dict = resp.json()
            for d in data['data']:
                try:
                    if d['pos'] == '0':
                        continue
                    position: PositionData = PositionData(
                        symbol=self.gateway.symbolMap[symbol],
                        exchange=Exchange.OKEX,
                        volume=float(d["pos"]),
                        price=float(d["avgPx"]),
                        mark_price=float(d['markPx']),
                        liquidation_price=None,
                        leverage=int(d['lever']),
                        pnl=float(d["upl"]),
                    )
                except Exception:
                    continue
                if d['liqPx']:
                    position.liquidation_price = float(d['liqPx'])
                pos_l.append(position)
                break
            return pos_l

    def query_depth(self, symbol: str, limit: int, depth_data: DepthData) -> DepthData:
        params: dict = {
            "instId": symbol,
            "sz": str(limit)
        }

        resp: Response = self.request(
            "GET",
            "/api/v5/market/books",
            params=params
        )
        if resp.status_code // 100 != 2:
            msg: str = f"查询depth数据失败, status code：{resp.status_code}，msg：{resp.text}"
            print(msg)
        else:
            data: dict = resp.json()
            data = data['data'][0]
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

    def get_order_id(self) -> str:
        self.order_count += 1
        count_str = str(self.order_count).rjust(6, "0")
        orderid = f"{self.connect_time}{count_str}"
        return orderid

    def withdraw_coin(self, req: WithDrawData) -> bool:
        asset_path = "/api/v5/asset/currencies"
        resp: Response = self.request(
            "GET",
            asset_path,
            params={
                "ccy": req.symbol,
            }
        )
        if resp.status_code // 100 != 2:
            msg = f"获取资产信息失败，状态码：{resp.status_code}，信息：{resp.text}"
            print(msg)
        else:
            data: dict = resp.json()
            whole_chain = req.symbol + "-" + req.chain.value
            path = "/api/v5/asset/withdrawal"
            for d in data['data']:
                if whole_chain == d['chain']:
                    if float(d['minWd']) > float(req.amount):
                        print("提币数量少于最小提币数量")
                        return False

                    if float(d['maxWd']) < float(req.amount):
                        print("提币数量大于最大提币数量")
                        return False

                    if float(d['minFee']) > float(req.fee):
                        print("手续费设置小于最小手续费")
                        return False

                    if float(d['maxFee']) < float(req.fee):
                        print("手续费设置大于最大手续费")
                        return False

                    params: dict = {
                        "ccy": req.symbol,
                        "amt": req.amount,
                        "dest": DEST_VT2OKEX[req.dest],
                        "toAddr": req.toAddress,
                        "fee": req.fee,
                        "chain": whole_chain,
                        "areaCode": req.areaCode,
                    }

                    self.add_request(
                        method="POST",
                        path=path,
                        callback=self.on_withdraw_coin,
                        data=params,
                    )
                    return True
        return False

    def transfer_coin(self, req: TransferRequest) -> bool:
        path: str = "/api/v5/asset/transfer"
        from_account, to_account = TRANSFERTYPE_VT2OKEX.get(req.type)
        if from_account:
            params: dict = {
                "ccy": req.symbol,  # 币种
                "amt": req.amount,  # 自定义提币ID
                "from": from_account,  # 转出账户
                "to": to_account,  # 转入账户
            }
            self.add_request(
                method="POST",
                path=path,
                callback=self.on_withdraw_coin,
                data=params
            )
            return True
        else:
            print("账户选择错误")

    def query_rate(self) -> dict:
        buf = {}
        resp: Response = self.request(
            "GET",
            "/api/v5/public/interest-rate-loan-quota",
        )
        if resp.status_code // 100 != 2:
            msg: str = f"查询接币杠杆利率失败, status code：{resp.status_code}，msg：{resp.text}"
            print(msg)
        else:
            data = resp.json()
            for i in data['data'][0]['basic']:
                buf[i['ccy']] = i['rate']
            return buf

    def send_order(self, req: OrderRequest, orderid: str):

        order: OrderData = req.create_order_data(
            orderid,
        )
        if req.positionSide == PositionSide.ONEWAY:
            params: dict = {
                "instId": req.symbol,  # 标的
                "tdMode": "cross",  # 交易模式
                "clOrdId": orderid,  # 用户定义的ID
                "side": DIRECTION_VT2OKEX[req.direction],  # 方向
                "sz": str(req.volume)  # 数量
            }
            if req.offset == Offset.CLOSE:
                params['reduceOnly'] = True
        else:
            if (req.direction == Direction.SHORT and req.offset == Offset.OPEN) or (
                    req.direction == Direction.LONG and req.offset == Offset.CLOSE):
                position_side = "short"
            else:
                position_side = "long"
            params: dict = {
                "instId": req.symbol,  # 标的
                "posSide": position_side,
                "tdMode": "cross",  # 交易模式
                "clOrdId": orderid,  # 用户定义的ID
                "side": DIRECTION_VT2OKEX[req.direction],  # 方向
                "sz": str(req.volume)  # 数量
            }

        if 'SPOT' in req.reference:
            # 币币交易需要的参数
            params['tdMode'] = 'cash'
            params['reduceOnly'] = False

        if 'MARGIN' in req.reference:
            # 杠杆交易
            params['tdMode'] = TDMODE_VT2OKEX[req.tdMode]
            params['ccy'] = req.ccy
        if req.type == OrderType.LIMIT:
            params['ordType'] = "limit"
            params['px'] = req.price  # 价格
        else:
            params['ordType'] = "market"

        path: str = "/api/v5/trade/order"

        if req.type == OrderType.STOP_LOSS_PROFIT:
            params['slTriggerPx'] = str(req.stop_loss_price)  # 止损触发价
            params['slOrdPx'] = '-1'  # 止损委托价,当为 -1 时。按市价止损
            params['tpTriggerPx'] = str(req.stop_profit_price)  # 止盈触发价
            params['tpOrdPx'] = '-1'  # 止盈委托价, 当为-1 时，按市价止盈
            params['ordType'] = "oco"
            path: str = "/api/v5/trade/order-algo"

        elif req.type == OrderType.STOP_MARKET:
            params['slTriggerPx'] = str(req.stop_loss_price)  # 止损触发价
            params['slOrdPx'] = '-1'  # 止损委托价,当为 -1 时。按市价止损
            params['ordType'] = "conditional"
            path: str = "/api/v5/trade/order-algo"

        elif req.type == OrderType.TAKE_PROFIT_MARKET:
            params['tpTriggerPx'] = str(req.stop_profit_price)  # 止盈触发价
            params['tpOrdPx'] = '-1'  # 止盈委托价, 当为-1 时，按市价止盈
            params['ordType'] = "conditional"
            path: str = "/api/v5/trade/order-algo"
        else:
            if params['ordType'] == "market" and "SPOT" in req.reference:
                params['tgtCcy'] = 'base_ccy'

        self.add_request(
            method="POST",
            path=path,
            callback=self.on_send_order,
            data=params,
            extra={'order': order, 'req': req, 'orderid': orderid},
            on_error=self.on_send_order_error,
            on_failed=self.on_send_order_failed
        )

    def cancel_order(self, req: CancelRequest) -> None:
        data: dict = {
            "instId": req.symbol,
            "clOrdId": req.orderid,
        }

        path: str = "/api/v5/trade/cancel-order"

        self.add_request(
            method="POST",
            path=path,
            callback=self.on_cancel_order,
            data=data,
            on_failed=self.on_cancel_order_failed,
        )

    # 发送订单成功回调
    def on_withdraw_coin(self, data: dict, request: Request) -> None:
        print(data)

    # 发送订单成功回调
    def on_send_order(self, data: dict, request: Request) -> None:
        if data['code'] != "0":
            if request.extra:
                order: OrderData = copy(request.extra['order'])
                order.status = Status.REJECTED  # 被拒绝
                order.rejected_reason = data['data'][0]['sMsg']  # 拒绝原因
                self.gateway.on_order(order)

    # 发送订单失败回调
    def on_send_order_failed(self, status_code: int, request: Request) -> None:
        order: OrderData = copy(request.extra['order'])
        order.status = Status.REJECTED  # 被拒绝
        order.rejected_reason = f"code: {status_code}, msg: {request.response.json().get('msg')}"  # 拒绝原因
        self.gateway.on_order(order)

    # 发送订单错误回调
    def on_send_order_error(
            self, exception_type: type, exception_value: Exception, tb, request: Request
    ) -> None:
        order: OrderData = copy(request.extra['order'])
        order.status = Status.REJECTED  # 被拒绝
        order.rejected_reason = repr(exception_value)  # 失败原因
        self.gateway.on_order(order)

    # 撤销订单成功回调
    def on_cancel_order(self, data: dict, request: Request) -> None:
        print(f"撤销订单成功: {request}")

    # 撤销订单失败
    def on_cancel_order_failed(self, status_code: int, request: Request) -> None:
        print(f"撤销订单失败: {request}")


class OkexWebsocketPublicApi(WebsocketClient):
    """"""

    def __init__(self, gateway: OkexGateway) -> None:
        """构造函数"""
        super().__init__()

        self.gateway: OkexGateway = gateway
        self.ticks: Dict[str, TickData] = {}
        self.bars: Dict[str, BarData] = {}

        self.ping_count = 0
        self.ping_max_num = 20

    def connect(
            self,
            proxy_host: str,
            proxy_port: int,
    ) -> None:
        """连接Websocket公共频道"""
        self.init(PUBLIC_WEBSOCKET_HOST, proxy_host, proxy_port, 20)
        self.start()

    def ping_pong(self, event: Event) -> None:
        if self.ping_count > self.ping_max_num:
            self.send_packet(packet="ping")
            self.ping_count = 0
        else:
            self.ping_count += 1

    def subscribe(self, symbol: str, interval: Interval = None) -> None:
        """订阅行情"""
        print("订阅行情")
        if interval:
            target = symbol + f"*{interval.value}"
            if target in self.bars:
                return
            bar: BarData = BarData(
                symbol=symbol,
                datetime=datetime.now(),
                endTime=datetime.now(),
                interval=interval,
                exchange=self.gateway.exchange,
                product=self.gateway.product
            )
            self.bars[target] = bar
            args = [
                {"channel": f"candle{interval.value}", "instId": symbol}
            ]
        else:
            if symbol in self.ticks:
                return
            tick: TickData = TickData(
                symbol=symbol,
                datetime=datetime.now(),
                exchange=self.gateway.exchange,
                product=self.gateway.product
            )
            self.ticks[symbol] = tick
            args = [
                {"channel": "tickers", "instId": symbol}
            ]

        req: dict = {
            "op": "subscribe",
            "args": args
        }
        self.send_packet(packet=req)

    def on_connected(self) -> None:
        """连接成功回报"""
        args = []
        for target in self.bars:
            symbol, interval = target.split("*")
            d = {"channel": f"candle{interval}", "instId": symbol}
            args.append(d)
        for target in self.ticks:
            d = {"channel": "tickers", "instId": target}
            args.append(d)
        if args:
            req: dict = {
                "op": "subscribe",
                "args": args
            }
            self.send_packet(packet=req)
        print("Okex Websocket Public API连接成功, 重新订阅")

    def on_disconnected(self) -> None:
        """连接断开回报"""
        print("Okex Websocket Public API连接断开")

    def on_packet(self, packet: dict) -> None:
        """推送数据回报"""

        self.ping_count = 0

        if packet == "pong":
            return

        if "event" in packet:
            event: str = packet["event"]
            if event == "subscribe":
                return
            elif event == "error":
                code: str = packet["code"]
                msg: str = packet["msg"]
                print(f"Okex Websocket Public API请求异常, 状态码：{code}, 信息：{msg}")
        else:
            channel: str = packet["arg"]["channel"]
            symbol: str = packet["arg"].get("instId")
            data: list = packet['data']
            if channel == "tickers":
                for d in data:
                    tick: TickData = self.ticks[symbol]
                    tick.last_price = float(d["last"])
                    tick.open_price = float(d["open24h"])
                    tick.high_price = float(d["high24h"])
                    tick.low_price = float(d["low24h"])
                    tick.volume = float(d["vol24h"])
                    if tick.last_price:
                        self.gateway.on_tick(copy(tick))

            elif channel.startswith("candle"):
                for d in data:
                    if d[8] == "1":
                        bar: BarData = self.bars[symbol + f"*{channel.split('e')[-1]}"]
                        bar.volume = float(d[5])
                        bar.turnover = float(d[7])
                        bar.open_price = float(d[1])
                        bar.high_price = float(d[2])
                        bar.low_price = float(d[3])
                        bar.close_price = float(d[4])
                        bar.datetime = generate_datetime(str(d[0]))
                        bar.endTime = None
                        self.gateway.on_bar(copy(bar))

    def on_error(self, exception_type: type, exception_value: Exception, tb) -> None:
        """触发异常回报"""
        msg: str = f"Okex 公共频道触发异常，类型：{exception_type}，信息：{exception_value}"
        print(msg)


class OkexWebsocketPrivateApi(WebsocketClient):
    """"""

    def __init__(self, gateway: OkexGateway) -> None:
        """构造函数"""
        super().__init__()

        self.gateway: OkexGateway = gateway

        self.key: str = ""
        self.secret: str = ""
        self.passphrase: str = ""
        self.login_tag: bool = False
        self.reqid: int = 0
        self.order_count: int = 0
        self.connect_time: int = 0

        self.callbacks: Dict[str, callable] = {
            "login": self.on_login,
            "orders": self.on_order,
            "orders-algo": self.on_order,
            "error": self.on_api_error
        }

        self.reqid_order_map: Dict[str, OrderData] = {}

        self.ping_count = 0
        self.ping_max_num = 20

    def connect(
            self,
            key: str,
            secret: str,
            passphrase: str,
            proxy_host: str,
            proxy_port: int
    ) -> None:
        """连接Websocket私有频道"""
        self.key = key
        self.secret = secret.encode()
        self.passphrase = passphrase
        self.connect_time = int(datetime.now().strftime("%y%m%d%H%M%S"))
        self.init(PRIVATE_WEBSOCKET_HOST, proxy_host, proxy_port, 20)
        self.start()

    def ping_pong(self, event: Event) -> None:
        if self.ping_count > self.ping_max_num:
            self.send_packet(packet="ping")
            self.ping_count = 0
        else:
            self.ping_count += 1

    def on_connected(self) -> None:
        """连接成功回报"""
        self.login_tag = True
        self.login()
        print("私有频道链接成功，重新登陆")

    def on_disconnected(self) -> None:
        """连接断开回报"""
        print("Websocket 私有频道 API连接断开")
        pass

    def on_packet(self, packet: dict) -> None:
        """推送数据回报"""
        self.ping_count = 0
        if packet == "pong":
            return

        if "event" in packet:
            cb_name: str = packet["event"]
        elif "op" in packet:
            cb_name: str = packet["op"]
        else:
            cb_name: str = packet["arg"]["channel"]

        callback: callable = self.callbacks.get(cb_name, None)
        if callback:
            callback(packet)

    def on_error(self, exception_type: type, exception_value: Exception, tb) -> None:
        """触发异常回报"""
        msg: str = f"私有频道触发异常，类型：{exception_type}，信息：{exception_value}"
        print(msg)

    def on_api_error(self, packet: dict) -> None:
        """用户登录请求回报"""
        code: str = packet["code"]
        msg: str = packet["msg"]
        print(f"Websocket Private API请求失败, 状态码：{code}, 信息：{msg}")

    def on_login(self, packet: dict) -> None:
        """用户登录请求回报"""
        if packet["code"] == '0':
            print("重新登陆成功，重新订阅 订单数据")
            self.subscribe_topic()
        else:
            self.login_tag = False
            print("Websocket Private API登录失败")

    def login(self) -> None:
        """用户登录"""
        timestamp: str = str(time.time())
        msg: str = timestamp + "GET" + "/users/self/verify"
        signature: bytes = generate_signature(msg, self.secret)

        okex_req: dict = {
            "op": "login",
            "args":
                [
                    {
                        "apiKey": self.key,
                        "passphrase": self.passphrase,
                        "timestamp": timestamp,
                        "sign": signature.decode("utf-8")
                    }
                ]
        }
        self.send_packet(packet=okex_req)

    def on_order(self, packet: dict) -> None:
        """委托更新推送"""
        data: list = packet["data"]
        for d in data:
            order: OrderData = parse_order_data(d)
            self.gateway.on_order(order)

    def subscribe_topic(self) -> None:
        """订阅委托推送"""
        okex_req: dict = {
            "op": "subscribe",
            "args": [
                {
                    "channel": "orders",
                    "instType": "ANY"
                },
                {
                    "channel": "orders-algo",
                    "instType": "ANY"
                },
            ]
        }
        self.send_packet(packet=okex_req)


def generate_datetime(timestamp: str) -> datetime:
    """generate time"""
    dt: datetime = datetime.fromtimestamp(int(timestamp) / 1000)
    return dt


def generate_timestamp() -> str:
    """生成时间戳"""
    now: datetime = datetime.utcnow()
    timestamp: str = now.isoformat("T", "milliseconds")
    return timestamp + "Z"


def generate_signature(msg: str, secret_key: str) -> bytes:
    """生成签名"""
    return base64.b64encode(hmac.new(secret_key, msg.encode(), hashlib.sha256).digest())


def parse_order_data(data: dict) -> OrderData:
    """解析委托回报数据"""
    order_id: str = data["clOrdId"]

    price = float(data["px"])  # 订单原始价格

    if data.get("fillPx") == "":
        fillPx = 0
    else:
        fillPx = float(data['fillPx'])

    order: OrderData = OrderData(
        symbol=data["instId"],  # 交易对
        exchange=Exchange.OKEX,
        orderid=order_id,  # 订单id
        type=ORDERTYPE_OKEX2VT[data["ordType"]],
        direction=DIRECTION_OKEX2VT[data["side"]],  # 订单方向
        price=price,
        volume=float(data["sz"]),  # 订单原始数量
        traded=float(data['accFillSz']),  # 订单累计已成交量
        traded_volume=float(data.get("fillSz")),  # 订单末次成交量
        traded_price=fillPx,  # 订单末次成交价格
        status=STATUS_OKEX2VT[data["state"]],
        datetime=generate_datetime(data["cTime"]),
    )
    stop_way = data.get("actualSide")
    if stop_way:
        if stop_way == "sl":
            order.type = OrderType.STOP_MARKET
        else:
            order.type = OrderType.TAKE_PROFIT_MARKET
    return order
