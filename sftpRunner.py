import os
import time
from sftpConnect import compare_files_with_remote_server, delete_files_on_remote_server, get_age_in_seconds, upload_files_to_remote_server
from sftpLogger import logme
import json

if os.path.isfile('sftp.json'):
    with open('sftp.json', "r") as f:
        sftp_config = json.loads(f.read())
else:
    logme("sftp.json Connection file not found in the root directory, please upload it there.")


def get_local_files_newer_than(source:str,extension:str,file_age:str):
    # all the list of files in the folder
    files=[]
    # Get the files with given extenstion and the date_created and size
    with os.scandir(source) as it:
        for entry in it:
            expected_files_age=get_age_in_seconds(file_age)
            file_epoch_time = os.stat(os.path.join(source,entry.name)).st_mtime
            current_epoch_time = int(time.time())
            time_diff = current_epoch_time - file_epoch_time
            # print(entry.name.endswith(extension),entry.is_file(),expected_files_age,time_diff)
            if entry.name.endswith(extension) and entry.is_file() and expected_files_age>time_diff:
                # Dont Delete for now
                # human_rea_epoch_time = time.ctime(expected_files_age)
                # print(entry.name)
                print("expected_files_age:",expected_files_age)
                # print("file_epoch_time:",file_epoch_time)
                # print("current_epoch_time:",current_epoch_time)
                # print("time_diff:",time_diff)
                files.append(entry.name)
            else:
                os.remove(os.path.join(source,entry.name))
                logme(f"Local: Deleted File {os.path.join(source,entry.name)}")
    return files

def runner(source,extension,file_age):
    if os.path.isdir(source):
        local_files=get_local_files_newer_than(source,extension,file_age)
        if local_files:
            try:
                new_upload_files=compare_files_with_remote_server(local_files,sftp_config)
                if new_upload_files:
                    delete_files_on_remote_server(sftp_config)
                    upload_files_to_remote_server(new_upload_files,source,sftp_config)

                else: logme(f"No new files older than {file_age} in the folder {source} to upload")
            except Exception as E:
                logme(str(E),"error")        
        else:
            logme(f"No new files older than {file_age} in the folder {source} to upload")
    else:
        logme(f"The Source Directory {source} is invalid or does not exist, POSSIBLE RESOLUTION: change your SOURCE path in the config","error")


source = sftp_config["SOURCE"]
extension = sftp_config["EXTENSION"]
file_age = sftp_config["FILE_AGE"]
runner(source,extension,file_age)
