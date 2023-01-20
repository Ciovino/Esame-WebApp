"use strict;";

const calcola_eliminati = function (episodi) {
    let eliminati = 0;
    for (let i = 0; i < episodi.length; i++) {
        if (episodi[i].classList.contains("non-visibile")) {
            eliminati++;
        }
    }
    return eliminati;
};

const reset_ricerca = function (
    icona_ricerca,
    icona_reset,
    input,
    episodi,
    nessun_risultato
) {
    input.value = "";
    icona_reset.classList.add("non-visibile");
    icona_ricerca.classList.remove("non-visibile");

    for (let i = 0; i < episodi.length; i++) {
        episodi[i].classList.remove("non-visibile");
    }

    nessun_risultato.classList.add("non-visibile");
};

const input_episodi = document.querySelector("#input-episodi");
const avvia_ricerca = document.querySelector("#cerca-episodi");
let lista_episodi = document.querySelectorAll("#episodio-pubblico");
let nessun_risultato = document.querySelector("#nessun-risultato");

avvia_ricerca.addEventListener("click", (event) => {
    event.preventDefault();

    let icona_ricerca = document.querySelector("#search-icon");
    let icona_reset = document.querySelector("#cancel-icon");

    let richiesta = input_episodi.value.toLowerCase();

    // Dopo una ricerca appare una X al posto della lente di ingrandimento
    // L'input viene prima liberato prima di iniziare una nuova ricerca
    let reset =
        !icona_reset.classList.contains("non-visibile") || richiesta == "";

    if (reset) {
        return reset_ricerca(
            icona_ricerca,
            icona_reset,
            input_episodi,
            lista_episodi,
            nessun_risultato
        );
    } else {
        icona_reset.classList.remove("non-visibile");
        icona_ricerca.classList.add("non-visibile");
    }

    let eliminati = calcola_eliminati(lista_episodi);

    for (let i = 0; i < lista_episodi.length; i++) {
        let titolo =
            lista_episodi[i].getElementsByClassName("titolo-episodio")[0];
        let descrizione = lista_episodi[i].getElementsByClassName(
            "descrizione-episodio"
        )[0];

        let testo_titolo = titolo.textContent || titolo.innerHTML;
        let testo_descrizione =
            descrizione.textContent || descrizione.innerHTML;

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
            if (!reset && !in_titolo && !in_descrizione) {
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
