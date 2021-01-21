from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json

driver = webdriver.Chrome()
driver.get("https://open.kattis.com/problems")

with open("problems.json", "r") as f:
	problems = json.load(f)

flag = False
while(not flag):
	try:
		problemList = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "problem_list_wrapper")))
	except:
		driver.quit()
		flag = True
	
	anchors = driver.find_elements_by_xpath("//*[@id=\"problem_list_wrapper\"]/table/tbody/tr/td[1]/a")
	
	for a in anchors:
		problem = {
			"name": a.text,
			"link": a.get_attribute("href")
		}
		problems[problem["name"]] = problem

	try:
		nextButton = driver.find_element_by_id("problem_list_next")
		nextButton.click()
	except ElementNotInteractableException:
		with open("problems.json", "w") as f:
			json.dump(problems, f, indent=4, sort_keys=True)
		driver.quit()
		flag = True
