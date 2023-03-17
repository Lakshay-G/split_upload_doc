from tkinter.filedialog import askopenfilename
import os
from easygui import *
from upload_crowdmark import *

if __name__ == '__main__':

    # asking for all the necessary info

    # file path needed for the assignment document
    file_path_extension = askopenfilename(
        title='Select your assignment document: ')
    # separating file_path and file_extension separately
    file_path, file_extension = os.path.splitext(file_path_extension)

    '''
    In this program I'm giving users 3 ways of inputting data:
        1. Using an inputs.json file
        2. Using a GUI app
        3. Using the command line
    The parameter input_method is 1 for the first case, 2 for the second case
    and 3 for the third case. The programmer would have to make the changes in here.
    '''

    input_method = 1

    if input_method == 1:
        inputs = config_inputs()
    elif input_method == 2:
        inputs = gui_app()
    else:
        inputs = terminal_inputs()

    '''
    The index 0, 1, 2, 3,.... indicate the question numbers
    The start question array gives the start of a question, based on the index (question number) value
    The end question array gives the end of a question, based on the index (question number) value
    '''

    start_question = list(map(int, inputs[0].split()))
    end_question = list(map(int, inputs[1].split()))

    [upload_link, submit_char, delete_char] = [inputs[2], inputs[3], inputs[4]]

    print([start_question, end_question, upload_link, submit_char, delete_char])

    # step 1: convert the pdf to individual question pdfs
    output_file_names = split_pdf_to_questions(
        file_path, file_extension, start_question, end_question)

    # step 2: initialize the driver by login()
    # login credentials are saved in login_credentials.json for privacy reasons
    [username, password] = login_credentials()

    driver = login(username=username, password=password)

    # step3: upload the individual question pdfs to crowdmark
    upload_to_crowdmark(driver=driver, upload_link=upload_link,
                        output_file_names=output_file_names, submit=submit_char)

    # step4: delete the individual question pdfs if user demands
    delete_question_docs(output_file_names, delete_char)
