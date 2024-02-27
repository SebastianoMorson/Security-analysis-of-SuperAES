- no more than $2^{32}$ different building IDs will be required
	- building ID is defined as unsigned 32 bit integer uint32
- no more than $2^{128}$ token IDs will be required
	- token ID is defined via four unsigned 32 bit integers [uint32, uint32, uint32, uint32]

- A ticket is a collection of all the building IDs that a user has access to. 
	- It is defined as concatenation of 32 bit integers ticket = buildingID1 buildingID2 ... buildingIDn

# Potenziali errori
## 1. 1536-bit MODP Group
Nelle specifiche è presente questa sezione
![[implementation_err1.png]]

All'interno del paper *RFC 3526* è però specificato in questa maniera
![[implementation_err1-1.png]]
Come si può notare, il generatore è 2, e non 3.

Inoltre chiedendo a ChatGPT cosa ne pensasse ho trovato questo:

	Dimensione del gruppo MODP: Un gruppo MODP da 1536 bit è considerato ancora abbastanza sicuro per molti scopi, ma è importante notare che la sicurezza è relativa al tempo. Con l'aumentare della potenza di calcolo e delle minacce informatiche, gruppi di dimensioni maggiori (ad esempio, 2048 bit o 3072 bit) sono diventati più comuni per garantire una maggiore resistenza alle attacchi crittografici. Tuttavia, 1536 bit potrebbero ancora essere sufficienti per molte applicazioni.

All'interno della pagina di [Cisco](https://community.cisco.com/t5/security-knowledge-base/diffie-hellman-groups/ta-p/3147010) è indicato che 
![[implementation_err1-2.png]]

Il post è del 2014, quindi ben 9 anni fa. Per incrementare la sicurezza consiglierei un gruppo più forte.

Continuando l'analisi ho individuato un [paper](https://www.rfc-editor.org/rfc/rfc8247.txt) in cui è specificato che:
![[implementation_err1-3.png]]

Se l'istituzione in cui si vuole inserire il meccanismo di sicurezza possiede materiale sensibile e segreto, non implementerei questo gruppo.


## 2. Reader side-channel attack
Per stabilire la chiave comune da usare viene usato Diffie-Hellman
![[implementation_err2-1.png]]
Il problema è il solito, il Man-In-The-Middle attack.
L'autenticità del lettore non viene verificata da parte della carta. Di conseguenza un soggetto terzo potrebbe emulare un lettore ed effettuare modifiche sul ticket associato alla card. 
Questo pone importanti problemi di sicurezza, difatti un attaccante potrebbe aggiornare il valore del ticket.
![[implementation_err2.png]]
Come si vede, Per aggiornare il ticket è sufficiente conoscere una chiave comune tra lettore e carta, dopodichè la cifratura del ticket viene effettuata tramite la chiave segreta $\text{smk}$.
Per correggere l'errore farei in modo che nelle prime due fasi dell'handshake tra reader e token, il messaggio di *Hello* scambiato sia tornato da parte del reader cifrato con $\text{smk}$
$$\text{ReaderResponse}=\text{Enc}_{\text{smk}}(\text{'Hello'})$$
A quel punto la card calcolerebbe
$$\text{ReaderAuth}=\text{Dec}_{\text{smk}}(\text{Enc}_{\text{smk}}(\text{'Hello'}))$$
Se $ReaderAuth == \text{'Hello'}$ allora l'autenticità del lettore è garantita, altrimenti la comunicazione viene abortita.



## 3. Binary exponentiation and no pre-computation
![[implementation_err3.png]]
Il fatto che venga effettuata la binary exponentiation (che è troppo semplice per non avere qualche problema di sicurezza legato al fatto che si può contare i cicli di moltiplicazione) e il fatto che non ci siano valori pre-computati, mi fanno pensare che sia possibile effettuare attacchi basati su tempo. 

**Risposta di ChatGPT**
Ci sono alcune preoccupazioni legate alla sicurezza nelle affermazioni che hai fatto riguardo all'implementazione del protocollo Diffie-Hellman (DH) con Montgomery exponentiation, special purpose hardware multiplier e l'assenza di SPA (Simple Power Analysis) e DPA (Differential Power Analysis) protezione. Ecco alcune delle principali preoccupazioni:

1. **Storage Limitato:** Se il tuo sistema ha problemi di storage limitato, è importante assicurarsi che l'implementazione sia ottimizzata ma anche sicura. Limitare la quantità di storage può comportare errori e vulnerabilità se non gestita attentamente.
    
2. **Precomputazione:** Affermi che a causa dei vincoli di storage, non puoi precalcolare valori. Tuttavia, la precomputazione di valori specifici può contribuire significativamente a migliorare l'efficienza e la sicurezza dell'implementazione DH. La mancanza di precomputazione potrebbe rendere l'implementazione vulnerabile a attacchi basati su tempi.
    
3. **SPA e DPA:** Sebbene tu possa ritenere che SPA e DPA non siano un problema a causa della natura "effimera" dei valori DH e delle dimensioni dei primi grandi, è importante notare che l'implementazione crittografica dovrebbe sempre prendere in considerazione la protezione contro possibili attacchi basati su potenza, soprattutto se si tratta di hardware condiviso o se ci sono altre possibili vie per misurare la potenza.
    
4. **Assunzioni sulla sicurezza:** L'asserzione che DPA-style attacks sarebbero estremamente difficili a causa delle dimensioni dei primi potrebbe non essere accurata. La sicurezza crittografica si basa su principi ben stabiliti e il fatto che il sistema utilizzi primi grandi non dovrebbe essere l'unico presupposto di sicurezza. Gli attacchi possono essere sofisticati e sfruttare debolezze nell'implementazione.


## 4. Cloning
Cosa impedisce a un utente non autorizzato di clonare la card di un utente non autorizzato?
Per esempio, immaginiamo che questa applicazione sia inserita in un contesto aziendale e che un dipendente sgradito sia licenziato. 
Una corretta politica di sicurezza prevederebbe che l'impiegato venga chiamato dalla human resources e licenziato, richiedendo indietro la card di sicurezza.

Immaginiamo che l'azienda detenga materiale pericoloso e coperto da segreto aziendale. O immaginiamo semplicemente che l'azienda possieda strumentazione costosa. 

**Basterebbe aver ritirato la carta per impedire all'impiegato di accedere alle strutture? Se questo impiegato avesse le conoscenze tecniche, potrebbe creare una copia della sua chiave di accesso?**
La risposta è si, o per lo meno le specifiche non trattano tale argomento.
Difatti viene specificato che:
- Therefore our system guarantees that employees can always access the buildings that they should have access to
- the reader only verifies but does not have to consult a central database
- To prove authenticity we assume that each token holds some ID encrypted under the system master key (SMK)
- the SuperSAM Token offering its secureID to the reader

Immaginiamo lo scenario in cui:
- ho una carta valida $X_{t}$ e una carta falsa $X_f$
- ho un lettore valido $Y_t$ e un lettore falso $Y_f$
Voglio rendere $X_f$ una carta valida
Per renderla tale ho bisogno di ottenere 
- un $\text{secureID}$ che venga accettato dal lettore
- un $\text{secureTicket}$ che contenga i token dei palazzi per cui è abilitato l'ingresso

Per recuperare un $secureID$ è sufficiente usare $Y_f$ per recuperare il $secureID$ di $X_t$ in fase di autenticazione iniziale. Lo posso fare perchè in quel caso non c'è alcun tipo di cifratura durante lo scambio di $secureID$ e di $g^T$.

A questo punto basta usare $Y_f$ per fingere un'interazione con $X_t$ . 
Durante questa interazione sappiamo che il primo passo è l'autenticazione da parte del reader.
Se $Y_f$ finge di autenticare $X_t$ a quel punto $X_t$ invierà il suo $secureToken$ per poter (normalmente) richiedere l'accesso al palazzo. 
Se però $Y_f$ invece di abilitare l'ingresso semplicemente copia il valore di $secureToken$, a quel punto 


## 5. ECB vs CBC 
"*Because all core data is likely to be smaller than 128 bits, we will use AES in ECB mode.*"
ma che vor dì? non è il caso di usare ECB, che ricordiamo usa questo schema qua:
![[Pasted image 20231025194351.png]]
non garantisce la proprietà di IND (indistinguishability).
Ciò significa che 
Un po' meglio usare CBC direi 
![[Pasted image 20231025194502.png]]![[Pasted image 20231025194508.png]]

## 6. fixed key equal to zero
"To convert the outcome of a DH key exchange to a symmetric session key we will use AES as block cipher to implement CBC-MAC with fixed key equal to zero"

## 7. Secret Master Key not protected
Bisogna usare una funzione di hash per proteggere la secret master key. Se non si usa, la chiave è salvata in chiaro e un potenziale attaccante potrebbe risalire ad essa. 

## 8. Implementation Note: PRNG test metods, Section 3.4 page 6
