from contract_gen import ContractGenerator
























if __name__ == '__main__':
    contracts_obj = ContractGenerator(symbol_list=['NIFTY', 'BANKNIFTY'])
    nse_df = contracts_obj.fetch_nse_contracts()