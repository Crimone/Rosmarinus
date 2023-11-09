from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

from tqdm import tqdm
import requests
import os
import argparse
import time

def main():

    options = Options()
    driver = webdriver.Edge()

    driver.get(f"https://www.tsdm39.com/forum.php?mod=forumdisplay&fid=4&page=1")

    url = ""
    time.sleep(2.5)


if __name__ == '__main__':
    main()


