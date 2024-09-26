import os
import logging
from flask import Flask, jsonify, request

app = Flask(__name__)

log_file_path = '/var/log/app.log'

if not os.path.exists('/var/log/'):
    print("/var/log/ directory does not exist. App will not start.")
    exit(1)

logging.basicConfig(filename=log_file_path, level=logging.INFO, 
                    format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger()

stored_product = None

@app.route('/v1/product', methods=['POST', 'GET'])
def handle_product():
    global stored_product

    if request.method == 'POST':
        if not request.is_json:
            logger.error("Invalid request: No JSON data")
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        product = data.get("product")

        if not product:
            logger.error("Invalid request: No product in JSON data")
            return jsonify({"error": "Product field is required"}), 400

        stored_product = product
        logger.info(f"Product received and stored: {product}")
        return jsonify({"product": product})

    elif request.method == 'GET':
        if stored_product is None:
            return jsonify({"error": "No product found"}), 404
        logger.info(f"Product retrieved: {stored_product}")
        return jsonify({"product": stored_product})

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    response = jsonify({"status": "OK"})
    logger.info("/healthcheck endpoint accessed")
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
