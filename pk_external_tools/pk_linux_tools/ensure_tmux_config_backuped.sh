mkdir -p $D_PK_DATA
filename=.tmux.conf
f_backup=$D_PK_DATA/$filename.bak.$(date +%Y%m%d_%H%M%S)
cp ~/$filename $f_backup
echo $f_backup
f_backup=$D_PK_DATA/$filename.bak
cp ~/$filename $f_backup
echo $f_backup


