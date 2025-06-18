import pytest
import time
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helperFunctions import createNewModel, deleteAllModels

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

def test_renameSimulator(driver):
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    # Switch to ideal world tab
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-rr-ui-event-key="idWorld"]'))).click()
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "idwTitle")))
    # Open sim modal
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="simOptions"]'))).click()
    nameInput = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="simnameComp"]')))
    nameInput.clear()
    nameInput.send_keys("TestName")
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()
    # Checks the sim name displays
    simName = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "simDnDName")))
    assert "TestName" == simName.text, "'TestName' is not displayed as sim name"

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    sim = data['model']['simulator']
    assert sim['name'] == 'TestName', "Sim name is not 'TestName' in JSON file"

def test_selectSimulatorRealFunctionality(driver):
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    # Switch to ideal world tab
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-rr-ui-event-key="idWorld"]'))).click()
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "idwTitle")))
    # Open sim modal
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="simOptions"]'))).click()
    driver.find_element(By.ID, "simRealFuncSelect").click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '//div[text()="Real_Functionality"]'))).click()
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()
    # Check if the arrow renders
    assert wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[stroke="red"]'))) is not None, "xArrow does not exist"

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    sim = data['model']['simulator']
    assert sim['realFunctionality'] != '', "Sim real functionality is null in JSON file"

def test_selectSimulatorBasicAdversarialInterface(driver):
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    # Create Basic Adversarial Interface
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-rr-ui-event-key="interfaces"]'))).click()
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "interTitle")))
    driver.find_element(By.CLASS_NAME, "interAdd").click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[title="Add Basic Interface"]'))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="accorBasicHeaderButton"]'))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[starts-with(@id, 'basic-interface-name')]"))).send_keys("BasicInt1")
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[title="adversarialBasicButton"]'))).click()

    # Switch to ideal world tab
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-rr-ui-event-key="idWorld"]'))).click()
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "idwTitle")))
    # Open sim modal
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="simOptions"]'))).click()
    driver.find_element(By.ID, "simBasicAdvIntSelect").click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '//div[text()="BasicInt1"]'))).click()
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()
    # Check if the arrow renders
    assert wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[stroke="red"]'))) is not None, "xArrow does not exist"

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    sim = data['model']['simulator']
    assert sim['basicAdversarialInterface'] != '', "Sim real functionality is null in JSON file"