"""
Data importer for OSC automation
"""

from config.osc.config import get_osc_data


class DataImporter:
    """Centralized data access for automation"""
    
    def __init__(self):
        self._data = get_osc_data()
    
    def get_sales_rep_name(self) -> str:
        return self._data.SALES_REPRESENTATIVE.get("name", "DEMONET1")
    
    def get_corporate_info(self) -> dict:
        return self._data.CORPORATE_INFO
    
    def get_location_info(self) -> dict:
        return self._data.LOCATION_INFO
