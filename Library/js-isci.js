/*jslint devel: true */
function izposoja() {
    'use strict';
    var x;
    if (confirm("Izposodili si boste izbrano knjigo.") === true) {
        x = "Knjiga izposojena!";
    } else {
        x = "Izposoja prekinjena.";
    }
    document.getElementById("demo").innerHTML = x;
}