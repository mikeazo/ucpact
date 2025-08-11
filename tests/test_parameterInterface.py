import pytest
import time
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from helperFunctions import createNewModel, deleteAllModels, createBasicModel
from env import USERNAME, PASSWORD

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

def test_createParameterInterface(driver):
    driver.maximize_window()
    action = ActionChains(driver) # Sets up drag and drop 
    wait = WebDriverWait(driver, 10)

    # Sets up drag and drop source and target
    source = wait.until(EC.visibility_of_element_located((By.ID, "parameterInterfaceCompBoxElem")))
    target = wait.until(EC.visibility_of_element_located((By.ID, "realFunctionality-environment")))
    action.drag_and_drop(source, target).perform()

    # Name the parameter 
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="paramInterNameComp"]'))).send_keys("ParamInter1")
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()

    # Check that the parameter name appears
    paramInterName = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "paramInterDnDName")))
    assert "ParamInter1" == paramInterName.text, "ParamInter1 is not displayed as Party name"

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    paramInterArray = data['model']['realFunctionality']['parameterInterfaces']

    assert paramInterArray[0]['name'] == 'ParamInter1', "Parameter name is not 'ParamInter1' in JSON file"

def test_renameParameterInterface(driver):
    driver.maximize_window()
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    source = wait.until(EC.visibility_of_element_located((By.ID, "parameterInterfaceCompBoxElem")))
    target = wait.until(EC.visibility_of_element_located((By.ID, "realFunctionality-environment")))
    action.drag_and_drop(source, target).perform()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="paramInterNameComp"]'))).send_keys("ParamInter1")
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="paramInterOptions"]'))).click()
    nameInput = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="paramInterNameComp"]')))
    nameInput.clear()
    nameInput.send_keys("ParamInter2")
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()

    paramInterName = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "paramInterDnDName")))
    assert "ParamInter2" == paramInterName.text, "ParamInter2 is not displayed as Party name"

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    paramInterArray = data['model']['realFunctionality']['parameterInterfaces']

    assert paramInterArray[0]['name'] == 'ParamInter2', "Parameter name is not 'ParamInter2' in JSON file"

def test_closeParamterInterfaceModal(driver):
    driver.maximize_window()
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    source = wait.until(EC.visibility_of_element_located((By.ID, "parameterInterfaceCompBoxElem")))
    target = wait.until(EC.visibility_of_element_located((By.ID, "realFunctionality-environment")))
    action.drag_and_drop(source, target).perform()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="paramInterNameComp"]'))).send_keys("ParamInter1")
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="paramInterOptions"]'))).click()
    nameInput = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="paramInterNameComp"]')))
    nameInput.clear()
    nameInput.send_keys("ParamInter2")
    driver.find_element(By.XPATH, "//button[text()=' Close ']").click()

    paramInterName = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "paramInterDnDName")))
    assert "ParamInter1" == paramInterName.text, "ParamInter1 is not displayed as Party name"

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    paramInterArray = data['model']['realFunctionality']['parameterInterfaces']

    assert paramInterArray[0]['name'] == 'ParamInter1', "Parameter name is not 'ParamInter1' in JSON file"

def test_deleteParameterInterface(driver):
    driver.maximize_window()
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    source = wait.until(EC.visibility_of_element_located((By.ID, "parameterInterfaceCompBoxElem")))
    target = wait.until(EC.visibility_of_element_located((By.ID, "realFunctionality-environment")))
    action.drag_and_drop(source, target).perform()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="paramInterNameComp"]'))).send_keys("ParamInter1")
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="paramInterOptions"]'))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="paramInterNameComp"]')))
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Delete']"))).click()

    paramInters = driver.find_elements(By.CLASS_NAME, "paramInter")

    assert len(paramInters) == 1, "Parameter array length is not 1"

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    paramInterArray = data['model']['realFunctionality']['parameterInterfaces']

    assert len(paramInterArray) == 0, "Parameter array is not empty in JSON file"

def test_changeParameterInterfaceColor(driver):
    driver.maximize_window()
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    source = wait.until(EC.visibility_of_element_located((By.ID, "parameterInterfaceCompBoxElem")))
    target = wait.until(EC.visibility_of_element_located((By.ID, "realFunctionality-environment")))
    action.drag_and_drop(source, target).perform()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="paramInterNameComp"]'))).send_keys("ParamInter1")
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="paramInterOptions"]'))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[title="#89D7DE"]'))).click()
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()

    paramInter = driver.find_elements(By.CLASS_NAME, "paramInter")[1]
    color = paramInter.value_of_css_property("background-color")
    assert "rgba(137, 215, 222, 1)" == color, "Parameter background color is not correct"

def test_selectCompositeDirectInterface(driver):
    createBasicModel()
    driver.maximize_window()
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    source = wait.until(EC.visibility_of_element_located((By.ID, "parameterInterfaceCompBoxElem")))
    target = wait.until(EC.visibility_of_element_located((By.ID, "realFunctionality-environment")))
    action.drag_and_drop(source, target).perform()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="paramInterNameComp"]'))).send_keys("ParamInter1")
    driver.find_element(By.ID, "paramInterCompDirSelect").click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '//div[text()="CompDir1 (BasicModel)"]'))).click()
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    paramInterArray = data['model']['realFunctionality']['parameterInterfaces']

    assert paramInterArray[0]['idOfInterface'] == '41e7ea4c-f764-4b92-a27f-902195fef6d1', "Parameter Composite Direct id is not correct in JSON file"
