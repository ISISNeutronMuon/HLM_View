const objectSearchURL = JSON.parse(document.getElementById('object-names-url').textContent);

var objectDisplay = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  prefetch: objectSearchURL,
  remote: {
    url: objectSearchURL,
    replace: function(url, query) {
      return url + "?q=" + query;
    }
  }
});

$('.objectSearchTypeahead').typeahead({
  minLength: 1,
  highlight: true,
  hint: true,
},
{
  name: 'objects-display',
  limit: 5,
  display: 'name',
  source: objectDisplay
});
