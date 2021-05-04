git_status() {
  local ref
  ref=$(command git status &> /dev/null)
  local ret=$?
  if [[ $ret != 0 ]]; then
    return
  fi

  echo ${ref}
}

git_current_branch() {
  local ref
  ref=$(command git symbolic-ref --quiet HEAD &> /dev/null)
  local ret=$?
  if [[ $ret != 0 ]]; then
    return
  fi

  echo ${ref}
}

