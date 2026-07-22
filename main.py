
from config.utilities import create_folder
from contract_gen import ContractGenerator
from fetch_hist_data import FetchHistoricalData



if __name__ == '__main__':

    create_folder()
    contracts_obj = ContractGenerator(symbol_list=['NIFTY', 'BANKNIFTY', 'FINNIFTY', 'BANKEX', 'SENSEX'])
    nse_df = contracts_obj.fetch_nse_contracts_v2(expiry_date=None)
    bse_df = contracts_obj.fetch_bse_contracts_v2(expiry_date=None)

    fetch_hist_obj = FetchHistoricalData()
    # fetch_hist_obj.fetch_historical_data(df=nse_df, start_date="2026-04-01", end_date="2026-06-30")
    # fetch_hist_obj.fetch_historical_data(df=bse_df, start_date="2026-04-01", end_date="2026-06-30")

    # fetch_hist_obj.testing_historical_data(symbol="NSE:NIFTY26JAN25500CE" , start_date="2026-04-01", end_date="2026-06-30")

    # for row in nse_df.itertuples():
    #     fetch_hist_obj.fetch_hist_data(symbol=row.symbol, start_date="2026-04-01", end_date="2026-06-30")
    #     time.sleep(1)


    # fetch_hist_obj.fetch_hist_data(symbol="NSE:NIFTY26JAN25500CE", start_date="2026-04-01", end_date="2026-06-30")


    fetch_hist_obj.fetch_hist_data_v2(df=bse_df, start_date="2026-07-01", end_date="2026-07-10")