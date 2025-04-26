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


class AIChat {
    constructor() {
        this.chatCircle = document.getElementById('aiChatCircle');
        this.chatContainer = document.getElementById('chatContainer');
        this.closeChatBtn = document.getElementById('closeChatBtn');
        this.sendMessageBtn = document.getElementById('sendMessageBtn');
        this.userInput = document.getElementById('userInput');
        this.chatMessages = document.getElementById('chatMessages');
        this.isChatOpen = false;
        this.apiKey = null;
        this.hasShownWelcome = false;

        if (this.chatCircle) {
            this.initializeEventListeners();
        }
        this.getApiToken();
    }

    async getApiToken() {
        try {
            const response = await fetch('/api/chat-token/');
            const data = await response.json();
            if (data.token) {
                this.apiKey = data.token;
            }
        } catch (error) {
            console.error('Error fetching API token:', error);
        }
    }

    initializeEventListeners() {
        this.chatCircle.addEventListener('click', () => this.toggleChat());
        this.closeChatBtn.addEventListener('click', () => this.toggleChat());
        this.sendMessageBtn.addEventListener('click', () => this.sendMessage());
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
    }

    toggleChat() {
        this.isChatOpen = !this.isChatOpen;
        this.chatContainer.style.display = this.isChatOpen ? 'flex' : 'none';

        // Show welcome message if this is the first time opening
        if (this.isChatOpen && !this.hasShownWelcome) {
            this.showWelcomeMessage();
            this.hasShownWelcome = true;
        }
    }

    showWelcomeMessage() {
        const welcomeMessage = `Hi, how can I assist you today?`;

        const formattedWelcome = marked.parse(welcomeMessage, {
            breaks: true,
            sanitize: true
        });
        this.addMessage(formattedWelcome, false);
    }

    addMessage(text, isUser = true) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', isUser ? 'user-message' : 'ai-message');
        if (isUser) {
            messageDiv.textContent = text;
        } else {
            messageDiv.innerHTML = text;
        }
        this.chatMessages.appendChild(messageDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    async sendMessage() {
        const message = this.userInput.value.trim();
        if (!message || !this.apiKey) return;

        // Add user message immediately
        this.addMessage(message, true);
        this.userInput.value = '';

        // Add loading message with dancing dots
        const loadingMessage = this.createLoadingMessage();
        this.chatMessages.appendChild(loadingMessage);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;

        try {
            const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.apiKey}`,
                },
                body: JSON.stringify({
                    model: 'deepseek/deepseek-chat-v3-0324:free',
                    messages: [
                        {
                            role: 'system',
                            content: `you are a dietitian, your name is Boo. Here are your core instructions:

                            1. You are a specialized health and diet assistant
                            2. Only answer questions related to:
                               - Diet and nutrition
                               - Healthy eating habits
                               - Meal planning
                               - Food-related health concerns
                               - Dietary restrictions and requirements
                            3. For any questions outside your expertise, politely respond with: "I apologize, but I can only assist with diet and nutrition-related questions. Please consult with appropriate healthcare professionals for other medical concerns."
                            4. Keep responses focused on scientifically-backed dietary information
                            5. Always encourage users to consult with healthcare providers for specific medical advice
                            6. answer briefly except if user want explanation`
                        },
                        {
                            role: 'user',
                            content: message
                        }
                    ]
                })
            });

            const data = await response.json();
            const aiResponse = data.choices[0].message.content;
            const formattedResponse = marked.parse(aiResponse, {
                breaks: true,
                sanitize: true
            });

            // Remove loading message and add AI response
            this.chatMessages.removeChild(loadingMessage);
            this.addMessage(formattedResponse, false);
        } catch (error) {
            console.error('Error:', error);
            // Remove loading message and show error
            this.chatMessages.removeChild(loadingMessage);
            this.addMessage('Sorry, I encountered an error. Please try again.', false);
        }
    }

    createLoadingMessage() {
        const loadingDiv = document.createElement('div');
        loadingDiv.classList.add('message', 'ai-message');

        const dotContainer = document.createElement('div');
        dotContainer.classList.add('dot-container');

        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('div');
            dot.classList.add('dot');
            dot.style.animationDelay = `${i * 0.2}s`;
            dotContainer.appendChild(dot);
        }

        loadingDiv.appendChild(dotContainer);
        return loadingDiv;
    }
}

// Initialize the chat when the document is ready
document.addEventListener('DOMContentLoaded', () => {
    new AIChat();
});