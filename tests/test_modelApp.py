import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from helperFunctions import createNewModel, returnModel, deleteAllModels
import os
import signal

@pytest.fixture
def driver():
    #selenium_url = os.getenv('SELENIUM_URL')
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
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

    retryModelCreation = 0
    while retryModelCreation < 3:
        try: 
            createNewModel(driver)
            break
        except:
            deleteAllModels()
            retryModelCreation += 1
            if retryModelCreation < 3:
                time.sleep(10)
            else:
                raise

    yield driver
 
    # Delete models
    deleteAllModels()

    driver.quit()

@pytest.fixture
def driver2():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--disable-dev-shm-usage")
  
    driver = webdriver.Remote(
        command_executor='http://selenium:4444',
        options = options
    )

    yield driver

    driver.quit()

@pytest.fixture
def crashDriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--disable-dev-shm-usage")
  
    driver = webdriver.Remote(
        command_executor='http://selenium:4444',
        options = options
    )

    yield driver 

def test_returnModel(driver):
    returnModel(driver)
    modelLink = driver.find_element(By.PARTIAL_LINK_TEXT, "TestModel")
    assert "Writable" in modelLink.text, "Writable not found in the 'TestModel' link"

@pytest.mark.skip()
def test_readOnlyCheck(driver, driver2):
    login(driver2, "testuser2", "testuser2")
    wait = WebDriverWait(driver2, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='All Models...']"))).click()
    viewLink = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "View")))
    # Checks for View link in the All Models modal
    assert viewLink is not None, "View link not found on the page"

def test_editModelName(driver):
    wait = WebDriverWait(driver, 10)
    # Clicks model settings button
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "modelSettings"))).click()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="modelNameComp"]'))).clear()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="modelNameComp"]'))).send_keys("OtherModel")

    driver.find_element(By.CLASS_NAME, "btn-primary").click()
    wait.until(EC.title_contains("OtherModel"))
    # Checks the title for the new model name
    assert "OtherModel" in driver.title, "Title does not contain 'OtherModel'"

@pytest.mark.skip()
def test_unableToEditReadOnlyModel(driver, driver2):
    login(driver2, "testuser2", "testuser2")
    wait = WebDriverWait(driver2, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='All Models...']"))).click()
    # Opens the test model as a different user, thus opening it in read only
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "View"))).click()
    wait.until(EC.title_contains("TestModel"))
    # Clicks the model settings button
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "modelSettings"))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="modelNameComp"]'))).clear()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="modelNameComp"]'))).send_keys("OtherModel")
    driver2.find_element(By.CLASS_NAME, "btn-primary").click()
    # Refreshes browser to see changes
    driver2.refresh()

    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "modelSettings")))
    assert "OtherModel" not in driver.title, "Model Name was changed in ReadOnly"

@pytest.mark.skip()
def test_reloadReadOnlyModelAsWritable(driver, driver2):
    login(driver2, "testuser2", "testuser2")
    wait = WebDriverWait(driver2, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='All Models...']"))).click()
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "View"))).click()
    wait.until(EC.title_contains("TestModel"))
    
    returnModel(driver)
    # Click model setting button
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "modelSettings"))).click()
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "refreshBtn"))).click()
    alert = Alert(driver2)
    alert.accept()

    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "modelSettings"))).click()
    # Changes the model name
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="modelNameComp"]'))).clear()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="modelNameComp"]'))).send_keys("OtherModel")

    driver2.find_element(By.CLASS_NAME, "btn-primary").click()
    wait.until(EC.title_contains("OtherModel"))
    assert "OtherModel" in driver2.title, "Title does not contain 'OtherModel'"

def test_homeLinkReturnsModel(driver):
    wait = WebDriverWait(driver, 10)
    # Clicks home link
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="home-link"]'))).click()
    modelLink = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "TestModel")))

    assert "Writable" in modelLink.text, "Writable not found in the 'TestModel' link"

@pytest.mark.skip()
def test_logoutReturnsModels(driver, driver2):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "logoutBtn"))).click()

    # Log in as a new user one a different driver
    login(driver2, "testuser2", "testuser2")
    wait2 = WebDriverWait(driver2, 10)
    modelLink = wait2.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "TestModel")))

    assert "Writable" in modelLink.text, "Writable not found in the 'TestModel' link"

@pytest.mark.skip()
def test_browserCloseReturnsModels(crashDriver, driver):

    login(crashDriver, "testuser2", "testuser2")
    createNewModel(crashDriver)

    wait = WebDriverWait(crashDriver, 10)
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "modelSettings")))

    # Get the process ID of the browser
    pid = crashDriver.service.process.pid

    # Simulate a crash by killing the process
    os.kill(pid, signal.SIGTERM)

    driver.refresh()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='All Models...']"))).click()
    actionLink = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="action-link"]')))
    assert "Edit" in actionLink.text , "Edit link is not found"
