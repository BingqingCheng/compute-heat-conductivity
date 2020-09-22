cp * $proj/df-hydrodynamics

for a in T*-D-0.4-*; do 
cd $a; 
mkdir trajectories
mv df.lammpstrj-part* trajectories 
mkdir $proj/df-hydrodynamics/$a
cp *  $proj/df-hydrodynamics/$a 
#tar -cf $a-results.tar $a-results 
cd ..; done
