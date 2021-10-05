"""
Author: Lucas Roberts
Date: 9/30/21
Description: I will be scrapping indeed for job listings, grabbing certain items
"""
import pandas
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time


def main():
    # Setting up Chromedriver
    PATH = "chromedriver.exe"
    driver = webdriver.Chrome(PATH)

    # Grabbing Job Title
    user_input = input("Enter the job title: ").lower()
    user_input.replace(" ", "%20")
    URL = f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={user_input}"
    driver.get(URL)

    # Close closes a single table quit() will completely close all
    jobs = int(input("Enter how many jobs would you like to find: "))
    counter = 1
    running = True
    company_name = []
    job_title = []
    location = []
    pay = []
    job_age = []

    # Check how many jobs are on the page after user inputted job title
    time.sleep(5)
    actual_jobs = driver.find_element_by_xpath("//div[@data-test='MainColSummary']/p[@data-test='jobsCount']").get_attribute("textContent")
    actual_jobs = int(actual_jobs.strip(" jobs"))

    # If there are no jobs, exits the program
    if actual_jobs == 0:
        print("You entered an incorrect job title or one with 0 job postings.\n Try searching another job title.")
        driver.close()
        return -1
    # If the jobs requested are more than the amount listed, lowers the amount requested to amount listed.
    elif jobs > actual_jobs:
        print("The amount of jobs you want are less than how many there are.\n Setting requested jobs to the amount"
              "listed on the site.")
        jobs = actual_jobs

    # Get rid of the pop-up
    temp_elem = driver.find_element_by_class_name("react-job-listing")
    temp_elem.click()
    close_popup = driver.find_element_by_class_name("modal_closeIcon-svg")
    close_popup.click()

    while running:
        for job_number in range(1, jobs+1, 1):
            print(job_number)

            # Grabs the company name
            try:
                company_name.append(driver.find_element_by_xpath(f"//li[{counter}]/div[2]/div[1]/a[1]/span").text)
            except selenium.common.exceptions.NoSuchElementException:
                company_name.append(-1)

            # Grabs the title of the job
            try:
                job_title.append(driver.find_element_by_xpath(f"//li[{counter}]/div[2]/a[1]/span").text)
            except selenium.common.exceptions.NoSuchElementException:
                job_title.append(-1)

            # Grabs the location of the job
            try:
                location.append(driver.find_element_by_xpath(f"//li[{counter}]/div[2]/div[2]/span").text)
            except selenium.common.exceptions.NoSuchElementException:
                location.append(-1)

            # Grabs how much the salary is
            try:
                pay.append(driver.find_element_by_xpath(f"//li[{counter}]/div[2]/div[3]/div[1]/span").text)
            except selenium.common.exceptions.NoSuchElementException:
                pay.append(-1)

            # Grabs how long the job has been up
            try:
                job_age.append(driver.find_element_by_xpath(f"//li[{counter}]/div[2]/div[3]/div[2]/div[2]").text)
            except selenium.common.exceptions.NoSuchElementException:
                job_age.append(-1)

            # Added a sleep due to pages not loading correctly
            # most likely will move this to after the next page button click and make it longer

            if counter == jobs:
                running = False
            elif counter == 30:
                # Clicks the next page button
                driver.find_element_by_xpath("//a[@data-test='pagination-next']").click()
                counter = 0
                jobs -= 30
                time.sleep(5)
            counter += 1
    print(company_name)
    print(job_title)
    print(location)
    print(pay)
    print(job_age)
    driver.close()


if __name__ == "__main__":
    main()
