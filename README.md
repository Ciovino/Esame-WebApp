# Esame 23/01/2023 - Introduzione alle Applicazioni Web

## Podcast
Realizzare un'applicazione web per la gestione di podcast.

### Homepage
- Navbar laterale:
  - Nome del sito (*ancora da scegliere*);
  - Pagina di registrazione (**Senza login**);
  - Pagina di login (**Senza login**);
  - Pagina personale (**Con Login**);
  - Link per logout (**Con Login**);
- Aside per la ricerca:
  - Pagina delle categorie:
    - Elenco di tutte le *categorie*;
    - Elenco di *tutti i podcast*, con ricerca testuale;
- Main, con i podcast:
  - *Podcast più seguiti*: I 3 podcast più seguiti nel sito.
  - *Tutti i podcast*: Tutti i podcast del sito (**da scegliere un ordinamento**);
- *Footer*, con le icone per i social.

### Registrati
- *Form* di registrazione contenente:
  - *Username* (**univoco**);
  - *Email* (*univoca*);
  - *Password*;
  - *Tipo* di utente;
  - *Immagine profilo*.
  
### Login
- *Form* di login contentente:
  - *Username*;
  - *Password*.

### Pagina Personale
- Messaggio di *benvenuto*;
- Elenco delle informazioni dell'utente:
  - *Username*;
  - *Email*;
  - *Password*;
  - *Tipo* di utente;
  - *Immagine profilo*.
- Link:
  - *Podcast seguiti*;
  - *Podcast creati* (se l'utente è un creatore);

### Pagina dei podcast seguiti
- Elenco dei podcast (*Se non ci sono podcast, viene visualizzato "Non segui nessun podcast"*).

### Pagina dei podcast creati
- Elenco dei podcast;
- *Bottone* per la creazione di un nuovo podcast:
  - *Titolo*;
  - *Descrizione*;
  - *Immagine*;
  - *Categorie*.

### Pagina del podcast
- Immagine del podcast, *titolo* del podcast, nome dell'*autore*, *descrizione* del podcast;
- Pulsante per seguire il podcast (se l'utente è loggato);
- Elenco di *episodi pubblici* (la ricerca viene fatta solo tra questi episodi);
- Elenco di *episodi privati* (visibili solo all'autore);
- *Form* per aggiunta di un nuovo episodio (visibili solo all'autore);
- Pulsanti per modifica e cancellazione del podcast.

### Pagina degli episodi
Sono gli utenti loggati vedranno il link per accedere a questa pagina.

- *Immagine del podcast*, *titolo del podcast*, nome dell'*autore*, *titolo dell'episodio* e *descrizione dell'episodio*;
- *Player* con link per:
  - *Episodio precedente* (se c'è);
  - Tornare al *podcast*;
  - *Episodio successivo* (se c'è);
- Sezione *commenti*:
  - Elenco di *tutti i commenti* presenti:
    - Ogni commento che l'utente loggato ha scritto è sia *modificabile* che *cancellabile*;
  - *Form* per aggiunta di un nuovo commento.
  - 
### Categorie
- Elenco di tutte le categorie presenti nel sito, divise per *macrocategorie*:
  - **Arte e Intrattenimento**: *Arte*, *Commedia*, *Narrativa*, *Cinema*, *Letteratura*, *Musica*;
  - **Business e Tecnologia**: *Economia*, *Tecnologia*, *Finanza*, *Politica*;
  - **Formazione**: *Storia*, *Scienza*, *Filosofia*;
  - **Sport e Divertimento**: *Sport*, *Tennis*, *Calcio*, *Bowling*, *Videogiochi*;
  - **Lifestyle e Benessere**. *Moda*, *Cibo*, *Fitness*.
- Ogni macrocategoria ha una pagina separata in cui sono elencati tutti i podcast appartenenti a quella categoria, con ricerca testuale.