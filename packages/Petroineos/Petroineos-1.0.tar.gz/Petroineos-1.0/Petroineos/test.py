import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import pandas as pd
import shutil
import datetime
import schedule
import time
import logging


class test:
    
    def __init__(self):
        
        '''Initializing the script...'''
        print("Initializing the script...")
        
        url = "https://www.gov.uk/government/statistics/oil-and-oil-products-section-3-energy-trends"

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.attachments = soup.find_all('section', class_='attachment embedded')


    def create_folder(self,folder_name):
        
        '''Creating a folder for files...'''
        print("Creating a folder for files...")
        time.sleep(2)

        # Get current working directory
        path = os.getcwd()

        # Concatenate the current directory and the file name 
        folder_path = os.path.join(path, f'{folder_name}')
        print(folder_path)
        
        # Create a folder if it doesn't exist       
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
            
    
    def download_files(self):
        
        '''Downloading the excel files from the website...'''
        print("Downloading the excel files from the website...")
        
        # Create folder for files, csv files, processed files and do the profiling checks
        p.create_folder(folder_name="processed_files")
        p.create_folder(folder_name="csv_files")
        p.create_folder(folder_name="files")

        files_folder_path = os.path.join(os.getcwd(), "files")
        processed_path = os.path.join(os.getcwd(), "processed_files")

        # Append the Quarter sheet from the excel file
        self.dfs = []  

        # Extract the href links from the child a elements within each attachment element 
        for i, attachment in enumerate(self.attachments):
            link = attachment.find('a')
            href = link['href']
            
            if href.endswith('.xlsx'):
                print(f"Downloading file {i}")
                
                # Download the file
                with open(os.path.join(files_folder_path, href.split('/')[-1]), 'wb') as f:
                    response = requests.get(href)
                    f.write(response.content)
                                    
                # Read the file into a pandas data frame
                df = pd.read_excel(os.path.join(files_folder_path, href.split('/')[-1]), sheet_name='Quarter')
                
                # Append the data frame to the list
                self.dfs.append(df)
                
         # get a list of all the Excel files in the source directory
        excel_files = [f for f in os.listdir(files_folder_path) if f.endswith('.xlsx')]

        # loop through each Excel file and move it to the destination directory
        for file in excel_files:
            src_file = os.path.join(files_folder_path, file)
            dest_file = os.path.join(processed_path, file)
            
            # check if a file with the same name already exists in the destination directory
            if os.path.exists(dest_file):
                os.remove(dest_file)  # remove the existing file

            shutil.move(src_file, dest_file)    
                
    
    def do_data_profiling(self):
        
        """Doing the profiling check..."""
        print("Doing the profiling check...")

        dfs = self.dfs
        data_profiling = []
        
        for i in range(4, 23):
            
            row_name = dfs[0].iloc[i,0]
            min_value = dfs[0].iloc[i, 1:].min()
            max_value = dfs[0].iloc[i, 1:].max()
            median_values = dfs[0].iloc[i, 1:].median()
            mean_values = dfs[0].iloc[i, 1:].mean()
            missing_values = dfs[0].iloc[i, 1:].isnull().sum()

            # Append the results as a dictionary to a list
            data_profiling.append({
                'Row Name': row_name,
                'Min Value': min_value,
                'Max Value': max_value,
                'Median Value': median_values,
                'Mean Value': mean_values,
                'Missing Values': missing_values
            })
            
            profiling_df = pd.DataFrame(data_profiling)
           
        # Concatenate the current directory and the file name, then save them as csv files
        folder_path = os.path.join(os.getcwd(), "csv_files")
        file_name = 'ET_3.1_DEC_22_data_profiling.csv'
        rows_file_name = 'ET_3.1_DEC_22.csv'
        
        output_file_path = f'{folder_path}/{file_name}'
        rows_output_file_path = f'{folder_path}/{rows_file_name}'
        
        profiling_df.to_csv(output_file_path, index=False)
        
        rows_df = self.dfs[0].iloc[3:23,:]
        print(rows_df)
        rows_df.to_csv(rows_output_file_path, index=False)
        
        print(profiling_df)
        print(rows_df)
        

    def check_files_for_update(self):
        
        """Check the downloaded files if there is an update..."""
        print("Check the downloaded files if there is an update...")
        
        data_consistency = []
        
        # The raw file rows and columns
        Number_of_rows = self.dfs[0].shape[0]
        print("File-Number_of_rows: ", Number_of_rows)
        Number_of_columns = self.dfs[0].shape[1]
        print("File-Number_of_columns: ", Number_of_columns)
        
        Missing_values = self.dfs[0].isnull().sum()
        
        # Concatenate the current directory and the processed_files folder 
        processed_files_path = os.path.join(os.getcwd(), 'processed_files/ET_3.1_DEC_22.xlsx')
        
        # Read the processed file into a pandas data frame with required Quarter sheet
        processed_file_df = pd.read_excel(processed_files_path, sheet_name='Quarter')
        
        # Processed file rows and columns
        Processed_Number_of_rows = processed_file_df.shape[0]
        print("Processed file-Number_of_rows: ", Processed_Number_of_rows)
        Processed_Number_of_columns = processed_file_df.shape[1]
        print("Processed file-Number_of_columns: ", Processed_Number_of_columns)
        
        # get the current date and time, and format the date and time as a string
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        # Check for new data, and if a new dataset is detected
        if self.dfs[0].shape == processed_file_df.shape:
            Quarter_sheet = f"[{timestamp}] No update found on Quarter sheet. No new rows, columns were created."
            print(f"[{timestamp}] No update found on Quarter sheet. No new rows, columns were created.")
            print("Empty the files folder.")
            
            # loop through all the files in the folder and delete them
            files_folder_path = os.path.join(os.getcwd(), 'files')

            for filename in os.listdir(files_folder_path):
                file_path = os.path.join(files_folder_path, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f"Error deleting file: {e}")
            
        else:
            Quarter_sheet = f"[{timestamp}] Update found on Quarter sheet. New rows, columns were created."
            print(f"[{timestamp}] Update found on Quarter sheet. New rows, columns were created.")
        
        data_consistency.append({
            'File-Number_of_rows' : Number_of_rows,
            'File-Number_of_columns' : Number_of_columns,
            'Processed file-Number_of_rows' : Processed_Number_of_rows,
            'Processed file-Number_of_columns' : Processed_Number_of_columns,
            'Missing values' : Missing_values,
            'Quarter_sheet': Quarter_sheet})
        
        data_consistency_df = pd.DataFrame(data_consistency)
        data_consistency_file = 'ET_3.1_DEC_22_data_consistency.csv'

         # identify the extra columns 
        extra_cols = set(self.dfs[0].columns) - set(processed_file_df.columns)

        # create a new data frame with the extra columns
        extra_cols_df = self.dfs[0][list(extra_cols)]
        
        # save the new data frame
        folder_path = os.path.join(os.getcwd(), "csv_files")
        file_name = 'ET_3.1_DEC_22_extra_columns.csv'
        output_file_path = f'{folder_path}/{file_name}'

        extra_cols_df.to_csv(output_file_path, index=False)
        
        data_consistency_file_path = f'{folder_path}/{data_consistency_file}'
        data_consistency_df.to_csv(data_consistency_file_path, index=False)
                       

    def move_files_to_processed_files(self):
        
        """Moving raw files to the processed files folder..."""
        print("Moving raw files to the processed files folder...")
        
        # set the path to the source directory (where the files are located)
        src_dir = 'files/'

        # set the path to the destination directory (where the processed files will be moved to)
        dest_dir = 'processed_files/'

        # get a list of all the Excel files in the source directory
        excel_files = [f for f in os.listdir(src_dir) if f.endswith('.xlsx')]

        # loop through each Excel file and move it to the destination directory
        for file in excel_files:
            src_file = os.path.join(src_dir, file)
            dest_file = os.path.join(dest_dir, file)
            
            # check if a file with the same name already exists in the destination directory
            if os.path.exists(dest_file):
                os.remove(dest_file)  # remove the existing file

            shutil.move(src_file, dest_file)    
    
    
    def setup_logging(self,log_folder, log_filename):
        
        # Create the log folder if it doesn't exist
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)

        # Set up logging
        log_file = os.path.join(log_folder, log_filename)
        logging.basicConfig(filename=log_file, level=logging.DEBUG,
                            format='%(asctime)s [%(levelname)s] %(message)s')


    def log_message(self, message, level='debug'):
        
        logger = logging.getLogger()
        if level == 'debug':
            logger.debug(message)
        elif level == 'warning':
            logger.warning(message)
        elif level == 'error':
            logger.error(message)
        elif level == 'critical':
            logger.critical(message)
        else:
            logger.info(message)

                

def run_test():
    
    log_folder = 'logs'
    log_filename = 'app.log'
    
    p.setup_logging(log_folder, log_filename)
    p.log_message('The script is running: ')
    
    p.download_files()
    p.check_files_for_update()
    p.do_data_profiling()    
    p.move_files_to_processed_files()

if __name__ == "__main__":
    
    p = test()

    # schedule the function to run every 24 hours
    schedule.every(24).hours.do(run_test)
    
    # run the function once to start with
    run_test()
    
    # loop to run scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(1)

