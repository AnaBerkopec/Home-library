/*jslint devel: true */
function check() {
    'use strict';
    console.log("check")
    if (document.getElementById('password1').value !== document.getElementById('password2').value) {
        alert("Gesli se ne ujemata!");
        return false;
    }
    console.log("after if")
    var x;
    if (confirm("Ste prepričani da se želite odjaviti?") === true) {
        return true;
    } else {
        return false;
    }
}