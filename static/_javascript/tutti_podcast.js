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

const input = document.querySelector("#input-tutti-podcast");
let lista_podcast = document.querySelectorAll(".tutti-podcast");
let nessun_risultato = document.querySelector("#nessun-risultato");

input.addEventListener("input", (event) => {
    event.preventDefault();

    let richiesta = input.value.toLowerCase();
    let eliminati = calcola_eliminati(lista_podcast);

    for (let i = 0; i < lista_podcast.length; i++) {
        let titolo = lista_podcast[i].getElementsByClassName("card-title")[0];
        let descrizione =
            lista_podcast[i].getElementsByClassName("card-text")[0];

        let testo_titolo = titolo.textContent || titolo.innerHTML;
        let testo_descrizione =
            descrizione.textContent || descrizione.innerHTML;

        let reset = richiesta == "";
        let in_titolo = testo_titolo.toLowerCase().indexOf(richiesta) > -1;
        let in_descrizione =
            testo_descrizione.toLowerCase().indexOf(richiesta) > -1;
        let gia_eliminato = lista_podcast[i].classList.contains("non-visibile");

        if (gia_eliminato) {
            if (reset || in_titolo || in_descrizione) {
                lista_podcast[i].classList.remove("non-visibile");
                eliminati--;
            }
        } else {
            if (!reset && !in_titolo && !in_descrizione) {
                lista_podcast[i].classList.add("non-visibile");
                eliminati++;
            }
        }

        if (eliminati == lista_podcast.length) {
            nessun_risultato.classList.remove("non-visibile");
        } else {
            nessun_risultato.classList.add("non-visibile");
        }
    }
});
