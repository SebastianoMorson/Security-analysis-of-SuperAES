#ifndef RAND_INCLUDE
#define RAND_INCLUDE

#include <stdint.h>

#define POLY_MASK_32 0xB4BCD35C
#define POLY_MASK_31 0x7A5BC2E3

typedef unsigned int uint;

extern unsigned int rngSeed1;
extern unsigned int rngSeed2;

//int shift_lfsr(uint *lfsr, uint polynomial_mask)  __attribute__((optimize("-O3")));
void init_lfsrs(uint seed1, uint seed2) __attribute__((optimize("-O3")));
uint8_t getRand(void) __attribute__((optimize("-O0")));
//unsigned int rand_interval(unsigned int max) __attribute__((optimize("-O0")));
//void CreateRandomState(uint8_t* random_input) __attribute__((optimize("-O3")));
//void shuffleArray(uint8_t *array, unsigned int n) __attribute__((optimize("-O3")));


#endif

