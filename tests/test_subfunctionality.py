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

def test_createSubfunctionality(driver):
    driver.maximize_window()
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    source = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "subFunc")))
    target = wait.until(EC.visibility_of_element_located((By.ID, "realFunctionality-environment")))
    action.drag_and_drop(source, target).perform()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="subfuncnamecomp"]'))).send_keys("Sub1")
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()

    subfunNameSpan = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "subFuncDnDName")))
    assert "Sub1" == subfunNameSpan.text, "Sub1 is not displayed as Party name"

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    subFuncArray = data['model']['subfunctionalities']['subfunctionalities']

    assert subFuncArray[0]['name'] == 'Sub1', "Subfunc name is not 'Sub1' in JSON file"

def test_renameSubfunctionality(driver):
    driver.maximize_window()
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    source = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "subFunc")))
    target = wait.until(EC.visibility_of_element_located((By.ID, "realFunctionality-environment")))
    action.drag_and_drop(source, target).perform()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="subfuncnamecomp"]'))).send_keys("Sub1")
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="subfuncOptions"]'))).click()
    nameInput = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="subfuncnamecomp"]')))
    nameInput.clear()
    nameInput.send_keys('Sub2')
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()

    subfunNameSpan = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "subFuncDnDName")))
    assert "Sub2" == subfunNameSpan.text, "Sub2 is not displayed as Party name"

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    subFuncArray = data['model']['subfunctionalities']['subfunctionalities']

    assert subFuncArray[0]['name'] == 'Sub2', "Subfunc name is not 'Sub2' in JSON file"    

def test_closeSubfunctionalityModal(driver):
    driver.maximize_window()
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    source = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "subFunc")))
    target = wait.until(EC.visibility_of_element_located((By.ID, "realFunctionality-environment")))
    action.drag_and_drop(source, target).perform()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="subfuncnamecomp"]'))).send_keys("Sub1")
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="subfuncOptions"]'))).click()
    nameInput = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="subfuncnamecomp"]')))
    nameInput.clear()
    nameInput.send_keys('Sub2')
    driver.find_element(By.XPATH, "//button[text()=' Close ']").click()

    subfunNameSpan = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "subFuncDnDName")))
    assert "Sub1" == subfunNameSpan.text, "Sub1 is not displayed as Party name"

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    subFuncArray = data['model']['subfunctionalities']['subfunctionalities']

    assert subFuncArray[0]['name'] == 'Sub1', "Subfunc name is not 'Sub1' in JSON file"  

def test_deleteSubfunctionality(driver):
    driver.maximize_window()
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    source = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "subFunc")))
    target = wait.until(EC.visibility_of_element_located((By.ID, "realFunctionality-environment")))
    action.drag_and_drop(source, target).perform()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="subfuncnamecomp"]'))).send_keys("Sub1")
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="subfuncOptions"]'))).click()
    driver.find_element(By.XPATH, "//button[text()='Delete']").click()

    subfuns = driver.find_elements(By.CLASS_NAME, "subFunc")

    assert len(subfuns) == 1, "Subfunc array length is not 1"

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    subfuncArray = data['model']['subfunctionalities']['subfunctionalities']

    assert len(subfuncArray) == 0, "Subfunc array is not empty in JSON file"

def test_changeSubfunctionalityColor(driver):
    driver.maximize_window()
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    source = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "subFunc")))
    target = wait.until(EC.visibility_of_element_located((By.ID, "realFunctionality-environment")))
    action.drag_and_drop(source, target).perform()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="subfuncnamecomp"]'))).send_keys("Sub1")
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="subfuncOptions"]'))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[title="#db585f"]'))).click()
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()

    subfunc = driver.find_elements(By.CLASS_NAME, "subFunc")[1]
    color = subfunc.value_of_css_property("background-color")
    assert "rgba(219, 88, 95, 1)" == color, "Subfunc background color is not correct"

def test_selectIdealFunctionality(driver):
    createBasicModel()
    driver.maximize_window()
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    source = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "subFunc")))
    target = wait.until(EC.visibility_of_element_located((By.ID, "realFunctionality-environment")))
    action.drag_and_drop(source, target).perform()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="subfuncnamecomp"]'))).send_keys("Sub1")
    driver.find_element(By.ID, "subfuncIdealFuncSelect").click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '//div[text()="IF (BasicModel)"]'))).click()
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()
    
    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    subfuncArray = data['model']['subfunctionalities']['subfunctionalities']

    assert subfuncArray[0]['idealFunctionalityId'] == '97e2f6a1-663d-ebc2-4fe3-7f806cf79964', "Subfunctionality IF id is not correct in JSON file"
