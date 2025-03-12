import { API_URL } from '../config/config.js';

export async function uploadFile(endpoint, formData) {
    const apiUrl = API_URL;
    const response = await fetch(`${apiUrl}/${endpoint}/upload`, {
        method: 'POST',
        body: formData
    });
    if (!response.ok) {
        return response.json().then(errorData => {
            throw new Error(errorData.error || 'Error uploading file');
        });
    }
    return await response.json();
}
