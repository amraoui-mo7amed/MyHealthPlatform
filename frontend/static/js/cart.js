document.addEventListener('DOMContentLoaded', function () {
    // Function to update the cart summary
    function updateCartSummary() {
        // Get all cart items
        const cartItems = document.querySelectorAll('.d-flex.align-items-center.justify-content-between.mb-3');

        let totalProducts = 0;
        let subtotal = 0;

        // Loop through each cart item
        cartItems.forEach(item => {
            // Get the quantity and price of the current item
            const quantityInput = item.querySelector('input[name="quantity"]');
            let quantity = parseInt(quantityInput.value);

            // Ensure quantity is >= 0
            if (quantity < 0) {
                quantity = 0; // Reset to 0 if the value is negative
                quantityInput.value = 0; // Update the input field
            }

            const price = parseFloat(item.querySelector('.item_price').textContent.replace(' DZD', ''));

            // Update total products and subtotal
            totalProducts += quantity;
            subtotal += quantity * price;
        });

        // Calculate shipping (example: 200 DZD for simplicity)
        const shipping = 20;

        // Calculate total amount
        const totalAmount = subtotal + shipping;

        // Update the DOM with the calculated values
        document.getElementById('products_count').textContent = totalProducts;
        document.getElementById('subtotal_count').textContent = `${subtotal.toFixed(2)} DZD`;
        document.getElementById('shipping_price').textContent = `${shipping.toFixed(2)} DZD`;
        document.getElementById('total_amount').textContent = `${totalAmount.toFixed(2)} DZD`;
    }

    // Call the function to update the cart summary when the page loads
    updateCartSummary();

    // Add event listeners to quantity inputs to update the cart summary when the quantity changes
    const quantityInputs = document.querySelectorAll('input[name="quantity"]');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function () {
            // Ensure quantity is >= 0
            if (input.value <= 0) {
                input.value = 1; // Reset to 0 if the value is negative
            }
            updateCartSummary();
        });
    });

});