from django.shortcuts import render, redirect, get_object_or_404
from .forms import PaymentForm
from store.models import Product
import requests

def initiate_payment(request, product_id):
    # Get the product details
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Extract data from the form (e.g., customer email, amount)
            amount = form.cleaned_data['amount']
            email = form.cleaned_data['email']
            
            # Generate payment link from Flutterwave
            payment_link = generate_payment_link(product, amount, email)
            
            # Redirect user to the payment gateway
            return redirect(payment_link)
    else:
        form = PaymentForm()
    
    return render(request, 'payments/initiate_payment.html', {'form': form, 'product': product})

def payment_success(request):
    # Handle success page logic here
    return render(request, 'payments/payment_success.html')

def payment_failed(request):
    # Handle failure page logic here
    return render(request, 'payments/payment_failed.html')

def generate_payment_link(product, amount, email):
    # Replace with your actual Flutterwave secret key and other details
    FLUTTERWAVE_SECRET_KEY = 'your_flutterwave_secret_key'
    headers = {
        'Authorization': f'Bearer {FLUTTERWAVE_SECRET_KEY}',
        'Content-Type': 'application/json',
    }
    
    # Define the payment request data
    data = {
        'tx_ref': f'order_{product.id}_{int(time.time())}',
        'amount': amount,
        'currency': 'NGN',
        'email': email,
        'phone_number': '08012345678',
        'redirect_url': 'http://127.0.0.1:8000/payment-success/',  # Redirect URL after payment
    }
    
    # Send a request to Flutterwave API to create payment link
    response = requests.post('https://api.flutterwave.com/v3/charges?type=mobilemoneyghana', json=data, headers=headers)
    
    if response.status_code == 200:
        response_data = response.json()
        if response_data['status'] == 'success':
            return response_data['data']['link']  # Payment link to redirect to
        else:
            return redirect('payment_failed')  # Redirect to failure page
    else:
        return redirect('payment_failed')  # Redirect to failure page
