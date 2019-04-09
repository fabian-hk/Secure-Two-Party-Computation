mkdir .bob > /dev/null ||	echo "folder is already available"  > /dev/null
#cp -r cbmc_parser/ .bob/ 
#cp -r exceptions/ .bob/
#cp -r fpre/ .bob/
#cp -r protobuf/ .bob/ 
##test has to be deleted
#cp -r tests/ .bob/ 
#cp -r tools/ .bob/ 
#cp MPC.py .bob/
#cp Server.py .bob/
#cp TwoPartyComputation.py .bob/ 
#cp ~/Downloads/CBMC-GC-2/bin/cbmc .bob/

cp -r ~/Downloads/certificates .bob/

cp Dockerfile_bob .bob/Dockerfile
cp conf_bob.py .bob/conf.py
cp function.o .bob/function.o


cd .bob/
docker build -t bob . 
cd ..
rm -r .bob/
