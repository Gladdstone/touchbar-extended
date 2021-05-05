import json
import os
import shutil
import sys
import tempfile

def display_function(plugin_file):
    utility_import = r"""source ${0:A:h}/functions.zsh
        source ${0:A:h}/utility.zsh"""

    definition = r'function display() {'

    initial_state_clear = r"""if [[ $state != "" ]]; then clear_touchbar; fi
        remove_and_unbind_keys;
        state="";"""
    
    plugin_file.write(
        utility_import +
        definition +
        initial_state_clear
    )

    for i, key in enumerate(json_config['default']):
        key_value = str(i + 1)
        key_text = key[key_value]['text']
        function_name = key[key_value]['command']
        build_key(plugin_file, key_value, key_text, function_name)

    function_termination = r'}'

    plugin_file.write(function_termination)

def build_key(file, value, text, func):
    key_command = ('set_key %s "%s" "%s"' % (value, text, func))
    file.write(key_command)

print('Executing will clear any customizations made to the touchbar-extended plugins directory.')
confirm = input('Confirm? [y/n] ')

if(confirm.lower() != 'y' and 
    confirm.lower() != 'yes'):
    shutil.rmtree(tmpdir)
    sys.exit(0)

zsh_path = os.path.join(os.environ['ZSH'], 'plugins')

# get zsh path and generate plugin directory
if(os.path.exists(zsh_path)):
    zsh_path = os.path.join(zsh_path, 'touchbar-extended')
    if(os.path.exists(zsh_path)):
        for filename in os.listdir(zsh_path):
            file_path = os.path.join(zsh_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                else:
                    shutil.rmtree(file_path)
            except Exception as err:
                shutil.rmtree(tmpdir)
                sys.exit('Unable to remove %s: %s' % (file_path, e))
    else:
        try:
            os.makedirs(zsh_path)
        except Exception as err:
            shutil.rmtree(tmpdir)
            sys.exit('Unable to generate plugin directory: %s', err)
else:
    sys.exit('Unable to locate plugins directory, please check $ZSH path')

with open('config.json') as config:
    json_config = json.load(config)

tmpdir = tempfile.mkdtemp()
plugin_path = os.path.join(tmpdir, 'touchbar-extended.plugin.zsh')
plugin_file = open(plugin_path, 'w+')

display_function(plugin_file)

plugin_file.close()

if(os.path.exists(zsh_path) and 
    os.path.isdir(zsh_path)):
    # support file management
    function_copy_from_path = os.path.join('scripts', 'functions.zsh')
    function_copy_to_path = os.path.join(zsh_path, 'functions.zsh')
    utility_copy_from_path = os.path.join('scripts', 'utility.zsh')
    utility_copy_to_path = os.path.join(zsh_path, 'utility.zsh')

    shutil.copyfile(function_copy_from_path, function_copy_to_path)
    shutil.copyfile(utility_copy_from_path, utility_copy_to_path)

    # copy final plugin file
    plugin_copy_path = os.path.join(zsh_path, 'touchbar-extended.plugin.zsh')
    shutil.copyfile(plugin_path, plugin_copy_path)

shutil.rmtree(tmpdir) # cleanup
print('Plugin generation complete. Please reload your terminal.')
