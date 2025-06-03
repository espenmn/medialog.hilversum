// define(['jquery'], function ($) {
//     $(document).ready(function () {
//         const $toggle = $('#filter-toggle');
//         const $filterSection = $('#filter-section');
//         const $icon = $('#filter-icon');
//         const urlParams = new URLSearchParams(window.location.search);

//         if (urlParams.has("collectionfilter")) {
//             $filterSection.toggleClass('hidden');
//             $icon.text($filterSection.hasClass('hidden') ? '▶' : '▼');
//         }

//         $toggle.on('click', function () {
//             $filterSection.toggleClass('hidden');
//             $icon.text($filterSection.hasClass('hidden') ? '▶' : '▼');
//         });
//     });
// });

$(function () {
    const $toggle = $('#filter-toggle');
    const $filterSection = $('#filter-section');
    const $icon = $('#filter-icon');
    const urlParams = new URLSearchParams(window.location.search);

    if (urlParams.has("collectionfilter")) {
        $filterSection.toggleClass('hidden');
        $icon.text($filterSection.hasClass('hidden') ? '▶' : '▼');
    }

    $toggle.on('click', function () {
        $filterSection.toggleClass('hidden');
        $icon.text($filterSection.hasClass('hidden') ? '▶' : '▼');
    });
});



document.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);
    const collectionFilter = urlParams.get("collectionfilter");

    const selects = document.querySelectorAll('select[id^="dropdown-"]');

    selects.forEach(function (select) {
        select.addEventListener('change', function () {
            const siteUrl = document.body.dataset.portalUrl;
            const baseUrl = siteUrl + '/proloog-collection';
            let params = new URLSearchParams();
            select.classList.remove('enabled');

            // Always include collectionfilter=1
            params.set("collectionfilter", "1");

            // Go through all selects and get their current value
            selects.forEach(function (s) {
                const k = s.id.replace("dropdown-", "");
                const v = s.value.trim();
                if (v) {
                    params.set(k, v);
                    if (s === select && k != v) {
                        select.classList.add('enabled');
                    }
                }
            });

            const url = baseUrl + "?" + params.toString();
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
            // console.log("Before removal:", favArray);
            // console.log("ID to remove:", id);

            if (remove) {
                // Remove the ID if it exists
                favArray = favArray.filter(fav => fav !== id);
                // alert("Removed from favorites!");
            } else {
                // Add ID if it doesn't exist
                if (!favArray.includes(id)) {
                    favArray.push(id);
                    // alert("Added to favorites!");
                }
            }

            // console.log("After removal:", favArray);
            // Set updated cookie (expires in 30 days)
            document.cookie = "favorites=" + favArray.join(",") + "; path=/; max-age=" + 60 * 60 * 24 * 30;
            // alert('reloading');
            location.reload(); // Reload the page to reflect changes
        });
    });

    function getCookie(name) {
        const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
        return match ? match[2] : null;
    }
});

