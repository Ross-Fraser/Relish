// Fetch Stripe public key and client secret from the template
var stripePublicKey = JSON.parse(document.getElementById('id_stripe_public_key').textContent);
var clientSecret = JSON.parse(document.getElementById('id_client_secret').textContent);
// Initialize Stripe with the public key
var stripe = Stripe(stripePublicKey);
// Create an instance of Elements
var elements = stripe.elements();
// Custom styling for the card element
var style = {
    base: {
        color: '#000',
        fontFamily: 'Chantal Bold Italic, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '15px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
// Create an instance of the card Element
var card = elements.create('card', {style: style, hidePostalCode: true});
// Mount the card Element into the `#card-element` div
var cardElement = document.getElementById('card-element');
if (cardElement) {
    card.mount('#card-element');
} else {
    console.error('Card element not found');
}
// Handle form submission
var form = document.getElementById('payment-form');
form.addEventListener('submit', function(event) {
    event.preventDefault();
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }
    }).then(function(result) {
        if (result.error) {
            // Show error in the card-errors element
            var errorElement = document.getElementById('card-errors');
            errorElement.textContent = result.error.message;
        } else {
            // Payment succeeded, submit the form
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});