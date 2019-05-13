function server () {
	echo "server"
	mkdir .server ||    echo "folder is already available"
	mkdir .server/conf
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
	cp conf/conf.py .server/conf/conf.py
	cp conf/cert_conf.py .server/conf/cert_conf.py
	cd .server/
	docker build -t server .
	cd ..
	rm -r .server/
	clear
	echo "Docker container built"
	docker run --net=host server python3 Server.py $@
}

function client () {
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

function alice () {
	echo "alice"
	mkdir .alice  > /dev/null ||    echo "folder is already available"  > /dev/null
	mkdir .alice/conf
	cp -r data/certificates_alice .alice/certificates
	cp docker/Dockerfile_alice .alice/Dockerfile
	cp conf/conf_alice.py .alice/conf/conf.py
	cp function.c .alice/function.c
	cd .alice/
	docker build -t alice .
	cd ..
	rm -r .alice/
	clear 
	echo "Alice built"
	docker run --net=host alice python3 TwoPartyComputation.py $@
		
}
function bob () {
	echo "bob"
	mkdir .bob > /dev/null ||   echo "folder is already available"  > /dev/null
	mkdir .bob/conf
	cp -r data/certificates_bob .bob/certificates
	cp docker/Dockerfile_bob .bob/Dockerfile
	cp conf/conf_bob.py .bob/conf/conf.py
	cp function.c .bob/function.c
	cd .bob/
	docker build -t bob  . 
	cd ..
	rm -r .bob/
	clear 
	echo "Bob built"
	docker run --net=host bob python3 TwoPartyComputation.py $@
}


switch ($Args[0]) {
	-s {server($args[1])}
	-a {client; alice($args[1])}
	-b {client; bob($args[1])}
}
