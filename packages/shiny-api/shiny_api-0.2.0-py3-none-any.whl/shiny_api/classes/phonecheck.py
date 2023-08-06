"""PhoneCheck class for information from PhoneCheck's API"""
import os
from dataclasses import dataclass
import requests
import shiny_api.modules.load_config as config

print(f"Importing {os.path.basename(__file__)}...")


@dataclass
class Device:
    """Describe object returned from PC_API_URL["device"]"""

    master_id: int
    model: str
    memory: str
    serial: str
    esn_response: list[str]

    def __init__(self, serial_number: str) -> None:
        """load data from API"""
        pc_params = {"Apikey": config.PHONECHECK_API_KEY, "imei": serial_number, "Username": "cloudshinycomputers"}
        response = requests.post(url=config.PC_API_URL["device"], data=pc_params, timeout=60)
        response_json = response.json()
        self.model = response_json.get("Model")
        self.memory = response_json.get("Memory")
        self.master_id = response_json.get("master_id")
