

for f in $(find data/XQ2/raw -type f -name "*.csv" ) ; do
  python plot_xq2_data.py $f

  done

