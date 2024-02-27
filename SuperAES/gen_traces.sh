#!/bin/bash

# Definisci il comando da eseguire
comando_da_eseguire="GILES superAES.bin -o test.trs"

# Crea una cartella per gli output se non esiste già
cartella_output="Tracce"
mkdir -p "$cartella_output"
mkdir -p "./Tracce/"
# Loop per eseguire il comando 50 volte
for ((i=1; i<=400; i++)); do
    echo $i
    comando_da_eseguire="GILES superAES.bin -o ./Tracce/traccia_$i.trs"
    # Crea una cartella per questa iterazione
    cartella_iterazione="./Inputs/"
    mkdir -p "$cartella_iterazione"

    # Esegui il comando e indirizza l'output nella cartella corrente
    $comando_da_eseguire> "./$cartella_iterazione/input_$i.txt"

    # Aggiungi una nuova linea vuota tra le iterazioni per chiarezza5
done

echo "Esecuzione completata."
