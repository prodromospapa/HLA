arlecore=arlecore_linux/arlecore3522_64bit

file=$1
if [ "$2" = "HL" ]; then
    settingsFile=arlecore_linux/h_l.ars
elif [ "$2" = "AMOVA" ]; then
    settingsFile=arlecore_linux/amova.ars
fi

echo "Processing file $file"

./$arlecore $file $settingsFile

rm -f arl_run.txt
rm -f arlequin.ini