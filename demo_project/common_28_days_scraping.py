import os
from dotenv import load_dotenv

# ENV_FILE = os.path.join(
#     'D:\\EPI_Saniya\\Id-Medical_old\\Ready_To_Deploy\\Github_action_project\\Github_Action_Demo\\demo_project',
#     ".env" 
# )

# load_dotenv(ENV_FILE)

class Constants:

    TOKEN_API_URL = "http://192.168.80.101:80/SecurityManagement/api/v1/token"
    NOTIFICATION_API_URL = "http://192.168.80.101:80/Notification/api/v1/queue"
    
    DB_SERVER=os.getenv("DB_SERVER")
    DB_USER=os.getenv("DB_USER")
    DB_PASSWORD=os.getenv("DB_PASSWORD")
    DB_NAME=os.getenv("DB_NAME")
    
    SECURITY_SERVICE_PATH = r"D:\EPI_Saniya\Id-Medical_old\Ready_To_Deploy"
    CRED_ENV_FILE_PATH = 'D:\\EPI_Saniya\\Id-Medical_old\\Ready_To_Deploy\\Security_Cipher_Service'
    
    WORKING_DIRECTORY = "D:\\EPI_Saniya\\Id-Medical_old\\Ready_To_Deploy\\GitHubExecutionFilesStore"
    
    JOB_ID = 30
    LOGIN_PAGE_FRAME_ID = 'aspnetForm'
    USERNAME_ELEMENT_ID = 'ctl00_content_login_UserName'
    PASSWORD_ELEMENT_ID = 'ctl00_content_login_Password'
    LOGIN_BUTTON_ELEMENT_ID = 'ctl00_content_login_LoginButton'
    
    FILTER_FIELD_ELEMENT_ID = 'ctl00_content_BookingStatus1_collapsibleImage'
    NEXT_28_DAYS_OPTION_ELEMENT_ID = 'ctl00_content_BookingStatus1_mListDateOptions'
    SUBMIT_FILTER_BUTTON_ID = 'ctl00_content_BookingStatus1_cmdSubmitPrint'
    EXPORT_EXCEL_ELEMENT_ID = 'ctl00_content_BookingStatus1_cmdXLS'
    TIME_PERIOD_DROPDOWN = '#select2-ctl00_content_BookingStatus1_mListDateOptions-container' 
    AGENCY_OPTION_ELEMENT_ID = 'ctl00_content_BookingStatus1_bankAgency_1'
    FILLED_BOOKING_OPTION_ID = 'ctl00_navigation_RequestsNav_FilledLink'
    
    
    # LOGOUT_BUTTON_XPATH = '/html/body/form/div[3]/table/tbody/tr/td[3]/div/table/tbody/tr[2]/td[4]/a'
    LOGOUT_BUTTON_XPATH = '/html/body/form/div[3]/table/tbody/tr/td[3]/div[1]/table/tbody/tr[2]/td[5]/a'
    DATA_LOADER_XPATH = '/html/body/form/table/tbody/tr/td[2]/div[2]/div/span/span'
    DATA_LOADER_ID = 'ctl00_content_PleaseWaitCaption'
    
                       
    # EXPORT_REQUIREMENT_EXCEL_DOWNLOAD_PATH = 'D:\\EPI_Saniya\\Id-Medical_old\\Ready_To_Deploy\\FHFT_NEW_UI\\download\\'
    # REQUIREMENT_EXCEL_FOLDER = 'D:\\EPI_Saniya\\Id-Medical_old\\Ready_To_Deploy\\FHFT_NEW_UI\\unfilled_requirements_excels\\'
    # EXPORT_FILLED_REQUIREMENT_EXCEL_DOWNLOAD_PATH = 'D:\\EPI_Saniya\\Id-Medical_old\\Ready_To_Deploy\\FHFT_NEW_UI\\filled_requirements_excels\\'
    # EXECUTION_SCREENSHOTS_FOLDER = 'D:\\EPI_Saniya\\Id-Medical_old\\Ready_To_Deploy\\FHFT_NEW_UI\\screenshots\\'
    # EXECUTION_LOGS_FOLDER = 'D:\\EPI_Saniya\\Id-Medical_old\\Ready_To_Deploy\\FHFT_NEW_UI\\execution_logs\\'
    # Cross-platform folder paths (relative to script location)
    
    
    # EXPORT_REQUIREMENT_EXCEL_DOWNLOAD_PATH = os.path.join(os.path.dirname(__file__), 'download') + os.sep
    # REQUIREMENT_EXCEL_FOLDER = os.path.join(os.path.dirname(__file__), 'unfilled_requirements_excels') + os.sep
    # EXPORT_FILLED_REQUIREMENT_EXCEL_DOWNLOAD_PATH = os.path.join(os.path.dirname(__file__), 'filled_requirements_excels') + os.sep
    # EXECUTION_SCREENSHOTS_FOLDER = os.path.join(os.path.dirname(__file__), 'screenshots') + os.sep
    # EXECUTION_LOGS_FOLDER = os.path.join(os.path.dirname(__file__), 'execution_logs') + os.sep
    
    
    EXPORT_REQUIREMENT_EXCEL_DOWNLOAD_PATH = os.path.join(WORKING_DIRECTORY, 'download') + os.sep
    REQUIREMENT_EXCEL_FOLDER = os.path.join(WORKING_DIRECTORY, 'unfilled_requirements_excels') + os.sep
    EXPORT_FILLED_REQUIREMENT_EXCEL_DOWNLOAD_PATH = os.path.join(WORKING_DIRECTORY, 'filled_requirements_excels') + os.sep
    EXECUTION_SCREENSHOTS_FOLDER = os.path.join(WORKING_DIRECTORY, 'screenshots') + os.sep
    EXECUTION_LOGS_FOLDER = os.path.join(WORKING_DIRECTORY, 'execution_logs') + os.sep
        
        
    COLUMNS_LIST = ['Request Id', 'Date', 'Start', 'End', 'Unit', 'Cost Centre', 'Request Grade', 'Skill',	'Agency', 'Staff']
    
    EXECUTION_LOGS_FILENAME = '28_Days_logfile_%d_%m_%Y_%H_%M_%S.log'
    EXPORTED_REQUIREMENT_EXCEL_FILENAME = '28_Days_Unfilled_Requireents_Excel_%d_%m_%Y_%H_%M_%S.xlsx'
    EXPORTED_FILLED_EXCEL_FILENAME = '28_Days_Filled_Requireents_Excel_%d_%m_%Y_%H_%M_%S.xlsx'
    
    # ------------------------------------------------------------------ #
    #  Auto-create all required folders when the class is first loaded    #
    # ------------------------------------------------------------------ #
    @classmethod
    def create_folders(cls) -> None:
        """Create all required working directories if they don't already exist."""
        folders = [
            cls.EXPORT_REQUIREMENT_EXCEL_DOWNLOAD_PATH,
            cls.REQUIREMENT_EXCEL_FOLDER,
            cls.EXPORT_FILLED_REQUIREMENT_EXCEL_DOWNLOAD_PATH,
            cls.EXECUTION_SCREENSHOTS_FOLDER,
            cls.EXECUTION_LOGS_FOLDER,
        ]
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
            print(f"[Constants] Folder ready: {folder}")
            
Constants.create_folders()