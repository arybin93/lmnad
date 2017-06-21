"use strict";

var myMap;

// Waiting for the API to load and DOM to be ready.
ymaps.ready(init);

function init () {
     myMap = new ymaps.Map(
        'map',
        {
            center: [55.76, 37.64],
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