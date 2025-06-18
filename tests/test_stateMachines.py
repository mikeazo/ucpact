import pytest
import time
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
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

def test_switchToStateMachinesTab(driver):
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-rr-ui-event-key="stateMachines"]'))).click()

    assert wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "smTitle"))) is not None, "State Machine title not found"

def test_createAndNameState(driver):
    driver.maximize_window()
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-rr-ui-event-key="stateMachines"]'))).click()

    source = wait.until(EC.visibility_of_element_located((By.ID, "stateCompBoxElem")))
    target = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "providerflow")))
    action.drag_and_drop(source, target).perform()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[placeholder="Enter a name"]'))).send_keys("State1")
    driver.find_element(By.CSS_SELECTOR, ".circle-picker > span:nth-child(2) > div:nth-child(1) > span:nth-child(1) > div:nth-child(1)").click()
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()
    time.sleep(1)

    stateEle = driver.find_element(By.CSS_SELECTOR, "div.react-flow__node:nth-child(2) > div:nth-child(1)")
    stateColor = stateEle.value_of_css_property("background-color")

    assert "State1" in driver.page_source, "State was not created"
    assert stateColor == "rgba(199, 151, 140, 1)"
    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    statesArray = data['model']['stateMachines']['states']

    assert statesArray[2]['name'] == "State1", "State name is not 'State1' in JSON file"
    assert statesArray[2]['color'] == "#c7978c", "State color is not '#c7978c' in JSON file"
    
def test_createTransition(driver):
    driver.maximize_window()
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-rr-ui-event-key="stateMachines"]'))).click()

    source = wait.until(EC.visibility_of_element_located((By.ID, "stateCompBoxElem")))
    target = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "providerflow")))
    action.drag_and_drop(source, target).perform()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[placeholder="Enter a name"]'))).send_keys("State1")
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()

    # Read the JSON file for the correct ids
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    initStateId = data['model']['stateMachines']['states'][0]['id']
    state1Id = data['model']['stateMachines']['states'][2]['id']

    initState_css_selector = f'[data-handleid="13"][data-nodeid="{initStateId}"]'
    state1_css_selector = f'[data-handleid="5"][data-nodeid="{state1Id}"]'

    source_handle = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, initState_css_selector)))
    target_handle = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, state1_css_selector)))
    action.drag_and_drop(source_handle, target_handle).perform()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[placeholder="Enter a name"]'))).send_keys("Transition1")
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    transitionArray = data['model']['stateMachines']['transitions']

    assert transitionArray[0]['name'] == "Transition1", "Transition name is not 'Transition1' in JSON file"