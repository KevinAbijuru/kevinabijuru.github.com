# Assignment 3 Test Plan

**Module:** Development Operations (ITLDO801)  
**Portfolio:** Kevin Abijuru Portfolio  
**Base URL:** https://kevinabijuru.github.io/  
**Test tool:** Python Selenium with headless Chromium  

| Test ID | What is tested | Steps | Expected result |
|---|---|---|---|
| TC-01 | Home navigation link | Open the portfolio, locate the Home link, click it, inspect the URL. | The URL path is `/index.html`; status is PASS. |
| TC-02 | About navigation link | Open the portfolio, locate the About link, click it, inspect the URL. | The URL path is `/about.html`; status is PASS. |
| TC-03 | Services navigation link | Open the portfolio, locate the Services link, click it, inspect the URL. | The URL path is `/services.html`; status is PASS. |
| TC-04 | Portfolio navigation link | Open the portfolio, locate the Portfolio link, click it, inspect the URL. | The URL path is `/portfolio.html`; status is PASS. |
| TC-05 | Contact navigation link | Open the portfolio, locate the Contact link, click it, inspect the URL. | The URL path is `/contact.html`; status is PASS. |
| TC-06 | Portfolio Details link in Pages menu | Open the portfolio, locate the Portfolio Details link, click it, inspect the URL. | The URL path is `/portfolio-details.html`; status is PASS. |
| TC-07 | Missing-link negative test | Open the portfolio and search for the deliberately absent `missing-assignment-link.html` link. | The locator timeout is handled, the test is recorded as FAIL, the error URL and screenshot are recorded, and later tests continue. |

## Logging evidence

Each generated run log records a timestamp, level, test ID, description, expected result, actual result, status, duration, page URL, browser details, operating system, and failure screenshot where applicable. The run header and summary record the website, browser, total tests, passed tests, failed tests, and total duration.
