import pexpect
import sys
import getpass
import time
import subprocess
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
# available since 2.26.0
from selenium.webdriver.support import expected_conditions as EC
import os
import os.path
from multiprocessing import Pool
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from datetime import datetime, timedelta
import logging
import logging.handlers
import logging.config
import socket


# Firefox driver connection
binary = FirefoxBinary('/usr/bin/firefox')
options = webdriver.FirefoxOptions()
options.set_headless()
#options = Options()
#options.headless = True
# driver = webdriver.Firefox()  # specfiy web driver

today = datetime.today()
# GET LAST 1 WEEK DATE
d = today - timedelta(days=7)
date = "{:%d_%m_%Y}".format(d.date())

today = "{:%d_%m_%Y}".format(today.date())
# CREATE NEW LOG FILE
new_logfile = "logs/log_"+today+".log"
open(new_logfile, 'a').close()

# DELETE OLD LOG FILES
old_logfile = "logs/log_"+date+".log"
if os.path.exists("logs/"+old_logfile):
    os.remove(old_logfile)
else:
    pass
# READ DATA FROM FILE
selected_cmd_file = open('ip_list2.txt', 'r')
selected_cmd_file.seek(0)

# LOGGING CONFIGURATON
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%d, %b %Y %I:%M:%S %p',
                    filename=new_logfile, filemode='w', level=logging.INFO)

# FUNCTION TO REBOOT THE DEVICES ACCORDING TO DIFFERENT WEB INTERFACE STRUCTURE.


def Model(driver, menu, tool, reboot):
    driver.switch_to.frame("bottomLeftFrame")
    systemtools = driver.find_element_by_id(menu)  # FIND REBOOT MENU
    systemtools.click()
    time.sleep(1)
    restart = driver.find_element_by_id(tool)  # CHOOSE REBOOT FIELD
    restart.click()
    time.sleep(1)
    driver.switch_to.default_content()
    driver.switch_to.frame("mainFrame")
    time.sleep(2)
    reboot = driver.find_element_by_id(reboot)  # CLICK TO REBOOT BUTTON
    time.sleep(1)
    reboot.click()


def webReboot(AP_name, ip_address):
    try:
        driver = webdriver.Firefox(
            firefox_options=options)  # specfiy web driver
        # Connection to the host
        # # open the device web interface
        driver.get('http://'+ip_address)
        # print (driver.current_url)
        wait = WebDriverWait(driver, 30)
        logging.info(AP_name+": Protocol - HTTP")
        # Analyzing device model
        model = driver.find_element_by_class_name(
            'style1').text  # get model of device
        # Authorization
        username = driver.find_element_by_id('userName')  # find username input
        username.send_keys("admin")  # enter the username
        password = driver.find_element_by_id(
            'pcPassword')  # find password input
        password.send_keys("radmin")  # enter the password
        login = driver.find_element_by_id('loginBtn')  # click login button
        login.click()
        time.sleep(3)
        logging.info(AP_name+": Authorized")
        # Check model of device and run the function
        if "WR840N" in model:
            logging.info(AP_name+": Model 840N")
            Model(driver, "menu_tools", "menu_restart", "button_reboot")
        else:
            logging.info(AP_name+": Model 841N")
            Model(driver, "a48", "a54", "reboot")
        time.sleep(1)
        alert = driver.switch_to_alert()
        alert.accept()
        logging.info(AP_name+": rebooted\n")
        print(AP_name+": rebooted by HTTP")
        time.sleep(1)
        driver.close()
    except Exception as e:
        print(AP_name+": not rebooted by HTTP")
        logging.info(AP_name+": not rebooted by HTTP")


def isOpen(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except:
        return False


def connection(hostname):
    try:
        # GET HOSTNAME AND IP ADDRESS OF DEVICE
        AP_name, ip_address = hostname.split("\t")
        logging.info("Connecting to: " + AP_name)
        # SEND 3 ICMP REQUEST TO DEVICE
        cmnd = "ping -c 3 -W 3 "+ip_address
        ping = subprocess.check_output(
            cmnd, stderr=subprocess.STDOUT, shell=True,
            universal_newlines=True)
        #response = os.system("ping -c 3 -W 3 "+ip_address)
    except subprocess.CalledProcessError as exc:
        logging.info(AP_name+": Status is down\n")
    else:
        logging.info(AP_name+": Status is up")
        telnet_status = isOpen(ip_address, 23)
        if telnet_status:
            logging.info("Protocol: Telnet")
            try:
                cmnd = 'bash telnet.sh '+ip_address + ' ' + AP_name
                telnet = subprocess.check_output(
                    cmnd, stderr=subprocess.STDOUT, shell=True,
                    universal_newlines=True)
            except subprocess.CalledProcessError as exc:
                if exc.returncode == 1 or exc.returncode == 127:
                    logging.info(AP_name+": rebooted by Telnet\n")
                    print(AP_name+": rebooted by Telnet")
                else:
                    logging.info(AP_name+": NOT rebooted by Telnet\n")
                    print(AP_name+": NOT rebooted by Telnet")
        else:
            webReboot(AP_name, ip_address)


def main():
    p = Pool(5)
    p.map(connection, selected_cmd_file.readlines())


if __name__ == '__main__':
    main()
