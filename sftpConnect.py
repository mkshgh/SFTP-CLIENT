import pysftp
import os

from sftpLogger import logme
def compare_files_with_remote_server(upload_files:str,sftp_config:dict):
        """Compare if the files are already uploaded to the server or not"""
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None 
        with pysftp.Connection(sftp_config["IP"], username=sftp_config["USER"], password=sftp_config["PASS"], cnopts=cnopts) as sftp:
            for remote_files in sftp.listdir_attr():
                if (remote_files.filename in upload_files):
                    upload_files.remove(remote_files.filename)
            return upload_files

def upload_files_to_remote_server(upload_files:str,source:str,sftp_config:dict):
        """Upload the files to the server in the root location"""
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None 
        with pysftp.Connection(sftp_config["IP"], username=sftp_config["USER"], password=sftp_config["PASS"], cnopts=cnopts) as sftp:
            for files in upload_files:
                sftp.put(os.path.join(source,files),preserve_mtime=True)
                logme(f"{os.path.join(source,files)} Uploaded Successfully")
            return upload_files
