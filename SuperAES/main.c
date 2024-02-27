/*
 * AES-128 Encryption in CBC Mode - Main File
 */
//#include "elmo-funcs-h."
#include "elmo-funcs.h"
#include "stdint.h"
#include "masked_combined.h"
#include "rand.h"
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Fixed 16 Byte Key:
uint8_t key[16] = {0x21, 0x32, 0x09, 0x21, 0x54, 0x16, 0xA3, 0x67, 0x58, 0x05, 0x11, 0x83, 0x74, 0x97, 0x28, 0x63};
// Initializing lfsr 
unsigned int rngSeed1 = 0; // Framework for embedded testing: get_rand();
unsigned int rngSeed2 = 0;// Framework for embedded testing: get_rand();

const int INT_MAX = 2147483647;

int mod_bld(int x, int y)
{
    int modulus = x, divisor = y;

    while (divisor <= modulus && divisor <= INT_MAX/2)
        divisor <<= 1;

    while (modulus >= y) {
        while (divisor > modulus)
            divisor >>= 1;
        modulus -= divisor;
    }

    return modulus;
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
int main(void) {

    int seed3 = get_rand();
    int seed4 = get_rand();
    
    init_lfsrs(seed3, seed3);
    uint8_t ciphertext[16];
    uint8_t plaintext[16];
    //Frame work for side channel testing: execute an encryption 1000 times
    //start_trigger();
    //for(int number_of_encryption=0; number_of_encryption < 100000 ;number_of_encryption++){
    // Generating a random plaintext 
        uint8_t x = get_rand();
        for(int i=0; i < 500000; i++){
            
             //97+mod_bld(getRand(), 25);
            
            //while(x > 122 || x<97){
            x = getRand();
            //}
            putchar(x);
            //plaintext[i] = x;
        }

        //add_to_trace(plaintext, 16);
        
        
        //for(int i =0; i<16; i++){

        //    putchar(plaintext[i]);
        
        //}
        
        //init_lfsrs(rngSeed1, rngSeed2);
    
        
        //Encrypt(ciphertext, plaintext, key);  
        
        //add_to_trace(ciphertext, 16);
        
        //putchar(number_of_encryption);
    }
    //pause_trigger();
    //add_to_trace(plaintext, 16);

