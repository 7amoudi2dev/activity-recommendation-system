from flask import Flask, render_template_string
import socket
import getpass

app = Flask(__name__)

SYSTEM_INFO = {
    'username': getpass.getuser(),
    'machine_name': socket.gethostname()
}

HTML_TEMPLATE = '''<!DOCTYPE html>
<html>
<head>
    <title>Activity Recommendation Client</title>
</head>
<body>
    <div class="container">
        <h1>Activity Recommendation System</h1>
        
        <form id="activityForm">
            <div class="form-group">
                <label for="client_name">Client Name</label>
                <input type="text" id="client_name" name="client_name" required placeholder="Enter your name">
            </div>
            <div class="form-group">
                <label for="birth_date">Birth Date</label>
                <input type="date" id="birth_date" name="birth_date" required>
            </div>
            <div class="form-group">
                <label for="temperature">Temperature (°C)</label>
                <input type="number" id="temperature" name="temperature" step="0.1" required placeholder="e.g., 25.5">
            </div>
            <button type="submit" id="submitBtn">Get Activity Recommendation</button>
        </form>

        <div id="result"></div>
    </div>

    <script>
        const API_BASE_URL = 'http://localhost:5002/api';

        // Submit form
        document.getElementById('activityForm').addEventListener('submit', function(e) {
            e.preventDefault();

            const submitBtn = document.getElementById('submitBtn');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Processing...';

            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);

            fetch(`${API_BASE_URL}/activity`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            })
            .then(response => {
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return response.json();
            })
            .then(result => {
                if (result.error) {
                    document.getElementById('result').innerHTML = 
                        `<div class="result error">
                            <p class="error">Error: ${result.error}</p>
                        </div>`;
                } else {
                    document.getElementById('result').innerHTML = 
                        `<div class="result success">
                            <h3 class="success">✓ Recommendation: ${result.activity}</h3>
                            <p>For temperature: ${result.temperature}°C</p>
                            <p><em>${result.message}</em></p>
                        </div>`;

                    // Clear form
                    document.getElementById('client_name').value = '';
                    document.getElementById('birth_date').value = '';
                    document.getElementById('temperature').value = '';
                }
            })
            .catch(err => {
                document.getElementById('result').innerHTML = 
                    `<div class="result error">
                        <p class="error">Failed to get recommendation.<br>
                        Error: ${err.message}</p>
                    </div>`;
            })
            .finally(() => {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Get Activity Recommendation';
            });
        });
    </script>
</body>
</html>'''


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE,
                                  username=SYSTEM_INFO['username'],
                                  machine_name=SYSTEM_INFO['machine_name'])

if __name__ == '__main__':
    app.run(port=5003, debug=True)