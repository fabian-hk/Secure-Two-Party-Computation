mkdir .alice  > /dev/null ||	echo "folder is already available"  > /dev/null

cp -r certificates_bob .alice/

#copy important stuff
cp Dockerfile_alice .alice/Dockerfile
cp conf_alice.py .alice/conf.py
cp function.c .alice/function.c

cd .alice/
docker build -t alice .
cd ..
rm -r .alice/
