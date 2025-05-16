document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('filter-toggle');
    const filterSection = document.getElementById('filter-section');
    const icon = document.getElementById('filter-icon');

    const urlParams = new URLSearchParams(window.location.search);
    const collectionFilter = urlParams.get("collectionfilter");

    if (urlParams.has("collectionfilter")) {
        filterSection.classList.toggle('hidden');
        icon.textContent = filterSection.classList.contains('hidden') ? '▶' : '▼';
    }

    toggle.addEventListener('click', function () {
        filterSection.classList.toggle('hidden');
        icon.textContent = filterSection.classList.contains('hidden') ? '▶' : '▼';
    });

    const selects = document.querySelectorAll('select[id^="dropdown-"]');

    selects.forEach(function (select) {
        select.addEventListener('change', function () {
            const item = this.value;
            // const key = select.id;
            var key = this.id.replace('dropdown-', '');

            select.classList.remove('enabled');

            if (key && item) {
                select.classList.add('enabled');
                const siteUrl = document.body.dataset.portalUrl;
                const baseUrl = siteUrl + '/prolong-collection';
                
                const query = 'collectionfilter=1&' + encodeURIComponent(key) + '=' + encodeURIComponent(item.replace(/^ /, ''));
                const url = baseUrl + '?' + query;
                

                fetch(url, {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                    .then(response => {
                        if (!response.ok) throw new Error('Network response was not ok');
                        return response.text();
                    })
                    .then(html => {
                        const parser = new DOMParser();
                        const doc = parser.parseFromString(html, 'text/html');
                        const newContent = doc.querySelector('#content-core');
                        const contentTarget = document.querySelector('#content-core');

                        if (newContent && contentTarget) {
                            contentTarget.innerHTML = newContent.innerHTML;
                        }
                    })
                    .catch(error => {
                        console.error('Error fetching filtered content:', error);
                    });
            }
        });
    });
});
