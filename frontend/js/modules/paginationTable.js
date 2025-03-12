import { fetchTotalItems, fetchData } from '../services/reports.js';

const paginationLimit = 10;

export function initPaginationForTable(paginationId, tableBodyId, endpoint, totalEndpoint, processData) {
    let totalItems = 0;
    let totalPages = 0;
    let currentPage = 1;

    async function fetchTotalItemsData() {
        totalItems = await fetchTotalItems(totalEndpoint);
        totalPages = Math.ceil(totalItems / paginationLimit);
        updatePagination();
    }

    async function fetchDataPage(page) {
        const items = await fetchData(endpoint, page, paginationLimit);
        updateTable(items);
    }

    function updateTable(items) {
        const tableBody = document.getElementById(tableBodyId);
        tableBody.innerHTML = "";

        items.forEach(item => {
            const row = document.createElement("tr");
            row.innerHTML = processData(item);
            tableBody.appendChild(row);
        });
    }

    function updatePagination() {
        const paginationElement = document.getElementById(paginationId);
        paginationElement.innerHTML = `
            <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
                <a class="page-link">Previous</a>
            </li>
        `;

        let pageItems = [];

        if (totalPages <= 5) {
            for (let i = 1; i <= totalPages; i++) {
                pageItems.push(createPageItem(i));
            }
        } else {
            if (currentPage <= 3) {
                for (let i = 1; i <= 4; i++) {
                    pageItems.push(createPageItem(i));
                }
                pageItems.push(createEllipsis());
                pageItems.push(createPageItem(totalPages));
            } else if (currentPage >= totalPages - 2) {
                pageItems.push(createPageItem(1));
                pageItems.push(createEllipsis());
                for (let i = totalPages - 4; i <= totalPages; i++) {
                    pageItems.push(createPageItem(i));
                }
            } else {
                pageItems.push(createPageItem(1));
                pageItems.push(createEllipsis());
                for (let i = currentPage - 1; i <= currentPage + 1; i++) {
                    pageItems.push(createPageItem(i));
                }
                pageItems.push(createEllipsis());
                pageItems.push(createPageItem(totalPages));
            }
        }

        pageItems.forEach(item => paginationElement.innerHTML += item);

        paginationElement.innerHTML += `
            <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
                <a class="page-link">Next</a>
            </li>
        `;

        addPaginationListeners();
    }

    function createPageItem(page) {
        const isActive = page === currentPage ? 'active' : '';
        return `
            <li class="page-item ${isActive}" data-page="${page}">
                <a class="page-link">${page}</a>
            </li>
        `;
    }

    function createEllipsis() {
        return `<li class="page-item disabled"><span class="page-link">...</span></li>`;
    }

    function changePage(page) {
        if (page >= 1 && page <= totalPages) {
            currentPage = page;
            fetchDataPage(currentPage);
            updatePagination();
        }
    }

    function nextPage() {
        if (currentPage < totalPages) {
            currentPage++;
            fetchDataPage(currentPage);
            updatePagination();
        }
    }

    function prevPage() {
        if (currentPage > 1) {
            currentPage--;
            fetchDataPage(currentPage);
            updatePagination();
        }
    }

    function addPaginationListeners() {
        const prevPageElement = document.querySelector(`#${paginationId} .page-item:first-child a`);
        prevPageElement.addEventListener("click", (e) => {
            e.preventDefault();
            prevPage();
        });

        const nextPageElement = document.querySelector(`#${paginationId} .page-item:last-child a`);
        nextPageElement.addEventListener("click", (e) => {
            e.preventDefault();
            nextPage();
        });

        const pageItems = document.querySelectorAll(`#${paginationId} .page-item[data-page]`);
        pageItems.forEach(item => {
            item.addEventListener("click", (e) => {
                e.preventDefault();
                const page = parseInt(item.dataset.page);
                changePage(page);
            });
        });
    }

    fetchTotalItemsData();
    fetchDataPage(currentPage);
}
