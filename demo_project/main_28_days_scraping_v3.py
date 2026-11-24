#### scraper using playwright library
#---------------------------------------------------------------------------------------------------------------------------------
# Change: Added credentials encryption and decryption functionality using Security_Cipher_Service package.
# Date: 2026-10-28
#---------------------------------------------------------------------------------------------------------------------------------

import time
from common_28_days_scraping import Constants
from datetime import datetime, timedelta
import pandas as pd
import logging
# from pytz import timezone
import os
import json
import sys
import traceback
import glob
import requests
import pymssql
from playwright.sync_api import sync_playwright

SECURITY_MODULE_DIR = Constants.SECURITY_SERVICE_PATH

# Add the module directory to Python's import path
if SECURITY_MODULE_DIR not in sys.path:
    sys.path.insert(0, SECURITY_MODULE_DIR)
      
ENV_FILE = os.path.join(
    Constants.CRED_ENV_FILE_PATH,
    ".env" 
)

from Security_Cipher_Service.security_cipher import SecurityCipher 
from Security_Cipher_Service.exception_handling import  SecurityTokenException

from dotenv import load_dotenv
 
load_dotenv(ENV_FILE)
   
   
logging.basicConfig(level=logging.INFO, 
                    filename=datetime.now().strftime(os.path.join( Constants.EXECUTION_LOGS_FOLDER, Constants.EXECUTION_LOGS_FILENAME)), 
                    filemode='a', format='%(asctime)s - [%(threadName)s] [%(levelname)s] - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
    

    
class FHFTPortalScraping():
    def gettoken():
        """
        get token from thor token service
        """
        try:    
    
            apiresponse=requests.get(Constants.TOKEN_API_URL,
            headers={
                            
                    "ApplicationId":"11101",
                    "BuId":"27807",
                    "SubBuId":"1",
                    "Environment":"dev",
                    "Content-Type":"application/json",
                    "userlogin":"pramila@gmail.com",
                    "issuer":"fptool"
                    # //jtitoken:eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJleUpoYkdjaU9pSklVekkxTmlKOS5leUpwWVhRaU9qRTFOek0xTlRZNU1EQXNJbk4xWWlJNkluQnlZVzFwYkdGQVoyMWhhV3d1WTI5dElpd2lhWE56SWpvaVptbHVlQ0lzSW1Gd2NFbGtJam9pTVRFeE1ESWlMQ0ppZFVsa0lqb2lNamM0TURjaUxDSmxlSEFpT2pFMU56TTFOVGczTURCOS5IcUwzZzFLS1ZnZ1NkZVBkUVhudHc2Sl9ldlZtQldvU08tSE9iZm00VEpZIiwiaWF0IjoxNTczNTU2OTAwLCJzdWIiOiJwcmFtaWxhQGdtYWlsLmNvbSIsImlzcyI6ImZpbngiLCJhcHBJZCI6IjExMTAyIiwiYnVJZCI6IjI3ODA3IiwiZXhwIjoxNTczNTU4NzAwfQ.DGxixtO9_kuUHR1y3IJhQGzpzz-JDd9FBoZejp_agbA
                    # //Tokentype:jwt
                    })
            apiresponse=apiresponse.json()
            token=apiresponse['responseObject']
            logging.info(f'Token generated successfully')
            
            return token
        
        
        except Exception as e:
            # print('exeception = ',str(e))
            logging.info(f'Error occuredwhile generating token: {str(e)}')

    def send_notification(token, errorMessage):
        
            doc_path = None
            # if screenshot_path:
            #     doc_path = "D:\\EPI_Saniya\\Id-Medical_old\\Ready_To_Deploy\\FHFT_NEW_UI\\screenshots\\28_days_after_error_occured_22_09_2026_16_52_19.png"#"C:\\ErrorSSTest\\test.png"#screenshot_path
            #     # doc_path = screenshot_path
            #     print(doc_path)
                
            """
            get token from thor token service
            """
            # current_date = datetime.today().strftime('%d-%m-%Y')
            current_datetime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            apiresponse=requests.post(Constants.NOTIFICATION_API_URL,
            headers={
                            
                    "ApplicationId":"11101",
                    "BuId":"27807",
                    "SubBuId":"1",
                    "Environment":"dev",
                    "Content-Type":"application/json",
                    "userlogin":"pramila@gmail.com",
                    "issuer":"fptool",
                    "jtitoken": token
                    # //Tokentype:jwt
                    },
            
            json={
                "notifyQueueId": None,
                "notifyEvent": {
                    "notifyEventId": 1
            },
            "notifyTemplate": {
                "notifyTemplateId": None,
                "Event notifyEvent": None,
                "notifyTemplateName": None,
                "notifyType": None,
                " notifyTarget": None,
                "deliveryChannel": None,
                "notifyTemplateXml": None,
                "isActive": None,
                "isAttachment": None,
                "attachmentCount": None,
                "documentId1": None,
                "documentId2": None,
                "documentId3": None,
                "documentId4": None,
                "documentId5": None,
                "createdBy": None,
                "createdDateTime": None,
                "lastModifiedBy": None,
                "lastModifiedDateTime": None
            },
            "isAttachment": 1,
            "attachmentCount": 1,
            "attachment1DocumentId": 0,
            "attachment2DocumentId": 0,
            "attachment3DocumentId": 0,
            "attachment4DocumentId": 0,
            "attachment5DocumentId": 0,
            "notifyDateTime": None,
            "deliveryChannel": "EMAIL",
            "notifyContactId": 86,
            "deliveryPriority": "Low",
            "dataPayloadXml": None,
            # "notifyTemplateXml": "<root><fromName>ID Medical</fromName><fromEmailId>idmedicaltest@gmail.com</fromEmailId><subject>URGENT(local): PY FHFT scraper has failed.</subject><to>kapil.patil@extrapreneursindia.com;saniya.pathan@extrapreneursindia.com;asmita.patil@extrapreneursindia.com;sourabh.shinde@extrapreneursindia.com</to><cc></cc><bcc></bcc><body><![CDATA[<br/>Dear Team, <br/><br/> The East Kent scraper has failed at {}.<br/><br/> The reason of the failure is : {}. <br/><br/><br/>Many thanks]]></body></root>".format(str(current_datetime), str(errorMessage)),
            "notifyTemplateXml": "<root><fromName>ID Medical</fromName><fromEmailId>idmedicaltest@gmail.com</fromEmailId><subject>URGENT(github action test): PY FHFT scraper has failed.</subject><to>saniya.pathan@extrapreneursindia.com</to><cc></cc><bcc></bcc><body><![CDATA[<br/>Dear Team, <br/><br/> The East Kent scraper has failed at {}.<br/><br/> The reason of the failure is : {}. <br/><br/><br/>Many thanks]]></body></root>".format(str(current_datetime), str(errorMessage)),
            "fromEmailId": None,
            "fromEmailName": None,
            "toEmailIdOrMobileNo": "",
            "emailSubjectText": "",
            "emailSMSBodyText": "",
            "addSignatureText": "",
            "ccEmailId": "",
            "bccEmailId": "",
            "addDisclaimerText": "",
            "addDndText": "",
            "deliveryAttemptCount": None,
            "deliveryLastErrorText": None,
            "deliveryStatus": None,
            "sessionId": None,
            "lastAttemptDatetime": None,
            "notificationRelatedContactId": None,
            "notifyRefType": "",
            "notifyRefRecordId": 121212,
            "notifyType": "System",
            "deviceToken": "",
            "pushNotificationType": None,
            "createdBy": None,
            "createdDate": None,
            "lastModifiedBy": None,
            "lastModifiedDateTime": None,
            # "attachmentFilePath": doc_path
            })
            
            apiresponse=apiresponse.json()
            print('response = ', apiresponse)
                    
            response =apiresponse['status']
            if response == 'success':
                logging.info(f'Notification sent succesfully')
            else:
                logging.info(f'Notification sending failed. Api response: {str(apiresponse)}')
                
            return 
    
    def get_credentials_from_db(cipher):
        try:
            
            db_user = cipher.decrypt(Constants.DB_USER)
            db_password = cipher.decrypt(Constants.DB_PASSWORD)
            conn = pymssql.connect(
                server=Constants.DB_SERVER,
                user=db_user,
                password=db_password,
                database=Constants.DB_NAME
            )
            
            cursor = conn.cursor()
            job_id = Constants.JOB_ID 
            cursor.execute(f"""
                SELECT attribute, value 
                FROM cfg_job_attribute_idmedical_clients WITH (NOLOCK)
                WHERE job_id={job_id} AND is_active = 1 AND 
                attribute IN ('Url', 'userName', 'Password')
            """)
            rows = cursor.fetchall()
            print('rows = ', rows)
            
            if len(rows) > 0:
                # Create a dictionary for easier access
                creds = {row[0]: row[1] for row in rows}
                url = creds.get('Url')
                username_ = creds.get('userName')
                password_ = creds.get('Password')
                
                try:
                    username = cipher.decrypt(username_)
                    password = cipher.decrypt(password_)  

                except Exception as e:
                    username = username_
                    password = password_
                    
                cursor.close()
                conn.close()
                logging.info(f'Credentials fetched successfully from database.')
                return url, username, password
            else:
                cursor.close()
                conn.close()
                logging.warning(f'No credentials found in database for job_id={job_id}')
                return None, None, None  
        
        except SecurityTokenException as e:
            logging.error(f'Security token exception while fetching credentials from DB: {str(e)}')
            return None, None, None
                
        except Exception as e:
            logging.error(f'Exception while fetching credentials from DB: {str(e)}')
            return None, None, None
            
    def unfilled_req_scraping():
        try:
            
            KEY = os.getenv("ENCRYPTION_KEY")

            cipher = SecurityCipher(KEY)
        
            start_time = time.time()
            logging.info(f'FHFT portal scraping started.')
            
            # Fetch credentials from database
            portal_url, portal_username, portal_password = FHFTPortalScraping.get_credentials_from_db(cipher)
            
            if not all([portal_url, portal_username, portal_password]):
                error_msg = "Failed to fetch credentials from database"
                logging.error(error_msg)
                return error_msg
            
            logging.info(f'Portal credentials fetched from database successfully.')
            
            list_of_unfilled_req_files_before_download = glob.glob(Constants.EXPORT_REQUIREMENT_EXCEL_DOWNLOAD_PATH + '*.xlsx')
                  
            with sync_playwright() as p:
                try:
                    # Launch Firefox instead of Chromium
                    browser = p.firefox.launch(headless=True)  # Set headless=False if you want to see the browser
                    # Set download directory
                    context = browser.new_context(accept_downloads=True)
                    driver = context.new_page()
                    # Visit the site
                    driver.goto(portal_url, timeout=60000)
                    time.sleep(3)
                    logging.info(f'Login page opened.')
                    
                    # Extract quotes
                    username = driver.locator('#'+Constants.USERNAME_ELEMENT_ID)                         
                    username.clear()
                    username.fill(portal_username)
                    
                    time.sleep(2)
                    
                    password = driver.locator("#"+Constants.PASSWORD_ELEMENT_ID)
                    password.clear()
                    password.fill(portal_password)
                    time.sleep(2)
                    
                    login_btn = driver.locator("#"+ Constants.LOGIN_BUTTON_ELEMENT_ID)
                    login_btn.click()
                    time.sleep(10)
                    logging.info(f'Login button clicked.')
                    
                    hidden_columns = driver.locator('#ctl00_content_BookingStatus1_cmdTable')
                    hidden_columns.click()
                    columns_list = driver.locator('#ctl00_content_BookingStatus1_display_ReorderList_ctl00_content_BookingStatus1_display_ReorderList_container')              
                    
                    gender_column = columns_list.locator("ul li").filter(has_text="Gender")
                    gender_column.scroll_into_view_if_needed()
                    gender_column.click()
                                
                    save_column = driver.locator('#ctl00_content_BookingStatus1_display_ReorderList__saveButton')
                    save_column.scroll_into_view_if_needed()
                    save_column.click()
                    time.sleep(10)
                    logging.info(f'Gender column selected and saved.')
                
                    # # select_next_28_days = driver.locator("#" + Constants.NEXT_28_DAYS_OPTION_ELEMENT_ID)
                    # select_next_28_days = driver.locator("select#"+ Constants.NEXT_28_DAYS_OPTION_ELEMENT_ID)
                    # # select_next_28_days.wait_for(state='visible', timeout=60000)
                    # select_next_28_days.select_option(label='Next 28 Days')
                    # # select_next_28_days.fill('Next 28 Days')
                    # driver.locator("span.select2").click()
                    # driver.locator("li.select2-results__option", has_text="Next 28 Days").click()
                    # driver.locator('span[aria-labelledby="select2-ctl00_content_BookingStatus1_mListDateOptions-container"]').click()
                    # driver.locator("li.select2-results__option", has_text="Next 28 Days").click()
                    
                    dropdown = driver.locator(Constants.TIME_PERIOD_DROPDOWN)
                    dropdown.click()
                                
                    
                    # 2. Wait for dropdown options to appear and click 'Next 28 Days'
                    option = driver.locator("xpath=//li[contains(text(), 'Next 28 Days')]")
                    option.click()
                    logging.info(f'Selected "Next 28 Days" period option.')
                    
                    driver.click("span#select2-ctl00_content_BookingStatus1_bankAgency-container")
                    driver.wait_for_selector("ul.select2-results__options", timeout=5000)
                    driver.click("li.select2-results__option >> text=Agency")
                    logging.info(f'Selected "Agency" option from What.')
                    
                    submit_filter = driver.locator('#'+ Constants.SUBMIT_FILTER_BUTTON_ID)
                    submit_filter.click()
                    
                    driver.locator('xpath='+Constants.DATA_LOADER_XPATH).wait_for(state='hidden',timeout=60000)
                    time.sleep(5)
                    logging.info(f'Filter submitted.')
                    
                    screenshot_path = datetime.now().strftime(os.path.join(Constants.EXECUTION_SCREENSHOTS_FOLDER, '28_days_unfilled_records_%d_%m_%Y_%H_%M_%S.png'))
                    driver.screenshot(path=screenshot_path, full_page=True) 
                    time.sleep(2)
                    
                    # # wait until requirements get loaded
                    # driver.locator('xpath='+Constants.DATA_LOADER_XPATH).wait_for(state='hidden',timeout=60000)
                    
                    # Wait and click download button
                    with driver.expect_download(timeout=80000) as download_info:
                        driver.click("#" + Constants.EXPORT_EXCEL_ELEMENT_ID)  # Replace with your actual button selector
                    # Get download object
                    download = download_info.value
                    
                    filename, ext = os.path.splitext(download.suggested_filename)
                    timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
                    unique_filename = f"{filename}_{timestamp}{ext}"
                    
                    file_path = os.path.join(Constants.EXPORT_REQUIREMENT_EXCEL_DOWNLOAD_PATH, unique_filename)
                    # Save the file with a custom name
                    download.save_as(file_path)
                    time.sleep(30)
                    
                    logging.info(f'Excel downloaded successfully.')
                    time.sleep(40)
                    
                    list_of_unfilled_req_files_after_download = glob.glob(Constants.EXPORT_REQUIREMENT_EXCEL_DOWNLOAD_PATH + '*.xlsx')
                    unfilled_req_excel_file = list(set(list_of_unfilled_req_files_after_download).difference(list_of_unfilled_req_files_before_download))
                    
                    if len(unfilled_req_excel_file)>0:
                        
                        logging.info(f'Unfilled Requirements excel available.')
                        
                        unfilled_req_file = unfilled_req_excel_file[0]
                        time.sleep(2)
                        unfilled_req_file_df = pd.read_excel(unfilled_req_file, dtype='object')
                        time.sleep(2) 
                        # unfilled_req_file_df["Request Id"] = unfilled_req_file_df["Request Id"].astype(str).str.zfill(10)
                        unfilled_req_file_df["Request Id"] = (
                                        unfilled_req_file_df["Request Id"]
                                        .fillna("")
                                        .astype(str)
                                        .str.replace(r"^'", "", regex=True)
                                        .str.strip()
                                        .str.zfill(10)
                                    )
                        unfilled_req_file_df['Date'] = pd.to_datetime(unfilled_req_file_df['Date']) # convert the column to a datetime object
                        unfilled_req_file_df['Date'] = unfilled_req_file_df['Date'].dt.strftime('%d-%b-%Y') # format the object
                        # src_file_df['Start'] = pd.to_datetime(src_file_df['Start'], format='%H:%M:%S').dt.strftime('%H:%M') # convert the column to a datetime object
                        # src_file_df['End'] = pd.to_datetime(src_file_df['End'], format='%H:%M:%S').dt.strftime('%H:%M')# format the object
                        time.sleep(2)
                        
                    else:
            
                        logging.info(f'No requirements file available.')
                        
                    time.sleep(2)
                    
                    ### Scraping Filled Bookings ###
                    list_of_filled_req_files_before_download = list_of_unfilled_req_files_after_download
                
                    click_filled_booking = driver.locator('#' + Constants.FILLED_BOOKING_OPTION_ID)
                    click_filled_booking.click()
                    time.sleep(15)
                    logging.info('Filled Bookings tab clicked.')
                    
                    dropdown = driver.locator(Constants.TIME_PERIOD_DROPDOWN)
                    dropdown.click()

                    # 2. Wait for dropdown options to appear and click 'Next 28 Days'
                    option = driver.locator("xpath=//li[contains(text(), 'Next 28 Days')]")
                    option.click()
                    time.sleep(3)
                    logging.info(f'Selected "Next 28 Days" period option.')
                    
                    submit_filter = driver.locator('#' + Constants.SUBMIT_FILTER_BUTTON_ID)
                    submit_filter.click() 
                    
                    # wait until requirements get loaded
                    driver.locator('xpath='+Constants.DATA_LOADER_XPATH).wait_for(state='hidden',timeout=80000)
                    time.sleep(5)
                    logging.info(f'Filter submitted.')

                    # TAKE SCREENSHOT AFTER ERROR
                    screenshot_path = datetime.now().strftime(os.path.join(Constants.EXECUTION_SCREENSHOTS_FOLDER, '28_days_filled_records_%d_%m_%Y_%H_%M_%S.png'))
                    driver.screenshot(path=screenshot_path) 
                    time.sleep(2)
                    
                    # # wait until requirements get loaded
                    # driver.locator('xpath='+Constants.DATA_LOADER_XPATH).wait_for(state='hidden',timeout=60000)
                    # Wait and click download button
                    with driver.expect_download(timeout=180000) as download_info:
                        driver.click("#" + Constants.EXPORT_EXCEL_ELEMENT_ID)  # Replace with your actual button selector
                    # Get download object
                    download = download_info.value
                    filename, ext = os.path.splitext(download.suggested_filename)
                    timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
                    unique_filename = f"{filename}_{timestamp}{ext}"
                    
                    file_path = os.path.join(Constants.EXPORT_REQUIREMENT_EXCEL_DOWNLOAD_PATH, unique_filename)
                    # Save the file with a custom name
                    download.save_as(file_path)
                    # time.sleep(30)
                    time.sleep(60)
                    logging.info(f'Filled Bookings Excel downloaded successfully.')
                    
                    #perform logout first to avoid cancel download popup
                    time.sleep(2)
                    logout_logo = driver.locator('#' + 'menuToggle')
                    logout_logo.click()
                    click_logout = driver.locator('.' + 'userPassword').all()
                    time.sleep(3)
                    click_logout[1].click()
                    time.sleep(5)
                    
                    driver.close()
                    
                    logging.info(f'Logged out successfully.')
                    
                    list_of_filled_req_files_after_download = glob.glob(Constants.EXPORT_REQUIREMENT_EXCEL_DOWNLOAD_PATH + '*.xlsx')
                    filled_req_exported_excel_file = list(set(list_of_filled_req_files_after_download).difference(list_of_filled_req_files_before_download))
                    
                    if len(filled_req_exported_excel_file) > 0:
                        
                        logging.info(f'Filled Requirements excel available.')
                        time.sleep(2)
                        exported_filled_req_file = filled_req_exported_excel_file[0]
                        time.sleep(2)
                        
                        filled_req_file_df = pd.read_excel(exported_filled_req_file, dtype='object')
                        # filled_req_file_df["Request Id"] = filled_req_file_df["Request Id"].astype(str).str.zfill(10)
                        filled_req_file_df["Request Id"] = (
                                        filled_req_file_df["Request Id"]
                                        .fillna("")
                                        .astype(str)
                                        .str.replace(r"^'", "", regex=True)
                                        .str.strip()
                                        .str.zfill(10)
                                    )
                        filled_req_file_df['Date'] = pd.to_datetime(filled_req_file_df['Date']) # convert the column to a datetime object
                        filled_req_file_df['Date'] = filled_req_file_df['Date'].dt.strftime('%d-%b-%Y') # format the object
                        time.sleep(2)
                        
                        file_name = datetime.now().strftime(os.path.join(Constants.EXPORTED_REQUIREMENT_EXCEL_FILENAME))
                        unfilled_requirement_file = os.path.join( Constants.REQUIREMENT_EXCEL_FOLDER, file_name)      
                        filled_req_file_name = datetime.now().strftime(os.path.join(Constants.EXPORTED_FILLED_EXCEL_FILENAME))
                        filled_req_file = os.path.join( Constants.EXPORT_FILLED_REQUIREMENT_EXCEL_DOWNLOAD_PATH, filled_req_file_name)  
                         
                        #Take only required columns everytime, if any new column is saved/added on portal
                        selected_columns = Constants.COLUMNS_LIST 
                        
                        unfilled_req_file_df = unfilled_req_file_df[selected_columns]                        
                        unfilled_req_file_df.to_excel(unfilled_requirement_file, index=False, engine='openpyxl' )   #, dtype={'Request Id': 'str'}) #, engine='openpyxl')
                        time.sleep(1)
                         
                        filled_req_file_df = filled_req_file_df[selected_columns]                        
                        filled_req_file_df.to_excel(filled_req_file, index=False)  #, engine='openpyxl')
                        time.sleep(1)
                        
                        logging.info(f'Unfilled requirements stored in file: {file_name}')
                        logging.info(f'Downloaded file moved to filled requirements folder.')
                        logging.info(f'Filled requirements stored in file: {filled_req_file_name}')
                        time.sleep(2)
                        
                    else:
                                    
                        logging.info(f'No requirements file available.')

                    logging.info('FHFT portal scraping completed.')
                
                    errorMessage = None
            
                except Exception:
                    try:
                        # TAKE SCREENSHOT AFTER ERROR
                        screenshot_path = datetime.now().strftime(os.path.join(Constants.EXECUTION_SCREENSHOTS_FOLDER, '28_days_after_error_occured_%d_%m_%Y_%H_%M_%S.png'))
                        driver.screenshot(path=screenshot_path) 
                        driver.close()
                        # driver.quit()
                    except:
                        logging.info(f'Inside exception of capturing error screenshot, driver not initialised.')        
                    
                    exception_type, exception_value, exception_traceback = sys.exc_info()
                    traceback_string = traceback.format_exception(exception_type,
                                    exception_value, exception_traceback)
                    err_msg = json.dumps({
                        "errorType": exception_type.__name__,
                        "errorMessage": str(exception_value),
                        "stackTrace": traceback_string
                    })
                    logging.error(f'Error Occured: {err_msg}') 
                    err_dict = json.loads(err_msg) 
                    errorMessage = err_dict['errorMessage']            
                    end_time = time.time()
                    total_time = end_time - start_time
                    logging.info(f'Time required for the execution is {total_time}')
         
        
        except SecurityTokenException as e:
        
            errorMessage = str(e)
            
            logging.error(f'errorMessage: {errorMessage}')    
                   
        except Exception as e:
    
            errorMessage = str(e)
        
        return errorMessage
    
        
if __name__ == '__main__':
    
    # GHCPortalScraping.unfilled_req_scraping()         
    start_time = time.time()
    iteration = 0
    
    # message = FHFTPortalScraping.unfilled_req_scraping()  

    # if message:
    #     print('1')
    message2 = FHFTPortalScraping.unfilled_req_scraping()
    if message2: 
        print('2')
        token = FHFTPortalScraping.gettoken()    
        if token:
            FHFTPortalScraping.send_notification(token, message2)  
        else:
            # print('Token generation failed')
            logging.info(f'Token generation failed')
            logging.info(f'Notification not sent.')
        
    end_time = time.time()
    total_time = end_time - start_time
    logging.info(f'Total time required for the execution is {total_time}')
            
                   
                    
  