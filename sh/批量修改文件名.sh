IFS=$'\n'
for file in `ls|grep .mp4`
do
        newfile=`echo $file | sed 's/将夜2第/将夜2--第/g'`
        echo $newfile
        mv $file $newfile
done