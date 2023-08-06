from selenite.core.driver_factory import DriverFactory
from selenite.shared.config import config

driver = DriverFactory(config)
browser = driver.webdriver
