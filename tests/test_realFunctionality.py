import pytest
import time
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from helperFunctions import createNewModel, deleteAllModels, createBasicModel, loadBasicModel
from env import COMPOSITE_DIRECT_INTERFACE_ID, COMPOSITE_ADVERSARIAL_INTERFACE_ID

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

def test_renameRealFunctionality(driver):
    # This test fails in headless mode, I don't know why
    driver.maximize_window()

    wait = WebDriverWait(driver, 10)

    # It fails on this line, saying the element is unclickable, but it's clickable when not in headless...?
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="realFuncOptions"]'))).click()
    nameInput = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="realFuncNameComp"]')))
    nameInput.clear()
    nameInput.send_keys("Unreal_Functionality")
    driver.find_element(By.CLASS_NAME, "btn-primary").click()

    realFuncName = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "rwTitle")))
    assert "Unreal_Functionality" == realFuncName.text

def test_closeRealFunctionalityModal(driver):
    # This test fails in headless mode, I don't know why
    driver.maximize_window()

    wait = WebDriverWait(driver, 10)

    # It fails on this line, saying the element is unclickable, but it's clickable when not in headless...?
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="realFuncOptions"]'))).click()
    nameInput = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="realFuncNameComp"]')))
    nameInput.clear()
    nameInput.send_keys("Unreal_Functionality")
    driver.find_element(By.CLASS_NAME, "btn-secondary").click()

    realFuncName = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "rwTitle")))
    assert "Real_Functionality" == realFuncName.text

def test_createParty(driver):
    driver.maximize_window()
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    source = wait.until(EC.visibility_of_element_located((By.ID, "partyCompBoxElem")))
    target = wait.until(EC.visibility_of_element_located((By.ID, "realFunctionality-environment")))
    action.drag_and_drop(source, target).perform()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="partynameComp"]'))).send_keys("Party1")
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()

    partyNameSpan = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "partyDnDName")))
    assert "Party1" == partyNameSpan.text, "Party1 is not displayed as Party name"

def test_createSubfunctionality(driver):
    driver.maximize_window()
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    source = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "subFunc")))
    target = wait.until(EC.visibility_of_element_located((By.ID, "realFunctionality-environment")))
    action.drag_and_drop(source, target).perform()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="subfuncnamecomp"]'))).send_keys("Subfunc1")
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()

    subfuncNameSpan = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "subFuncDnDName")))
    assert "Subfunc1" == subfuncNameSpan.text, "Subfunc1 is not displayed as Party name"

def test_createParameterInterface(driver):
    driver.maximize_window()
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    source = wait.until(EC.visibility_of_element_located((By.ID, "parameterInterfaceCompBoxElem")))
    target = wait.until(EC.visibility_of_element_located((By.ID, "realFunctionality-environment")))
    action.drag_and_drop(source, target).perform()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="paramInterNameComp"]'))).send_keys("ParamInter1")
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()

    paramInterName = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "paramInterDnDName")))
    assert "ParamInter1" == paramInterName.text, "ParamInter1 is not displayed as Party name"

def test_selectCompositeDirectInterface(driver):
    createBasicModel()
    loadBasicModel(driver)

    driver.maximize_window()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="realFuncOptions"]'))).click()
    wait.until(EC.visibility_of_element_located((By.ID, "compDirIntSelect"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '//div[text()="CompDir1"]'))).click()
    driver.find_element(By.CLASS_NAME, "btn-primary").click()

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="realFuncOptions"]'))).click()
    selection = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[text()="CompDir1"]')))
    assert "CompDir1" in selection.text

    # Check JSON file
    fileName = os.path.join('models', 'BasicModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    assert data['model']['realFunctionality']['compositeDirectInterface'] == COMPOSITE_DIRECT_INTERFACE_ID

def test_selectCompositeAdversarialInterface(driver):
    createBasicModel()
    loadBasicModel(driver)

    driver.maximize_window()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="realFuncOptions"]'))).click()
    wait.until(EC.visibility_of_element_located((By.ID, "compAdvIntSelect"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '//div[text()="CompAdv1"]'))).click()
    driver.find_element(By.CLASS_NAME, "btn-primary").click()

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="realFuncOptions"]'))).click()
    selection = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[text()="CompAdv1"]')))
    assert "CompAdv1" in selection.text

    # Check JSON file
    fileName = os.path.join('models', 'BasicModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    assert data['model']['realFunctionality']['compositeAdversarialInterface'] == COMPOSITE_ADVERSARIAL_INTERFACE_ID
