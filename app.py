from flask import Flask, render_template, request, jsonify
import random, razorpay
import os

RAZORPAY_KEY = os.getenv("RAZORPAY_KEY")
RAZORPAY_SECRET = os.getenv("RAZORPAY_SECRET")

client = razorpay.Client(auth=(RAZORPAY_KEY, RAZORPAY_SECRET))
client.set_app_details({"title": "Test Pay", "version": "1.0"})

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', razorpay_key = RAZORPAY_KEY)

@app.route('/process_payment', methods=['POST'])
def process_payment():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        amount = int(request.form.get('amount')) * 100  
        
        receipt_id = f"receipt_{random.randint(1000, 9999)}"
        
        order = client.order.create({
            "amount": amount,  
            "currency": "INR",
            "receipt": receipt_id,
            "payment_capture": 1 
        })
        return jsonify({
            "order_id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"],
            "status": order["status"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/receipt')
def receipt():
    name = request.args.get('name')
    email = request.args.get('email')
    amount = request.args.get('amount')
    transaction_id = request.args.get('transaction_id')
    order_id = request.args.get('order_id')

    return render_template(
        'receipt.html', 
        name=name, email=email, 
        amount=amount, 
        transaction_id=transaction_id, 
        order_id=order_id
        )


if __name__ == '__main__':
    app.run(debug=True)
