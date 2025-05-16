
document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('filter-toggle');
    const filterSection = document.getElementById('filter-section');
    const icon = document.getElementById('filter-icon');
    // Check if collectionfilter is in url
    const fullUrl = window.location.href;
    // console.log("Full URL:", fullUrl);
    // Use URLSearchParams to extract query parameters
    const urlParams = new URLSearchParams(window.location.search);
    const collectionFilter = urlParams.get("collectionfilter");
    // for (const [key, value] of urlParams.entries()) {
    //     console.log(`${key}: ${value}`);
    // 'dropdown-' + key = id
    // }

    if (urlParams.has("collectionfilter")) {
        filterSection.classList.toggle('hidden');
    }

    toggle.addEventListener('click', function () {
        filterSection.classList.toggle('hidden');
        icon.textContent = filterSection.classList.contains('hidden') ? '▶' : '▼';
    });

    var selects = document.querySelectorAll('select[id^="dropdown-"]');


    // Parse URL parameters
    const params = new URLSearchParams(window.location.search);

    selects.forEach(function (select) {
        
        // Bind change handler for AJAX loading
        select.addEventListener('change', function () {
            var item = this.value;
            var key = select.id;            

            const dropdown = document.getElementById(key);
            select.classList.remove('enabled');
                

            if (key && item) {
                // If this key is present in the URL, add 'enabled' class            
                const dropdown = document.getElementById(key);
                select.classList.add('enabled');
                const siteUrl = document.body.dataset.portalUrl;
                const baseUrl = siteUrl + '/prolong-collection';
                const query = 'collectionfilter=1&' + encodeURIComponent(key) + '=' + encodeURIComponent(item);
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
