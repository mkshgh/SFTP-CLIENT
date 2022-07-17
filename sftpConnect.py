import pysftp
import os
import time
from sftpLogger import logme
import shutil

def get_age_in_seconds(file_age):
    if file_age[-1] in "0123456789": return int(file_age)
    time = {"m":60,"h":3600,"d":86400}
    return int(file_age[:-1])*time[file_age[-1]]

def compare_files_with_remote_server(upload_files:str,sftp_config:dict):
        """Compare if the files are already uploaded to the server or not"""
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None 
        with pysftp.Connection(sftp_config["IP"], username=sftp_config["USER"], port=sftp_config["PORT"],  password=sftp_config["PASS"], cnopts=cnopts) as sftp:
            for remote_files in sftp.listdir_attr():
                if (remote_files.filename in upload_files):
                    upload_files.remove(remote_files.filename)
            return upload_files

def upload_files_to_remote_server(upload_files:str,source:str,sftp_config:dict):
        """Upload the files to the server in the root location"""
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None 
        with pysftp.Connection(sftp_config["IP"], username=sftp_config["USER"], port=sftp_config["PORT"],  password=sftp_config["PASS"], cnopts=cnopts) as sftp:
            
            for files in upload_files:
                src_file=os.path.join(source,files)
                # Copy the files
                if not os.path.isdir(".TEMP"): os.mkdir(".TEMP")
                temp_file=os.path.join(".TEMP",files)
                shutil.copyfile(src_file, temp_file)
                sftp.put(os.path.join(source,files),preserve_mtime=True)
                logme(f"{os.path.join(source,files)} Uploaded Successfully")
                time.sleep(2.4)
                os.remove(temp_file)
            return upload_files

def delete_files_on_remote_server(sftp_config:dict):
        """Compare if the files are already uploaded to the server or not"""
        file_age=sftp_config["FILE_AGE"]
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None 
        deleted_files=[]
        with pysftp.Connection(sftp_config["IP"], username=sftp_config["USER"], port=sftp_config["PORT"],  password=sftp_config["PASS"], cnopts=cnopts) as sftp:
            for remote_files in sftp.listdir_attr():
                expected_files_age=get_age_in_seconds(file_age)
                file_epoch_time=remote_files.st_mtime
                current_epoch_time = int(time.time())
                time_diff = current_epoch_time - file_epoch_time
                if time_diff>expected_files_age:
                    sftp.remove(remote_files.filename)
                    deleted_files.append(remote_files.filename)
                    logme(f"Remote: {remote_files.filename} Deleted Successfully")
        return deleted_files