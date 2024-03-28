$(document).ready(function() {
    // Add event listener for the Add button
    $('#add-btn').click(function() {
        var name = $('#todo-name').val();
        var category = $('#todo-category').val();
        var price = $('#todo-price').val();

        // Perform client-side validation
        if (name === '' || category === '' || price === '') {
            alert('Please fill in all fields.');
            return;
        }

        // Send AJAX request to add the budget item
        $.ajax({
            type: 'POST',
            url: '/table',
            data: {
                name: name,
                category: category,
                price: price
            },
            success: function(response) {
                // Reload the page to reflect the changes
                location.reload();
            },
            error: function(xhr, status, error) {
                console.error('Error adding budget item:', error);
            }
        });
    });

    // Add event listener for the Delete buttons
    $('.delete-btn').click(function() {
        var id = $(this).data('id');

        // Send AJAX request to delete the budget item
        $.ajax({
            type: 'POST',
            url: '/delete',
            data: {
                id: id
            },
            success: function(response) {
                // Reload the page to reflect the changes
                location.reload();
            },
            error: function(xhr, status, error) {
                console.error('Error deleting budget item:', error);
            }
        });
    });
});
