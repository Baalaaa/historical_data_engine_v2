import os
import requests
import pandas as pd

from io import StringIO


class ContractGenerator:

    def __init__(self, symbol_list: list):
        self.nse_folder_name = "NSE"
        self.bse_folder_name = "BSE"
        self.base_path = os.getcwd()
        self.folder_name = "contracts"
        self.symbol_list = symbol_list
        self.contract_urls = {
            "nse_contract_fo_url" :"https://public.fyers.in/sym_details/NSE_FO.csv",
            "bse_contract_fo_url" : "https://public.fyers.in/sym_details/BSE_FO.csv"
        }
        self.headers = [ "fytoken", "symbol_Details", "exchange_Instrument_type", "minimum_lot_size", "tick_size", "isin",
                         "trading_Session", "last_update_date", "expiry_date", "symbol_ticker", "exchange",
                         "segment", "scrip_code", "underlying_symbol", "underlying_scrip_code", "strike_price",
                         "option_type", "underlying_fyToken", "reserved_column1", "reserved_column2", "reserved_column3"
                        ]


    def fetch_nse_contracts(self) -> pd.DataFrame | None:
        try:
            contract_df = []
            today = pd.Timestamp.today().normalize()
            response = requests.get(self.contract_urls.get("nse_contract_fo_url"))
            print(f"url: {response.url} | Status Code: {response.status_code} !")
            df = pd.read_csv(StringIO(response.text), header=None, names=self.headers)

            for sym in self.symbol_list:
                filtered_df = df[df["underlying_symbol"] == sym]
                filtered_df['expiry_date'] = pd.to_datetime(filtered_df['expiry_date'], unit='s')
                nearest_expiry = filtered_df.loc[filtered_df['expiry_date'] >= today, 'expiry_date'].min()
                filtered_df = filtered_df[filtered_df['expiry_date'] == nearest_expiry]
                # print(f"symbol: {sym} & dataframe: {filtered_df.shape[0]} rows !")
                contract_df.append(filtered_df)

            path = os.path.join(self.base_path, self.folder_name, self.nse_folder_name)
            final_df = pd.concat(contract_df)

            final_df.to_csv(f"{path}/nse_contract_fo.csv", index=False)
            # print(f"final df: {len(final_df)} !")
            return final_df

        except Exception as e:
            print(f"exception occurred while fetching nse contracts: {e} !")
            return None


    def fetch_bse_contracts(self) -> pd.DataFrame | None:
        try:
            contract_df = []
            today = pd.Timestamp.today().normalize()
            response = requests.get(self.contract_urls.get("bse_contract_fo_url"))
            print(f"url: {response.url} | Status Code: {response.status_code} !")
            df = pd.read_csv(StringIO(response.text), header=None,  names=self.headers)

            for sym in self.symbol_list:
                filtered_df = df[df["underlying_symbol"] == sym]
                filtered_df['expiry_date'] = pd.to_datetime(filtered_df['expiry_date'], unit='s')
                nearest_expiry = filtered_df.loc[filtered_df['expiry_date'] >= today, 'expiry_date'].min()
                filtered_df = filtered_df[filtered_df['expiry_date'] == nearest_expiry]
                # print(f"symbol: {sym} & dataframe: {filtered_df.shape[0]} rows !")
                contract_df.append(filtered_df)

            path = os.path.join(self.base_path, self.folder_name, self.bse_folder_name)
            final_df = pd.concat(contract_df)
            final_df.to_csv(f"{path}/bse_contract_fo.csv", index=False)
            return final_df

        except Exception as e:
            print(f"exception occurred while fetching bse contracts: {e} !")
            return None
