#import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from helperFunctions import createNewModel, deleteModel, deleteAllModels, returnModel
from env import BASE_URL

@pytest.fixture
def driver():
    #selenium_url = os.getenv('SELENIUM_URL')
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--allow-insecure-localhost")

    retryDriver = 0
    while retryDriver < 3:
        try:
            driver = webdriver.Remote(
                command_executor='http://selenium:4444/wd/hub',
                options = options
            )
            break
        except:
            retryDriver += 1
            if retryDriver < 3:
                time.sleep(30) 
            else:
                raise

    yield driver
 
    # Delete models
    deleteAllModels()

    driver.quit()

#@pytest.mark.skip()
def test_frontendLoad(driver):
    driver.get(BASE_URL)
    assert "UC-PACT" in driver.title

#@pytest.mark.skip()
def test_createNewModel(driver):
    createNewModel(driver)
    assert "TestModel" in driver.title

#@pytest.mark.skip()
def test_openExistingModel(driver):
    createNewModel(driver)

    returnModel(driver)

    wait = WebDriverWait(driver, 30)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='All Models...']"))).click()
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Edit"))).click()
    wait.until(EC.title_contains("TestModel"))
    assert "TestModel" in driver.title

#@pytest.mark.skip()
def test_deleteModel(driver):
    createNewModel(driver)
    deleteModel(driver)
    driver.get(BASE_URL)
    page_source = driver.page_source
    assert "TestModel" not in page_source, "'TestModel' found on page, but it should not appear."
