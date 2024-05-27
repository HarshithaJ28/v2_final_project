from flask import Flask, render_template, Response, jsonify, request
import subprocess
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
from datetime import datetime

app = Flask(__name__)

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.IN)
GPIO.setup(11, GPIO.OUT)

DHT_PIN = 4
DHT_SENSOR = Adafruit_DHT.DHT11

request_data_list = []

# Function to read sensor data
def get_sensor_reading():  
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    humidity_val = 30
    temperature_val = 30
    if humidity is not None and temperature is not None:
        humidity_val = humidity
        temperature_val = temperature
        print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity))
    else:
        print("Sensor failure. Check wiring.")
    return (temperature_val, humidity_val)

# Home page route
@app.route("/")
def hello_world():
    # Log request data
    curtime = datetime.now()
    datetimestring = curtime.strftime("[%Y/%m/%d %H:%M:%S]")
    requestdata = f"{request.remote_addr} - - {datetimestring}  \"{request.method} {request.path} HTTP/{request.environ['SERVER_PROTOCOL']}"
    request_data_list.append(requestdata)
    print(request_data_list)
    return render_template("index.html")

# Server Sent Events (SSE) route for streaming request data
@app.route('/stream')
def stream():
    def generate():
        # Loop indefinitely to send new request data
        while True:
            if request_data_list:
                # Pop the oldest request data from the list
                data = request_data_list.pop(0)
                yield f"data: {data}\n\n"  # SSE format
            time.sleep(1)  # Adjust the interval as needed
    return Response(generate(), mimetype='text/event-stream')

# Route to fetch sensor readings
@app.route("/sensorReadings")
def get_sensor_readings():
    temperature, humidity = get_sensor_reading()
    return jsonify(
        {
            "status": "OK",
            "temperature": temperature,
            "humidity": humidity,
        }
    )

# Route to handle fetching IP address
@app.route("/fetchip", methods=['POST'])
def fetchip():
    try:
        data = request.json
        if data and 'ip' in data:
            ip_address = data['ip']
            print("Received IP address:", ip_address)
            # Toggle buzzer and run script
            toggle_buzzer("on")
            script_path = "/home/hp/Desktop/project/script.sh"
            subprocess.run([script_path, ip_address])
            # Render template with IP address
            return render_template("attack.html", ip_address=ip_address)
        else:
            raise ValueError("Invalid JSON data or missing 'ip' key")
    except Exception as e:
        print("Error:", e)
        return "An error occurred", 500  # Return an error response

# Route to control buzzer
@app.route("/buzzer/<status>")
def buzzer_status(status):
    if status == "on":
        toggle_buzzer("on")
    elif status == "off":
        toggle_buzzer("off")
    return "Buzzer"

# Function to toggle buzzer
def toggle_buzzer(status):
    num_beeps = 5
    interval = 1
    if status == "on":
        for _ in range(num_beeps):
            print("Buzzer on")
            GPIO.output(11, GPIO.HIGH)
            time.sleep(0.5)
        print("Buzzer off")
        GPIO.output(11, GPIO.LOW)
        time.sleep(0.1)  
    elif status == "off":
        print("Buzzer off")
        GPIO.output(11, GPIO.LOW)

# Main function
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
