#include <stdio.h>
#include <stdlib.h>

#define MAX 65535
void countOccurrences(FILE *inputFile, FILE *outputFile) {
    int number;
    int occurrences[MAX] = {0};  // Modifica la dimensione in base ai tuoi requisiti

    // Leggi il file di input e controlla le occorrenze
    while (fscanf(inputFile, "%d", &number) == 1) {
        // Assumiamo che i numeri siano compresi tra 0 e 99
        if (number >= 0 && number < MAX) {
            occurrences[number]++;
        }
    }

    // Scrivi le occorrenze nel file di output
    fprintf(outputFile, "| numero | occorrenze |\n");
    for (int i = 0; i < MAX; i++) {
        fprintf(outputFile, "|%d| %d |\n", i, occurrences[i]);
    }
}
void findSeeds(int* seeds){
    for(int i = 2; i<=2000; i++){
        for(int j=2;j<=2000;j++){
            int z = i>>2;
            int x = j>>1;
            //printf("%d\n",(z^x)&0xffff );
            if(((z^x)&0xffff) == 15){
                printf("Found!!! %d -- %d\n", i, j);
                seeds[0] = i;
                seeds[1] = j;
                return;
            }
        }
    }
    
}
int main(void) {
    FILE *inputFile, *outputFile;

    // Apri il file di input in lettura
    if ((inputFile = fopen("filename.txt", "r")) == NULL) {
        perror("Errore nell'apertura del file di input");
        return EXIT_FAILURE;
    }

    // Apri il file di output in scrittura
    if ((outputFile = fopen("output.txt", "w")) == NULL) {
        perror("Errore nell'apertura del file di output");
        fclose(inputFile);
        return EXIT_FAILURE;
    }

    // Chiamata alla funzione per contare le occorrenze
    countOccurrences(inputFile, outputFile);

    // Chiudi i file
    fclose(inputFile);
    fclose(outputFile);

    printf("Conteggio delle occorrenze completato.\n");

    int seeds[2];
    findSeeds(seeds);
    printf("%d ++ %d", seeds[0], seeds[1]);
    return EXIT_SUCCESS;
}