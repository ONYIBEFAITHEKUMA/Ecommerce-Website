$(document).ready(function() {
    $('#search-input').on('input', function() {
        let query = $(this).val();
        if (query.length > 2) {  // Start searching after typing 3 characters
            $.ajax({
                url: searchUrl,  // We'll define `searchUrl` in the HTML template
                data: {
                    'q': query
                },
                dataType: 'json',
                success: function(data) {
                    let resultsDiv = $('#search-results');
                    resultsDiv.empty();  // Clear previous results
                    if (data.length > 0) {
                        data.forEach(function(item) {
                            resultsDiv.append(`
                                <a href="/product_detail/${item.id}/" class="search-result-item">
                                    <p>${item.name}</p>
                                </a>
                            `);
                        });
                    } else {
                        resultsDiv.append('<p>No results found.</p>');
                    }
                }
            });
        } else {
            $('#search-results').empty();  // Clear results if query is too short
        }
    });
});
