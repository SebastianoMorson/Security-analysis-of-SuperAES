#include "rand.h"
// This random nuber generator shifts the 32-bit LFSR
// twice before XORing it with the 31-bit LFSR.
//the bottom 16 bits are used for the random number 

//è una buona scelta scegliere come tipo "volatile"? Non potrebbe causare problemi di sicurezza?

uint volatile lfsr32, lfsr31, retrand;


// "Linear Feedback Shift Register",
void init_lfsrs(uint seed1, uint seed2) {
    lfsr32 = seed1;
    lfsr31 = seed2;
}

uint8_t getRand(void) {
    int feedback;
    feedback = lfsr32 & 1;
  	lfsr32 >>= 1;
    if(feedback == 1) {
        lfsr32 ^= (uint volatile)POLY_MASK_32;
    } else {
        retrand ^= (uint volatile)POLY_MASK_32;
    }
  	feedback = lfsr32 & 1;
  	lfsr32 >>= 1;
  	if(feedback == 1) {
        lfsr32 ^= POLY_MASK_32;
    } else {
        retrand ^= POLY_MASK_32;
    }
  	feedback = lfsr31 & 1;
  	lfsr31 >>= 1;
  	if(feedback == 1) {
        lfsr31 ^= POLY_MASK_31;
    } else {
        retrand ^= POLY_MASK_31;
    }
  	return (lfsr32 ^ lfsr31) & 0xffff;
}


void get_16_Byte_rand(uint8_t* random_input) {
    uint8_t i;
    for(i = 0; i < 16; i++) {
        random_input[i] = getRand();
    }
}
