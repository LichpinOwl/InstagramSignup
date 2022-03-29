import pathlib
from re import search
import random
import string
import os
import time
from tkinter import Tk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


def passwordGenerator():
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    random.shuffle(characters)
    password = []
    for i in range(15):
        password.append(random.choice(characters))
    random.shuffle(password)
    return "".join(password)


def randomNameGenerator(nameList):
    lines = open(nameList).read().splitlines()
    return [random.choice(lines), random.choice(lines), random.choice(lines) + '_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))]


for i in range(100):
    os.system('cls')

    chromrDriverPath = str(pathlib.Path(
        __file__).parent.resolve()) + '\\chromedriver.exe'
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(chromrDriverPath, options=options)

    password = passwordGenerator()

    # Mail Agent
    driver.get('https://app.getmailet.com/guest')
    mailElement = driver.find_element_by_id('temp_mail')
    mailElement.send_keys(Keys.CONTROL, 'a')
    mailElement.send_keys(Keys.CONTROL, 'c')
    mailAddress = Tk().clipboard_get()
    with open('mailList.txt', 'a') as ml:
        ml.write(mailAddress + ' ' + ':' + ' ' + password + '\n')
    # Mail Agent
    # open instagram tab and insert fields
    driver.execute_script("window.open('about:blank', 'tab2');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get('https://www.instagram.com/accounts/emailsignup/')
    time.sleep(5)
    try:
        driver.find_element_by_xpath(
            '/html/body/div[4]/div/div/button[2]').click()
        time.sleep(5)
    except NoSuchElementException:
        pass

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@name='emailOrPhone']"))).send_keys(mailAddress)
    time.sleep(1)
    driver.find_element_by_xpath("//input[@name='fullName']").send_keys(
        randomNameGenerator('nameList.txt')[0] + ' ' + randomNameGenerator('nameList.txt')[1])
    time.sleep(1)
    driver.find_element_by_xpath(
        "//input[@name='username']").send_keys(randomNameGenerator('nameList.txt')[2])
    time.sleep(1)
    driver.find_element_by_xpath(
        "//input[@name='password']").send_keys(password)
    time.sleep(1)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="react-root"]/section/main/div/div/div[1]/div/form/div[7]/div/button'))).click()
    time.sleep(1)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, "//*[@id='react-root']/section/main/div/div/div[1]/div/div[4]/div/div/span/span[1]/select/option[9]"))).click()
    time.sleep(1)
    driver.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/div/div/div[1]/div/div[4]/div/div/span/span[2]/select/option[11]').click()
    time.sleep(1)
    driver.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/div/div/div[1]/div/div[4]/div/div/span/span[3]/select/option[22]').click()
    time.sleep(1)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="react-root"]/section/main/div/div/div[1]/div/div[6]/button'))).click()
    time.sleep(1)
    # get back to mail tab for comfirmation code
    driver.switch_to.window(driver.window_handles[0])
    # waiting for code
    elementExists = True
    while elementExists:
        try:
            driver.find_element_by_xpath(
                '/html/body/div[1]/div/div/div/div/div/div[2]/table/tbody/tr/td[1]/a')
            elementExists = False
        except NoSuchElementException:
            time.sleep(10)
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="sidebar"]/ul/li/span/a'))).click()

    # code received
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div[1]/div/div/div/div/div/div[2]/table/tbody/tr/td[1]/a"))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="email_content"]/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td[2]'))).click()
    mailConfirmationCode = driver.find_element_by_xpath(
        '//*[@id="email_content"]/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td[2]').text
    print(mailConfirmationCode)
    # go to instagram email confirmation page
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/div/div/div[1]/div[2]/form/div/div[1]/input').send_keys(mailConfirmationCode)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="react-root"]/section/main/div/div/div[1]/div[2]/form/div/div[2]/button'))).click()
    time.sleep(90)
    driver.quit()
