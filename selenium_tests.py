"""Selenium link tests with structured, timestamped evidence logging."""

from __future__ import annotations

import logging
import os
import platform
import sys
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

ROOT = Path(__file__).resolve().parent
LOG_DIR = ROOT / "logs"
SCREENSHOT_DIR = LOG_DIR / "screenshots"
BASE_URL = os.getenv("PORTFOLIO_BASE_URL", "https://kevinabijuru.github.io/")
WAIT_SECONDS = int(os.getenv("SELENIUM_WAIT_SECONDS", "15"))


@dataclass(frozen=True)
class TestCase:
    test_id: str
    description: str
    target: str
    expected: str
    negative: bool = False


TEST_CASES = (
    TestCase("TC-01", "Click Home from the portfolio navigation", "index.html", "URL path is /index.html"),
    TestCase("TC-02", "Click About from the portfolio navigation", "about.html", "URL path is /about.html"),
    TestCase("TC-03", "Click Services from the portfolio navigation", "services.html", "URL path is /services.html"),
    TestCase("TC-04", "Click Portfolio from the portfolio navigation", "portfolio.html", "URL path is /portfolio.html"),
    TestCase("TC-05", "Click Contact from the portfolio navigation", "contact.html", "URL path is /contact.html"),
    TestCase("TC-06", "Click Portfolio Details from the Pages menu", "portfolio-details.html", "URL path is /portfolio-details.html"),
    TestCase("TC-07", "Locate a deliberately missing navigation link", "missing-assignment-link.html", "Missing locator is handled and recorded as FAIL", True),
)


class AssignmentFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.fromtimestamp(record.created, timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S")
        return f"{timestamp} | {record.levelname:<7} | {record.getMessage()}"


def make_logger(log_path: Path) -> logging.Logger:
    logger = logging.getLogger(f"assignment3.{log_path.stem}")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setFormatter(AssignmentFormatter())
    logger.addHandler(handler)
    return logger


def create_driver() -> webdriver.Chrome:
    options = Options()
    options.page_load_strategy = "eager"
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1440,1000")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--proxy-server=direct://")
    options.add_argument("--proxy-bypass-list=*")
    service = Service(executable_path="/usr/bin/chromedriver") if Path("/usr/bin/chromedriver").exists() else Service()
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(WAIT_SECONDS)
    return driver


def path_of(url: str) -> str:
    return urlparse(url).path.rstrip("/") or "/"


def target_url(case: TestCase) -> str:
    return urljoin(BASE_URL, case.target)


def find_navigation_link(driver: webdriver.Chrome, case: TestCase):
    if case.negative:
        return WebDriverWait(driver, 3).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "a[href='missing-assignment-link.html']"))
        )
    page = case.target
    if case.test_id == "TC-06":
        pages_menu = WebDriverWait(driver, WAIT_SECONDS).until(
            expected_conditions.presence_of_element_located((By.XPATH, "//a[contains(normalize-space(), 'Pages') and contains(@class, 'dropdown-toggle')]"))
        )
        driver.execute_script("arguments[0].click();", pages_menu)
        return WebDriverWait(driver, WAIT_SECONDS).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, f"a[href$='{page}']"))
        )
    return WebDriverWait(driver, WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, f"a[href$='{page}']"))
    )


def run() -> int:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    log_path = LOG_DIR / f"selenium_run_{run_id}.log"
    logger = make_logger(log_path)
    run_started = time.perf_counter()
    passed = 0
    failed = 0
    driver = None

    try:
        driver = create_driver()
        capabilities = driver.capabilities
        browser = capabilities.get("browserName", "unknown")
        browser_version = capabilities.get("browserVersion", "unknown")
        logger.info("RUN START | website=%s | browser=%s %s | operating_system=%s | run_id=%s", BASE_URL, browser, browser_version, platform.platform(), run_id)

        for case in TEST_CASES:
            started = time.perf_counter()
            expected_url = target_url(case)
            actual = "not reached"
            screenshot = "none"
            try:
                driver.get(BASE_URL)
                link = find_navigation_link(driver, case)
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
                driver.execute_script("arguments[0].click();", link)
                if case.negative:
                    raise AssertionError("Controlled negative test unexpectedly found the missing link")
                WebDriverWait(driver, WAIT_SECONDS).until(lambda browser_instance: path_of(browser_instance.current_url) == path_of(expected_url))
                actual = driver.current_url
                duration = time.perf_counter() - started
                passed += 1
                logger.info("%s | what_tested=%s | expected=%s | actual=%s | status=PASS | duration=%.3fs | title=%s", case.test_id, case.description, case.expected, actual, duration, driver.title)
            except (AssertionError, TimeoutException, WebDriverException) as error:
                failed += 1
                actual = driver.current_url if driver else "driver unavailable"
                screenshot_path = SCREENSHOT_DIR / f"{run_id}_{case.test_id}_fail.png"
                try:
                    if driver:
                        driver.save_screenshot(str(screenshot_path))
                        screenshot = str(screenshot_path.relative_to(ROOT))
                except WebDriverException:
                    screenshot = "screenshot unavailable"
                duration = time.perf_counter() - started
                logger.error("%s | what_tested=%s | expected=%s | actual=%s | status=FAIL | duration=%.3fs | page_url=%s | error=%s | screenshot=%s", case.test_id, case.description, case.expected, actual, duration, actual, error, screenshot)
            finally:
                if driver:
                    try:
                        driver.get(BASE_URL)
                    except WebDriverException:
                        pass

        total_duration = time.perf_counter() - run_started
        logger.info("RUN END | total_tests=%d | passed=%d | failed=%d | duration=%.3fs | log_file=%s", len(TEST_CASES), passed, failed, total_duration, log_path.name)
        print(f"Run complete: {passed} passed, {failed} failed; log={log_path}")
        return 0
    finally:
        if driver:
            driver.quit()
        for handler in logger.handlers:
            handler.close()
            logger.removeHandler(handler)


if __name__ == "__main__":
    sys.exit(run())
