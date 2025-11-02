"""
Data importer for OSC automation
"""

from data.osc.osc_data import SALES_REPRESENTATIVE, MERCHANT_INFO, BUSINESS_ADDRESS


class DataImporter:
    """Centralized data access for automation"""
    
    @staticmethod
    def get_sales_rep_name() -> str:
        return SALES_REPRESENTATIVE.get("name", "DEMONET1")
    
    @staticmethod
    def get_merchant_info() -> dict:
        return MERCHANT_INFO
    
    @staticmethod
    def get_business_address() -> dict:
        return BUSINESS_ADDRESS