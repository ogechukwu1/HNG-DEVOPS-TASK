from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Helper functions
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    divisors = [i for i in range(1, n) if n % i == 0]
    return sum(divisors) == n

def is_armstrong(n):
    digits = [int(i) for i in str(n)]
    power_sum = sum([digit ** len(digits) for digit in digits])
    return power_sum == n

def get_digit_sum(n):
    return sum([int(digit) for digit in str(n)])

def get_fun_fact(n):
    # Fetch fun fact using Numbers API
    response = requests.get(f"http://numbersapi.com/{n}?json")
    if response.status_code == 200:
        return response.json().get("text", "No fun fact available.")
    return "No fun fact available."

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    # Get the 'number' parameter from query string
    number_str = request.args.get('number')
    
    # Input validation
    try:
        number = int(number_str)
    except ValueError:
        return jsonify({"number": number_str, "error": True}), 400

    # Check if number is prime, perfect, Armstrong, odd, or even
    prime = is_prime(number)
    perfect = is_perfect(number)
    armstrong = is_armstrong(number)
    odd_or_even = "odd" if number % 2 != 0 else "even"
    digit_sum = get_digit_sum(number)
    fun_fact = get_fun_fact(number)

    # Determine the properties
    properties = []
    if armstrong:
        properties.append("armstrong")
    if odd_or_even == "odd":
        properties.append("odd")
    else:
        properties.append("even")

    # Build the response JSON
    response = {
        "number": number,
        "is_prime": prime,
        "is_perfect": perfect,
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
