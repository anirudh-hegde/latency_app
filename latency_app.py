from flask import Flask, render_template_string, jsonify, request
import time
import random
import logging

app = Flask(__name__)


logging.basicConfig(level=logging.INFO)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Latency Demo</title>
    <style>
        body { font-family: sans-serif; margin: 20px; background-color: #f4f4f4; color: #333; }
        .container { background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        button {
            background-color: #007bff; color: white; padding: 10px 15px;
            border: none; border-radius: 5px; cursor: pointer; font-size: 16px;
        }
        button:hover { background-color: #0056b3; }
        #result { margin-top: 20px; padding: 10px; border: 1px solid #ddd; background-color: #e9e9e9; border-radius: 5px;}
        .loader {
            border: 5px solid #f3f3f3; /* Light grey */
            border-top: 5px solid #3498db; /* Blue */
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            display: none; /* Hidden by default */
            margin-top: 10px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Simulate Backend Latency</h1>
        <p>Click the button below. The server will intentionally delay its response.</p>
        <button id="latencyButton">Trigger Latency</button>
        <div class="loader" id="loader"></div>
        <div id="result">Click the button to see the response.</div>
    </div>

    <script>
        const button = document.getElementById('latencyButton');
        const resultDiv = document.getElementById('result');
        const loader = document.getElementById('loader');

        button.addEventListener('click', async () => {
            resultDiv.textContent = 'Request sent, waiting for server response...';
            loader.style.display = 'block'; // Show loader
            button.disabled = true; // Disable button during request

            const startTime = Date.now();

            try {
                // Make a POST request (or GET, depends on your preference for such actions)
                const response = await fetch('/simulate_latency', {
                    method: 'POST', // Using POST as it's an action
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    // body: JSON.stringify({ data: "some_payload" }) // Optional payload
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                const endTime = Date.now();
                const duration = ((endTime - startTime) / 1000).toFixed(2); // in seconds

                resultDiv.innerHTML = `<strong>Server responded:</strong> ${data.message}<br>`

            } catch (error) {
                resultDiv.textContent = `Error: ${error.message}`;
                app.logger.error(`Frontend error: ${error.message}`);
            } finally {
                loader.style.display = 'none'; // Hide loader
                button.disabled = false; // Re-enable button
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/simulate_latency', methods=['POST'])
def simulate_latency():
    delay_seconds = 15
    app.logger.info(f"Received request for /simulate_latency. Intentionally delaying for {delay_seconds:.2f} seconds.")

    time.sleep(delay_seconds)

    app.logger.info(f"Finished delay. Sending response.")
    return jsonify({
        "message": f"Processed successfully after a {delay_seconds:.2f} second delay!",
        "simulated_delay_seconds": round(delay_seconds, 2)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5005) 
