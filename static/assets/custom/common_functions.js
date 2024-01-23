// Filter all cars...
$(document).ready(function () {
    // Function to handle filtering
    function filterCars() {
        var filters = {
            condition: $('#condition').val(),
            brand: $('#brand').val(),
            model: $('#model').val(),
            year: $('#year').val(),
            mileage: $('#mileage').val(),
            price_min: $('#price_min').val(),
            price_max: $('#price_max').val(),
            body_type: $('#body_type').val(),
        };

        $.ajax({
            url: '#',  // Replace with your actual URL
            type: 'POST',
            data: filters,
            success: function (response) {
                console.log(response.cars);
                // Handle the filtered cars in the frontend
            },
            error: function (error) {
                console.error('Error filtering cars:', error);
            }
        });
    }

    // Attach an event listener to the filter button
    $('#filter_button').click(function () {
        filterCars();
    });
});


// Add favorite car...
// Assuming you have a button with the class "favorite-button" and data-car-id attribute
$('#favorite-button').click(function () {
    const carId = $(this).data('car-id');

    $.ajax({
        url: `/cars/toggle_favorite/${carId}/`,
        type: 'POST',
        data: {
            csrfmiddlewaretoken: "{{csrf_token}}"
        },
        success: function (response) {
            console.log(response.is_favorite);

            // Handle success or error messages
            if (response.is_favorite) {
                showSuccessNotification(response.message);
                $("#add_favorite_icon").removeClass('far fa-heart').addClass('fas fa-xmark');
            } else {
                showErrorNotification(response.message);
                $("#add_favorite_icon").removeClass('fas fa-xmark').addClass('far fa-heart');
            }
        },
        error: function (error) {
            console.log("something went wrong...");
            showErrorNotification(error.message);
        }
    });
});


// Remove favorite car...
// Assuming you have a button with the class "remove-favorite-button" and data-favorite-id attribute
$('#remove-favorite-button').click(function () {
    const carId = $(this).data('car-id');

    $.ajax({
        url: `/cars/remove_favorite/${carId}/`,
        type: 'POST',
        data: {
            csrfmiddlewaretoken: "{{csrf_token}}"
        },
        success: function (response) {
            console.log(response);

            // Handle success or error messages
            if (response.status === 'success') {
                showSuccessNotification(response.message);
                // Here i want to refresh the page
                location.reload();
            } else {
                showErrorNotification(response.message);
            }
        },
        error: function (error) {
            console.log("something went wrong...");
            showErrorNotification(error.message);
        }
    });
});
