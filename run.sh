#!/bin/bash 
#======================================================================================
#
#		   FILE:	run.sh
#		
#		  USAGE:	run.sh [-s] [-a] [-b] [--server] [--alice] [--bob]
#
#	DESCRPITION:	Execute TwoPartyComputation, as Server or Client.
#
# 		OPTIONS:	see function 'usage' below
#  REQUIREMENTS:	docker
#======================================================================================
usage () {
	cat <<-EOF
	usage: $0 [-h] [-s [-n]]
	usage: $0 [-a FUNCTION INPUT... -cn NAME -s SERVER_IP -p PORT]
	usage: $0 [-b FUNCTION INPUT... -cn NAME -s SERVER_IP -p PORT]
	usage: $0 [-a FUNCTION INPUT... -n]
	usage: $0 [-b FUNCTION INPUT... -n]
	
	-h | --help 		print this help
	-s | --server		start Server
	-a | --alice		start Alice
	-b | --bob		start Bob
	-cn			specify common name you want to talk to
	-n			no certificates
	EOF
}


server () {
	echo "server"
	mkdir -p .server 
	mkdir .server/conf
	mkdir .server/data
	cp -r exceptions/ .server/
	cp -r fpre/ .server/
	cp -r protobuf/ .server/ 
	cp -r tests/ .server/ 
	cp -r tools/ .server/ 
	cp MPC.py .server/
	cp Server.py .server/
	cp TwoPartyComputation.py .server/ 
	cp -r data/certificates_server/ .server/data/certificates
	cp docker/Dockerfile_server .server/Dockerfile
	cp conf/conf.py .server/conf/conf.py
	cp conf/cert_conf_server.py .server/conf/cert_conf.py
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
	mkdir -p .client_base/data/CBMC-GC-2/bin
	cp -r cbmc_parser/ .client_base/
	cp -r exceptions/ .client_base/
	cp -r fpre/ .client_base/
	cp -r protobuf/ .client_base/
	cp -r tests/ .client_base/
	cp -r tools/ .client_base/
	cp MPC.py .client_base/
	cp TwoPartyComputation.py .client_base/
	mkdir -p .client_base/CBMC-GC-2/bin/
	cp data/CBMC-GC-2/bin/cbmc-gc .client_base/data/CBMC-GC-2/bin/cbmc-gc
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
	mkdir -p .alice  
	mkdir .alice/conf
	mkdir .alice/data
	cp -r data/certificates_alice .alice/data/certificates
	cp docker/Dockerfile_alice .alice/Dockerfile
	cp conf/conf.py .alice/conf/conf.py
	cp conf/cert_conf_alice.py .alice/conf/cert_conf.py
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
	mkdir -p .bob 
	mkdir .bob/conf
	mkdir .bob/data
	cp -r data/certificates_bob .bob/data/certificates
	cp docker/Dockerfile_bob .bob/Dockerfile
	cp conf/conf.py .bob/conf/conf.py
	cp conf/cert_conf_bob.py .bob/conf/cert_conf.py
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
case "$1" in
	--server | -s)
		shift
		server "$@"
		;;
	--alice | -a)
		shift
		client
		alice "$@"
		;;
	--bob | -b)
		shift
		client
		bob "$@"
		;;
	--help | -h)
		usage
		;;
	*)
		usage
esac
