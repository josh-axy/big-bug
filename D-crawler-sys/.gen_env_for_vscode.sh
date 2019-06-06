source env.sh

array=`python .gen_env_for_vscode.py`

# target file
target=.env
# clear the file
: > $target
for v in ${array[@]}
do
    tmp=$`echo $v`
    eval echo "$v=$tmp" >> $target
done
