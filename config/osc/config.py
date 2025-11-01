"""OSC application-specific configuration."""

from dataclasses import dataclass

from core.utils import get_env, get_env_int


@dataclass
class OSCSettings:
    """OSC application settings.

    Attributes:
        base_url: Base URL for OSC application
        login_path: Login endpoint path
        dashboard_path: Dashboard endpoint path
        quote_path: Quote creation endpoint path
        timeout_ms: OSC-specific timeout override (optional)
    """

    base_url: str
    login_path: str
    dashboard_path: str
    quote_path: str
    timeout_ms: int

    def __init__(self) -> None:
        """Initialize OSC settings from environment variables."""
        self.base_url = get_env("OSC_BASE_URL", "https://uno.eftsecure.net")
        self.login_path = get_env("OSC_LOGIN_PATH", "/SalesCenter/frmHome.aspx")
        self.dashboard_path = get_env("OSC_DASHBOARD_PATH", "/SalesCenter/frmHome.aspx")
        self.quote_path = get_env("OSC_QUOTE_PATH", "/SalesCenter/quote/create")
        self.timeout_ms = get_env_int("OSC_TIMEOUT_MS", default=30000)

    @property
    def login_url(self) -> str:
        """Full login URL."""
        return f"{self.base_url}{self.login_path}"

    @property
    def dashboard_url(self) -> str:
        """Full dashboard URL."""
        return f"{self.base_url}{self.dashboard_path}"

    @property
    def mfa_url(self) -> str:
        """Full MFA page URL."""
        return f"{self.base_url}{self.mfa_path}"


# Singleton instance
osc_settings = OSCSettings()
