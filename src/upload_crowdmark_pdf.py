from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from PyPDF2 import PdfWriter, PdfReader, PdfReader, PdfWriter
from selenium.webdriver.common.by import By
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
import json


def split_pdf_to_questions(file_path, file_extension):
    '''
    The index 0, 1, 2, 3,.... indicate the question numbers
    The start question array gives the start of a question, based on the index (question number) value
    The end question array gives the end of a question, based on the index (question number) value
    '''
    start_question = list(
        map(int, input("Enter start value of questions\n:: ").split()))
    end_question = list(
        map(int, input("Enter end value of questions\n:: ").split()))

    input_file_name = file_path+file_extension
    output_file_name = file_path
    output = []

    # Open the input PDF file
    with open(input_file_name, 'rb') as input_file:

        # Loop through the pages and add the selected pages to the output PDF
        for i in range(0, len(start_question)):

            # Create a PDF reader object
            pdf_reader = PdfReader(input_file)

            # Create a PDF writer object
            pdf_writer = PdfWriter()

            start = int(start_question[i]) - 1
            end = int(end_question[i])

            print('Q'+str(i+1)+' range:: '+str(start),
                  '-', str(end)+' page numbers')

            for page_num in range(start, end):
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)

            # Open the output PDF file and write the selected pages to it
            with open(output_file_name+'_q'+str(i+1)+file_extension, 'wb') as output_file:
                pdf_writer.write(output_file)
                # print(output_file_name+'_q'+str(i+1)+file_extension)
                output.append(output_file_name+'_q'+str(i+1)+file_extension)
    # we are returned with the array of the location of the individual question pdfs on the local computer
    return output


def login(username, password):
    # adding chrome options to enable javascript in the browser
    options = webdriver.ChromeOptions()
    options.add_argument("--enable-javascript")

    # initializing the chrome driver
    driver = webdriver.Chrome(
        "split_upload_doc/resources/chromedriver", options=options)

    # going to the crowdmark UW login page
    driver.get(
        "https://app.crowdmark.com/sign-in?force_form=true&institution=waterloo")

    # find username/email field and send the username itself to the input field
    driver.find_element("id", "user_email").send_keys(username)

    # find password input field and insert password as well
    driver.find_element("id", "user_password").send_keys(password)

    # click login button
    driver.find_element("name", "commit").click()
    return driver


def upload_to_crowdmark(driver, upload_link, output_file_names, submit):
    # driver goes to the page of the particular assignment. you have to enter it in the system
    driver.get(upload_link)
    # necessary steps: 1. Maximize the window of the website to allow all tags to be visible 2. Driver should wait a bit until it gets an input tag, or until 10 seconds.
    driver.maximize_window()
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "input"))
    )
    # collecting all the input tags from the website as an object.
    inputs = driver.find_elements(By.TAG_NAME, "input")
    # print(inputs)

    # send all the questions from the location to the input fields
    for i in range(0, len(output_file_names)):
        # print(output_file_names[i])
        inputs[i].send_keys(output_file_names[i])

    # wait until you find the button on the page which is the submit button, but this is only activated once you have successfully uploaded the docs
    element = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(., 'page')]")))
    buttons = driver.find_element(
        By.XPATH, "//button[contains(., 'page')]")

    # wait until the button is enabled
    while not buttons.is_enabled():
        WebDriverWait(driver, 1)

    # we only want to press the submit button if the user says yes to it
    if submit == 'y' or submit == 'Y':
        driver.find_element(By.XPATH, "//button[contains(., 'page')]").click()
        element = WebDriverWait(driver, 4)


def delete_question_docs(question_paths, delete_char):
    if delete_char == 'y' or delete_char == 'Y':
        for question_path in question_paths:
            os.remove(question_path)


if __name__ != '__main__':
    # asking for all the necessary info

    # file path needed for the assignment document
    file_path_extension = askopenfilename(
        title='Select your assignment document: ')
    # separating file_path and file_extension separately
    file_path, file_extension = os.path.splitext(file_path_extension)

    # enter the link of the assignment which needs to be uploaded
    upload_link = input(
        "Enter link of the assignment which needs to be uploaded\n:: ")
    # ask the user if they want to automate the submit button too
    submit_char = input(
        "Do you want to automate the crowdmark submit button too? (y/n)\n:: ")
    # ask the user if they want to delete the separate question docs after the process
    delete_char = input(
        "Do you want to delete the separate question docs after the process? (y/n)\n:: ")

    # step 1: convert the pdf to individual question pdfs
    # output_file_names = split_pdf_to_questions(
    #     '/Users/lakshaygoel/Documents/Fall2022/mini_projects/upload-crowdmark-pdf-split/document')

    output_file_names = split_pdf_to_questions(file_path, file_extension)

    # step 2: initialize the driver by login()
    driver = login(username='enter your username',
                   password='enter your password')

    # step3: upload the individual question pdfs to crowdmark
    upload_to_crowdmark(driver=driver, upload_link=upload_link,
                        output_file_names=output_file_names, submit=submit_char)

    # step4: delete the individual question pdfs if user demands
    delete_question_docs(output_file_names, delete_char)

if __name__ == '__main__':
    with open("resources/inputs.json") as input_file:
        inputs = json.load(input_file)
    print(inputs['start_questions'])
