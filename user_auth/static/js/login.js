$(document).ready(function () {

    // Password visibility toggle
    $('#password-visibility').on('click', function () {
        var passwordField = $('#floatingPassword');
        var icon = $(this).find('i');

        // Toggle password visibility
        if (passwordField.attr('type') === 'password') {
            passwordField.attr('type', 'text');
            icon.removeClass('uil-eye').addClass('uil-eye-slash');
        } else {
            passwordField.attr('type', 'password');
            icon.removeClass('uil-eye-slash').addClass('uil-eye');
        }
    });

    // Form submission via AJAX
    $('#login-form').on('submit', function (e) {
        e.preventDefault(); // Prevent the form from submitting the traditional way

        var formData = $(this).serialize(); // Serialize form data
        // Clear previous error messages
        $('#error-messages').empty().addClass('d-none');

        // Get CSRF token from the form data
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

        // AJAX request to submit form
        $.ajax({
            url: $(this).attr('action'), // Use the form's action URL
            type: 'POST',
            data: formData,
            headers: {
                'X-CSRFToken': csrfToken // Add CSRF token to headers
            },
            dataType: 'json', // Explicitly set the response type to JSON
            success: function (response) {
                console.log(response); // Log 
                                // Check if the response contains errors
                if (response.errors) {
                    
                    var errorHtml = '<ul>';
                    response.errors.forEach(function (error) {
                        errorHtml += '<li>' + error + '</li>';
                    });
                    errorHtml += '</ul>';

                    // Show the error messages in the error-messages div
                    $('#error-messages').html(errorHtml).removeClass('d-none');
                } else {
                    // If successful, handle redirect or other actions
                    console.log(response.redirect_url)
                    window.location.href = response.redirect_url; // Redirect to the dashboard or appropriate page
                }
            },
            
        });
    });

});
