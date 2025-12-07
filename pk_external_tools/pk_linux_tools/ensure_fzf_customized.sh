# from apt
sudo apt-get install -y fzf


# from git
# git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
# ~/.fzf/install


# pk fzf 
# export FZF_DEFAULT_OPTS='--height 40% --layout=reverse --border --color fg:#bbccdd,fg+:#ddeeff,bg:#334455,preview-bg:#223344,border:#778899'
# export FZF_DEFAULT_OPTS="--height 40% --layout reverse --info inline --border \
#     --preview 'file {}' --preview-window up,1,border-horizontal \
#     --bind 'ctrl-/:change-preview-window(50%|hidden|)' \
#     --color 'fg:#bbccdd,fg+:#ddeeff,bg:#334455,preview-bg:#223344,border:#778899'"
export FZF_DEFAULT_OPTS="--height 40% \
--layout=reverse \
--border \
--bind 'ctrl-/:change-preview-window(50%|hidden|)' \
--preview '[[ -d {} ]] && exa -T --color=always {} | head -100 || (bat --style=numbers --color=always --line-range :200 {} 2>/dev/null || cat {} 2>/dev/null | head -100)' \
"

export FZF_DEFAULT_COMMAND=’fd — type f’


# nvim $(fzf)

