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

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    partyArray = data['model']['parties']['parties']

    assert partyArray[0]['name'] == 'Party1', "Party name is not 'Party1' in JSON file"

def test_renameParty(driver):
    driver.maximize_window()
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    source = wait.until(EC.visibility_of_element_located((By.ID, "partyCompBoxElem")))
    target = wait.until(EC.visibility_of_element_located((By.ID, "realFunctionality-environment")))
    action.drag_and_drop(source, target).perform()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="partynameComp"]'))).send_keys("Party1")
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="partyOptions"]'))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="partynameComp"]'))).clear()
    driver.find_element(By.CSS_SELECTOR, '[name="partynameComp"]').send_keys("Party2")
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()

    partyNameSpan = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "partyDnDName")))
    assert "Party2" == partyNameSpan.text, "Party2 is not displayed as Party name"

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    partyArray = data['model']['parties']['parties']

    assert partyArray[0]['name'] == 'Party2', "Party name is not 'Party2' in JSON file"

def test_closePartyModal(driver):
    driver.maximize_window()
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    source = wait.until(EC.visibility_of_element_located((By.ID, "partyCompBoxElem")))
    target = wait.until(EC.visibility_of_element_located((By.ID, "realFunctionality-environment")))
    action.drag_and_drop(source, target).perform()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="partynameComp"]'))).send_keys("Party1")
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="partyOptions"]'))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="partynameComp"]'))).clear()
    driver.find_element(By.CSS_SELECTOR, '[name="partynameComp"]').send_keys("Party2")
    driver.find_element(By.XPATH, "//button[text()=' Close ']").click()

    partyNameSpan = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "partyDnDName")))
    assert "Party1" == partyNameSpan.text, "Party1 is not displayed as Party name"

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    partyArray = data['model']['parties']['parties']

    assert partyArray[0]['name'] == 'Party1', "Party name is not 'Party1' in JSON file"

def test_deleteParty(driver):
    driver.maximize_window()
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    source = wait.until(EC.visibility_of_element_located((By.ID, "partyCompBoxElem")))
    target = wait.until(EC.visibility_of_element_located((By.ID, "realFunctionality-environment")))
    action.drag_and_drop(source, target).perform()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="partynameComp"]'))).send_keys("Party1")
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="partyOptions"]'))).click()
    driver.find_element(By.XPATH, "//button[text()='Delete']").click()

    parties = driver.find_elements(By.CLASS_NAME, "party")

    assert len(parties) == 1, "Length of party array is not 1"

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    partyArray = data['model']['parties']['parties']

    assert len(partyArray) == 0, "Party array is not empty in JSON file"


def test_changePartyColor(driver):
    driver.maximize_window()
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    source = wait.until(EC.visibility_of_element_located((By.ID, "partyCompBoxElem")))
    target = wait.until(EC.visibility_of_element_located((By.ID, "realFunctionality-environment")))
    action.drag_and_drop(source, target).perform()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="partynameComp"]'))).send_keys("Party1")
    driver.find_element(By.CSS_SELECTOR, '[title="#c7978c"]').click()
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()

    party = driver.find_elements(By.CLASS_NAME, "party")[1]
    color = party.value_of_css_property("background-color")
    assert "rgba(199, 151, 140, 1)" == color, "Party background color is not correct"

def test_selectBasicDirectInterface(driver):
    createBasicModel()
    loadBasicModel(driver)
    driver.maximize_window()
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="realFuncOptions"]'))).click()
    wait.until(EC.visibility_of_element_located((By.ID, "compDirIntSelect"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '//div[text()="CompDir1"]'))).click()
    driver.find_element(By.CLASS_NAME, "btn-primary").click()

    source = wait.until(EC.visibility_of_element_located((By.ID, "partyCompBoxElem")))
    target = wait.until(EC.visibility_of_element_located((By.ID, "realFunctionality-environment")))
    action.drag_and_drop(source, target).perform()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="partynameComp"]'))).send_keys("Party1")
    driver.find_element(By.ID, "partyBasicDirIntSelect").click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '//div[text()="BasicInt1"]'))).click()
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "partyDnDName")))

    # Check xArrow line render
    assert wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[stroke="CornflowerBlue"]'))) is not None, "xArrow does not exist"
    
    # Check JSON file
    fileName = os.path.join('models', 'BasicModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    partyArray = data['model']['parties']['parties']

    assert partyArray[0]['basicDirectInterface'] == '0dafcf3f-d7f7-3a99-8779-2c63b909c16d', "Party Basic Direct Interface is not correct in JSON file"
    
def test_selectBasicAdversarialInterface(driver):
    createBasicModel()
    loadBasicModel(driver)
    driver.maximize_window()
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="realFuncOptions"]'))).click()
    wait.until(EC.visibility_of_element_located((By.ID, "compAdvIntSelect"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '//div[text()="CompAdv1"]'))).click()
    driver.find_element(By.CLASS_NAME, "btn-primary").click()

    source = wait.until(EC.visibility_of_element_located((By.ID, "partyCompBoxElem")))
    target = wait.until(EC.visibility_of_element_located((By.ID, "realFunctionality-environment")))
    action.drag_and_drop(source, target).perform()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="partynameComp"]'))).send_keys("Party1")
    driver.find_element(By.ID, "partyBasicAdvIntSelect").click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '//div[text()="BasicInt2"]'))).click()
    driver.find_element(By.XPATH, "//button[text()=' Save Changes ']").click()
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "partyDnDName")))

    # Check xArrow line render
    assert wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[stroke="red"]'))) is not None, "xArrow does not exist"
    
    # Check JSON file
    fileName = os.path.join('models', 'BasicModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    partyArray = data['model']['parties']['parties']

    assert partyArray[0]['basicAdversarialInterface'] == 'b8f17598-0b6e-bc3f-5715-ceee6e33d4cc', "Party Basic Direct Interface is not correct in JSON file"
    
