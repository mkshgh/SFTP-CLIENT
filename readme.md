# SFTP RUNNER
A really simple implementation of sftp client for windows.

## USAGE

- Create the config file named sftp.json
    ```
    sftp_config = {
        "USER":"yourUsername",
        "PASS":"yourpass",
        "IP":"IP of the server",
        "PORT":"Empty if standard port or 22",
        "SOURCE":"C:\\PATH\\TO\\FOLDER",
        "UPLOAD_INTERVAL":"200|1m|2h|1d",
        "FILE_AGE":"200|1m|2h|1d",
        "EXTENSION":"exe|bak|csv|xsls"
    }
    ```
- put it in the same folder as the sftpRunner.exe
- Sample json is given in the folder

## Config specifications

  - FILE_AGE: Time boundary for uploading the files. File which are older than this time will not be uploaded.
  - UPLOAD_INTERVAL: The interval in which the file should be uploaded. For now put it Empty as we will use Windows Scheduler.

## UPLOAD_INTERVAL and FILE_AGE


- The time should be integers.
  
    ```
    EG: "FILE_AGE":"200" is valid 
    EG: "FILE_AGE":"200.5" is not valid 
    ```
- If only digits are given, then the time is regarded as seconds
  
    ```
    EG: "FILE_AGE":"200" is 200 s
    ```
- Here m,h,d are minutes, hours and days (Case Sensitive)
  
    ```
    EG: "FILE_AGE":"200" is 200 seonds
    EG: "FILE_AGE":"2m" is 200 minutes
    EG: "FILE_AGE":"2h" is 200 hours
    EG: "FILE_AGE":"2d" is 200 days
    ```

## Things to consider

- If the file size if big, think about the time it might take to upload the file. 
  
  ```
  Eg: if the file size is 4GB and you try to upload it every 1 minutes over a slow connection. The file may not be uploaded as it tries to upload the same files every 1 minute.
  ```
- The file should not be used by other services while trying to upload this may cause read/write error. It is better to upload the files when the system is least used.

## Making your own exe build

Add only the following files in YourFilePath
- sftpRunner.py
- sftpConnect.py
- sftpLogger.py

```
pip install pyinstaller

cd YourFilePath

pyinstaller --onefile YourFileName

```

## TODO
- Make it into a background service
- Add scheduling functionality in the script
- Add functionality to delete the files in the remote server if older than some time.
- Compatibility with linux, IS MAC WORTH IT?
- Custom Port Doesn't Work for now.

## REFERENCES
- https://pysftp.readthedocs.io/en/release_0.2.9/
- https://docs.python.org/3/library/os.path.html#module-os.path
- https://docs.python.org/3/library/os.html
- One More Magic Remains