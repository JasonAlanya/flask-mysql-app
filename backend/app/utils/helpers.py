import csv
import io

def process_csv(file):
    """
    Processes a CSV file and returns a list of tuples.
    Args:
        file (file-like object): The CSV file to be processed.
    Returns:
        list of tuple: A list where each element is a tuple representing a row in the CSV file.
    """
    try:
        stream = io.StringIO(file.stream.read().decode("utf-8"))
        csv_data = csv.reader(stream)

        my_data = []
        for row in csv_data:
            row = [None if value == '' else value for value in row]
            my_data.append(tuple(row))
        
        return my_data
    except Exception as e:
        raise ValueError(f"Error processing CSV file: {e}")