// Filter all cars...
$(document).ready(function () {
    // Function to handle filtering
    function filterCars() {
        var filters = {
            condition: $('#condition').val(),
            brand: $('#car_brand').val(),
            model: $('#car_model').val(),
            year: $('#year').val(),
            mileage: $('#mileage').val(),
            price: $('#price').val(),
            body_type: $('#body_type').val(),
            csrfmiddlewaretoken: "{{csrf_token}}"
        };
        $.ajax({
            url: "/filtered_results/",  // Replace with your actual URL
            type: 'POST',
            data: filters,
            success: function (response) {
                console.log(response.cars);
                showSuccessNotification("Filtered complete.");
            },
            error: function (error) {
                console.log('Error filtering cars:', error);
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



$(document).ready(function () {
    // Add a click event listener to all category-item links
    $('.category-item').on('click', function (event) {
        event.preventDefault(); // Prevent the default link behavior

        // Get the selected body type from the data attribute
        var bodyType = $(this).data('body-type');

        // Send an AJAX request to your backend with the selected body type
        $.ajax({
            type: 'POST',
            url: '/filtered_results/', // Replace with the actual URL of your FilterCarView
            data: { body_type: bodyType },
            success: function (response) {
                console.log("Data sent")
                // Handle the response from the backend (e.g., redirect to search.html)
                window.location.href = '/filtered_results/';
            },
            error: function (error) {
                console.log('Error:', error);
            }
        });
    });
});


$(document).ready(function () {
    // Add a click event listener to all category-item links
    $('.brand-item').on('click', function (event) {
        event.preventDefault();

        var brand = $(this).data('brand');

        $.ajax({
            type: 'POST',
            url: "/cars/car_filter/",
            data: {
                brand: brand,
                csrfmiddlewaretoken: "{{csrf_token}}"
            },
            success: function (data) {
                console.log("Data sent")
                // Clear existing car list
                $('#car-list').empty();

                // Update car list with filtered data
                $.each(data.filtered_cars, function (index, car) {
                    var carItem = `
                        <div class="col-md-6 col-lg-4">
                            <div class="car-item">
                                <div class="car-img">
                                    <span class="car-status status-1">${car.status}</span>
                                    <img src="${car.get_main_image}" style="height:150px; width:100%">
                                    <div class="car-btns">
                                        <a type="button" id="favorite-button" data-car-id="${car.slug}">
                                            ${car.favorited_by ? '<i class="fas fa-xmark" id="remove_favorite_icon"></i>' : '<i class="far fa-heart" id="add_favorite_icon"></i>'}
                                        </a>
                                    </div>
                                </div>
                                <div class="car-content">
                                    <div class="car-top">
                                        <h4><a href="/cars/${car.slug}">${car.get_car_name}</a></h4>
                                    </div>
                                    <ul class="car-list">
                                        <li><i class="far fa-steering-wheel"></i>${car.transmission}</li>
                                        <li><i class="far fa-road"></i>${car.power}</li>
                                        <li><i class="far fa-car"></i>Model: ${car.model_year}</li>
                                        <li><i class="far fa-gas-pump"></i>${car.fuel}</li>
                                    </ul>
                                    <div class="car-footer">
                                        <span class="car-price">₦${car.price.toLocaleString()}</span>
                                        <a href="/cars/${car.slug}" class="theme-btn"><span class="far fa-eye"></span>Details</a>
                                    </div>
                                </div>
                            </div>
                        </div>`;

                    $('#car-list').append(carItem);
                });
            },
            error: function (error) {
                console.log('Error:', error);
            }
        });
    });
});
