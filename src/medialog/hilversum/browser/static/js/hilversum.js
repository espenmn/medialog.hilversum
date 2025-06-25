document.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);
    const collectionFilter = urlParams.get("collectionfilter");
    const selects = document.querySelectorAll('select[id^="prolog-dropdown-"]');
    const baseUrl = document.body.getAttribute('data-base-url');
    
 


    document.getElementById('clear-filters').addEventListener('click', function () {
        const selects = document.querySelectorAll('select[id^="prolog-dropdown-"]');
        selects.forEach(select => {
          select.selectedIndex = 0; // Set to first option
          select.classList.remove('enabled'); //remove 'selected color'
        });
    
        // Optional: trigger form submission or event after reset
        // document.querySelector('form').submit(); 
        const paramsStr = buildParams();
        const url = baseUrl + "?" + paramsStr;
        fetchFilteredContent(url);
      });

    // Function to build the query string from the selects
    function buildParams() {
        let params = new URLSearchParams();
        params.set("collectionfilter", "1");

        selects.forEach(function (s) {
            const k = s.id.replace("prolog-dropdown-", "");
            const v = s.value.trim();
            if (v) {
                params.set(k, v);
            }
        });

        return params.toString();
    }

    // Function to perform fetch and update content
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
    
                // Return a resolved promise to chain the next `.then`
                return Promise.resolve();
            })
            .then(initTableSorter)
            .catch(error => {
                console.error('Error fetching filtered content:', error);
            });
    }
    
    function initTableSorter() {
        const tables = document.querySelectorAll('table.sortable');
        tables.forEach(function (table) {
            if (typeof $(table).tablesorter === 'function') {
                $(table).tablesorter({ sortList: [[0, 0]] });
            }
        });
    }

    // Event listener for select dropdowns
    selects.forEach(function (select) {
        select.addEventListener('change', function () {
            const baseUrl = document.body.getAttribute('data-base-url');
            const paramsStr = buildParams();

            // Update UI for changed select
            select.classList.remove('enabled');
            selects.forEach(function (s) {
                const v = s.value.trim();
                if (s === select && v) {
                    select.classList.add('enabled');
                }
            });

            const url = baseUrl + "?" + paramsStr;
            fetchFilteredContent(url);
        });
    });

    

    // Delegated event listeners for dynamic buttons
    document.body.addEventListener('click', function (event) {
        const baseUrl = document.body.getAttribute('data-base-url');
        const paramsStr = buildParams();

        if (event.target.matches('.to_folderview')) {
            const url = baseUrl + "/@@proloog-folder-view?" + paramsStr;
            fetchFilteredContent(url);
        }

        if (event.target.matches('.to_listing')) {
            const url = baseUrl + "/@@proloog-listing?" + paramsStr;
            fetchFilteredContent(url);

        }
    });


    // Delegated event listener for alphabet buttons
    document.body.addEventListener("click", function (event) {
        if (event.target.classList.contains("alphabet-btn")) {
            const baseUrl = document.body.getAttribute("data-base-url") || window.location.pathname;
            const letter = event.target.getAttribute("data-letter");

            let params = new URLSearchParams();
            params.set("collectionfilter", "1");

            if (letter !== "all") {
                params.set("firstletter", letter);
            }

            const url = baseUrl + "?" + params.toString();
            fetchFilteredContent(url);

            // Highlight active button
            // TO Do, move this to viewlet so filter does not load with Ajax Load
            document.querySelectorAll(".alphabet-btn").forEach(b => b.classList.remove("active"));
            event.target.classList.add("active");             
        }
    });



    // Favorites button handling
    document.querySelectorAll(".buttonFavorit").forEach(button => {
        button.addEventListener("click", function () {
            const id = this.getAttribute("data-id");
            const remove = this.getAttribute("data-remove") === "1";

            let favorites = getCookie("favorites");
            let favArray = favorites ? favorites.split(",") : [];

            if (remove) {
                favArray = favArray.filter(fav => fav !== id);
            } else {
                if (!favArray.includes(id)) {
                    favArray.push(id);
                }
            }

            document.cookie = "favorites=" + favArray.join(",") + "; path=/; max-age=" + 60 * 60 * 24 * 30;
            location.reload();
        });
    });

    function getCookie(name) {
        const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
        return match ? match[2] : null;
    }

    const tables = document.querySelectorAll('table.sortable');
    tables.forEach(function (table) {
        if (typeof $(table).tablesorter === 'function') {
            $(table).tablesorter({ sortList: [[0, 0]] });
        }
    });
});

