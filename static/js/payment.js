const checkoutButton = document.getElementById('pay-with-flutterwave');

checkoutButton.addEventListener('click', async () => {
  const paymentData = {
    public_key: 'YOUR_FLUTTERWAVE_PUBLIC_KEY',
    customer: {
      email: 'customer@example.com', // Replace with user's email
      phonenumber: '2348012345678', // Replace with user's phone number (optional)
      name: 'Customer Name', // Replace with user's name (optional)
    },
    customizations: {
      title: 'Payment for Quiz',
      description: 'Payment before writing a quiz',
      logo: 'https://assets.piedpiper.com/logo.png', // Optional logo URL
    },
    callback: async (response) => {
      // Handle successful or failed payment response here
      console.log('Transaction reference:', response.transaction_id);
      console.log('Status:', response.status);

      // Send the response.transaction_id to your server for verification
      const verifyUrl = '/payments/verify/'; // Replace with your verification endpoint

      const response = await fetch(verifyUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          transaction_id: response.transaction_id,
        }),
      });

      const verificationData = await response.json();
      console.log('Verification response:', verificationData);

      // Update UI based on verification result
    },
    meta: {
      user_id: 123, // Replace with actual user ID from your application
    },
    payment_options: 'card, mobilemoney, banktransfer', // Optional payment methods to allow (default: all)
    amount: {{ total_price }}, // Replace with dynamic total price from your app
    currency: 'NGN',
  };

  const flw = new FlutterwaveCheckout(paymentData);
  flw.showPaymentModal();
});