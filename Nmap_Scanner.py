import PySimpleGUI as sg
import subprocess
import threading

# Function to run Nmap scan and update output in window
def run_nmap(target_ip, nmap_command, port, output_elem):
    # Construct the Nmap command
    nmap_cmd = f'nmap -Pn {nmap_command} {target_ip} -p {port}'

    # Run the Nmap command and update the output window
    try:
        process = subprocess.Popen(nmap_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in iter(process.stdout.readline, ''):
            output_elem.print(line.strip())
        process.stdout.close()
        process.wait()
    except subprocess.CalledProcessError as e:
        output_elem.print(f"Error running Nmap: {e.stderr}")

# Define layout for the GUI window
layout = [
    [sg.Text('Enter Target IP:'), sg.InputText(key='-TARGET_IP-')],
    [sg.Text('Select Nmap Command:'), sg.Combo(['-sS', '-sV', '-sS -sV', '-sU', '-sS -sV -vv', '-A -T4 -sS -sV -vv', '--script ssl-cert', '--script ssl-enum-ciphers', '--script ssl-dh-params', '--script ssl-poodle', '--script http-headers', '--script http-security-headers', '--script http-slowloris-check', '--script rtsp-url-brute'], key='-NMAP_COMMAND-', enable_events=True)],
    [sg.Text('Port/Port Range:'), sg.InputText(key='-PORT-')],
    [sg.Button('Run Scan'), sg.Button('Exit')],
    [sg.Text('Note: By default this tool disables ping scan i.e., it uses (-Pn) in background.')],
    [sg.Multiline(size=(80, 20), key='-OUTPUT-', autoscroll=True)]
]

# Create the GUI window
window = sg.Window('Nmap Scanner By Srikanth Rudrarapu', layout)

# Event loop to process events and get user input
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
    elif event == 'Run Scan':
        target_ip = values['-TARGET_IP-']
        nmap_command = values['-NMAP_COMMAND-'] if '-NMAP_COMMAND-' in values else values['-NMAP_COMMAND-0']
        port = values['-PORT-']
        output_elem = window['-OUTPUT-']

        # Clear previous output
        output_elem.update('')

        # Create a separate thread to run the Nmap scan
        threading.Thread(target=run_nmap, args=(target_ip, nmap_command, port, output_elem), daemon=True).start()

window.close()
