import pandas as pd
import io
import csv

def validate_columns(df, expected_columns):
    """
    Validate that the number of columns matches the expected number.
    
    Args:
        df (pd.DataFrame): The DataFrame to validate.
        expected_columns (list): The list of expected column names.
    
    Raises:
        ValueError: If the number of columns does not match the expected number.
    """
    if len(df.columns) != len(expected_columns):
        raise ValueError(f"Number of columns in CSV does not match expected. Expected {len(expected_columns)}, got {len(df.columns)}.")
    df.columns = expected_columns

def validate_column_types(df, expected_types):
    """
    Convert columns to the expected data types.
    
    Args:
        df (pd.DataFrame): The DataFrame to validate.
        expected_types (dict): A dictionary where keys are column names and values are the expected data types.
    
    Raises:
        ValueError: If a column cannot be converted to the expected data type.
    """
    for column, dtype in expected_types.items():
        if column in df.columns:
            try:
                if dtype == int:
                    df[column] = pd.to_numeric(df[column]).fillna(0).astype(int)
                else:
                    df[column] = df[column].astype(dtype)
            except ValueError:
                raise ValueError(f"Cannot convert column {column} to {dtype}")

async def process_csv(file, expected_types):
    """
    Processes a CSV file and returns a list of tuples.
    
    Args:
        file (file-like object): The CSV file to be processed.
        expected_types (dict): A dictionary where keys are column names and values are the expected data types.
    
    Returns:
        list of tuple: A list where each element is a tuple representing a row in the CSV file.
    
    Raises:
        ValueError: If there is an error processing the CSV file.
    """
    try:
        file_content = file.stream.read().decode("utf-8")
        
        expected_columns = list(expected_types.keys())
        df = pd.read_csv(io.StringIO(file_content), header=None, names=expected_columns)
        
        validate_columns(df, expected_columns)
        validate_column_types(df, expected_types)

        csv_data = csv.reader(io.StringIO(file_content))

        my_data = []
        for row in csv_data:
            row = [None if value == '' else value for value in row]
            my_data.append(tuple(row))
        
        return my_data
    except Exception as e:
        raise ValueError(f"Error processing CSV file: {e}")
