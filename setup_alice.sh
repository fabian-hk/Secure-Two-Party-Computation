mkdir .alice  > /dev/null ||	echo "folder is already available"  > /dev/null
#cp -r cbmc_parser/ .alice/ 
#cp -r exceptions/ .alice/
#cp -r fpre/ .alice/
#cp -r protobuf/ .alice/ 
##test has to be deleted
#cp -r tests/ .alice/ 
#cp -r tools/ .alice/ 
#cp MPC.py .alice/
#cp Server.py .alice/
#cp TwoPartyComputation.py .alice/ 
#cp ~/Downloads/CBMC-GC-2/bin/cbmc .alice/

cp -r ~/Downloads/certificates .alice/

#copy important stuff
cp Dockerfile_alice .alice/Dockerfile
cp conf_alice.py .alice/conf.py
cp function.c .alice/function.c

cd .alice/
docker build -t alice .
cd ..
rm -r .alice/
