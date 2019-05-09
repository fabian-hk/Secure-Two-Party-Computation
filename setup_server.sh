mkdir .server ||	echo "folder is already available" 
#cp -r cbmc_parser/ .server/ 
cp -r exceptions/ .server/
cp -r fpre/ .server/
cp -r protobuf/ .server/ 
#test has to be deleted
cp -r tests/ .server/ 
cp -r tools/ .server/ 
cp MPC.py .server/
cp Server.py .server/
cp TwoPartyComputation.py .server/ 

cp -r certificates_server/ .server/certificates

cp Dockerfile_server .server/Dockerfile
cp conf_server.py .server/conf.py
cd .server/
docker build -t server .
cd ..
rm -r .server/
