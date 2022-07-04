import os
import time
from sftpConnect import compare_files_with_remote_server, upload_files_to_remote_server
from sftpLogger import logme
import json
if os.path.isfile('sftp.json'):
    with open('sftp.json', "r") as f:
        sftp_config = json.loads(f.read())
else:
    logme("sftp.json Connection file not found in the root directory, please upload it there.")

def get_age_in_seconds(file_age):
    if file_age[-1] in "0123456789": return int(file_age)
    time = {"m":60,"h":3600,"d":86400}
    return int(file_age[:-1])*time[file_age[-1]]

def get_local_files_older_than(source:str,extension:str,file_age:str):
    # all the list of files in the folder
    files=[]
    # Get the files with given extenstion and the date_created and size
    with os.scandir(source) as it:
        for entry in it:
            expected_files_age=get_age_in_seconds(file_age)
            file_epoch_time = os.path.getctime(os.path.join(source,entry.name))
            current_epoch_time = int(time.time())
            time_diff = current_epoch_time - file_epoch_time
            if entry.name.endswith(extension) and entry.is_file() and time_diff<expected_files_age:
                # Dont Delete for now
                # human_rea_epoch_time = time.ctime(expected_files_age)
                # print(entry.name)
                # print("expected_files_age:",expected_files_age)
                # print("file_epoch_time:",file_epoch_time)
                # print("current_epoch_time:",current_epoch_time)
                # print("time_diff:",time_diff)
                files.append(entry.name)
    return files

def runner(source,extension,file_age):
    if os.path.isdir(source):
        local_files=get_local_files_older_than(source,extension,file_age)
        if local_files:
            try:
                new_upload_files=compare_files_with_remote_server(local_files,sftp_config)
                if new_upload_files: upload_files_to_remote_server(new_upload_files,source,sftp_config)
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
