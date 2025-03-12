const navSelectors = {
    home: document.getElementById('home-selector'),
    employees: document.getElementById('employees-selector'),
    reports: document.getElementById('reports-selector'),
    integrations: document.getElementById('integrations-selector')
};

function activateSection(navLink, section) {
    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
    document.querySelectorAll('.main-content section').forEach(sec => sec.classList.remove('active'));
    section.classList.add('active');
    navLink.classList.add('active');
}

export function initNavigation() {
    Object.keys(navSelectors).forEach(key => {
        navSelectors[key].addEventListener('click', function (event) {
            event.preventDefault();
            activateSection(navSelectors[key], document.getElementById(key));
        });
    });
}
