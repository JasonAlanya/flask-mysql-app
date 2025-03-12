# Frontend Documentation

## Overview
This is the frontend for the data management system, built using vanilla JavaScript, HTML, CSS and Bootstrap. It provides an interface for uploading CSV files, viewing reports, and navigating the system efficiently. The frontend interacts with the backend API to fetch and display data.

## Folder Structure
```
frontend/
┣ js/
┃ ┣ config/
┃ ┃ ┗ config.js           # Configuration settings (API URLs, etc.)
┃ ┣ modules/
┃ ┃ ┣ color-modes.js      # Dark/light mode functionality
┃ ┃ ┣ fileUpload.js       # Handles CSV file uploads
┃ ┃ ┣ modal.js            # Modal window functionality
┃ ┃ ┣ navigation.js       # Navigation menu logic
┃ ┃ ┗ paginationTable.js  # Handles table pagination
┃ ┣ services/
┃ ┃ ┣ apiUploadFile.js    # API calls for file uploads
┃ ┃ ┗ reports.js          # API calls for fetching reports
┃ ┗ main.js               # Main script entry point
┣ styles.css/
┃ ┗ styles.css            # Main stylesheet for the application
┣ dockerfile              # Docker configuration for containerizing the frontend
┗ index.html              # Main HTML file
```

## Installation & Setup

### 1. API Configuration
Modify `js/config/config.js` to set the correct backend API URLs:
```js
const API_BASE_URL = "http://127.0.0.1:5000"; // Change this if backend runs on a different host/port
```

## Features
- **CSV Uploads**: Users can upload CSV files for departments, jobs, and employees.
- **Reports**: Displays data analytics retrieved from the backend API.
- **Pagination**: Large datasets are paginated for better usability.
- **Modals**: Used for displaying information or warnings.

## Docker Setup
To build and run the frontend as a Docker container:
```sh
docker build -t my-frontend .
docker run --name frontend-container -p 8080:80 -d my-frontend
```
Then, access it at `http://localhost:8080/`.