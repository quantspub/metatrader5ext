from nautilus_metatrader5.symbol import Symbol, SymbolInfo, process_symbol_details


class MT5Client:

    def __init__(
        self,
        host: str = "localhost",
        port: int = 18812,
        keep_alive: bool = False,
        logger: Optional[Callable] = None,
    ):
        super().__init__(host, port, keep_alive)

    def req_account_summary(self, req_id: TickerId):
        return

    def cancel_account_summary(self, req_id: TickerId):
        return

    def req_positions(self):
        return

    def req_symbol_details(
        self, req_id: TickerId, symbol: str
    ) -> list[SymbolInfo] | None:
        if symbol == "":
            return None

        if "-" in symbol:
            symbol = symbol.replace("-", " ")

        mt5_results = self.symbols_get(symbol)
        if len(mt5_results) > 0:
            symbol_details: List[SymbolInfo] = []
            for symbol_info in mt5_results:
                if (
                    "*" not in symbol or "!" not in symbol,
                    "," not in symbol,
                ) and symbol_info.name == symbol:
                    symbol_details.append(
                        process_symbol_details(symbol_info, self.connected_server)
                    )
                    break

            # if self.market_data_type == MarketDataTypeEnum.REALTIME:
            self.send_msg((req_id, current_fn_name(), symbol_details))
            return symbol_details

        return None

    def req_matching_symbols(self, req_id: TickerId, pattern: str):
        mt5_results = self.symbols_get(pattern)
        if len(mt5_results) > 0:
            symbol_details: List[SymbolInfo] = []
            for symbol_info in mt5_results:
                symbol_details.append(
                    process_symbol_details(symbol_info, self.connected_server)
                )

            # if self.market_data_type == MarketDataTypeEnum.REALTIME:
            self.send_msg((req_id, current_fn_name(), symbol_details))
            return symbol_details

        return None

    def req_tick_by_tick_data(
        self,
        req_id: TickerId,
        symbol: Symbol,
        type: str = "BidAsk",
        size: int = 1,
        ignore_size: bool = False,
    ):
        # Attempt to enable the display of the symbol in MarketWatch
        if not self.symbol_select(symbol.symbol, True):
            code, msg = self.get_error()
            raise ClientException(code, msg, f"Failed to select {symbol.symbol}")

        _current_fn_name = current_fn_name()

        if self.market_data_type == MarketDataTypeEnum.REALTIME:

            def fetch_latest_tick(symbol):
                tick = self.symbol_info_tick(symbol)
                self.send_msg((req_id, _current_fn_name, type, tick))
                return tick

            # Start the streaming task in its own thread
            self.stream_manager.create_streaming_task(
                f"TICK-{str(req_id)}",
                [symbol.symbol],
                self.stream_interval,
                fetch_latest_tick,
            )

    def cancel_tick_by_tick_data(
        self,
        req_id: TickerId,
        symbol: Symbol,
        type: str = "BidAsk",
        size: int = 1,
        ignore_size: bool = False,
    ):
        self.stream_manager.stop_streaming_task(f"TICK-{str(req_id)}", [symbol.symbol])
        print(f"Streaming task for {req_id} has been stopped.")

    def req_real_time_bars(
        self,
        req_id: TickerId,
        symbol: Symbol,
        bar_size: int,
        what_to_show: str,
        use_rth: bool,
    ):
        _current_fn_name = current_fn_name()

        if self.market_data_type == MarketDataTypeEnum.REALTIME:

            def fetch_latest_bar(symbol):
                raw_bars = self.copy_rates_from_pos(
                    symbol, MetaTrader5.TIMEFRAME_M1, 0, 1
                )

                processed_bars = []
                for raw_bar in raw_bars:
                    processed_bars.append(
                        BarData(
                            time=raw_bar[0],
                            open_=raw_bar[1],
                            high=raw_bar[2],
                            low=raw_bar[3],
                            close=raw_bar[4],
                            tick_volume=raw_bar[5],
                            spread=raw_bar[6],
                            real_volume=raw_bar[7],
                        )
                    )

                self.send_msg((req_id, _current_fn_name, processed_bars))
                return processed_bars

            # Start the streaming task in its own thread
            self.stream_manager.create_streaming_task(
                f"BAR-{str(req_id)}",
                [symbol.symbol],
                MetaTrader5.TIMEFRAME_M1 * 60,
                fetch_latest_bar,
            )
        else:
            pass

    def cancel_real_time_bars(self, req_id: TickerId, symbol: Symbol):
        self.stream_manager.stop_streaming_task(f"BAR-{str(req_id)}", [symbol.symbol])
        print(f"Streaming task for {req_id} has been stopped.")

    def req_historical_data(
        self,
        req_id: TickerId,
        symbol: Symbol,
        end_datetime: str,
        duration_str: str,
        bar_size_setting: str,
        what_to_show: str,
        use_rth: int,
        format_date: int,
        keep_up_to_date: bool,
    ):
        """Requests symbols' historical data. When requesting historical data, a
        finishing time and date is required along with a duration string.

        req_id: TickerId - The id of the request. Must be a unique value. When the
            market data returns.
        symbol: Symbol - This object contains a description of the symbol for which
            market data is being requested.
        end_datetime: str - Defines a query end date and time at any point during the past 6 mos.
            Valid values include any date/time within the past six months in the format:
            YYYY-MM-dd HH:MM:SS
        duration_str: str - Set the query duration up to one week, using a time unit
            of minutes, days or weeks. Valid values include any integer followed by a space
            and then M (minutes), D (days) or W (week). If no unit is specified, minutes is used.
        bar_size_setting: str - Specifies the size of the bars that will be returned (within Terminal listimits).
            Valid values include:
            1 sec
            5 secs
            15 secs
            30 secs
            1 min
            2 mins
            3 mins
            5 mins
            15 mins
            30 mins
            1 hour
            1 day
        what_to_show: str - Determines the nature of data being extracted. Valid values include:
            TRADES
            BID_ASK
        use_rth: int - Determines whether to return all data available during the requested time span,
            or only data that falls within regular trading hours. Valid values include:

            0 - all data is returned even where the market in question was outside of its
            regular trading hours.
            1 - only data within the regular trading hours is returned, even if the
            requested time span falls partially or completely outside of the RTH.
        format_date: int - Determines the date format applied to returned bars. Valid values include:
            1 - dates applying to bars returned in the format: yyyymmdd{space}{space}hh:mm:dd
            2 - dates are returned as a long integer specifying the number of seconds since
                1/1/1970 GMT.
        """

        _current_fn_name = current_fn_name()

        # if self.market_data_type == MarketDataTypeEnum.REALTIME:
        #     def fetch_latest_tick(symbol):
        #         raw_bars = self.copy_rates_from(symbol, MetaTrader5.TIMEFRAME_M1, 0, 1)

        #         processed_bars = []
        #         for raw_bar in raw_bars:
        #             processed_bars.append(BarData(
        #                 time=raw_bar[0],
        #                 open_=raw_bar[1],
        #                 high=raw_bar[2],
        #                 low=raw_bar[3],
        #                 close=raw_bar[4],
        #                 tick_volume=raw_bar[5],
        #                 spread=raw_bar[6],
        #                 real_volume=raw_bar[7],
        #             ))

        #         self.send_msg((req_id, _current_fn_name, processed_bars))
        #         return processed_bars

        #     # Start the streaming task in its own thread
        #     self.stream_manager.create_streaming_task(f"HISTORICAL-BAR-{str(req_id)}", [symbol.symbol], MetaTrader5.TIMEFRAME_M1 * 60, fetch_latest_tick)
        # else:
        #     pass
        #     # TODO: fix this
        #   copy_ticks_range(
        #   symbol,       # symbol name
        #   date_from,    # date the ticks are requested from
        #   date_to,      # date, up to which the ticks are requested
        #   flags         # combination of flags defining the type of requested ticks
        #   )
        #   ticks = self.copy_ticks_range()

    def cancel_historical_data(self, req_id: TickerId, symbol: Symbol):
        self.stream_manager.stop_streaming_task(
            f"HISTORICAL-BAR-{str(req_id)}", [symbol.symbol]
        )
        print(f"Streaming task for {req_id} has been stopped.")
