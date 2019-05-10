#!/bin/bash


## functions
server () {
	echo "server"
	mkdir .server ||    echo "folder is already available"
	cp -r exceptions/ .server/
	cp -r fpre/ .server/
	cp -r protobuf/ .server/ 
	cp -r tests/ .server/ 
	cp -r tools/ .server/ 
	cp MPC.py .server/
	cp Server.py .server/
	cp TwoPartyComputation.py .server/ 
	cp -r data/certificates_server/ .server/certificates
	cp docker/Dockerfile_server .server/Dockerfile
	cp conf/conf_server.py .server/conf.py
	cd .server/
	docker build -t server .
	cd ..
	rm -r .server/
	clear
	echo "Docker container built"
	docker run --net=host server python3 Server.py $@
}

client () {
	echo "client"
	mkdir .client_base ||   echo "folder is already available"
	cp -r cbmc_parser/ .client_base/
	cp -r exceptions/ .client_base/
	cp -r fpre/ .client_base/
	cp -r protobuf/ .client_base/
	cp -r tests/ .client_base/
	cp -r tools/ .client_base/
	cp MPC.py .client_base/
	cp TwoPartyComputation.py .client_base/
	mkdir -p .client_base/CBMC-GC-2/bin/
	cp data/CBMC-GC-2/bin/cbmc-gc .client_base/CBMC-GC-2/bin/cbmc-gc
	cp docker/Dockerfile_client_base .client_base/Dockerfile
	cd .client_base/
	docker build -t client_base  . 
	cd ..
	rm -r .client_base/
	clear
	echo "client built"
}

alice () {
	echo "alice"
	mkdir .alice  > /dev/null ||    echo "folder is already available"  > /dev/null	
	cp -r certificates_alice .alice/certificates
	cp docker/Dockerfile_alice .alice/Dockerfile
	cp conf/conf_alice.py .alice/conf.py
	cp function.c .alice/function.c
	cd .alice/
	docker build -t alice .
	cd ..
	rm -r .alice/
	clear 
	echo "Alice built"
	docker run --net=host alice python3 TwoPartyComputation.py $@
		
}
bob () {
	echo "bob"
	mkdir .bob > /dev/null ||   echo "folder is already available"  > /dev/null 
	cp -r data/certificates_bob .bob/certificates
	cp docker/Dockerfile_bob .bob/Dockerfile
	cp conf/conf_bob.py .bob/conf.py
	cp function.c .bob/function.c
	cd .bob/
	docker build -t bob  . 
	cd ..
	rm -r .bob/
	clear 
	echo "Bob built"
	docker run --net=host bob python3 TwoPartyComputation.py $@
}


## Main
if [[ "$1" == "Server" ]] || [[ "$1" == "server" ]] || [[ "$1" == "s" ]] ;  then
	echo "Server is chosen"
	shift
	server "$@"
elif [[ "$1" == "Alice" ]] || [[ "$1" == "alice" ]] || [[ "$1" == "a" ]] ;  then
	echo "Alice is chosen"
	shift
	client
	alice "$@"
elif [[ "$1" == "Bob" ]] || [[ "$1" == "bob" ]] || [[ "$1" == "b" ]] ;  then
	echo "Bob is chosen"
	shift
	client
	bob "$@"
fi
