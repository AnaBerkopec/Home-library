/*jslint devel: true */

function openNav() {
    'use strict';
    document.getElementById("mySidenav").style.width = "200px";
}
function closeNav() {
    'use strict';
    document.getElementById("mySidenav").style.width = "0";
}
function odjava() {
    'use strict';
    var x;
    if (confirm("Ste prepričani da se želite odjaviti?") === true) {
        return true;
    } else {
        return false;
    }
}