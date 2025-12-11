"""Main file to run on Raspberry Pi.

Sets up a flask server, receives data from Pico, and creates a polar graph based on data.
"""
from flask import Flask, request, jsonify
import json
import threading
import time
import graph

app = Flask(__name__)

stop_flag = False
# Thread lock for safe data access
data_lock = threading.Lock()

# Global Data Storage
data_to_send_to_pico = [10, 20, 30] # This is part of a defunct use of the file.
# This variable holds the last data received from the Pico.
last_data_from_pico = {}

# RPI to Pico Communication (The Server/Get Endpoint)
@app.route('/get_rpi_data', methods=['GET'])
def get_rpi_data():
    """Get data to send to Pico.

    This function is currently defunct.
    """
    global data_to_send_to_pico
    print(f"Pico requested data. Sending: {data_to_send_to_pico}")
    
    # Use the lock to read shared data
    with data_lock:
        data_to_send = data_to_send_to_pico
        
    return jsonify({"rpi_data": data_to_send}), 200

# RPI Control Endpoint (Sending data from an RPI App)
@app.route('/send_data', methods=['POST'])
def send_data_to_pico():
    """Sends data to pico.

    Currently defunct.
    
    Returns:
        json: Status message.
    """
    global data_to_send_to_pico
    try:
        content = request.json
        if 'new_data' in content and isinstance(content['new_data'], list):
            # Use the lock to write shared data
            with data_lock:
                data_to_send_to_pico = content['new_data']
            print(f"Data updated by RPI app: {data_to_send_to_pico}")
            return jsonify({"status": "success", "message": "Data updated"}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid format. Expected {'new_data': list}"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Pico to RPI Communication (The Server/Post Endpoint)
@app.route('/pico_data', methods=['POST'])
def receive_pico_data():
    """Receives data from Pico.

    Receives pico payload and updates last_data_from_pico accordingly.
    
    Returns:
        json: Status message.
    """
    global last_data_from_pico
    try:
        pico_payload = request.json
        
        # Use the lock to write shared data
        with data_lock:
            last_data_from_pico = pico_payload
            print('recieved', len(last_data_from_pico['sensor data']), 'points')
        
        return jsonify({"status": "received"}), 200
    except Exception as e:
        print(f"Error processing Pico data: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

def main_plotting_loop():
    """Continuously plots data on the main thread.
    """
    global last_data_from_pico
    print("\n--- Starting Plotting Loop on Main Thread ---")
    while not stop_flag:
        # Use the lock to read shared data
        with data_lock:
            # Extract the actual sensor data list
            points_to_plot = last_data_from_pico.get("sensor data")

        if points_to_plot:
            try:
                # The plotting function must be called in the main thread
                graph.update_plot_from_list(points_to_plot)
            except Exception as e:
                print(f"Plotting error: {e}")
    
        time.sleep(0.1) # Check for new data 10 times per second

if __name__ == '__main__':
    try:
        # Start the Flask server in a SEPARATE thread, so the main thread is free for plotting
        print("\n--- Starting Flask Server in background thread ---\n")
        server_thread = threading.Thread(target=app.run, kwargs={'host': '10.133.0.147', 'port': 5000}, daemon=True)
        server_thread.start()

        # Run the plotting loop in the MAIN thread
        main_plotting_loop()

    except KeyboardInterrupt:
        print("\nStopping application.")

    finally:
        # Set the stop flag to shut down the threads
        stop_flag = True
        if 'server_thread' in locals() and server_thread.is_alive():
             # Flask thread may not join easily, but setting stop_flag is enough for cleanup
             pass
