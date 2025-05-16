
document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('filter-toggle');
    const filterSection = document.getElementById('filter-section');
    const icon = document.getElementById('filter-icon');

    toggle.addEventListener('click', function () {
        filterSection.classList.toggle('hidden');
        icon.textContent = filterSection.classList.contains('hidden') ? '▶' : '▼';
    });

    var selects = document.querySelectorAll('select[id^="dropdown-"]');
  
    selects.forEach(function (select) {
      select.addEventListener('change', function () {
        var key = this.id.replace('dropdown-', '');
        var item = this.value;
  
        if (key && item) {
          var siteUrl = document.body.dataset.portalUrl;
          var baseUrl = siteUrl + '/prolong-collection/';
          var query = 'collectionfilter=1&' + encodeURIComponent(key) + '=' + encodeURIComponent(item) + '&discipline_op=or';
          window.location.href = baseUrl + '?' + query;
        }
      });
    });
  });