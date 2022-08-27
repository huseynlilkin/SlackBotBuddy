import glob
import os
import pprint

import boto3
import zipfile

ZIP_OUTPUT_PATH = "dist/build.zip"
FUNCTION_NAME = "slackBotProcessor"
LIST_OF_FILES_TO_WRITE = ['AI.py', 'lambda_function.py']


def zip_files():
    """
    Creates a zip archive from given files/folders. Add your files, folders to the
    LIST_OF_FILES_TO_WRITE variable above
    """
    os.makedirs(os.path.dirname(ZIP_OUTPUT_PATH), exist_ok=True)
    with zipfile.ZipFile(ZIP_OUTPUT_PATH, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for path in LIST_OF_FILES_TO_WRITE:
            for file in glob.glob(path):
                z.write(file)


def update_lambda():
    client = boto3.client('lambda', region_name='us-east-1')
    response = client.update_function_code(
        FunctionName=FUNCTION_NAME,
        ZipFile=open(ZIP_OUTPUT_PATH, 'rb').read(),
        Publish=False
    )
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(response)


if __name__ == '__main__':
    zip_files()
    update_lambda()
