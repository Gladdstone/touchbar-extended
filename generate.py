import json
import os
import shutil
import sys
import tempfile

def display_function(plugin_file):
    utility_import = ('source ${0:A:h}/functions.zsh\n' 
        'source ${0:A:h}/utility.zsh\n\n')

    function_display = ('function display() {\n'
        '\tif [[ $state != "" ]]; then\n'
        '\t\tclear_touchbar;\n'
        '\tfi\n'
        '\tremove_and_unbind_keys\n'
        '\tstate=""\n')
    
    plugin_file.write(
        utility_import +
        function_display
    )

    for i, key in enumerate(json_config['default']):
        key_value = str(i + 1)
        key_text = key[key_value]['text']
        function_name = key[key_value]['command']
        build_key(plugin_file, key_value, key_text, function_name)

    function_display_termination = '}\n\n'

    function_precmd = ('precmd_touchbar_extended() {\n'
        '\tdisplay\n'
        '}\n\n')

    zsh_hook = ('autoload -Uz add-zsh-hook\n'
        'add-zsh-hook precmd precmd_touchbar_extended\n')

    plugin_file.write(
        function_display_termination +
        function_precmd +
        zsh_hook
    )

def build_key(file, value, text, func):
    key_command = ('\tset_key %s "%s" %s\n' % (value, text, func))
    file.write(key_command)

def load_plugin(zsh_path, plugin_path):
    if(os.path.exists(zsh_path) and 
        os.path.isdir(zsh_path)):
        # support file management
        function_copy_from_path = os.path.join('scripts', 'functions.zsh')
        function_copy_to_path = os.path.join(zsh_path, 'functions.zsh')
        utility_copy_from_path = os.path.join('scripts', 'utility.zsh')
        utility_copy_to_path = os.path.join(zsh_path, 'utility.zsh')
        try:
            shutil.copyfile(function_copy_from_path, function_copy_to_path)
            shutil.copyfile(utility_copy_from_path, utility_copy_to_path)

            # copy final plugin file
            plugin_copy_path = os.path.join(zsh_path, 'touchbar-extended.plugin.zsh')
            shutil.copyfile(plugin_path, plugin_copy_path)
        except Exception as err:
            clean_exit()

def clean_exit(exit_message: str = ''):
    shutil.rmtree(tmpdir)
    if len(exit_message) < 1:
        sys.exit(0)
    sys.exit(exit_message)

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

# testing purposes
# try:
#     shutil.copyfile(plugin_path, './touchbar-extended.plugin.zsh')
# except Exception as err:
#     clean_exit("Unable to copy file to test location")

load_plugin(zsh_path, plugin_path)

print('Plugin generation complete. Please reload your terminal.')
clean_exit()
