for den in 0.4; do 
for temp in 0.7 0.8 1.0 1.2 1.4 1.6 1.8 2.0; do 
cd T-${temp}-D-${den}-1; 
#python ../fit_fft_density_results.py $temp $den density-real; wait; 
python ../fit_fft_density_results.py $temp $den density-imag; wait;
echo $temp $den; 
cd ..; 
done; done
