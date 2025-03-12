export function showAlertModal(title, body) {
    const alertModal = new bootstrap.Modal(document.getElementById('alert-modal'));
    const alertModalTitle = document.getElementById('alert-modal-title');
    const alertModalBody = document.getElementById('alert-modal-body');

    alertModalTitle.textContent = title;
    alertModalBody.textContent = body;

    alertModal.show();
}

export function closeAlertModal() {
    const alertModalCloseBtn = document.getElementById('alert-modal-close-btn');
    const alertModalElement = document.getElementById('alert-modal');

    alertModalCloseBtn.addEventListener('click', (event) => {
        event.preventDefault();
        const modalInstance = bootstrap.Modal.getInstance(alertModalElement);
        modalInstance.hide();
    });
}