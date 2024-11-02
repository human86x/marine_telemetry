import subprocess
import time
import smtplib
import socket
import requests
from email.mime.text import MIMEText

# Configuration
script_name = 'lora_rec3.py'
email_address = 'lorasensorone@gmail.com'  # Your Gmail address
email_password = 'zzwa bngy hjgs quju'  # Your Gmail App Password
mosquitto_service_name = 'mosquitto'  # Name of the Mosquitto service

def get_ip_addresses():
    """Get both the internal and external IP addresses of the machine."""
    try:
        # Internal IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(('8.8.8.8', 80))
        internal_ip = s.getsockname()[0]
        s.close()
    except Exception as e:
        print(f"Error getting internal IP address: {e}")
        internal_ip = "Unknown Internal IP"

    try:
        # External IP address using an external service
        external_ip = requests.get('https://api.ipify.org').text
    except Exception as e:
        print(f"Error getting external IP address: {e}")
        external_ip = "Unknown External IP"

    return internal_ip, external_ip

def is_script_running(script_name):
    """Check if the script is running."""
    try:
        result = subprocess.run(['pgrep', '-f', script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return len(result.stdout) > 0
    except Exception as e:
        print(f"Error checking if script is running: {e}")
        return False

def restart_script(script_name):
    """Restart the script."""
    try:
        subprocess.Popen(['python3', script_name])
        print(f"Restarted {script_name}")
    except Exception as e:
        print(f"Error restarting script: {e}")

def send_email(subject, body):
    """Send an email notification."""
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = email_address
        msg['To'] = email_address

        # Connect to Gmail's SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.set_debuglevel(1)  # Enable debug output for troubleshooting
            server.login(email_address, email_password)  # Login using your email and password
            server.sendmail(email_address, email_address, msg.as_string())  # Send email
            print(f"Email sent to {email_address}")
    except Exception as e:
        print(f"Error sending email: {e}")

def kill_script(script_name):
    """Kill the running script."""
    try:
        subprocess.run(['pkill', '-f', script_name])
        print(f"Killed {script_name}")
        subject = f"{script_name} Killed"
        internal_ip, external_ip = get_ip_addresses()
        body = f"{script_name} has been manually killed.\nInternal IP: {internal_ip}\nExternal IP: {external_ip}"
        send_email(subject, body)
    except Exception as e:
        print(f"Error killing script: {e}")

def is_mosquitto_running():
    """Check if the Mosquitto service is running."""
    try:
        result = subprocess.run(['systemctl', 'is-active', mosquitto_service_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode().strip() == 'active'
    except Exception as e:
        print(f"Error checking Mosquitto service status: {e}")
        return False

def restart_mosquitto():
    """Restart the Mosquitto service."""
    try:
        subprocess.run(['sudo', 'systemctl', 'restart', mosquitto_service_name])
        print(f"Restarted {mosquitto_service_name} service")
        subject = f"{mosquitto_service_name} Service Restarted"
        internal_ip, external_ip = get_ip_addresses()
        body = f"The {mosquitto_service_name} service has been restarted.\nInternal IP: {internal_ip}\nExternal IP: {external_ip}"
        send_email(subject, body)
    except Exception as e:
        print(f"Error restarting Mosquitto service: {e}")

if __name__ == "__main__":
    # Send an email right after starting the script
    internal_ip, external_ip = get_ip_addresses()
    subject = "Monitoring Script for lora_rec3.py Started"
    body = f"The monitoring script for {script_name} has started.\nInternal IP: {internal_ip}\nExternal IP: {external_ip}"
    send_email(subject, body)

    while True:
        # Check if the script is running
        if not is_script_running(script_name):
            print(f"{script_name} is not running. Restarting...")
            restart_script(script_name)
            # Send email notification
            subject = f"{script_name} Restarted"
            body = f"{script_name} was not running and has been restarted.\nInternal IP: {internal_ip}\nExternal IP: {external_ip}"
            send_email(subject, body)
        else:
            print(f"{script_name} is running.")
        
        # Check if the Mosquitto service is running
        if not is_mosquitto_running():
            print(f"{mosquitto_service_name} service is not running. Restarting...")
            restart_mosquitto()

        # Sleep for a specified interval before checking again
        time.sleep(5)  # Check every 5 seconds
