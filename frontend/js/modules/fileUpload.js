// file-upload.js
import { uploadButtons, fileInput, spinners } from '../config/config.js';
import { showAlertModal, closeAlertModal } from './modal.js';
import { uploadFile } from '../services/apiUploadFile.js';

let currentEndpoint = "";

export function handleFileUploadClick(endpoint) {
    currentEndpoint = endpoint;
    fileInput.click();
}

export function initFileUpload() {
    uploadButtons.departments.addEventListener('click', () => handleFileUploadClick('departments'));
    uploadButtons.jobs.addEventListener('click', () => handleFileUploadClick('jobs'));
    uploadButtons.employees.addEventListener('click', () => handleFileUploadClick('employees'));

    closeAlertModal();

    fileInput.addEventListener('change', () => {
        const file = fileInput.files[0];
        let alertModalTitle = "";
        let alertModalBody = "";
        if (file) {
            const formData = new FormData();
            formData.append('file', file);
            toggleButtonState(true);

            uploadFile(currentEndpoint,formData)
                .then(response => {
                    alertModalTitle = 'File uploaded successfully!';
                    alertModalBody = response.message || '';
                })
                .catch(error => {
                    alertModalTitle = 'Error uploading file!';
                    alertModalBody = error.message;
                })
                .finally(() => {
                    setTimeout(() => {
                        toggleButtonState(false);
                        showAlertModal(alertModalTitle, alertModalBody);
                    }, 2000); // Wait 2 seconds before showing the modal
                });

            fileInput.value = ''; // Reset file input
        } else {
            alertModalTitle = 'No file selected.';
            alertModalBody = 'Please choose a file before uploading.';
            setTimeout(() => {
                toggleButtonState(false);
                showAlertModal(alertModalTitle, alertModalBody);
            }, 2000);
        }
    });
}

function toggleButtonState(isLoading) {
    const buttons = Object.keys(uploadButtons);
    buttons.forEach((buttonKey) => {
        const button = uploadButtons[buttonKey];
        const spinner = spinners[buttonKey];
        if (currentEndpoint === buttonKey) {
            if (isLoading) {
                spinner.classList.add('active');
                button.classList.add('disabled');
            } else {
                spinner.classList.remove('active');
                button.classList.remove('disabled');
            }
        }
    });
}
