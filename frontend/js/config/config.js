export const API_URL = 'http://20.253.27.22:5000'; //change this for production

export const uploadButtons = {
    departments: document.getElementById('upload-btn-departments'),
    jobs: document.getElementById('upload-btn-jobs'),
    employees: document.getElementById('upload-btn-employees')
};

export const spinners = {
    departments: document.getElementById('upload-spinner-departments'),
    jobs: document.getElementById('upload-spinner-jobs'),
    employees: document.getElementById('upload-spinner-employees')
};

export const fileInput = document.getElementById('csv-file');

export function processDataForEmployees(item) {
    return `
      <td>${item.id}</td>
      <td>${item.name}</td>
      <td>${new Date(item.datetime).toLocaleString()}</td>
      <td>${item.department}</td>
      <td>${item.job}</td>
    `;
  }

export function processDataForHiredPerQuarter(item) {
    return `
      <td>${item.department}</td>
      <td>${item.job}</td>
      <td>${item.Q1}</td>
      <td>${item.Q2}</td>
      <td>${item.Q3}</td>
      <td>${item.Q4}</td>
    `;
  }

export function processDataForDepartmentsAboveAvg(item) {
    return `
      <td>${item.id}</td>
      <td>${item.department}</td>
      <td>${item.hired}</td>
    `;
  }