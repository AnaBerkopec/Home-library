/*jslint devel: true */
function check() {
    'use strict';
    if (document.getElementById('oldpassword').value === document.getElementById('newpassword1').value) {
        alert("Novo in staro geslo ne smeta biti enaka!");
        return false;
    }
    if (document.getElementById('newpassword2').value !== document.getElementById('newpassword1').value) {
        alert("Novi gesli se ne ujemata!");
        return false;
    }
}