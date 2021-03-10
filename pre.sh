path0=`pwd`
cd rmrb/7z
path=`pwd`
ls $path | while read line
do
	7z e $line -o$path0'/rmrb7z'/${line%.*}
done

