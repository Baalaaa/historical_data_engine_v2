import os

# from loggers import logger


def create_folder():
    try:
        base_path = os.getcwd()
        folders_names = [
            "contracts", "historical_data",
            "fyers_logs", "logs",
        ]
        for folder in folders_names:
            os.makedirs(os.path.join(base_path, folder), exist_ok=True)
    except Exception as e:
        print(f"exception occurred while creating folder: {e} !")

