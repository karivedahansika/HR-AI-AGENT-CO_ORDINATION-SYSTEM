from connectors.base import BaseConnector
from connectors.hrms_api import HRMSConnector
from connectors.email_api import EmailConnector

CONNECTORS = {
    "hrms": HRMSConnector,
    "email": EmailConnector,
}

def get_connector(name: str, config=None):
    cls = CONNECTORS.get(name)
    if not cls:
        raise KeyError(f"Unknown connector: {name}")
    return cls(config)
