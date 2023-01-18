"use strict;";

const input_episodi = document.querySelector("#input-episodi");
let lista_episodi = document.querySelectorAll("#episodio-pubblico");
let nessun_risultato = document.querySelector("#nessun-risultato");

input_episodi.addEventListener("input", (event) => {
    event.preventDefault();

    let richiesta = input_episodi.value.toLowerCase();

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

        let reset = richiesta == "";
        let in_titolo = testo_titolo.toLowerCase().indexOf(richiesta) > -1;
        let in_descrizione =
            testo_descrizione.toLowerCase().indexOf(richiesta) > -1;
        let gia_eliminato = lista_episodi[i].classList.contains("non-visibile");

        if (gia_eliminato) {
            if (reset || in_titolo || in_descrizione) {
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

    console.log(eliminati);
    if (eliminati == lista_episodi.length) {
        nessun_risultato.classList.remove("non-visibile");
    } else {
        nessun_risultato.classList.add("non-visibile");
    }
});

const calcola_eliminati = function (episodi) {
    let eliminati = 0;
    for (let i = 0; i < episodi.length; i++) {
        if (lista_episodi[i].classList.contains("non-visibile")) {
            eliminati++;
        }
    }
    return eliminati;
};
