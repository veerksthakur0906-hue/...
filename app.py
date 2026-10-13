from flask import Flask, render_template, request, jsonify
import requests
import json
import uuid

app = Flask(__name__)

# ==========================================
# CONFIGURATION
# ==========================================
PAYTM_MID = "YOUR_PAYTM_MERCHANT_ID_HERE"
PAYTM_KEY = "YOUR_PAYTM_SECRET_KEY_HERE"

# गूगल ड्राइव का मुख्य फोल्डर लिंक
DRIVE_FOLDER_URL = "https://drive.google.com/drive/folders/14cTkVYJvICcEM_FohFN_7ofUr2cf1Iaw?usp=sharing"

# तेरे 10 प्रोडक्ट्स की लिस्ट, नाम और प्राइस
PRODUCTS = {
    "neon_custom_text": {"name": "Neon Custom Text Generator", "price": "200.00"},
    "ai_prompt_generator": {"name": "AI Prompt Generator", "price": "100.00"},
    "neon_arcade_runner": {"name": "Neon Arcade Runner", "price": "0.00"},
    "ai_teacher_pro": {"name": "AI Teacher Pro", "price": "100.00"},
    "pc_hand_gesture": {"name": "PC Hand Gesture Control", "price": "100.00"},
    "friday_ai_bot": {"name": "Friday AI Developer Bot", "price": "150.00"},
    "voice_assistant_bot": {"name": "Voice Assistant Desktop Bot", "price": "100.00"},
    "local_ai_pack": {"name": "Custom Local AI Model Pack", "price": "200.00"},
    "jewelry_template": {"name": "Luxury Jewellery Web Template", "price": "250.00"},
    "dental_template": {"name": "Dental Clinic Website Template", "price": "250.00"}
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create-qr', methods=['POST'])
def create_qr():
    data = request.json
    product_id = data.get('product_id')
    
    if product_id not in PRODUCTS:
        return jsonify({"status": "ERROR", "message": "Invalid Product"}), 400
        
    product = PRODUCTS[product_id]
    
    # अगर प्रोडक्ट फ्री (₹0) है, तो सीधे ड्राइव लिंक दे दो
    if float(product['price']) == 0:
        return jsonify({
            "status": "SUCCESS",
            "free": True,
            "download_url": DRIVE_FOLDER_URL
        })
    
    order_id = f"ORDER_{uuid.uuid4().hex[:8].upper()}"
    
    return jsonify({
        "status": "SUCCESS",
        "free": False,
        "order_id": order_id,
        "amount": product['price'],
        "qr_data": f"upi://pay?pa={PAYTM_MID}@paytm&pn=NeonStore&am={product['price']}&tr={order_id}"
    })

@app.route('/check-status', methods=['POST'])
def check_status():
    data = request.json
    order_id = data.get('order_id')
    
    return jsonify({
        "status": "SUCCESS",
        "paid": True,
        "download_url": DRIVE_FOLDER_URL
    })

if __name__ == '__main__':
    app.run(debug=True)