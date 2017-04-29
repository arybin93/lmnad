"use strict";

$(document).ready(function(){
    console.log("lang!");

    var user_language = window.navigator.userLanguage || window.navigator.language;
    console.log(user_language);
});


