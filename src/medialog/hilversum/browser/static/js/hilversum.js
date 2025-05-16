
$(document).ready(function () {
    $('select[id^="dropdown-"]').on('change', function () {
        var key = this.id.replace('dropdown-', '');
        var item = $(this).val();

        if (key && item) {
            var baseUrl = '${portal_url}/prolong-collection/';
            var query = 'collectionfilter=1&' + encodeURIComponent(key) + '=' + encodeURIComponent(item) + '&discipline_op=or';
            window.location.href = baseUrl + '?' + query;
        }
    });
});

 

document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('filter-toggle');
    const filterSection = document.getElementById('filter-section');
    const icon = document.getElementById('filter-icon');

    toggle.addEventListener('click', function () {
        filterSection.classList.toggle('hidden');
        icon.textContent = filterSection.classList.contains('hidden') ? '▶' : '▼';
    });
});
