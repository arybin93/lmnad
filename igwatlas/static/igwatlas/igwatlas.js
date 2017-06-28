"use strict";

var myMap;

// Waiting for the API to load and DOM to be ready.
ymaps.ready(init);

$(document).ready(function(){
    $('.datepicker').datepicker();

    $(".js-example-basic-multiple").select2({
        placeholder: "Select types"
    });

    $("#search_btn").click(function(event) {
        console.log('search');
        // request to server with params
        event.preventDefault();
    })
});

function init () {
     myMap = new ymaps.Map(
        'map',
        {
            center: [53.97, 148.50],
            zoom: 5,
            type: 'yandex#satellite',
            controls: ['zoomControl', 'fullscreenControl']
        }
    );

     var objectManager = new ymaps.ObjectManager({
         clusterize: true,
         gridSize: 32,
         clusterDisableClickZoom: true
     });
     myMap.geoObjects.add(objectManager);

     $.ajax({
        url: "http://localhost:8000/api/v1/records/get_records/?api_key=d837d31970deb03ee35c416c5a66be1bba9f56d3"
    }).done(function(data) {
        console.log(data);
        objectManager.add(data);
    });
}