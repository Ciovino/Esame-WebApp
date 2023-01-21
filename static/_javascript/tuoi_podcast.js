"use strict;";

const calcola_eliminati = function (podcast) {
    let eliminati = 0;
    for (let i = 0; i < podcast.length; i++) {
        if (podcast[i].classList.contains("non-visibile")) {
            eliminati++;
        }
    }
    return eliminati;
};

const reset_ricerca = function (
    icona_ricerca,
    icona_reset,
    input,
    podcast,
    nessun_risultato,
    posizione_originale,
    destinazione,
    nuovo_podcast,
    go_back_link
) {
    input.value = "";
    icona_reset.classList.add("non-visibile");
    icona_ricerca.classList.remove("non-visibile");

    for (let i = 0; i < podcast.length; i++) {
        podcast[i].classList.remove("non-visibile");
    }

    if (!nessun_risultato.classList.contains("non-visibile")) {
        nessun_risultato.classList.add("non-visibile");

        destinazione.removeChild(nuovo_podcast);
        posizione_originale.appendChild(nuovo_podcast);
    }
};

let input = document.querySelector("#input-tuoi-podcast");
const avvia_ricerca = document.querySelector("#cerca-podcast");
let lista_podcast = document.querySelectorAll(".tutti-podcast");
let nessun_risultato = document.querySelector("#nessun-risultato");

let posizione_originale = document.querySelector(".immagini-podcast");
let nuovo_podcast = document.querySelector("#card-nuovo-podcast");
let go_back_link = document.querySelector("#go-back");
let destinazione = document.querySelector("main");

avvia_ricerca.addEventListener("click", (event) => {
    event.preventDefault();

    let icona_ricerca = document.querySelector("#search-icon");
    let icona_reset = document.querySelector("#cancel-icon");

    let richiesta = input.value.toLowerCase();

    // Dopo una ricerca appare una X al posto della lente di ingrandimento
    // L'input viene prima liberato prima di iniziare una nuova ricerca
    let reset =
        !icona_reset.classList.contains("non-visibile") || richiesta == "";

    if (reset) {
        return reset_ricerca(
            icona_ricerca,
            icona_reset,
            input,
            lista_podcast,
            nessun_risultato,
            posizione_originale,
            destinazione,
            nuovo_podcast
        );
    } else {
        icona_reset.classList.remove("non-visibile");
        icona_ricerca.classList.add("non-visibile");
    }

    let eliminati = calcola_eliminati(lista_podcast);

    for (let i = 0; i < lista_podcast.length; i++) {
        let titolo = lista_podcast[i].getElementsByClassName("card-title")[0];
        let descrizione =
            lista_podcast[i].getElementsByClassName("card-text")[0];

        let testo_titolo = titolo.textContent || titolo.innerHTML;
        let testo_descrizione =
            descrizione.textContent || descrizione.innerHTML;

        let in_titolo = testo_titolo.toLowerCase().indexOf(richiesta) > -1;
        let in_descrizione =
            testo_descrizione.toLowerCase().indexOf(richiesta) > -1;
        let gia_eliminato = lista_podcast[i].classList.contains("non-visibile");

        if (gia_eliminato) {
            if (in_titolo || in_descrizione) {
                lista_podcast[i].classList.remove("non-visibile");
                eliminati--;
            }
        } else {
            if (!reset && !in_titolo && !in_descrizione) {
                lista_podcast[i].classList.add("non-visibile");
                eliminati++;
            }
        }
    }

    if (eliminati == lista_podcast.length) {
        destinazione.insertBefore(nuovo_podcast, go_back_link);
        nessun_risultato.classList.remove("non-visibile");
    } else {
        destinazione.removeChild(nuovo_podcast);
        posizione_originale.appendChild(nuovo_podcast);
        nessun_risultato.classList.add("non-visibile");
    }
});
