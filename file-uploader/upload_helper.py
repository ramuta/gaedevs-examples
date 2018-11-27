import os
import cloudstorage
import time
from models.uploaded_file import UploadedFile


GCS_BUCKET = '/your-bucket-name'  # enter the name of your bucket


def upload_file_helper(uploaded_file):
    file_content = uploaded_file.file.read()  # read the file

    # edit the file name
    file_name = str(uploaded_file.filename).replace(" ", "-").replace(".", "-")  # remove spaces
    file_name += str(int(time.time()))  # add a timestamp at the end of the file

    # file type
    file_type = uploaded_file.type
    file_name += "." + file_type.split("/")[1]  # if type is image/png, add .png at the end

    # upload the file to Google Cloud Storage
    gcs_file = cloudstorage.open(
        GCS_BUCKET + '/' + file_name,
        'w',
        content_type=file_type,
        retry_params=cloudstorage.RetryParams(backoff_factor=1.1)
    )

    gcs_file.write(file_content)
    gcs_file.close()

    # get the URL
    url = 'http://localhost:8080/_ah/gcs' if is_local() else 'https://storage.googleapis.com'
    url += GCS_BUCKET + '/' + file_name

    # store the URL in the Datastore
    saved_file = UploadedFile(url=url)
    saved_file.put()

    return url


def is_local():
    """ Check if you are currently running on localhost or on GAE. """
    if os.environ.get('SERVER_NAME', '').startswith('localhost'):
        return True
    elif 'development' in os.environ.get('SERVER_SOFTWARE', '').lower():
        return True
    else:
        return False
