# Enables colors on the CLI
#export CLICOLOR=1

# List aliases
alias la="ls -A"
alias ll="ls -l"
alias ltr="ls -ltr"
alias ls="ls -F"

# Mac Specific Aliases
if [[ $(uname) == "Darwin" ]]; then
    alias safari="open -a Safari"
    alias chrome="open -a Google\ Chrome"
    test -e /Applications/Sublime\ Text.app/ && alias sublime="open -a $_"
fi

# List functions
function cdl { cd "$1" && ls; }

# Overwrites default prompt, not including user signed in as
PS1="\h:\W\$ "

# If bash-completion script is present from homebrew installation, use it.
test -f /usr/local/etc/bash_completion ] && source $_

# If git-completion script is present from github pull, use it.
test -f ~/.git-completion.bash && source $_
# More concise way of stating the following:
# "if [ -f ~/.git-completion.bash ]; then
#     . ~/.git-completion.bash
# fi`
# Git completion script can be found at:`
# https://github.com/git/git/blob/master/contrib/completion/git-completion.bash
# Note: Git completion functionality also installed as part of bash-completion
