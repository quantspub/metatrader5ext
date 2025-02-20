import pytest
import asyncio
from unittest.mock import MagicMock
from nautilus_metatrader5.stream_manager import StreamManager


@pytest.fixture
def stream_manager():
    return StreamManager()


@pytest.mark.asyncio
async def test_create_streaming_task(stream_manager):
    mock_func = MagicMock(return_value="mock_data")
    req_id = "test_req"
    symbols = ["EURUSD", "GBPUSD"]
    interval = 1.0

    stream_manager.create_streaming_task(req_id, symbols, interval, mock_func)

    for symbol in symbols:
        _id = f"{symbol}-{req_id}"
        assert _id in stream_manager.stream_tasks
        task = stream_manager.stream_tasks[_id]
        assert not task.done()

    await asyncio.sleep(2)

    for symbol in symbols:
        _id = f"{symbol}-{req_id}"
        task = stream_manager.stream_tasks[_id]
        assert not task.done()
        mock_func.assert_any_call(symbol)


@pytest.mark.asyncio
async def test_stop_streaming_task(stream_manager):
    mock_func = MagicMock(return_value="mock_data")
    req_id = "test_req"
    symbols = ["EURUSD", "GBPUSD"]
    interval = 1.0

    stream_manager.create_streaming_task(req_id, symbols, interval, mock_func)
    await asyncio.sleep(2)
    stream_manager.stop_streaming_task(req_id, symbols)

    for symbol in symbols:
        _id = f"{symbol}-{req_id}"
        assert _id not in stream_manager.stream_tasks
        mock_func.assert_any_call(symbol)
