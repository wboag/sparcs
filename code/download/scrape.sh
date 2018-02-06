for i in {1..1000} ; do 
    curl "https://ace.iime.cloud/static/files/csv/SPARCS_${i}_2015.csv" > SPARCS_${i}_2015.csv
    mv SPARCS_${i}_2015.csv ../../data
done
