/* outputs the mean of all 10 inputs - 5 per party */
int mpc_main(int INPUT_A_0, int INPUT_A_1, int INPUT_A_2, int INPUT_A_3, int INPUT_B_0, int INPUT_B_1, int INPUT_B_2, int INPUT_B_3)
{
	int tmp = INPUT_A_0 + INPUT_A_1 + INPUT_A_2 + INPUT_A_3  + INPUT_B_0 + INPUT_B_1 + INPUT_B_2 + INPUT_B_3;
	return tmp / 8;
}
