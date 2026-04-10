from datetime import datetime
import pytest

def pytest_configure(config):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    config.option.htmlpath = f"reports/Report_{timestamp}.html"