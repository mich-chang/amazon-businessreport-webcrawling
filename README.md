# amazon-businessreport-webcrawling

This file is used for auto login to amazon, and download ten days (today-2days ~ today-12days) business reports and the lastest all listing report. 
After downloading business report, this program will also add data date and download date columns, rename the report and save the new business report in the folder which contains this program. 
Since we don't reset all listing report, so it will still be at download folder.

## Before you run this code, please do the following things first:
1. Please download chromedriver in your computer, you can access it from this website: https://sites.google.com/a/chromium.org/chromedriver/downloads, and put the file into the same folder as this program.
2. Please change following parameters in this code:
   - **USEREMAIL** and **PASSWORD**: Please change them to your own account email and password.
   - **FILE_PATH**: It's your download folder's path, e.g. file:///Users/michelle/Downloads/
3. Please make sure that you haven't download any business report today. If you have downloaded already and they're in your download file, please delete them all.
4. Please install selenium and pandas in your running environment.

## After you run this code, you will get:
1. Ten days new business report in the folder which contains this program.
2. Lastest all listing report in the download folder.
3. Log file and is named as today's date in the folder which contains this program. If there's error while running the code, or can't download/reset the reports successfully, please check the log file
