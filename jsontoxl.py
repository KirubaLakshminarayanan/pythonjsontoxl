import json
import os
import logging
from openpyxl import Workbook
from datetime import datetime

# Create a log folder if it doesn't exist
log_folder = 'logs'
os.makedirs(log_folder, exist_ok=True)

# Add timestamp to the log filename
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
log_filename = os.path.join(log_folder, f'conversion_{timestamp}.log')


# Function to configure logging with a custom log file name
def configure_logging(log_filename):
    logging.basicConfig(
        filename=log_filename,
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='w'  # Use 'w' to overwrite the log file each time, 'a' to append
    )


# Call the logging configuration function
configure_logging(log_filename)


# Function to check if a file is a JSON file
def is_json(file_path):
    try:
        with open(file_path) as f:
            json.load(f)
            return True
    except (ValueError, FileNotFoundError):
        return False


# Function to flatten JSON data
def flatten_json(data, parent_key='', sep='_'):
    if isinstance(data, dict):
        items = {}
        for k, v in data.items():
            new_key = parent_key + sep + k if parent_key else k
            items.update(flatten_json(v, new_key, sep=sep))
        return items
    elif isinstance(data, list):
        items = {}
        for i, v in enumerate(data):
            new_key = parent_key + sep + str(i)
            items.update(flatten_json(v, new_key, sep=sep))
        return items
    else:
        return {parent_key: data}


# Function to convert JSON data to Excel
def convert_to_excel(file_paths):
    total_files = len(file_paths)
    success_count = 0  # Track the number of successful conversions

    for file_path in file_paths:
        if not file_path.endswith('.json'):
            logging.error(f"Skipping {file_path}: Invalid file format. Please provide a JSON file.")
            continue

        if os.path.getsize(file_path) == 0:
            logging.error(f"Skipping {file_path}: File is empty.")
            continue

        try:
            with open(file_path, 'r') as json_file:
                try:
                    data = json.load(json_file)
                except ValueError as e:
                    error_message = f"Invalid JSON format in {file_path}: {str(e)}"
                    logging.error(error_message)
                    continue

                if isinstance(data, dict):
                    records = [data]
                elif isinstance(data, list):
                    records = data
                else:
                    logging.error(f"Skipping {file_path}: Invalid JSON data format.")
                    continue

                if not records:
                    logging.error(f"No records found in {file_path}.")
                    continue

                flattened_records = [flatten_json(record) for record in records]

                # Get the headers in the order of keys from the first record
                headers = list(flattened_records[0].keys())

                excel_file_name = file_path[:-5] + '_' + datetime.now().strftime("%Y%m%d%H%M%S") + '.xlsx'
                wb = Workbook()
                ws = wb.active

                ws.append(headers)

                for record in flattened_records:
                    row_data = []
                    for header in headers:
                        row_data.append(
                            record.get(header, ''))  # Get value for each header or empty string if not present
                    ws.append(row_data)

                wb.save(excel_file_name)
                logging.info(f"{file_path} conversion successful. Converted to {excel_file_name}.")
                logging.info(f"Size of converted file: {os.path.getsize(excel_file_name)} bytes")
                success_count += 1  # Increment the success count
        except Exception as e:
            logging.error(f"{file_path} conversion failed! Error: {str(e)}")

    failed_files_count = total_files - success_count
    return success_count, failed_files_count


# Test the functions
if __name__ == "__main__":
    # Include the JSON file paths here
    file_paths = [
        r'C:\Users\LKiruba\Desktop\Json_to_csv\Sample_Scenarios\Individual_json_File.json',
        r'C:\Users\LKiruba\Desktop\Json_to_csv\Sample_Scenarios\equal key-value pairs.json'
    ]
    success_count, failed_files_count = convert_to_excel(file_paths)
    print(f"Conversion successful for {success_count} file(s). Conversion failed for {failed_files_count} file(s).")
