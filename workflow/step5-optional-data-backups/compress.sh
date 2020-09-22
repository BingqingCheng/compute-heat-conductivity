mkdir compressed-results

cp * compressed-results
cp -r input-template compressed-results

for a in T*-D-0.*-*; do 
cd $a; 
mkdir ../compressed-results/$a
cp autocorr* fft* fit* heatflux.dat kgrid.dat lmplog in.df ../compressed-results/$a 
cd ..; done
