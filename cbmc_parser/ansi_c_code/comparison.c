// _Bool not supported
void mpc_main(int INPUT_B_x, int INPUT_A_y){

	_Bool OUTPUTz;
	_Bool z;

	z = 1;

	//if (INPUT_A_x < INPUT_B_x) {
	if (INPUT_B_x > INPUT_A_y) {
		z = 0;
	}

	OUTPUTz = z;
}

