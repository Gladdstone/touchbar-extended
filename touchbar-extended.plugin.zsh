source ${0:A:h}/functions.zsh
source ${0:A:h}/utility.zsh

function display() {
    if [[ $state != "" ]]; then
        clear_touchbar
    fi
    remove_and_unbind_keys
    state=""

    set_key 1 "🎋 `git_current_branch`" git_current_branch '-q'
    set_key 2 "status" "git status"
}

precmd_touchbar_extended() {
    display
}

autoload -Uz add-zsh-hook
add-zsh-hook precmd precmd_touchbar_extended
