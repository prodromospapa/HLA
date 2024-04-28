arlecore=arlecore_linux/arlecore3522_64bit

file=$1
if [ "$2" = "HL" ]; then
    settingsFile=arlecore_linux/h_l.ars
elif [ "$2" = "FST" ]; then
    settingsFile=arlecore_linux/fst.ars
fi

echo "Processing file $file"

./$arlecore $file $settingsFile
