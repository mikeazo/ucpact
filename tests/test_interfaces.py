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

def test_switchToInterfacesTab(driver):
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-rr-ui-event-key="interfaces"]'))).click()

    assert wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "interTitle"))) is not None, "Interfaces title not found"

def test_createCompositeInterface(driver):
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-rr-ui-event-key="interfaces"]'))).click()

    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'interAdd'))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[title="Add Composite Interface"]'))).click()

    assert wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="accorCompHeaderButton"]'))) is not None, "Composite Interface does not exist"
    
    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    compInterfaceArray = data['model']['interfaces']['compInters']

    assert compInterfaceArray[0] is not None, "Comp Interface does not exist in JSON file"

def test_createBasicInterface(driver):
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-rr-ui-event-key="interfaces"]'))).click()
    
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'interAdd'))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[title="Add Basic Interface"]'))).click()

    assert wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="accorBasicHeaderButton"]'))) is not None, "Basic Interface does not exist"

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    basicInterfaceArray = data['model']['interfaces']['basicInters']

    assert basicInterfaceArray[0] is not None, "Basic Interface does not exist in JSON file"

def test_nameCompositeInterface(driver):
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-rr-ui-event-key="interfaces"]'))).click()

    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'interAdd'))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[title="Add Composite Interface"]'))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="accorCompHeaderButton"]'))).click() 

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[placeholder="Interface Name"]'))).send_keys("Comp1")
    time.sleep(1)
    header = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'accordion-button')))

    assert "Comp1" in header.text, 'Composite Interface Name is not "Comp1"'

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    compInterfaceArray = data['model']['interfaces']['compInters']

    assert compInterfaceArray[0]['name'] == "Comp1", "Basic Interface name is not 'Comp1' in JSON file"

def test_nameBasicInterface(driver):
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-rr-ui-event-key="interfaces"]'))).click()
    
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'interAdd'))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[title="Add Basic Interface"]'))).click()
    
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="accorBasicHeaderButton"]'))).click() 
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[placeholder="Interface Name"]'))).send_keys("Basic1")
    time.sleep(1)
    header = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'accordion-button')))

    assert "Basic1" in header.text, 'Basic Interface Name is not "Basic1"'

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    basicInterfaceArray = data['model']['interfaces']['basicInters']

    assert basicInterfaceArray[0]['name'] == "Basic1", "Basic Interface name is not 'Basic1' in JSON file"

def test_createBasicInstance(driver):
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-rr-ui-event-key="interfaces"]'))).click()

    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'interAdd'))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[title="Add Composite Interface"]'))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="accorCompHeaderButton"]'))).click() 

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[placeholder="Interface Name"]'))).send_keys("Comp1")
    time.sleep(1)

    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'interAdd'))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[title="Add Basic Interface"]'))).click()
    
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="accorBasicHeaderButton"]'))).click() 
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[placeholder="Interface Name"]'))).send_keys("Basic1")
    time.sleep(1)
    
    wait.until(EC.visibility_of_element_located((By.ID, "addBasicToComposite"))).click()

    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[starts-with(@id, 'comp-interface-basic-id')]"))).click()
    wait.until(EC.visibility_of_element_located((By.ID, "react-select-2-option-1"))).click()
    selectedOption = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[text()='Basic1']")))

    assert selectedOption is not None, "Basic1 was not assigned as Basic Instance"

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    basicInstancesArrayofComp1 = data['model']['interfaces']['compInters'][0]['basicInterfaces']

    assert basicInstancesArrayofComp1[0]['idOfBasic'] is not None, "Basic Instance not assigned in JSON file"

def test_nameBasicInstance(driver):
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-rr-ui-event-key="interfaces"]'))).click()

    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'interAdd'))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[title="Add Composite Interface"]'))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="accorCompHeaderButton"]'))).click() 

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[placeholder="Interface Name"]'))).send_keys("Comp1")
    time.sleep(1)

    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'interAdd'))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[title="Add Basic Interface"]'))).click()
    
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="accorBasicHeaderButton"]'))).click() 
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[placeholder="Interface Name"]'))).send_keys("Basic1")
    time.sleep(1)
    
    wait.until(EC.visibility_of_element_located((By.ID, "addBasicToComposite"))).click()

    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[starts-with(@id, 'comp-interface-basic-id')]"))).click()
    wait.until(EC.visibility_of_element_located((By.ID, "react-select-2-option-1"))).click()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[placeholder="Instance Name"]'))).send_keys("BasicInt1")
    time.sleep(2)

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    basicInstancesArrayofComp1 = data['model']['interfaces']['compInters'][0]['basicInterfaces']

    assert basicInstancesArrayofComp1[0]['name'] == 'BasicInt1', "Basic Instance name is not 'BasicInt1' in JSON file"

def test_deleteBasicInstance(driver):
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-rr-ui-event-key="interfaces"]'))).click()

    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'interAdd'))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[title="Add Composite Interface"]'))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="accorCompHeaderButton"]'))).click() 

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[placeholder="Interface Name"]'))).send_keys("Comp1")
    time.sleep(1)

    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'interAdd'))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[title="Add Basic Interface"]'))).click()
    
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="accorBasicHeaderButton"]'))).click() 
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[placeholder="Interface Name"]'))).send_keys("Basic1")
    time.sleep(1)
    
    wait.until(EC.visibility_of_element_located((By.ID, "addBasicToComposite"))).click()

    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[starts-with(@id, 'comp-interface-basic-id')]"))).click()
    wait.until(EC.visibility_of_element_located((By.ID, "react-select-2-option-1"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//div[text()='Basic1']")))

    wait.until(EC.visibility_of_element_located((By.ID, "deleteBasicInstance"))).click()
    time.sleep(1)

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    basicInstancesArrayofComp1 = data['model']['interfaces']['compInters'][0]['basicInterfaces']

    assert len(basicInstancesArrayofComp1) == 0, "Basic Instance not deleted in JSON file"

def test_deleteCompositeInterface(driver):
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-rr-ui-event-key="interfaces"]'))).click()

    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'interAdd'))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[title="Add Composite Interface"]'))).click()

    wait.until(EC.visibility_of_element_located((By.ID, "deleteCompInter"))).click()
    time.sleep(1)
    
    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    compInterfaceArray = data['model']['interfaces']['compInters']

    assert len(compInterfaceArray) == 0, "Comp Interface was not deleted in JSON file"

def test_deleteBasicInterface(driver):
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-rr-ui-event-key="interfaces"]'))).click()
    
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'interAdd'))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[title="Add Basic Interface"]'))).click()

    wait.until(EC.visibility_of_element_located((By.ID, "deleteBasicInter"))).click()
    time.sleep(1)

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    basicInterfaceArray = data['model']['interfaces']['basicInters']

    assert len(basicInterfaceArray) == 0, "Basic Interface was not deleted in JSON file"

def test_addMessage(driver):
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-rr-ui-event-key="interfaces"]'))).click()
    
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'interAdd'))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[title="Add Basic Interface"]'))).click()
    
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="accorBasicHeaderButton"]'))).click() 
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[placeholder="Interface Name"]'))).send_keys("Basic1")
    time.sleep(1)

    wait.until(EC.visibility_of_element_located((By.ID, "addMessageToInterface"))).click()

    accordHeader = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="accorHeaderMessage"]')))

    assert accordHeader is not None, "Message was not created"

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    messagesArray = data['model']['interfaces']['messages']

    assert messagesArray[0]['id'] is not None, "Message does not exist in JSON file"

def test_nameMessage(driver):
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-rr-ui-event-key="interfaces"]'))).click()
    
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'interAdd'))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[title="Add Basic Interface"]'))).click()
    
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="accorBasicHeaderButton"]'))).click() 
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[placeholder="Interface Name"]'))).send_keys("Basic1")
    time.sleep(1)

    wait.until(EC.visibility_of_element_located((By.ID, "addMessageToInterface"))).click()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="accorHeaderMessage"]'))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[placeholder="Message Name"]'))).send_keys("message1")
    time.sleep(1)
    accorTitle = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="accorHeaderMessage"]')))

    assert "message1" in accorTitle.text, "Message Header does not say 'message1'"

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    messagesArray = data['model']['interfaces']['messages']

    assert messagesArray[0]['name'] == "message1", "Message is not named 'message1' in JSON file"

def test_deleteMessage(driver):
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-rr-ui-event-key="interfaces"]'))).click()
    
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'interAdd'))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[title="Add Basic Interface"]'))).click()
    
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="accorBasicHeaderButton"]'))).click() 
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[placeholder="Interface Name"]'))).send_keys("Basic1")
    time.sleep(1)

    wait.until(EC.visibility_of_element_located((By.ID, "addMessageToInterface"))).click()

    wait.until(EC.visibility_of_element_located((By.ID, "deleteMessage"))).click()
    time.sleep(1)

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    messagesArray = data['model']['interfaces']['messages']

    assert len(messagesArray) == 0, "Message was not deleted in JSON file"

def test_toggleMessageType(driver):
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-rr-ui-event-key="interfaces"]'))).click()
    
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'interAdd'))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[title="Add Basic Interface"]'))).click()
    
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="accorBasicHeaderButton"]'))).click() 
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[placeholder="Interface Name"]'))).send_keys("Basic1")
    time.sleep(1)

    wait.until(EC.visibility_of_element_located((By.ID, "addMessageToInterface"))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="accorHeaderMessage"]'))).click()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="message-out"]'))).click()
    time.sleep(1)

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    messagesArray = data['model']['interfaces']['messages']

    assert messagesArray[0]['type'] == 'out', "Message type was not changed to 'out' in JSON file"

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="message-in"]'))).click()
    time.sleep(1)

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    messagesArray = data['model']['interfaces']['messages']

    assert messagesArray[0]['type'] == 'in', "Message type was not changed to 'in' in JSON file"

def test_addParameterToMessage(driver):
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-rr-ui-event-key="interfaces"]'))).click()
    
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'interAdd'))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[title="Add Basic Interface"]'))).click()
    
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="accorBasicHeaderButton"]'))).click() 
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[placeholder="Interface Name"]'))).send_keys("Basic1")
    time.sleep(1)

    wait.until(EC.visibility_of_element_located((By.ID, "addMessageToInterface"))).click()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="accorHeaderMessage"]'))).click()

    wait.until(EC.visibility_of_element_located((By.ID, "addParameter"))).click()
    time.sleep(1)

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    parameterArray = data['model']['interfaces']['messages'][0]['parameters']

    assert parameterArray[0]['id'] is not None, "Message parameter does not exist in JSON file"

def test_nameMessageParameter(driver):
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-rr-ui-event-key="interfaces"]'))).click()
    
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'interAdd'))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[title="Add Basic Interface"]'))).click()
    
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="accorBasicHeaderButton"]'))).click() 
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[placeholder="Interface Name"]'))).send_keys("Basic1")
    time.sleep(1)

    wait.until(EC.visibility_of_element_located((By.ID, "addMessageToInterface"))).click()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="accorHeaderMessage"]'))).click()

    wait.until(EC.visibility_of_element_located((By.ID, "addParameter"))).click()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[placeholder="Parameter Name"]'))).send_keys("param1")
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[placeholder="Parameter Type"]'))).send_keys("type1")
    time.sleep(2)

    # Check JSON file
    fileName = os.path.join('models', 'TestModel') + '.json'
    with open(fileName, 'r') as file:
        data = json.load(file)

    parameterArray = data['model']['interfaces']['messages'][0]['parameters']

    assert parameterArray[0]['name'] == 'param1', "Message parameter name is not 'param1 in JSON file"
    assert parameterArray[0]['type'] == 'type1', "Message parameter type is not 'type1 in JSON file"