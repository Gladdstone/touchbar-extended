# generate a zsh file
# remove and unbind
# read config
# set keys
# add zsh hook
# generate plugin file, move into flugin directory
# ask user to reload their terminal

import json
import tempfile

json_config = None
with open('config.json') as config:
    json_config = json.loads(config)

tmpdir = tempfile.mkdtemp()
plugin_file = open('tmp/touchbar_extended.plugin.zsh', 'w+')

def display_function(plugin_file):
    definition = r'function display() {'
    initial_state_clear = r"""if [[ $state != "" ]]; then clear_touchbar; fi
        remove_and_unbind_keys;
        state="";"""
    
    plugin_file.write(
        definition +
        initial_state_clear
    )

    for key in json_config['default']:
        key_value = key
        key_text = json_config['default'][key]['text']
        function_name = json_config['default'][key]['command']
        build_key(file, key_value, key_text, function_name)

    function_termination = r'}'

    plugin_file.write(function_termination)

def build_key(file, value, text, func):
    key_command = f'set_key {key} "{key_text}" "{function_name}"'
    file.write(key_command)
