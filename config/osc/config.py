"""OSC application-specific configuration."""

from dataclasses import dataclass
from typing import Tuple, Literal

from core.utils import get_env, get_env_int


# Valid data environments
DataEnvironment = Literal["dev", "qa", "prod"]


@dataclass
class OSCSettings:
    """OSC application settings.

    Attributes:
        base_url: Base URL for OSC application
        login_path: Login endpoint path
        dashboard_path: Dashboard endpoint path
        quote_path: Quote creation endpoint path
        timeout_ms: OSC-specific timeout override (optional)
        environment: Current environment (prod/qa)
        data_env: Test data environment to use (dev/qa/prod)
    """

    base_url: str
    login_path: str
    dashboard_path: str
    quote_path: str
    timeout_ms: int
    environment: str
    data_env: DataEnvironment

    def __init__(self) -> None:
        """Initialize OSC settings from environment variables."""
        self.base_url = get_env("OSC_BASE_URL", "https://uno.eftsecure.net")
        self.login_path = get_env("OSC_LOGIN_PATH", "/SalesCenter/")
        self.dashboard_path = get_env("OSC_DASHBOARD_PATH", "/SalesCenter/frmHome.aspx")
        self.new_application_path = get_env("OSC_NEW_APP_PATH", "/SalesCenter/frmNewApplication.aspx")
        self.mfa_path = get_env("OSC_MFA_PATH", "/SalesCenter/mfa")
        self.quote_path = get_env("OSC_QUOTE_PATH", "/SalesCenter/quote/create")
        self.timeout_ms = get_env_int("OSC_TIMEOUT_MS", default=30000)
        self.environment = get_env("OSC_ENV", "prod").lower()
        
        # Data environment: which test data file to use
        # Can be: dev, qa, prod (defaults to same as environment)
        self.data_env = get_env("OSC_DATA_ENV", self.environment).lower()
        
        # Validate data_env
        if self.data_env not in ("dev", "qa", "prod"):
            self.data_env = "prod"  # fallback to prod

    @property
    def credentials(self) -> Tuple[str, str]:
        """Get credentials based on environment."""
        if self.environment == "qa":
            # QA environment credentials (for org laptop)
            username = get_env("OSC_QA_USER", "ContractorQA")
            password = get_env("OSC_QA_PASS", "QAContractor!123")
        else:
            # PROD environment credentials (for development - READ ONLY)
            username = get_env("OSC_USER", "contractordemo")
            password = get_env("OSC_PASS", "QAContractor@123")
        
        return username, password

    @property
    def is_production_safe(self) -> bool:
        """Check if current environment allows data modifications."""
        return self.environment == "qa"

    @property
    def login_url(self) -> str:
        """Full login URL."""
        return f"{self.base_url}{self.login_path}"

    @property
    def dashboard_url(self) -> str:
        """Full dashboard URL."""
        return f"{self.base_url}{self.dashboard_path}"

    @property
    def new_application_url(self) -> str:
        """Full new application URL."""
        return f"{self.base_url}{self.new_application_path}"

    @property
    def mfa_url(self) -> str:
        """Full MFA page URL."""
        return f"{self.base_url}{self.mfa_path}"

    @property
    def data_module_name(self) -> str:
        """
        Get the data module name based on data_env.
        
        Returns:
            str: Module name like 'osc_data_qa', 'osc_data_dev', or 'osc_data' (prod)
        """
        if self.data_env == "prod":
            return "osc_data"  # Default/prod uses osc_data.py
        return f"osc_data_{self.data_env}"


def get_osc_data():
    """
    Dynamically load the OSC data module based on configured data environment.
    
    This allows switching between different test data sets:
    - OSC_DATA_ENV=prod  → data/osc/osc_data.py (default)
    - OSC_DATA_ENV=qa    → data/osc/osc_data_qa.py
    - OSC_DATA_ENV=dev   → data/osc/osc_data_dev.py
    
    Returns:
        module: The loaded data module with all test data exports
        
    Raises:
        ImportError: If the specified data module doesn't exist
        
    Usage:
        from config.osc.config import get_osc_data
        data = get_osc_data()
        
        # Access data from the loaded module
        app_info = data.APPLICATION_INFO
        corp_info = data.CORPORATE_INFO
    """
    import importlib
    
    module_name = osc_settings.data_module_name
    full_module_path = f"data.osc.{module_name}"
    
    try:
        data_module = importlib.import_module(full_module_path)
        return data_module
    except ImportError as e:
        # Fallback to default prod data if env-specific doesn't exist
        if module_name != "osc_data":
            print(f"Warning: Data module '{full_module_path}' not found. "
                  f"Falling back to 'data.osc.osc_data'. Error: {e}")
            return importlib.import_module("data.osc.osc_data")
        raise


# Singleton instance
osc_settings = OSCSettings()
