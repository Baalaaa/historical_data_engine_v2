import time

import pandas as pd

from contract_gen import ContractGenerator
from fetch_hist_data import FetchHistoricalData





if __name__ == '__main__':

    contracts_obj = ContractGenerator(symbol_list=['NIFTY', 'BANKNIFTY', 'FINNIFTY', 'BANKEX', 'SENSEX'])
    nse_df = contracts_obj.fetch_nse_contracts()
    bse_df = contracts_obj.fetch_bse_contracts()

    fetch_hist_obj = FetchHistoricalData()
    # fetch_hist_obj.fetch_historical_data(df=nse_df, start_date="2026-04-01", end_date="2026-06-30")
    # fetch_hist_obj.fetch_historical_data(df=bse_df, start_date="2026-04-01", end_date="2026-06-30")

    # fetch_hist_obj.testing_historical_data(symbol="NSE:NIFTY2672118750PE" , start_date="2026-04-01", end_date="2026-06-30")

    # for row in nse_df.itertuples():
    #     fetch_hist_obj.fetch_hist_data(symbol=row.symbol, start_date="2026-04-01", end_date="2026-06-30")
    #     time.sleep(1)


    # fetch_hist_obj.fetch_hist_data(symbol="NSE:BANKNIFTY26JULFUT", start_date="2026-04-01", end_date="2026-06-30")


    fetch_hist_obj.fetch_hist_data(df=nse_df, start_date="2026-04-01", end_date="2026-06-30")