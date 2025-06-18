import os
import glob
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from env import BASE_URL

# Deletes all models in the tests/models folder
def deleteAllModels():
    current_dir = os.path.dirname(__file__)
    sibling_folder = os.path.join(current_dir, './models')

    files = glob.glob(os.path.join(sibling_folder, '*'))

    for file in files:
        try:
            os.remove(file)
        except OSError as e:
            print(f"Error deleting {file}: {e}")

# Creates new model called "TestModel"
def createNewModel(driver):
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "new-model-name"))).send_keys("TestModel")
    wait.until(EC.visibility_of_element_located((By.XPATH, "//button[text()='New Model...']"))).click()
    wait.until(EC.title_contains("TestModel"))

# Deletes the first model in the modal list
def deleteModel(driver):
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='All Models...']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//td[@class='modelDelete']"))).click()
    alert = Alert(driver)
    alert.accept()

# Returns an actively open model
def returnModel(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "modelSettings"))).click()
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "refreshBtn"))).click()
    alert = Alert(driver)
    alert.accept()
    wait.until(EC.title_is("UC-PACT"))

# Add the BasicModel.json file to the test/models folder so it is accessible to the tests
def createBasicModel():
    with open('BasicModel.json', 'r') as file:
        data = json.load(file)

    newFilename = os.path.join('models', 'BasicModel') + '.json'
    with open(newFilename, 'w') as newFile:
        json.dump(data, newFile, indent=2)

    time.sleep(3)

# Add the model for code generation
def createCodeGenerationModel():
    with open('CodeGeneration.json', 'r') as file:
        data = json.load(file)

    newFilename = os.path.join('models', 'CodeGeneration') + '.json'
    with open(newFilename, 'w') as newFile:
        json.dump(data, newFile, indent=2)

def waitForExists(fp, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if os.path.exists(fp):
            return True
        time.sleep(1)
    return False

# Opens the "BasicModel"
def loadBasicModel(driver):
    driver.get(BASE_URL + "/model/BasicModel")
    time.sleep(5)
    wait = WebDriverWait(driver, 10)
    # wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='All Models...']"))).click()
    # wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Edit"))).click()
    wait.until(EC.title_contains("BasicModel"))
