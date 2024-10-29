import subprocess
import time
import smtplib
import socket
from email.mime.text import MIMEText
import urllib.request
import netifaces

# Configuration
script_name = 'lora_sender_tss2.py'
email_address = 'lorasensorone@gmail.com'  # Your Gmail address
email_password = 'zzwa bngy hjgs quju'  # Your Gmail App Password

def get_internal_ip_address():
    """Get the internal IP address of the machine by checking network interfaces."""
    try:
        interfaces = netifaces.interfaces()
        for interface in interfaces:
            if netifaces.AF_INET in netifaces.ifaddresses(interface):
                ip_info = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]
                ip_address = ip_info['addr']
                if ip_address != "127.0.0.1":  # Ignore localhost
                    return ip_address
        return "Unknown Internal IP"
    except Exception as e:
        print(f"Error getting internal IP address: {e}")
        return "Unknown Internal IP"

def get_external_ip_address():
    """Get the external IP address of the machine."""
    try:
        external_ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
        return external_ip
    except Exception as e:
        print(f"Error getting external IP address: {e}")
        return "Unknown External IP"

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
        body = f"{script_name} has been manually killed.\nInternal IP: {get_internal_ip_address()}\nExternal IP: {get_external_ip_address()}"
        send_email(subject, body)
    except Exception as e:
        print(f"Error killing script: {e}")

if __name__ == "__main__":
    # Send an email right after starting the script
    internal_ip = get_internal_ip_address()
    external_ip = get_external_ip_address()
    subject = "Monitoring Script Started"
    body = f"The monitoring script has started.\nInternal IP: {internal_ip}\nExternal IP: {external_ip}"
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
        
        # Sleep for a specified interval before checking again
        time.sleep(5)  # Check every 5 seconds
