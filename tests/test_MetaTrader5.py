import pytest
import pytz
from datetime import datetime
from nautilus_metatrader5 import MetaTrader5
from typing import Tuple, Generator


@pytest.fixture(scope="module")
def mt5_setup() -> Generator[MetaTrader5, None, None]:
    mt5 = MetaTrader5()
    mt5.initialize()
    yield mt5
    mt5.shutdown()


@pytest.fixture(scope="module")
def setup_data(
    mt5_setup: MetaTrader5,
) -> Tuple[pytz.BaseTzInfo, str, float, float, float, int]:
    timezone = pytz.timezone("Etc/UTC")
    symbol = "EURUSD"
    lot = 0.1
    point = mt5_setup.symbol_info(symbol).point
    price = mt5_setup.symbol_info_tick(symbol).ask
    deviation = 20

    setup_data = (timezone, symbol, lot, point, price, deviation)
    return setup_data


def test_initialize(mt5_setup: MetaTrader5) -> None:
    assert mt5_setup.initialize()


def test_version(mt5_setup: MetaTrader5) -> None:
    version = mt5_setup.version()
    assert isinstance(version, tuple)
    assert len(version) == 3


def test_last_error(mt5_setup: MetaTrader5) -> None:
    error = mt5_setup.last_error()
    assert isinstance(error, tuple)
    assert len(error) == 2


def test_terminal_info(mt5_setup: MetaTrader5) -> None:
    terminal_info = mt5_setup.terminal_info()
    assert terminal_info is not None


def test_login(mt5_setup: MetaTrader5) -> None:
    assert (
        mt5_setup.login(login=12345678, password="password", server="server") == False
    )


def test_shutdown(mt5_setup: MetaTrader5) -> None:
    assert mt5_setup.shutdown() is None


def test_account_info(mt5_setup: MetaTrader5) -> None:
    account_info = mt5_setup.account_info()
    assert account_info is not None


def test_symbols_total(mt5_setup: MetaTrader5) -> None:
    total_symbols = mt5_setup.symbols_total()
    assert isinstance(total_symbols, int)


def test_symbols_get(mt5_setup: MetaTrader5) -> None:
    symbols = mt5_setup.symbols_get()
    assert isinstance(symbols, tuple)


def test_symbol_info(
    mt5_setup: MetaTrader5,
    setup_data: Tuple[pytz.BaseTzInfo, str, float, float, float, int],
) -> None:
    _, symbol, _, _, _, _ = setup_data
    symbol_info = mt5_setup.symbol_info(symbol)
    assert symbol_info is not None


def test_symbol_info_tick(
    mt5_setup: MetaTrader5,
    setup_data: Tuple[pytz.BaseTzInfo, str, float, float, float, int],
) -> None:
    _, symbol, _, _, _, _ = setup_data
    tick_info = mt5_setup.symbol_info_tick(symbol)
    assert tick_info is not None


def test_symbol_select(
    mt5_setup: MetaTrader5,
    setup_data: Tuple[pytz.BaseTzInfo, str, float, float, float, int],
) -> None:
    _, symbol, _, _, _, _ = setup_data
    assert mt5_setup.symbol_select(symbol, True)


def test_market_book_add(
    mt5_setup: MetaTrader5,
    setup_data: Tuple[pytz.BaseTzInfo, str, float, float, float, int],
) -> None:
    _, symbol, _, _, _, _ = setup_data
    assert mt5_setup.market_book_add(symbol)


def test_market_book_get(
    mt5_setup: MetaTrader5,
    setup_data: Tuple[pytz.BaseTzInfo, str, float, float, float, int],
) -> None:
    _, symbol, _, _, _, _ = setup_data
    mt5_setup.market_book_add(symbol)
    market_book = mt5_setup.market_book_get(symbol)
    assert isinstance(market_book, tuple)
    mt5_setup.market_book_release(symbol)


def test_market_book_release(
    mt5_setup: MetaTrader5,
    setup_data: Tuple[pytz.BaseTzInfo, str, float, float, float, int],
) -> None:
    _, symbol, _, _, _, _ = setup_data
    mt5_setup.market_book_add(symbol)
    assert mt5_setup.market_book_release(symbol)


def test_copy_rates_from(
    mt5_setup: MetaTrader5,
    setup_data: Tuple[pytz.BaseTzInfo, str, float, float, float, int],
) -> None:
    timezone, symbol, _, _, _, _ = setup_data
    utc_from = datetime(2020, 1, 10, tzinfo=timezone)
    rates = mt5_setup.copy_rates_from(symbol, mt5_setup.TIMEFRAME_H1, utc_from, 10)
    assert isinstance(rates, list)


def test_copy_rates_from_pos(
    mt5_setup: MetaTrader5,
    setup_data: Tuple[pytz.BaseTzInfo, str, float, float, float, int],
) -> None:
    _, symbol, _, _, _, _ = setup_data
    rates = mt5_setup.copy_rates_from_pos(symbol, mt5_setup.TIMEFRAME_H1, 0, 10)
    assert isinstance(rates, list)


def test_copy_rates_range(
    mt5_setup: MetaTrader5,
    setup_data: Tuple[pytz.BaseTzInfo, str, float, float, float, int],
) -> None:
    timezone, symbol, _, _, _, _ = setup_data
    utc_from = datetime(2020, 1, 10, tzinfo=timezone)
    utc_to = datetime(2020, 1, 11, tzinfo=timezone)
    rates = mt5_setup.copy_rates_range(symbol, mt5_setup.TIMEFRAME_H1, utc_from, utc_to)
    assert isinstance(rates, list)


def test_copy_ticks_from(
    mt5_setup: MetaTrader5,
    setup_data: Tuple[pytz.BaseTzInfo, str, float, float, float, int],
) -> None:
    timezone, symbol, _, _, _, _ = setup_data
    utc_from = datetime(2020, 1, 10, tzinfo=timezone)
    ticks = mt5_setup.copy_ticks_from(symbol, utc_from, 100, mt5_setup.COPY_TICKS_ALL)
    assert isinstance(ticks, list)


def test_copy_ticks_range(
    mt5_setup: MetaTrader5,
    setup_data: Tuple[pytz.BaseTzInfo, str, float, float, float, int],
) -> None:
    timezone, symbol, _, _, _, _ = setup_data
    utc_from = datetime(2020, 1, 10, tzinfo=timezone)
    utc_to = datetime(2020, 1, 11, tzinfo=timezone)
    ticks = mt5_setup.copy_ticks_range(
        symbol, utc_from, utc_to, mt5_setup.COPY_TICKS_ALL
    )
    assert isinstance(ticks, list)


def test_orders_total(mt5_setup: MetaTrader5) -> None:
    total_orders = mt5_setup.orders_total()
    assert isinstance(total_orders, int)


def test_orders_get(mt5_setup: MetaTrader5) -> None:
    orders = mt5_setup.orders_get()
    assert isinstance(orders, tuple)


def test_order_calc_margin(
    mt5_setup: MetaTrader5,
    setup_data: Tuple[pytz.BaseTzInfo, str, float, float, float, int],
) -> None:
    _, symbol, lot, _, price, _ = setup_data
    margin = mt5_setup.order_calc_margin(mt5_setup.ORDER_TYPE_BUY, symbol, lot, price)
    assert isinstance(margin, float)


def test_order_calc_profit(
    mt5_setup: MetaTrader5,
    setup_data: Tuple[pytz.BaseTzInfo, str, float, float, float, int],
) -> None:
    _, symbol, lot, point, price, _ = setup_data
    profit = mt5_setup.order_calc_profit(
        mt5_setup.ORDER_TYPE_BUY, symbol, lot, price, price + 100 * point
    )
    assert isinstance(profit, float)


def test_order_check(
    mt5_setup: MetaTrader5,
    setup_data: Tuple[pytz.BaseTzInfo, str, float, float, float, int],
) -> None:
    _, symbol, lot, point, price, deviation = setup_data
    request = {
        "action": mt5_setup.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5_setup.ORDER_TYPE_BUY,
        "price": price,
        "sl": price - 100 * point,
        "tp": price + 100 * point,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script",
        "type_time": mt5_setup.ORDER_TIME_GTC,
        "type_filling": mt5_setup.ORDER_FILLING_RETURN,
    }
    result = mt5_setup.order_check(request)
    assert result is not None


def test_order_send(
    mt5_setup: MetaTrader5,
    setup_data: Tuple[pytz.BaseTzInfo, str, float, float, float, int],
) -> None:
    _, symbol, lot, point, price, deviation = setup_data
    request = {
        "action": mt5_setup.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5_setup.ORDER_TYPE_BUY,
        "price": price,
        "sl": price - 100 * point,
        "tp": price + 100 * point,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script",
        "type_time": mt5_setup.ORDER_TIME_GTC,
        "type_filling": mt5_setup.ORDER_FILLING_RETURN,
    }
    result = mt5_setup.order_send(request)
    assert result is not None


def test_positions_total(mt5_setup: MetaTrader5) -> None:
    total_positions = mt5_setup.positions_total()
    assert isinstance(total_positions, int)


def test_positions_get(mt5_setup: MetaTrader5) -> None:
    positions = mt5_setup.positions_get()
    assert isinstance(positions, tuple)


def test_history_orders_total(
    mt5_setup: MetaTrader5,
    setup_data: Tuple[pytz.BaseTzInfo, str, float, float, float, int],
) -> None:
    timezone, _, _, _, _, _ = setup_data
    from_date = datetime(2020, 1, 1, tzinfo=timezone)
    to_date = datetime.now(tz=timezone)
    total_history_orders = mt5_setup.history_orders_total(from_date, to_date)
    assert isinstance(total_history_orders, int)


def test_history_orders_get(
    mt5_setup: MetaTrader5,
    setup_data: Tuple[pytz.BaseTzInfo, str, float, float, float, int],
) -> None:
    timezone, _, _, _, _, _ = setup_data
    from_date = datetime(2020, 1, 1, tzinfo=timezone)
    to_date = datetime.now(tz=timezone)
    history_orders = mt5_setup.history_orders_get(from_date, to_date)
    assert isinstance(history_orders, tuple)


def test_history_deals_total(
    mt5_setup: MetaTrader5,
    setup_data: Tuple[pytz.BaseTzInfo, str, float, float, float, int],
) -> None:
    timezone, _, _, _, _, _ = setup_data
    from_date = datetime(2020, 1, 1, tzinfo=timezone)
    to_date = datetime.now(tz=timezone)
    total_history_deals = mt5_setup.history_deals_total(from_date, to_date)
    assert isinstance(total_history_deals, int)


def test_history_deals_get(
    mt5_setup: MetaTrader5,
    setup_data: Tuple[pytz.BaseTzInfo, str, float, float, float, int],
) -> None:
    timezone, _, _, _, _, _ = setup_data
    from_date = datetime(2020, 1, 1, tzinfo=timezone)
    to_date = datetime.now(tz=timezone)
    history_deals = mt5_setup.history_deals_get(from_date, to_date)
    assert isinstance(history_deals, tuple)
