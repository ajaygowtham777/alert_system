from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'psg.alert.system@gmail.com'
app.config['MAIL_PASSWORD'] = 'xiho gqle fdub abay'

mail = Mail(app)

@app.route('/check', methods=['POST'])
def check_values():
    try:
        data = request.json
        print("Received data:", data)  # Debug print
        
        if not data:
            raise ValueError("No JSON data provided")
        
        if 'temperature' not in data or 'vibration' not in data:
            raise KeyError("Missing 'temperature' or 'vibration' key in request data")
        
        temperature = float(data['temperature'])  # Convert to float
        vibration = float(data['vibration'])      # Convert to float
        print(f"Temperature: {temperature}, Vibration: {vibration}")  # Debug print
        
        current = (temperature + vibration) * 0.1  # Example formula for current
        alert_message = None

        if temperature > 30:
            alert_message = f"Alert: High Temperature ({temperature}°C)!"
        elif vibration > 20:
            alert_message = f"Alert: High Vibration Rate ({vibration} units)!"

        if alert_message:
            try:
                msg = Message('Machine Alert', sender='psg.alert.system@gmail.com', recipients=[data.get('email')])
                msg.body = alert_message
                mail.send(msg)
            except Exception as e:
                print("Error sending email:", str(e))  # Debug print
                return jsonify({"error": "Failed to send email", "details": str(e)}), 500

        return jsonify({"current": current, "alert": alert_message}), 200

    except ValueError as ve:
        print("ValueError:", str(ve))  # Debug print
        return jsonify({"error": "Invalid data type", "details": str(ve)}), 400
    except KeyError as ke:
        print("KeyError:", str(ke))  # Debug print
        return jsonify({"error": "Missing required field", "details": str(ke)}), 400
    except Exception as e:
        print("General Exception:", str(e))  # Debug print
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
