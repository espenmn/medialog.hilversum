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

    if (toggle) {
        toggle.addEventListener('click', function () {
            filterSection.classList.toggle('hidden');
            icon.textContent = filterSection.classList.contains('hidden') ? '▶' : '▼';
        });
    }

    const selects = document.querySelectorAll('select[id^="dropdown-"]');

    selects.forEach(function (select) {
        select.addEventListener('change', function () {
            const item = this.value;
            // const key = select.id;
            var key = this.id.replace('dropdown-', '');

            select.classList.remove('enabled');
            const siteUrl = document.body.dataset.portalUrl;
            const baseUrl = siteUrl + '/prolong-collection';
            var url = baseUrl;

            if (key && item) {
                select.classList.add('enabled');
                const query = 'collectionfilter=1&' + encodeURIComponent(key) + '=' + encodeURIComponent(item.replace(/^ /, ''));
                url = baseUrl + '?' + query;
            }

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

        });
    });
});

// need to allow cookies for this
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".buttonFavorit").forEach(button => {
        button.addEventListener("click", function () {
            const id = this.getAttribute("data-id");
            const remove = this.getAttribute("data-remove") === "1";

            // Get current cookie (if any)
            let favorites = getCookie("favorites");
            let favArray = favorites ? favorites.split(",") : [];

            if (remove) {
                // Remove the ID if it exists
                favArray = favArray.filter(fav => fav !== id);
                alert("Removed from favorites!");
            } else {
                // Add ID if it doesn't exist
                if (!favArray.includes(id)) {
                    favArray.push(id);
                    alert("Added to favorites!");
                }
            }

            // Set updated cookie (expires in 30 days)
            document.cookie = "favorites=" + favArray.join(",") + "; path=/; max-age=" + 60 * 60 * 24 * 30;
        });
    });

    function getCookie(name) {
        const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
        return match ? match[2] : null;
    }
});

