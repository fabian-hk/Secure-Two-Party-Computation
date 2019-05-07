mkdir .client_base ||	echo "folder is already available" 
cp -r cbmc_parser/ .client_base/ 
cp -r exceptions/ .client_base/
cp -r fpre/ .client_base/
cp -r protobuf/ .client_base/ 
#test has to be deleted
cp -r tests/ .client_base/ 
cp -r tools/ .client_base/ 
cp MPC.py .client_base/
#cp Server.py .client_base/
cp TwoPartyComputation.py .client_base/ 
mkdir -p .client_base/CBMC-GC-2/bin/
cp CBMC-GC-2/bin/cbmc-gc .client_base/CBMC-GC-2/bin/cbmc-gc
cp function.c .client_base/function.c
#cp -r ~/Downloads/certificates .client_base/

cp Dockerfile_client_base .client_base/Dockerfile

cd .client_base/
docker build -t client_base  . 
cd ..
rm -r .client_base/
