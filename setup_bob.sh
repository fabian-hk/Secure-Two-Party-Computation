mkdir .bob > /dev/null ||	echo "folder is already available"  > /dev/null

cp -r certificates_bob .bob/certificates

cp Dockerfile_bob .bob/Dockerfile
cp conf_bob.py .bob/conf.py
cp function.c .bob/function.c


cd .bob/
docker build -t bob  . 
cd ..
rm -r .bob/
