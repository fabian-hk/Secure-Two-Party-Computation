GOTO serverorclient

:serverorclient
	set _all=%*
	call set _tail=%%_all:*%2=%%
	set _tail=%2%_tail%
	IF "%1" == "-s" GOTO server
	IF "%1" == "--server" GOTO server
	IF "%1" == "-a" GOTO client
	IF "%1" == "--alice" GOTO client
	IF "%1" == "-b" GOTO client
	IF "%1" == "--bob" GOTO client
:who
	IF "%1" == "-a"  GOTO alice
	IF "%1" == "--alice" GOTO alice
	IF "%1" == "-b" GOTO bob
	IF "%1" == "--bob" GOTO bob
	exit

:server
	echo "server"
	mkdir server\
	mkdir server\conf
	mkdir server\fpre
	mkdir server\protobuf
	mkdir server\tests
	mkdir server\tools
	mkdir server\data
	robocopy exceptions server\exceptions /s
	robocopy fpre server\fpre /s
	robocopy protobuf server\protobuf /s
	robocopy tests server \tests /s
	robocopy tools server\tools /s
	copy MPC.py server
	copy Server.py server
	copy TwoPartyComputation.py server\ 
	robocopy data\certificates_server server\data\certificates /s
	copy docker\Dockerfile_server server\Dockerfile
	copy conf\conf.py server\conf\conf.py
	copy conf\cert_conf_server.py server\conf\cert_conf.py
	cd server\
	docker build --no-cache -t server .
	cd ..
	rmdir .server\ /s/q
	echo "Docker container built"
	shift
	docker run --net=host server python3 Server.py %_tail%
	exit

:client
	echo "client"
	mkdir client_base
	mkdir client_base\
	mkdir client_base\data
	mkdir client_base\cbmc_parser
	mkdir client_base\exceptions
	mkdir client_base\fpre
	mkdir client_base\protobuf
	mkdir client_base\tests
	mkdir client_base\tools
	robocopy cbmc_parser client_base\cbmc_parser /s
	robocopy exceptions client_base\exceptions /s
	robocopy fpre client_base\fpre /s
	robocopy protobuf client_base\protobuf /s
	robocopy tests client_base\tests /s 
	robocopy tools client_base\tools /s
	robocopy data\CBMC-GC-2 client_base\data\CBMC-GC-2 /s
	copy MPC.py client_base\
	copy TwoPartyComputation.py client_base\
	mkdir client_base\CBMC-GC-2\bin\
	copy docker\Dockerfile_client_base client_base\Dockerfile
	cd client_base\
	docker build -t client_base  . 
	cd ..
	rmdir client_base\ /s/q
	echo "client built"
	GOTO who

:alice
	echo "alice"
	mkdir alice
	mkdir alice\certificates
	mkdir alice\conf
	mkdir alice\data
	robocopy data\certificates_alice\ alice\data\certificates
	copy docker\Dockerfile_alice alice\Dockerfile
	copy conf\conf.py alice\conf\conf.py
	copy conf\cert_conf_alice.py alice\conf\cert_conf.py
	copy function.c alice\function.c
	cd alice\
	docker build -t alice .
	cd ..
	rmdir alice\ /s/q
	echo "Alice built"
	shift 
	docker run --net=host alice python3 TwoPartyComputation.py %_tail%
	exit		

:bob
	echo "bob"
	mkdir bob
	mkdir bob\certificates
	mkdir bob\conf
	mkdir bob\data
	robocopy data\certificates_bob\ bob\data\certificates
	copy docker\Dockerfile_bob bob\Dockerfile
	copy conf\conf.py bob\conf\conf.py
	copy conf\cert_conf_bob.py bob\conf\cert_conf.py
	copy function.c bob\function.c
	cd bob\
	docker build -t bob .
	cd ..
	rmdir bob\ /s/q
	echo "bob built"
	shift
	docker run --net=host bob python3 TwoPartyComputation.py %_tail%
	exit		

