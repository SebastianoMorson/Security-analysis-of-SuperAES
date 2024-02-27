
#include <stddef.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include "rand.h"
#include "masked_combined.h"
#include <sodium.h>


int get_seeds(unsigned int* random_buffer, size_t buffer_size){
    if (sodium_init() < 0) {
        // La libreria sodium non è stata inizializzata correttamente
        return -1;
    }
    // Genera numeri casuali sicuri
    randombytes_buf(random_buffer, buffer_size);
    return 0;

}

int sodium_initialization(void){
    size_t size = 2;
    unsigned int seeds[size];
    printf("fin qui tutto okay");
    if (get_seeds(seeds, size) != 0){
        printf("%s", "Unexptected error during seeds generator. Exit");
        return -1;
    } 
    init_lfsrs(20,20); //seeds[0], seeds[1]);
    printf("%d",seeds[0]);
    return 0;
}

// function to convert decimal to binary 
int decToBin(int n, int* binaryNum) 
{ 
    // array to store binary number 
    
    // counter for binary array 
    int i = 0; 
    while (n > 0) { 
  
        // storing remainder in binary array 
        binaryNum[i] = n % 2; 
        n = n / 2; 
        i++; 
    }
    return i;
    
} 

int contaZeri(int array[], int lunghezza) {
    int conteggioZeri = 0;

    // Scorre l'array e incrementa il conteggio per ogni zero
    for (int i = 0; i < lunghezza; i++) {
        if (array[i] == 0) {
            conteggioZeri++;
        }
    }

    return conteggioZeri;
}


int contaUni(int* array, int lunghezza) {
    int conteggioUno = 0;

    // Scorre l'array e incrementa il conteggio per ogni zero
    for (int i = 0; i < lunghezza; i++) {
        if (array[i] == 1) {
            conteggioUno++;
        }
    }

    return conteggioUno;
}

int test_getRand(){
    int iterations = 100000;
    int counter_zeros =0;
    int counter_ones =0;
    for(int i=0; i<iterations; i++ ){
        unsigned int numero = getRand();
        int seq[32]; 
        int len = decToBin(numero, seq);
        /*
        for (int j = len-1; j >= 0; j--){
            printf("%d", seq[j]); 
        }
        */
        counter_zeros= counter_zeros+contaZeri(seq, len);
        counter_ones= counter_ones+contaUni(seq, len);
        
    }
    printf("\nZeri: %d\n", counter_zeros);
    printf("Uni: %d\n", counter_ones);
    return 0;
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
int main(void) {
    
    if (sodium_initialization()!= 0){
        printf("%s", "Unexpected error during sodium initialization");
        return -1;
    }
    FILE *fptr;
    fptr = fopen("filename.txt", "w");
    for(long i=0; i<10000; i++){

        // Write some text to the file
        fprintf(fptr, "%d\n",getRand());

        printf("%d\n", getRand());   
    }
    // Close the file
    fclose(fptr);

    printf("%d", 1^0);
    //test_getRand();
    return 0;

   // }
    
}