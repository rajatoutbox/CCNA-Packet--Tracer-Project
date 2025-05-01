import os
import yaml

# Path to input config file
input_file = r"C:\Users\RajatSingh\Downloads\full_config.txt"
output_file = os.path.expanduser(r"C:\Users\RajatSingh\Downloads\playbook.yml")

def parse_device_configs(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    device_configs = {}
    current_device = None
    current_config = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('!DEVICE:'):
            if current_device and current_config:
                device_configs[current_device] = current_config
                current_config = []
            current_device = stripped.split(':', 1)[1].strip().lower()
        elif stripped == '!':
            if current_device and current_config:
                device_configs[current_device] = current_config
                current_device = None
                current_config = []
        elif current_device:
            current_config.append(stripped)

    return device_configs

def build_ansible_playbook(device_configs):
    playbook = []
    for device, config_lines in device_configs.items():
        play = {
            'name': f'Configure {device.upper()}',
            'hosts': device,
            'gather_facts': False,
            'connection': 'network_cli',
            'tasks': [
                {
                    'name': f'Push config to {device.upper()}',
                    'ios_config': {
                        'lines': config_lines
                    }
                }
            ]
        }
        playbook.append(play)
    return playbook

def main():
    device_configs = parse_device_configs(input_file)
    playbook = build_ansible_playbook(device_configs)
    
    with open(output_file, 'w') as f:
        yaml.dump(playbook, f, sort_keys=False)

    print(f"✅ Ansible playbook written to: {output_file}")

if __name__ == '__main__':
    main()
