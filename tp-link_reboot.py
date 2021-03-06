import pexpect
import sys
import getpass
import time
from selenium import webdriver    
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import os,os.path 
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from datetime import datetime,timedelta
import logging,logging.handlers,logging.config





#Firefox driver connection
binary = FirefoxBinary('/usr/bin/firefox')



today = datetime.today()
// GET LAST 1 WEEK DATE
d = today - timedelta(days=7)
date="{:%d_%m_%Y}".format(d.date())

today="{:%d_%m_%Y}".format(today.date())
// CREATE NEW LOG FILE
new_logfile="logs/log_"+today+".log"
open(new_logfile,'a').close()

//DELETE OLD LOG FILES
old_logfile="logs/log_"+date+".log"
if os.path.exists("logs/"+old_logfile):
    os.remove(old_logfile)
else:
    pass
// READ DATA FROM FILE
selected_cmd_file=open('ip_list.txt', 'r')
selected_cmd_file.seek(0)

// LOGGING CONFIGURATON
logging.basicConfig(format='%(asctime)s %(message)s',datefmt='%d, %b %Y %I:%M:%S %p',filename=new_logfile,filemode='w', level=logging.INFO)

// FUNCTION TO REBOOT THE DEVICES ACCORDING TO DIFFERENT WEB INTERFACE STRUCTURE.
def Model(menu,tool,reboot):
    driver.switch_to.frame("bottomLeftFrame")
    systemtools = driver.find_element_by_id(menu) // FIND REBOOT MENU
    systemtools.click()
    time.sleep(1)
    restart=driver.find_element_by_id(tool) // CHOOSE REBOOT FIELD
    restart.click()
    time.sleep(1)
    driver.switch_to.default_content()
    driver.switch_to.frame("mainFrame") 
    time.sleep(2)
    reboot=driver.find_element_by_id(reboot) // CLICK TO REBOOT BUTTON
    time.sleep(1)
    reboot.click()


for hostname in selected_cmd_file.readlines():
    AP_name, ip_address=hostname.split("\t") // GET HOSTNAME AND IP ADDRESS OF DEVICE
    logging.info("Connecting to: "+ AP_name)
    response=os.system("ping -c 3 "+ip_address) // SEND 3 ICMP REQUEST TO DEVICE

    if response==0:
        logging.info("Status is up")

        #Telnet Connection
        try:
            child=pexpect.spawn('telnet '+ ip_address) // connect to device via telnet
            child.timeout=30
            
            #child.logfile=sys.stdout

            child.expect("username:") 
            time.sleep(2)
            child.sendline("admin") // enter username
            child.expect("password:")
            child.sendline("admin") // enter password
            time.sleep(2)
            child.sendline("\r\n")
            i=child.expect("#")
            logging.info("Protocol: Telnet")
            if i==0:
                logging.info("Authorized")
                child.sendline("dev reboot") // send reboot command
                child.sendline("\n\r")
            else:
                logging.info("Could not connect to the host")
            k=child.expect("host")
            if k==0:
                logging.info("Device is rebooted\n")
            else:
                logging.info ("Process failed")
                logging.warning(AP_name+" could not be rebooted\n")

        except pexpect.exceptions.EOF:
            try:
                driver = webdriver.Firefox() // specfiy web driver

                #Connection to the host
                driver.get('http://'+ip_address) // open the device web interface
                #print (driver.current_url)
                wait=WebDriverWait(driver,30)
                logging.info("Protocol: HTTP")

                #Analyzing device model
                model=driver.find_element_by_class_name('style1').text // get model of device
                print(model)

                #Authorization
                username = driver.find_element_by_id('userName') // find username input
                username.send_keys("admin") // enter the username
                password = driver.find_element_by_id('pcPassword') // find password input
                password.send_keys("admin") // enter the password
                login = driver.find_element_by_id('loginBtn') // click login button
                login.click()
                time.sleep(3)
                logging.info("Authorized")
                // Check model of device and run the function
                if "WR840N" in model: 
                    logging.info("Model is 840N")
                    Model("menu_tools", "menu_restart", "button_reboot")
                else:
                    logging.info("Model is 841N")
                    Model("a48", "a54", "reboot")


        

                time.sleep(1)
                alert = driver.switch_to_alert()
                alert.accept()
                logging.info ("Device is rebooted\n")
                time.sleep(1)
                driver.close()
               
            except Exception:

                logging.info ("Process failed")


                 
                logging.warning(AP_name+" could not rebooted \n ")
    else:
        logging.info("Status is down\n")
        
