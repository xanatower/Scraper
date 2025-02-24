from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains
import time

from natrual_hazard import run_natural_hazard

from age_gender import run_age_gender

from income import run_income

from renter_onwer import run_owner_renter

import pandas as pd
from datetime import datetime

import random