import subprocess
import time
import smtplib
import socket
import urllib.request
from email.mime.text import MIMEText
from datetime import datetime

# Configuration
script_name = 'lora_sender_tss3.py'
email_address = 'lorasensorone@gmail.com'  # Your Gmail address
email_password = 'xxxx xxxx xxxx xxxx'  # Your Gmail App Password
log_file = '/home/sensor/watcher_log.txt'  # Log file path
log_interval = 120  # Interval for emailing the log in seconds (2 minutes)

last_log_sent_time = time.time()

def log_message(message):
    """Log a message to both the log file and console."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} - {message}\n"
    print(log_entry.strip())
    with open(log_file, 'a') as f:
        f.write(log_entry)
#
#   The email and log parts are just a sketch for now, and will be properly implemented
#   at the next stage of the project
#   
#   
#
def get_internal_ip():
    """Get the internal IP address."""
    return socket.gethostbyname(socket.gethostname())

def get_external_ip():
    """Get the external IP address."""
    try:
        with urllib.request.urlopen('https://api.ipify.org') as response:
            return response.read().decode('utf-8')
    except Exception as e:
        log_message(f"Error getting external IP: {e}")
        return "Unavailable"

def send_email(subject, body):
    """Send an email notification with the log file."""
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = email_address
        msg['To'] = email_address

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(email_address, email_password)
            server.sendmail(email_address, email_address, msg.as_string())
        log_message(f"Email sent with subject: {subject}")
    except Exception as e:
        log_message(f"Error sending email: {e}")

def send_log_via_email():
    """Send the log file content via email every log_interval seconds."""
    global last_log_sent_time
    if time.time() - last_log_sent_time >= log_interval:
        internal_ip = get_internal_ip()
        external_ip = get_external_ip()
        with open(log_file, 'r') as f:
            log_content = f.read()
        email_body = f"Internal IP: {internal_ip}\nExternal IP: {external_ip}\n\nLog Content:\n{log_content}"
        send_email("LoRa Monitoring Log", email_body)
        last_log_sent_time = time.time()

def is_script_running(script_name):
    """Check if the script is running."""
    try:
        result = subprocess.run(['pgrep', '-f', script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return len(result.stdout) > 0
    except Exception as e:
        log_message(f"Error checking if script is running: {e}")
        return False

def restart_script(script_name):
    """Restart the script."""
    try:
        subprocess.Popen(['python3', script_name])
        log_message(f"Restarted {script_name}")
    except Exception as e:
        log_message(f"Error restarting script: {e}")

if __name__ == "__main__":
    # Log initial information and send an email on start
    log_message("Monitoring script started.")
    send_email("Monitoring Script Started", "The watcher script has started monitoring.")

    while True:
        # Check if the script is running
        if not is_script_running(script_name):
            log_message(f"{script_name} is not running. Restarting...")
            restart_script(script_name)
            send_email(f"{script_name} Restarted", f"{script_name} was not running and has been restarted.")
        else:
            log_message(f"{script_name} is running.")

        # Send log via email every 2 minutes
        send_log_via_email()

        time.sleep(5)  # Check every 5 seconds
