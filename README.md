# Rebooting-TP-link-Router-with-Phyton-
Rebooting Tplink Router ( 840N &amp; 841N ) via telnet &amp; web browser using phyton 

Some of the Tp-link devices does not work efficiently and start to freeze after some interval. This script helps to reboot these models automatically. These models may have the newest software version or previous one.  In previous software versions, telnet service is not supported on these devices. Even when you try to upgrade the software, sometimes it resets the devices and remote connection lost. If these devices are used in production, then this solution is risky. That is why, I reboot the devices according to their model and  software version. If devices support telnet connection, they are rebooted via telnet. if not, these devices are rebooted via web interface using Selenium.

Fistyly you need to install and add these libraries.

import pexpect // FOR TELNET CONNECTION
import sys
import getpass
import time
from selenium import webdriver    
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # availablesince 2.26.0
import os,os.path 
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary // I used Firefox webdriver/ You can use another webdriver also.
from datetime import datetime,timedelta
import logging,logging.handlers,logging.config // For logging purpose


1. To use the webdriver , firstly you need to download the geckodriver of the spesific web browser and add it to the system PATH.

2. This code is used daily basis on production, that is why the logging details are structed for it

3. Log files are created automatically for per day and system stores the files of last one week. Others are deleted automatically.

4. You need to specify the ip address of devices on file which the script will have access and read data from there. 

CODE DESCRIPTION

  IT READS DATA FROM ip_list.txt FILE AND SEND 3 ICMP REQUEST TO EACH IP TO CHECK THE AVAILABILITY OF DEVICE.
  IF STATUS IS UP , THEN CONNECT VIA TELNET USING "PEXPECT"
  IF TELNET CONNECTION IS SUCCESSFULL, SEND THE CONFIGRUATION COMMANDS TO THE DEVICES AND WRITE THE PROCESSES TO LOG FILES. 
  DEVICE IS REBOOTED!!
  IF TELNET CONNECTION IS NOT SUCCESSFULL, TRY TO CONNECT VIA WEB INTERFACE USING SELENIUM
  1. WEB DRIVER OPENED.
  2. URL IS ENTERED. 
  3. ENTER THE CREDENTIALS TO LOGIN THE SYSTEM.
  4. CHECK THE MODEL VERSION AND GET  IDs OF SPECIFIC HTML TAGS TO CLICK.
  5. WRITE PROCESSES TO LOG FILE.
  DEVICE IS REBOOTED!!
  
