
# Main function -- main.c
```C
uint8_t key[16] = {0x00, 0x01, 0x02, 0x03, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};

// Initializing lfsr

unsigned int rngSeed1 = 0; // Framework for embedded testing: get_rand();
unsigned int rngSeed2 = 0;// Framework for embedded testing: get_rand();

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

int main(void) {
	init_lfsrs(rngSeed1, rngSeed2);
	uint8_t ciphertext[16];
	uint8_t plaintext[16];
	
	//Frame work for side channel testing: execute an encryption 1000 times
	//for(int number_of_encryption=0; number_of_encryption < 1000 ;number_of_encryption++){
	
	// Generating a random plaintext
	for(int i=0; i < 16; i++){
		plaintext[i]= getRand();
	}
	Encrypt(ciphertext, plaintext, key);
	printf("Ciao a tutti");
	// }	
}
```
Questa funzione presenta diversi problemi:
## fixed seed
In questa porzione di codice:
```C
unsigned int rngSeed1 = 0; // Framework for embedded testing: get_rand();
unsigned int rngSeed2 = 0;// Framework for embedded testing: get_rand();
```
vengono definiti i seed per il random number generator. Il problema è che con seed=0 otterrò sempre un valore di output =0 essendo che gli shift a destra di `lfsr32` e di `lfsr31` saranno sempre uguali a 0 ed essendo che la funzione `getRand()` termina con l'istruzione 
`return (lfsr32 ^ lfsr31) & 0xffff;`

Suggerirei quindi di far in modo che il seed fosse $\neq 0$ . 

## easy key
In questa porzione 
```C
uint8_t key[16] = {0x00, 0x01, 0x02, 0x03, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
```
è definita una chiave di lunghezza 16 e uguale a `012340000000000`. Ad occhio direi che è troppo prevedibile.



# Random Number Generator -- rand.c
Il codice in esame è il seguente:

```C 
#include "rand.h"
// This random nuber generator shifts the 32-bit LFSR
// twice before XORing it with the 31-bit LFSR.
//the bottom 16 bits are used for the random number

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
```

### Idea:
L'idea generale di questa funzione è quella di:
- prendere due seed iniziali 
- prendere due maschere `POLY_MASK_32` e `POLY_MASK_31`, inizializzate ai valori `3032273756` e `2052834019` rispettivamente
- shiftare di uno a destra il seed iniziale e xorarlo con la maschera se tale seed è =1
- ripetere l'operazione precedente una seconda volta prendendo come seed il risultato dell'operazione precedente
- ripetere l'operazione precedente prendendo come seed il valore del primo seed e come maschera `POLY_MASK_31`
- tornare come risultato $\text{lfsr32}\oplus \text{lfsr31}$

Quindi in definitiva vengono effettuati 2 shift a destra del seed1 iniziale e 1 shift a destra del seed2  a ogni iterazione.

### Scelta del seed 1 e 2
La scelta dei seed iniziali da usare non può essere casuale.
Il programma iniziale usava un seed iniziale inizializzato a 0. Questo porta ad ottenere una serie di numeri randomici sempre =0.
Questo non va chiaramente bene, in quanto #todo 

Se invece seed1 e seed2 sono inizializzati a 1, cosa succede?
In questo caso il primo numero ritornato sarà uguale a $\text{POLY\_MASK\_32 shifted by 1}\oplus \text{POLY\_MASK\_31}$

Se invece seed1 e seed2 sono inizializzati a 2 e 1, cosa succede?
In questo caso il primo numero ritornato sarà uguale a $\text{POLY\_MASK\_32}\oplus \text{POLY\_MASK\_31}$. Un attaccante a conoscenza di uno dei due valori potrebbe ricavare il secondo facilmente.

Se invece seed1 e seed2 sono inizializzati a 2 e 0, cosa succede?
In questo caso il primo numero ritornato sarà uguale a $\text{POLY\_MASK\_32}\oplus 0 = \text{POLY\_MASK\_32}$. 

Attacchi basati sul seed usato possono essere utili, ma il fatto che il valore di ritorno sia di tipo uint8_t fa sì che il valore finale sia modulo 256.




## `uint volatile lfsr32, lfsr31, retrand;
In questa porzione di codice vengono definite 3 variabili di tipo unsigned int, con opzione ***volatile***.
Questa opzione #todo

## `void init_lfsrs(uint seed1, uint seed2)
In questa porzione di codice viene definita una funzione che assegna i valori di due seed alle due variabili volatili `lfsr32` e  `lfsr31`

## `uint8_t getRandom(void)

All'interno della funzione `getRand()` sembrerebbe star applicando il concetto di **LFSR**.

All'interno di questo [[https://www.analog.com/en/design-notes/random-number-generation-using-lfsr.html|articolo]] è spiegato molto bene come funziona LFSR e cosa bisogna e non bisogna fare. 

Il problema, citato in [[P2CryptoEngineering_RNG.pdf#page=17|P2CryptoEngineering_RNG, page 17]] è che, riprendendo ciò che viene detto:
`The problem with this approach is that the resulting numbers are not unpredictable (not even for a computationally limited adversary); although for suitably chosen LFSRs the resulting numbers are unbiased (thus they are useful for testing and experimentation)`

Questo significa che per un uso pratico, la funzione di RNG va modificata.

Per verificare se la funzione `getRand()` sia corretta dal punto di vista deduttivo, voglio provare ad applicare i due test di verifica sperimentale chiamati $frequency\;test$ e $poker\;test$.
Per farlo scriverò due programmi in C.


### Frequency test

### Poker test

### Correlation test
Questo test non è citato nelle slide, ma è presente nel libro [[Applied_Cryptography_Protocols,_Algorithms_and_Source_Code_in_C.pdf#page=406|Applied_Cryptography_Protocols,_Algorithms_and_Source_Code_in_C, page 406]] .
Analizzando uno stream di numeri random generati con seed1 e seed2 =0, ho avuto l'intuizione di verificare se alcuni numeri era più o meno probabile che si presentassero vicini ad altri numeri. 

In effetti no, però il fatto che i valori random generabili varino soltanto tra 0 e 255 mi sembra eccessivamente riduttivo, ma potrebbe non essere così. Bisogna verificare. #todo

Un altro fatto che mi è venuto in mente è: la distribuzione dei numeri generati è uniforme o si concentra attorno a dei valori medi? Per verificare quest'ultima ipotesi ho generato un file di 100'000'000 numeri random e ho contato le occorrenze per ciascun carattere.
Come si può vedere dalla tabella sottostante i valori sono uniformemente distribuiti.

| numero | occorrenze |
| ------ | ---------- |
| 0      | 420543     |
| 1      | 419335     |
| 2      | 419952     |
| 3      | 420141     |
| 4      | 420882     |
| 5      | 421084     |
| 6      | 421057     |
| 7      | 420539     |
| 8      | 419386     |
| 9      | 420139     |
| 10     | 419912     |
| 11     | 420166     |
| 12     | 420654     |
| 13     | 419601     |
| 14     | 420023     |
| 15     | 420513     |
| 16     | 420311     |
| 17     | 420531     |
| 18     | 418508     |
| 19     | 420187     |
| 20     | 419947     |
| 21     | 419075     |
| 22     | 420838     |
| 23     | 419220     |
| 24     | 421070     |
| 25     | 420443     |
| 26     | 418738     |
| 27     | 420691     |
| 28     | 420763     |
| 29     | 419424     |
| 30     | 420000     |
| 31     | 420887     |
| 32     | 419573     |
| 33     | 420656     |
| 34     | 420435     |
| 35     | 419467     |
| 36     | 419094     |
| 37     | 419985     |
| 38     | 420545     |
| 39     | 422555     |
| 40     | 420564     |
| 41     | 419404     |
| 42     | 420531     |
| 43     | 419658     |
| 44     | 420025     |
| 45     | 420827     |
| 46     | 419746     |
| 47     | 421380     |
| 48     | 419991     |
| 49     | 420983     |
| 50     | 420940     |
| 51     | 420377     |
| 52     | 420451     |
| 53     | 420186     |
| 54     | 420235     |
| 55     | 421105     |
| 56     | 419857     |
| 57     | 420008     |
| 58     | 420699     |
| 59     | 420557     |
| 60     | 420423     |
| 61     | 421976     |
| 62     | 419905     |
| 63     | 420633     |
| 64     | 420677     |
| 65     | 420411     |
| 66     | 420583     |
| 67     | 419379     |
| 68     | 420226     |
| 69     | 419919     |
| 70     | 420847     |
| 71     | 420426     |
| 72     | 421057     |
| 73     | 420642     |
| 74     | 420228     |
| 75     | 419964     |
| 76     | 419944     |
| 77     | 421514     |
| 78     | 420745     |
| 79     | 419562     |
| 80     | 420117     |
| 81     | 420017     |
| 82     | 419144     |
| 83     | 421318     |
| 84     | 419124     |
| 85     | 420219     |
| 86     | 419829     |
| 87     | 421289     |
| 88     | 420478     |
| 89     | 420663     |
| 90     | 420360     |
| 91     | 419720     |
| 92     | 420868     |
| 93     | 420504     |
| 94     | 420218     |
| 95     | 419853     |
| 96     | 419939     |
| 97     | 420319     |
| 98     | 421301     |
| 99     | 419838     |
| 100    | 420932     |
| 101    | 420873     |
| 102    | 420315     |
| 103    | 421356     |
| 104    | 419762     |
| 105    | 419733     |
| 106    | 420109     |
| 107    | 420526     |
| 108    | 419815     |
| 109    | 420227     |
| 110    | 421351     |
| 111    | 419290     |
| 112    | 420887     |
| 113    | 420769     |
| 114    | 420585     |
| 115    | 418844     |
| 116    | 421541     |
| 117    | 419818     |
| 118    | 420409     |
| 119    | 419967     |
| 120    | 418948     |
| 121    | 421081     |
| 122    | 419427     |
| 123    | 419958     |
| 124    | 420172     |
| 125    | 420703     |
| 126    | 420687     |
| 127    | 421480     |
| 128    | 421468     |
| 129    | 420672     |
| 130    | 421423     |
| 131    | 419037     |
| 132    | 421184     |
| 133    | 420129     |
| 134    | 420553     |
| 135    | 419161     |
| 136    | 420809     |
| 137    | 421109     |
| 138    | 418739     |
| 139    | 420282     |
| 140    | 420655     |
| 141    | 419787     |
| 142    | 420701     |
| 143    | 420133     |
| 144    | 420538     |
| 145    | 420737     |
| 146    | 419982     |
| 147    | 420147     |
| 148    | 421730     |
| 149    | 420812     |
| 150    | 420676     |
| 151    | 420017     |
| 152    | 419232     |
| 153    | 419393     |
| 154    | 420558     |
| 155    | 421099     |
| 156    | 421098     |
| 157    | 421472     |
| 158    | 420181     |
| 159    | 420688     |
| 160    | 420827     |
| 161    | 419841     |
| 162    | 420357     |
| 163    | 419478     |
| 164    | 420036     |
| 165    | 419703     |
| 166    | 419802     |
| 167    | 420852     |
| 168    | 419023     |
| 169    | 420000     |
| 170    | 419877     |
| 171    | 419891     |
| 172    | 421300     |
| 173    | 420003     |
| 174    | 419042     |
| 175    | 419712     |
| 176    | 420958     |
| 177    | 419622     |
| 178    | 420165     |
| 179    | 419613     |
| 180    | 418936     |
| 181    | 420355     |
| 182    | 420284     |
| 183    | 419417     |
| 184    | 419734     |
| 185    | 420698     |
| 186    | 420345     |
| 187    | 418465     |
| 188    | 418906     |
| 189    | 420639     |
| 190    | 420878     |
| 191    | 420884     |
| 192    | 421249     |
| 193    | 419762     |
| 194    | 420778     |
| 195    | 419506     |
| 196    | 420576     |
| 197    | 421368     |
| 198    | 418645     |
| 199    | 419089     |
| 200    | 420014     |
| 201    | 420249     |
| 202    | 419403     |
| 203    | 420174     |
| 204    | 420424     |
| 205    | 419862     |
| 206    | 420375     |
| 207    | 422315     |
| 208    | 420229     |
| 209    | 420230     |
| 210    | 420517     |
| 211    | 420965     |
| 212    | 421067     |
| 213    | 420261     |
| 214    | 420440     |
| 215    | 420059     |
| 216    | 419511     |
| 217    | 419672     |
| 218    | 420769     |
| 219    | 420340     |
| 220    | 420016     |
| 221    | 421261     |
| 222    | 419970     |
| 223    | 421001     |
| 224    | 418721     |
| 225    | 420385     |
| 226    | 418798     |
| 227    | 420349     |
| 228    | 419729     |
| 229    | 420780     |
| 230    | 421576     |
| 231    | 419520     |
| 232    | 420670     |
| 233    | 420690     |
| 234    | 419903     |
| 235    | 420099     |
| 236    | 420022     |
| 237    | 419866     |
| 238    | 420972     |
| 239    | 420015     |
| 240    | 420264     |
| 241    | 420267     |
| 242    | 420647     |
| 243    | 419237     |
| 244    | 421268     |
| 245    | 419999     |
| 246    | 420063     |
| 247    | 420634     |
| 248    | 420919     |
| 249    | 419607     |
| 250    | 420347     |
| 251    | 419280     |
| 252    | 421037     |
| 253    | 420162     |
| 254    | 419776     |
|255| 420946 |

# masked_combined.c
Il codice di *masked_combined.c* è una copia del codice presente in questa pagina github:
https://github.com/knarfrank/Higher-Order-Masked-AES-128/blob/master/masked_combined.c

Eseguendo un'analisi delle differenze rispetto al codice originale, ho potuto constatare che sono presenti alcune differenze quasi invisibili, ma che potrebbero fare la differenze:
## numero di round
In questa porzione di codice
```C
  

void Encrypt(uint8_t* output, uint8_t* input, uint8_t* key) {
	uint8_t rcon[10] = {0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36};
	uint8_t round;
	uint8_t i, j, d;
	uint8_t tmp[4][NUM_SHARES];
	
	// Mask both the input and key
	
	MaskArray(state, input, 16);
	MaskArray(round_key, key, 16);
	  
	for(round = 0; round < 9; round++) { //nel codice originale è <10
	
		// Add Round Key Stage
		for(j = 0; j < NUM_SHARES; j++) {
			for(i = 0; i < 16; i++) {
				state[i][j] ^= round_key[i][j];
			}
		}
	
		// Framework for testing: start_trigger()
		CombinedSbox(state);
		
		// Framework for testing: pause_trigger()
		ShiftRowsMixColumns(state, round);
		
		// Key Schedule
		round_key[0][0] ^= rcon[round];
		DualSbox(tmp[0], tmp[1], round_key[13], round_key[14]);
		DualSbox(tmp[2], tmp[3], round_key[15], round_key[12]);
		
		for(d = 0; d < NUM_SHARES; d++) {
			round_key[0][d] ^= tmp[0][d];
			round_key[1][d] ^= tmp[1][d];
			round_key[2][d] ^= tmp[2][d];
			round_key[3][d] ^= tmp[3][d];
			round_key[4][d] ^= round_key[0][d];
			round_key[5][d] ^= round_key[1][d];
			round_key[6][d] ^= round_key[2][d];
			round_key[7][d] ^= round_key[3][d];
			round_key[8][d] ^= round_key[4][d];
			round_key[9][d] ^= round_key[5][d];
			round_key[10][d] ^= round_key[6][d];
			round_key[11][d] ^= round_key[7][d];
			round_key[12][d] ^= round_key[8][d];
			round_key[13][d] ^= round_key[9][d];
			round_key[14][d] ^= round_key[10][d];
			round_key[15][d] ^= round_key[11][d];
		}
	}
	
	// Final Add Round Key
	for(j = 0; j < NUM_SHARES; j++) {
		for(i = 0; i < 16; i++) {
			state[i][j] ^= round_key[i][j];
		}
	}
	
	// Unmask the state revealing the encrypted output
	UnMaskArray(output, state, 16);
}
```

Come si può vedere, nella prima parte è presente il seguente ciclo for
`for(round = 0; round < 9; round++) {`
Il problema è che nel codice originale il round è limitato al valore 10, non al valore 9. 
Questo cambiamento fa si che non venga considerato il valore `0x36` (ossia  `512`) del vettore `rcon[]` inizializzato inizialmente.
In generale, non è provata la sicurezza per un numero di round minore. è meglio dunque che il valore di round sia 10.

## Different for cicle
In questa sezione del codice
```C
void SecEvalCombined(uint8_t w[16][NUM_SHARES], uint8_t z[16][NUM_SHARES], const uint8_t h[]) {
	
	uint8_t i,j,k,r,s0,t0,t1;
	for(j = 0; j < 16; j++) {
		for(i = 0; i < (NUM_SHARES/2); i++) {
			r = getRand();
```
C'è una piccola differenza rispetto al codice originale.
In particolare nel codice originale la stessa sezione è scritta come
```C
void SecEvalCombined(uint8_t w[16][NUM_SHARES], uint8_t z[16][NUM_SHARES], const uint8_t h[]) {
	
	uint8_t i,j,k,r,s0,t0,t1;
	for(i = 0; i < (NUM_SHARES/2); i++) {
		r = getRand();
		for(j = 0; j < 16; j++) {
		
```

Bisognerebbe valutare se questo cambiamento inficia la sicurezza o il normale comportamento di AES. Difatti in questo modo il numero di numeri random generati è molto maggiore. Bisogna capire se l'utilizzo di valori random sempre diversi può in qualche modo peggiorare il codice.
#todo 

# Timing attacks
#### TODO: verificare se le operazioni di shifting possono portare a timing attacks

# AES implementation
#### TODO: le specifiche di AES prevedono che il column mix sia effettuato prima dell'ultimo round, verificare se l'implementazione non estende il column mix anche per l'ultimo round

$$
n1 = 010101 \;\;
n2 = 011011 \;\;
n3 = 111010 \;\;
...
n_{k} = 100101
$$


$$
X_{1} = \frac{n_{1,0} + n_{1,1}}{n} 
X_{2} \dots
X_{3} \dots
$$

$$
Q = \sum_{i=1}^k (X_{i})^2
$$
