conda activate uav-analysis-env


ifile_imet=$(zenity --file-selection \
       --title "Select imet file" \
       --filename "${PWD}/")

python plot_uav_data.py $ifile_imet