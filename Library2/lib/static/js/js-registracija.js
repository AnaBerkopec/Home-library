/*jslint devel: true */
function check() {
    'use strict';
    if (document.getElementById('geslo2').value !== document.getElementById('geslo').value) {
        alert("Gesli se ne ujemata!");
        return false;
    }
}