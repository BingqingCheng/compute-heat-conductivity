for d in 0.2 0.4 0.6 0.8; do 
for t in 1.0 0.8 0.7; do 
cd T-$t-D-$d-1/; 

for sys in jx-real jx-imag jy-real jy-imag; do
	paste kgrid.dat autocorrtime-$sys.dat | tail -n +2 | awk '{if($1*$2+$2*$3+$1*$3==0){print ($1*$1+$2*$2+$3*$3),$1,$2,$3, (1./($8*0.0025*20*($1**2.+$2**2.+$3**2.)))}}' > fit-autocorr-nu-$sys.dat
wait
done 

cat fit-autocorr-nu-*.dat | awk 'NF==5{print $5}' | autocorr -maxlag 1 | head -n 1 | awk -v d=$d -v t=$t '{print d,t,"nu", $2,"nu_error", $6}'
cd .. 
done
done
