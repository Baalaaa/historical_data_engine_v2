
import os
import time
import pandas as pd

from datetime import timedelta
from dotenv import load_dotenv
from fyers_apiv3 import fyersModel
from config.loggers import logger


load_dotenv()


class FetchHistoricalData:

    def __init__(self):
        self.payload = {}
        self.resolution = "1"
        self.dateformat = "1"
        self.content_flag = "1"
        self.CLIENT_ID = os.getenv('FYERS_CLIENT_ID')
        self.ACCESS_TOKEN = self.fetch_access_token()
        self.fyers_log_path = os.path.join(os.getcwd(), 'fyers_logs')
        self.fyers = fyersModel.FyersModel(client_id=self.CLIENT_ID, token=self.ACCESS_TOKEN, is_async=False,
                                           log_path=self.fyers_log_path)

    def fetch_access_token(self)-> str | None:
        try:
            with open("access_token.json", "r") as f:
                acc_token = f.read()
            return acc_token
        except Exception as e:
            logger.error(f"exception occurred while reading access token: {e} !")
            return None

    def testing_historical_data(self, symbol: str, start_date: str, end_date: str) -> None:
        try:
            self.payload = {
                "symbol": symbol,
                "range_from": start_date,
                "range_to": end_date,
                "resolution": self.resolution,
                "date_format": self.dateformat,
                "cont_flag": self.content_flag,
            }
            response = self.fyers.history(data=self.payload)
            print(response)

        except Exception as e:
            print(f"exception occurred while fetching historical data: {e} !")


    # def fetch_historical_data(self, df: pd.DataFrame, start_date: str, end_date: str) -> None:
    #     try:
    #         global exchange
    #
    #         if df.empty:
    #             logger.warning(f"Dataframe is Empty: {df} !")
    #             return None
    #
    #         if "symbol" not in df.columns:
    #             logger.warning(f"Symbol columns not found for {df.columns} !")
    #             return None
    #
    #         if "underlying" not in df.columns:
    #             logger.warning(f"Underlying columns not found in: {df.columns} !")
    #             return None
    #
    #         if "expiry_date" not in df.columns:
    #             logger.warning(f"Expiry_date columns not found in {df.columns} !")
    #             return None
    #
    #         for row in df.itertuples():
    #             # print(row.Symbol)
    #             self.historical_data = {
    #                 "symbol": row.symbol,
    #                 "range_from": start_date,
    #                 "range_to": end_date,
    #                 "resolution": self.resolution,
    #                 "date_format": self.dateformat,
    #                 "cont_flag": self.content_flag,
    #             }
    #
    #             response = self.fyers.history(historical_data=self.historical_data)
    #             # print(response)
    #             if response.get('S') != "ok":
    #                 logger.warning(f"failed to fetch historical historical_data for : {row.symbol} !")
    #
    #             elif response.get("candles"):
    #                logger.warning(f"no historical historical_data for: {row.symbol} !")
    #
    #             elif response.get('s') == "no_data":
    #                logger.warning(f"no historical_data for this symbol: {row.symbol} !")
    #             else:
    #
    #                 if row.symbol.startswith("NSE*"):
    #                     exchange = "NSE"
    #                 else:
    #                     exchange = "BSE"
    #
    #                 os.makedirs(f"historical_data/{exchange}", exist_ok=True)
    #                 with open(f"historical_data/{exchange}/{row.underlying}_{row.expiry_date}_.csv", mode="w", newline="") as f:
    #                     writer = csv.writer(f)
    #
    #                     writer.writerow(["Timestamp", "Open", "High", "Low", "Close", "Volume"])
    #                     writer.writerows(response.get("candles"))
    #
    #                 print(f"historical_data fetched successfully for: {row.symbol} !")
    #             print(f"{row.symbol} & {row.expiry_date}")
    #             time.sleep(2)
    #     except Exception as e:
    #         print(f"exception occurred while fetching historical historical_data: {e} !")
    #         return None
    #

    # def fetch_historical_data_2(self, symbol: str, start_date: str, end_date: str, expiry_date: str, underlying: str) -> None:
    #     try:
    #         global exchange
    #
    #         self.historical_data = {
    #             "symbol": symbol,
    #             "range_from": start_date,
    #             "range_to": end_date,
    #             "resolution": self.resolution,
    #             "date_format": self.dateformat,
    #             "cont_flag": self.content_flag,
    #         }
    #
    #         response = self.fyers.history(historical_data=self.historical_data)
    #
    #         status = response.get("s")
    #
    #         if status == "no_data":
    #             print(f"no historical historical_data for: {symbol} !")
    #             return None
    #
    #         if status != "ok":
    #             print(f"failed to fetch historical historical_data for : {symbol} !")
    #             return None
    #
    #         if symbol.startswith("NSE"):
    #             exchange = "NSE"
    #         else:
    #             exchange = "BSE"
    #
    #         candles = response.get("candles", [])
    #
    #         filename = f"historical_data/{exchange}/{underlying}_{expiry_date}_.csv"
    #         with open(filename, mode="w", newline="") as f:
    #             writer = csv.writer(f)
    #             writer.writerow(["Timestamp", "Open", "High", "Low", "Close", "Volume"])
    #             writer.writerows(candles)
    #
    #         print(f"historical_data fetched successfully for: {symbol} && Number of candles: {len(candles)} !")
    #
    #     except Exception as e:
    #         print(f"exception occurred while fetching historical historical_data: {e} !")
    #         return None


    def fetch_hist_data(self, df: pd.DataFrame, start_date: str | None, end_date: str | None) -> None:
        try:
            count = 0
            symbol_name = None
            hist_data_list = []
            failed_data_sym_list = []
            today = pd.Timestamp.today().normalize()

            nearest_date = df[df['expiry_date'] >= today]['expiry_date'].min()
            if start_date is None and end_date is None:
                start_date = nearest_date - timedelta(days=90)
                end_date = nearest_date

            logger.info(f"start_date: {start_date} & end_date: {end_date} !")

            for row in df.itertuples():
                symbol_name = row.underlying_symbol
                self.data = {
                    "symbol": row.symbol_ticker,
                    "range_from": start_date,
                    "range_to": end_date,
                    "resolution": "1",
                    "date_format": "1",
                    "cont_flag": "1",
                    "oi_flag": "1"
                }
                response = self.fyers.history(data=self.data)

                status = response.get('s')
                if status == 'no_data':
                    logger.warning(f"no data from this symbol: {response.get('s')} !")
                if status != 'ok':
                    logger.warning(f"failed to fetch for this symbol: {response.get('s')} !")

                if response.get('candles'):
                    hist_data_list.extend(response.get('candles'))
                else:
                    failed_data_sym_list.extend(row.symbol_ticker)

                # print(f"symbol: {row.symbol_ticker} & status: {response.get('s')} !")
                if count == 10:
                    logger.warning("sleeping for 5 sec")
                    time.sleep(5)
                    count = 0
                count += 1

            df = pd.DataFrame(hist_data_list, columns=["timestamp", "open", "high", "low", "close", "volume", "oi"])
            df.insert(0, "symbol", symbol_name)
            df.to_csv(f"Data/NSE/Nse_hist_data.csv", index=False)
            logger.info(f"saved file")
            logger.info(f"total symbol: {len(df)}, available data: {len(hist_data_list)} "
                  f"& failed symbol: {len(failed_data_sym_list)} !")
            with open('failed_symbol.txt', mode='w') as f:
                f.write(str(failed_data_sym_list))

        except Exception as e:
            logger.error(f"exception occurred while fetching hist data: {e} !")