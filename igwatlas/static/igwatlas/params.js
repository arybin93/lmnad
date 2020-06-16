"use strict";

var myMap;
var PARAMS_URL = 'http://localhost:8000/api/v1/wave_params/?api_key=d837d31970deb03ee35c416c5a66be1bba9f56d3';

// Waiting for the API to load and DOM to be ready.
ymaps.ready(init);

function init () {

     myMap = new ymaps.Map(
        'map-params',
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
     fetchData(objectManager, PARAMS_URL);

     // search form
     $('.datepicker').datepicker();

    var types_multi_select = $(".types_multiple").select2({
        placeholder: "Select type",
        allowClear: true
    });

    $("#search_btn").click(function(event) {

        myMap.geoObjects.removeAll();
        objectManager.removeAll();
        myMap.geoObjects.add(objectManager);

        function fetchSearchData(url) {
            // send request with params
            $.ajax({
                url: url,
                type: 'get',
                data: {
                    api_key: 'd837d31970deb03ee35c416c5a66be1bba9f56d3',
                    wave_types: $('#id_label_types').val()[0],
                    mode: $('#wave_mode').val(),
                    amplitude_from: $('#wave_amplitude_from').val(),
                    amplitude_to: $('#wave_amplitude_to').val(),
                    period_from: $('#wave_period_from').val(),
                    period_to: $('#wave_period_to').val(),
                    date_from: $('#date_from').val(),
                    date_to: $('#date_to').val(),
                }
            }).done(function(data) {
                objectManager.add(data);
                console.log(data);
            });
        }

        fetchSearchData('http://localhost:8000/api/v1/wave_params/');
        console.log($('#id_label_types').val()[0]);
        event.preventDefault();
    });

    $("#search_cancel").click(function(event) {
        console.log('reset');
        // close and clear, and get all records
        types_multi_select.val([]);
        $(".types_multiple").select2({
            placeholder: "Select type",
            allowClear: true
        });
        $('#id_label_types').val('');
        $('#wave_mode').val('');
        $('#wave_amplitude_from').val('');
        $('#wave_amplitude_to').val('');
        $('#wave_period_from').val('');
        $('#wave_period_to').val('');
        $('#date_from').val('');
        $('#date_to').val('');
        reset_request()
    });

    function reset_request() {
        myMap.geoObjects.removeAll();
        objectManager.removeAll();
        myMap.geoObjects.add(objectManager);
        fetchData(objectManager, PARAMS_URL);
    }
    function fetchData(objectManager, url) {
        $.ajax({
            url: url
        }).done(function(data) {
            console.log(data);
            objectManager.add(data);
        });
    }

//    function fetchData(objectManager, url) {
//        $.ajax({
//            url: url
//        }).done(function(data) {
//            objectManager.add({
//                type: 'Feature',
//                id: data[0]['id'],
//                geometry: {
//                type: 'Point',
//                coordinates: [data[0]['lat'], data[0]['lon']]
//                },
//        properties: {
//        hintContent: 'Содержание всплывающей подсказки',
//        balloonContent: 'Содержание балуна'
//        }
//         });
//
//            //if (data['next']) {
//           //     fetchData(objectManager, data['next'])
//           // }
//        });
//    }
}
