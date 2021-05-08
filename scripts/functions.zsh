git_status() {
  local ref
  ref=$(command git status 2> /dev/null)
  local ret=$?
  if [[ $ret != 0 ]]; then
    return
  fi

  echo ${ref}
}

git_current_branch() {
  local ref
  ref=$(command git symbolic-ref --quiet HEAD 2> /dev/null)
  local ret=$?
  if [[ $ret != 0 ]]; then
    return
  fi

  echo ${ref}
}

zshconfig() {
  source ~/.zshrc
}
