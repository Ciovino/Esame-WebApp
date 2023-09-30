"use strict;";

const input = document.querySelector("#input-episodi"); // Campo input per la ricerca
const avvia_ricerca = document.querySelector("#cerca-episodi"); // Bottone per iniziare la ricerca

// Dopo una ricera, se l'input cambia viene ri-visualizzata la lente di ingrandimento, per effettuare una nuova ricerca
input.addEventListener("input", (event) => {
    event.preventDefault();

    let icona_ricerca = document.querySelector("#search-icon"); // Icona con la lente di ingrandimento
    let icona_reset = document.querySelector("#cancel-icon"); // Icona con una X

    if (!icona_reset.classList.contains("non-visibile")) {
        icona_reset.classList.add("non-visibile");
        icona_ricerca.classList.remove("non-visibile");
    }
});

avvia_ricerca.addEventListener("click", (event) => {
    event.preventDefault();

    // Nodi da usare
    let lista_episodi = document.querySelectorAll("#episodio-pubblico"); // Lista di tutti gli episodi
    let nessun_risultato = document.querySelector("#nessun-risultato"); // Messaggio da visualizzare se la ricerca non ha trovato nulla
    let icona_ricerca = document.querySelector("#search-icon"); // Icona con la lente di ingrandimento
    let icona_reset = document.querySelector("#cancel-icon"); // Icona con una X

    let richiesta = input.value.toLowerCase();

    // Dopo una ricerca appare una X al posto della lente di ingrandimento
    // L'input viene prima liberato prima di iniziare una nuova ricerca
    let reset =
        !icona_reset.classList.contains("non-visibile") || // Se c'è una X
        richiesta == "" || // Se c'è scritto qualcosa nell'input
        lista_episodi.length == 0; // Se ci sono degli episodi tra cui effettuare la ricerca

    if (reset) {
        input.value = ""; // Cancella

        // Ripristina la lente di ingrandimento
        icona_reset.classList.add("non-visibile");
        icona_ricerca.classList.remove("non-visibile");

        nessun_risultato.classList.add("non-visibile");

        for (let i = 0; i < lista_episodi.length; i++) {
            lista_episodi[i].classList.remove("non-visibile");
        }

        return;
    } else {
        // Scambia la lente di ingrandimento con la X
        icona_reset.classList.remove("non-visibile");
        icona_ricerca.classList.add("non-visibile");
    }

    // Calcola quanti episodi sono stati nascosti con la precedente ricerca
    let eliminati = calcola_eliminati(lista_episodi);

    for (let i = 0; i < lista_episodi.length; i++) {
        // Nodi
        let titolo =
            lista_episodi[i].getElementsByClassName("titolo-episodio")[0];
        let descrizione = lista_episodi[i].getElementsByClassName(
            "descrizione-episodio"
        )[0];

        // Stringhe
        let testo_titolo = titolo.textContent || titolo.innerHTML;
        let testo_descrizione =
            descrizione.textContent || descrizione.innerHTML;

        // Booleani
        let in_titolo = testo_titolo.toLowerCase().indexOf(richiesta) > -1;
        let in_descrizione =
            testo_descrizione.toLowerCase().indexOf(richiesta) > -1;
        let gia_eliminato = lista_episodi[i].classList.contains("non-visibile");

        if (gia_eliminato) {
            if (in_titolo || in_descrizione) {
                lista_episodi[i].classList.remove("non-visibile");
                eliminati--;
            }
        } else {
            if (!in_titolo && !in_descrizione) {
                lista_episodi[i].classList.add("non-visibile");
                eliminati++;
            }
        }
    }

    if (eliminati == lista_episodi.length) {
        nessun_risultato.classList.remove("non-visibile");
    } else {
        nessun_risultato.classList.add("non-visibile");
    }
});

const calcola_eliminati = function (episodi) {
    let eliminati = 0;
    for (let i = 0; i < episodi.length; i++) {
        if (episodi[i].classList.contains("non-visibile")) {
            eliminati++;
        }
    }
    return eliminati;
};
