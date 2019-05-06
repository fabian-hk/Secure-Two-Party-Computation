/* output median with bubble sort - smaller median candidate is returned*/
void mpc_main() {
    int INPUT_A_a0;
    int INPUT_A_a1;
    int INPUT_A_a2;
    int INPUT_A_a3;
    int INPUT_A_a4;
    int INPUT_B_a5;
    int INPUT_B_a6;
    int INPUT_B_a7;
    int INPUT_B_a8;
    int INPUT_B_a9;
	int arr[10];
  int i, j, tmp1, tmp2, inc;
  int OUTPUT_median;

  arr[0] = INPUT_A_a0;
  arr[1] = INPUT_A_a1;
  arr[2] = INPUT_A_a2;
  arr[3] = INPUT_A_a3;
  arr[4] = INPUT_A_a4;
  arr[5] = INPUT_B_a5;
  arr[6] = INPUT_B_a6;
  arr[7] = INPUT_B_a7;
  arr[8] = INPUT_B_a8;
  arr[9] = INPUT_B_a9;

  for (i = 9; i > 0; i--) {
    for (j = 0; j < i; j++) {
      inc = j + 1;
      tmp1 = arr[j];
      tmp2 = arr[inc];
      if (tmp1 > tmp2) {
    	  arr[j] = tmp2;
    	  arr[inc] = tmp1;
      }
    }
  }
  OUTPUT_median = arr[4];
}
