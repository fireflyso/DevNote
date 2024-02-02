IFS=$'\n'
for file in `ls`
do
        newfile=`echo $file | sed 's/.V2.WEB-DL.4k.H265.DDP.AAC-Xiaomi//g'`
        echo $newfile
        mv $file $newfile
done