// JavaScript für CRM System

document.addEventListener('DOMContentLoaded', function() {
    // Klickbare Tabellenzeilen
    initClickableRows();
    
    // Tooltips initialisieren
    initTooltips();
    
    // Automatisches Ausblenden von Alerts
    initAutoHideAlerts();
    
    // Datumsfilter-Validierung
    initDateValidation();
});

/**
 * Macht Tabellenzeilen klickbar
 */
function initClickableRows() {
    const rows = document.querySelectorAll('.clickable-row');
    rows.forEach(row => {
        row.style.cursor = 'pointer';
        row.addEventListener('click', function(e) {
            // Klick nur verarbeiten, wenn nicht auf Link oder Button geklickt wurde
            if (!e.target.closest('a') && !e.target.closest('button')) {
                const href = this.dataset.href;
                if (href) {
                    window.location.href = href;
                }
            }
        });
    });
}

/**
 * Initialisiert Bootstrap Tooltips
 */
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Blendet Alerts nach 5 Sekunden automatisch aus
 */
function initAutoHideAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

/**
 * Validiert Datumsfilter (Von-Datum muss vor Bis-Datum liegen)
 */
function initDateValidation() {
    const dateFromInput = document.getElementById('date_from');
    const dateToInput = document.getElementById('date_to');
    
    if (dateFromInput && dateToInput) {
        function validateDates() {
            const fromDate = new Date(dateFromInput.value);
            const toDate = new Date(dateToInput.value);
            
            if (fromDate && toDate && fromDate > toDate) {
                dateToInput.setCustomValidity('Das Enddatum muss nach dem Startdatum liegen');
            } else {
                dateToInput.setCustomValidity('');
            }
        }
        
        dateFromInput.addEventListener('change', validateDates);
        dateToInput.addEventListener('change', validateDates);
    }
}

/**
 * Lädt Umsatzdaten per AJAX (für zukünftige Erweiterungen)
 */
function loadRevenueData(customerId, dateFrom, dateTo) {
    const url = `/customers/${customerId}/revenue?from=${dateFrom}&to=${dateTo}`;
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log('Revenue data loaded:', data);
            // Hier könnten die Daten dynamisch in die Seite eingefügt werden
        })
        .catch(error => {
            console.error('Error loading revenue data:', error);
        });
}

/**
 * Formatiert eine Zahl als Währung (EUR)
 */
function formatCurrency(value) {
    return new Intl.NumberFormat('de-AT', {
        style: 'currency',
        currency: 'EUR'
    }).format(value);
}

/**
 * Formatiert ein Datum nach deutschem Standard
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('de-AT', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    }).format(date);
}

/**
 * Zeigt eine Bestätigungsmeldung an
 */
function confirmAction(message) {
    return confirm(message);
}

/**
 * Zeigt einen Loading-Spinner an
 */
function showLoading() {
    const spinner = document.createElement('div');
    spinner.id = 'loading-spinner';
    spinner.className = 'position-fixed top-50 start-50 translate-middle';
    spinner.innerHTML = `
        <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Laden...</span>
        </div>
    `;
    document.body.appendChild(spinner);
}

/**
 * Versteckt den Loading-Spinner
 */
function hideLoading() {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) {
        spinner.remove();
    }
}

// Export für Module (falls benötigt)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        formatCurrency,
        formatDate,
        confirmAction,
        showLoading,
        hideLoading,
        loadRevenueData
    };
}
