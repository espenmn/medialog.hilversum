document.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);
    const collectionFilter = urlParams.get("collectionfilter");
    const baseUrl = document.body.getAttribute('data-base-url') || window.location.pathname;
    const selects = document.querySelectorAll('select[id^="prolog-dropdown-"]');

    // Clear Filters button
    const clearBtn = document.getElementById('clear-filters');
    if (clearBtn) {
        clearBtn.addEventListener('click', function () {
            selects.forEach(select => {
                select.selectedIndex = 0;
                select.classList.remove('enabled');
            });

            const url = baseUrl + "?" + buildParams();
            fetchFilteredContent(url);
        });
    }

    // Build query params from selects
    function buildParams() {
        const params = new URLSearchParams();
        params.set("collectionfilter", "1");

        selects.forEach(s => {
            const key = s.id.replace("prolog-dropdown-", "");
            const value = s.value.trim();
            if (value) params.set(key, value);
        });

        return params.toString();
    }

    // Fetch updated content
    function fetchFilteredContent(url) {
        console.log("Fetching URL:", url);
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
            } else {
                console.warn("Could not find #content-core in response or target.");
            }

            initTableSorter();
        })
        .catch(error => {
            console.error('Error fetching filtered content:', error);
        });
    }

    // Table sorter
    function initTableSorter() {
        document.querySelectorAll('table.sortable').forEach(table => {
            if (typeof $(table).tablesorter === 'function') {
                $(table).tablesorter({ sortList: [[0, 0]] });
            }
        });
    }

    // Filter select change handler
    selects.forEach(select => {
        select.addEventListener('change', function () {
            selects.forEach(s => s.classList.remove('enabled'));
            if (select.value.trim()) {
                select.classList.add('enabled');
            }

            const url = baseUrl + "?" + buildParams();
            fetchFilteredContent(url);
        });
    });

    // Dynamic buttons (folderview, listing)
    document.body.addEventListener('click', function (event) {
        const target = event.target;
        const paramsStr = buildParams();

        if (target.matches('.to_folderview')) {
            const url = baseUrl + "/@@proloog-folder-view?" + paramsStr;
            fetchFilteredContent(url);
        }

        if (target.matches('.to_listing')) {
            const url = baseUrl + "/@@proloog-listing?" + paramsStr;
            fetchFilteredContent(url);
        }
    });

    // Alphabet filter
    document.body.addEventListener("click", function (event) {
        if (event.target.classList.contains("alphabet-btn")) {
            const letter = event.target.getAttribute("data-letter");

            const params = new URLSearchParams();
            params.set("collectionfilter", "1");
            if (letter !== "all") {
                params.set("firstletter", letter);
            }

            const url = baseUrl + "?" + params.toString();
            fetchFilteredContent(url);

            document.querySelectorAll(".alphabet-btn").forEach(btn => btn.classList.remove("active"));
            event.target.classList.add("active");
        }
    });

    // Favorites
    document.querySelectorAll(".buttonFavorit").forEach(button => {
        button.addEventListener("click", function () {
            const id = this.getAttribute("data-id");
            const remove = this.getAttribute("data-remove") === "1";

            let favArray = getCookie("favorites")?.split(",") || [];

            if (remove) {
                favArray = favArray.filter(fav => fav !== id);
            } else if (!favArray.includes(id)) {
                favArray.push(id);
            }

            document.cookie = `favorites=${favArray.join(",")}; path=/; max-age=${60 * 60 * 24 * 30}`;
            location.reload();
        });
    });

    function getCookie(name) {
        const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
        return match ? match[2] : null;
    }

    // Initial tablesorter init
    initTableSorter();
});
