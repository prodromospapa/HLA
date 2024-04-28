arlecore=arlecore_linux/arlecore3522_64bit

file=$1
permutation=$2
if [ "$3" = "HL" ]; then
    python3 ars_file.py -t HL -p $permutation
elif [ "$3" = "AMOVA" ]; then
    python3 ars_file.py -t AMOVA -p $permutation
fi

settingsFile=arlecore_linux/output.ars

echo "Processing file $file"

./$arlecore $file $settingsFile

rm -f arl_run.txt
rm -f arlequin.ini
rm -f arl_pro.txt
rm -f arl_run.ars
rm -f randseed.txt