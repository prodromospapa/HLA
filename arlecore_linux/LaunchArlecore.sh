arlecore=arlecore_linux/arlecore3522_64bit

file=$1

if [ ! -f $file ]; then
    echo "File $file does not exist"
    exit 1
fi
echo "Processing file $file"

settingsFile=arlecore_linux/popgen.ars
./$arlecore $file $settingsFile

rm -f arl_run.txt
rm -f arlequin.ini
rm -f arl_pro.txt
rm -f arl_run.ars
rm -f randseed.txt