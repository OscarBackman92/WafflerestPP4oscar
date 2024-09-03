$(document).ready(function() {
    $('#booking-form').submit(function(event) {
        event.preventDefault();
    
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    alert(response.message);
                    // Optionally redirect or update the page here
                } else {
                    // Clear previous errors
                    $('.errorlist').remove();

                    if (response.errors) {
                        var error_data = JSON.parse(response.errors);
                        $.each(error_data, function(field, errors) {
                            var field_errors = '<ul class="errorlist">';
                            $.each(errors, function(index, error) {
                                field_errors += '<li>' + error + '</li>';
                            });
                            field_errors += '</ul>';

                            // Find the field element and insert errors after it
                            var fieldElement = $('#id_' + field);
                            if (fieldElement.length) {  // Check if the field exists
                                fieldElement.after(field_errors);
                            } else if (field === '__all__') {  // Handle non-field errors
                                $('#booking-form').prepend(field_errors); 
                            }
                        });
                    } else {
                        alert("An error occurred. Please try again.");
                    }
                }
            },
            error: function(error) {
                console.error('Error submitting booking:', error);
                alert("An error occurred. Please try again.");
            }
        });
    });
});
