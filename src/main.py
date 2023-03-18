from tkinter.filedialog import askopenfilename
import os
from easygui import *
from upload_crowdmark import *

if __name__ == "__main__":

    file_path_extension = askopenfilename(
        title='Select your assignment document: ')

    upload_obj = Upload(
        input_method=2, file_path_extension=file_path_extension)

    upload_obj.login()

    upload_obj.upload_to_crowdmark()

    delete_question_docs(upload_obj.output_file_names, upload_obj.delete_char)
