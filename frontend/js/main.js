import { initNavigation } from './modules/navigation.js';
import { initFileUpload } from './modules/fileUpload.js';
import { initPaginationForTable } from './modules/paginationTable.js';
import { processDataForEmployees, processDataForHiredPerQuarter, processDataForDepartmentsAboveAvg } from './config/config.js';

window.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initFileUpload();
    initPaginationForTable('pagination-employees', 'table-body-employees', 
        'employees', 'employees/total', processDataForEmployees);
  
      initPaginationForTable('pagination-hired-per-quarter', 'table-body-hired-per-quarter', 
        'reports/hired_per_quarter', 'reports/total_hired_per_quarter', processDataForHiredPerQuarter);
  
      initPaginationForTable('pagination-departments-above-avg', 'table-body-departments-above-avg', 
        'reports/departments_above_avg', 'reports/total_departments_above_avg', processDataForDepartmentsAboveAvg);
});