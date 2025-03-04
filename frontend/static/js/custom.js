// the slider
var swiper = new Swiper('.swiper', {
    // autoplay: {
    //     delay: 5000,  // Slide change interval (in ms)
    // },
    slidesPerView: 1,  // Number of slides visible at once
    spaceBetween: 10,  // Space between slides
    centerSlides: true,
});
// Handle HTML tag when the page loads 
document.addEventListener("DOMContentLoaded", function () {
    // Get the current language from the template variable
    const currentLanguage = document.documentElement.getAttribute("data-lang");

    // Set direction and language based on current language
    const htmlTag = document.documentElement;

    if (currentLanguage === "ar") {
        htmlTag.setAttribute("dir", "rtl");
        htmlTag.setAttribute("lang", "ar");
        swiper.changeLanguageDirection("rtl");
    } else {
        htmlTag.setAttribute("dir", "ltr");
        htmlTag.setAttribute("lang", "en");
        swiper.changeLanguageDirection("ltr");

    }
});
//  the language changer
document.addEventListener("DOMContentLoaded", function () {
    const langSelector = document.getElementById("lang");

    if (langSelector) {
        langSelector.addEventListener("change", function () {
            document.getElementById("languageForm").submit();
        });
    }
});
document.addEventListener("DOMContentLoaded", function () {
    // Select all forms with the class "form"
    const forms = document.querySelectorAll(".form");
    const errorListContainer = document.getElementsByClassName('errorList')[0]; // Access the first element

    forms.forEach(form => {
        form.addEventListener("submit", function (e) {
            e.preventDefault(); // Prevent the form from submitting normally

            // Create a new FormData object
            const formData = new FormData(form);

            // Send the form data via AJAX
            fetch(form.action, {
                method: form.method,
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest", // Indicate this is an AJAX request
                    "X-CSRFToken": formData.get("csrfmiddlewaretoken"), // Include CSRF token
                },
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Handle successful form submission with SweetAlert2
                        Swal.fire({
                            icon: 'success',
                            title: 'Success!',
                            text: data.message || 'Form submitted successfully!',
                            confirmButtonText: 'OK',
                        }).then(() => {
                            form.reset(); // Reset the form

                            // Redirect if needed
                            if (data.redirect_url) {
                                window.location.href = data.redirect_url;
                            }
                        });
                    } else {
                        // Handle form submission failure

                        if (errorListContainer) {
                            errorListContainer.classList.add('w-100')
                            errorListContainer.innerHTML = ""; // Clear previous errors
                            Object.keys(data.errors).forEach(errorKey => {
                                const errorItem = document.createElement('li');
                                errorItem.className = 'alert alert-danger';
                                errorItem.setAttribute('role', 'alert');
                                errorItem.innerText = data.errors[errorKey];
                                errorListContainer.appendChild(errorItem);
                            });
                        }
                    }
                })

        });
    });
});
//  a function to handle the item deletion
document.addEventListener("DOMContentLoaded", function () {
    // Select all delete buttons or forms
    const deleteButtons = document.querySelectorAll(".delete-button");

    deleteButtons.forEach(button => {
        button.addEventListener("click", function (e) {
            e.preventDefault(); // Prevent the default action

            // Confirm deletion with SweetAlert2
            Swal.fire({
                title: 'Are you sure?',
                text: 'You will not be able to recover this item!',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Yes, delete it!',
                cancelButtonText: 'No, cancel!',
            }).then((result) => {
                if (result.isConfirmed) {
                    // Send the deletion request via AJAX
                    fetch(button.dataset.deleteUrl, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': button.dataset.csrfToken,
                            'X-Requested-With': 'XMLHttpRequest',
                        },
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                // Show success message
                                Swal.fire({
                                    icon: 'success',
                                    title: 'Deleted!',
                                    text: data.message,
                                    confirmButtonText: 'OK',
                                }).then(() => {
                                    // Reload the page or update the UI
                                    window.location.reload();
                                });
                            } else {
                                // Show error message
                                Swal.fire({
                                    icon: 'error',
                                    title: 'Error!',
                                    text: data.message || 'An error occurred.',
                                    confirmButtonText: 'OK',
                                });
                            }
                        })
                        .catch(error => {
                            console.error("Error:", error);
                            Swal.fire({
                                icon: 'error',
                                title: 'Error!',
                                text: 'An unexpected error occurred.',
                                confirmButtonText: 'OK',
                            });
                        });
                }
            });
        });
    });
});
// A function to handle image upload 
document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('id_thumbnail');
    const preview = document.getElementById('thumbnail_preview');

    if (fileInput || preview) {
        fileInput.addEventListener('change', function (event) {
            if (event.target.files && event.target.files[0]) {
                const reader = new FileReader();

                reader.onload = function (e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block'; // Show the image preview
                };

                reader.readAsDataURL(event.target.files[0]);
            }
        });

    }
});
// function to handle adding item to cart
document.addEventListener('DOMContentLoaded', function () {
    // Select all "Add to Cart" buttons
    const addToCartButtons = document.querySelectorAll('.add-to-cart');

    if (addToCartButtons) {
        // Add click event listener to each button
        addToCartButtons.forEach(button => {
            button.addEventListener('click', function (event) {
                event.preventDefault(); // Prevent the default form submission

                // Get the product ID from the data attribute
                const productId = button.getAttribute('data-product-id');

                // Send an AJAX request to add the product to the cart
                fetch(`/cart/add/${productId}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token for security
                    },
                    body: JSON.stringify({
                        quantity: 1, // Default quantity (can be dynamic if needed)
                    }),
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // Optionally, update the cart icon or total items in the cart
                            const ordersCountElement = document.getElementById('orders_count');
                            if (ordersCountElement) {
                                const currentCount = parseInt(ordersCountElement.textContent) || 0;
                                ordersCountElement.textContent = currentCount + 1; // Increment the count
                            }


                        } else {
                            alert('Failed to add product to cart.'); // Show error message
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('An error occurred while adding the product to the cart.');
                    });
            });
        });

    }

    // Function to get the CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
// Mobile menu toggle
const mobileMenu = document.getElementById('mobile-menu');
const navMenu = document.querySelector('.nav-menu');

if (mobileMenu && navMenu) {
    mobileMenu.addEventListener('click', () => {
        mobileMenu.classList.toggle('active');
        navMenu.classList.toggle('active');
    });
}