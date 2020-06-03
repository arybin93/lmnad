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
     console.log('хочу спать');
     fetchData(objectManager, PARAMS_URL);

//     // search form
//     $('.datepicker').datepicker();
//
//    var types_multi_select = $(".types_multiple").select2({
//        placeholder: "Select types",
//        allowClear: true
//    });
//    var source_value = $('#id_label_sources');
//
//    $("#search_btn").click(function(event) {
//
//        var types_array = types_multi_select.val();
//
//        var types = '';
//        for(var i = 0; i < types_array.length; i++) {
//            if (types_array.length == 1) {
//                types = types_array[i]
//            } else {
//                types += types_array[i] + ',';
//            }
//        }
//
//        myMap.geoObjects.removeAll();
//        objectManager.removeAll();
//        myMap.geoObjects.add(objectManager);
//
//        function fetchSearchData(url) {
//            // send request with params
//            $.ajax({
//                url: url,
//                type: 'get',
//                data: {
//                    api_key: 'd837d31970deb03ee35c416c5a66be1bba9f56d3',
//                    wave_types: wave_types,
//                    mode: $$('#mode').val(),
//                    amplitude_from: $('#amplitude_from').val(),
//                    amplitude_to: $('#amplitude_to').val(),
//                    date_from: $('#date_from').val(),
//                    date_to: $('#date_to').val(),
//                    record: source_value.val()
//                }
//            }).done(function(data) {
//                objectManager.add(data['results']);
//                console.log(data);
//                if (data['next']) {
//                    fetchSearchData(data['next'])
//                }
//            });
//        }
//
//        fetchSearchData('http://localhost:8000/api/v1/wave_params/?api_key=');
//
//        event.preventDefault();
//    });
//
//    $("#search_cancel").click(function(event) {
//        console.log('reset');
//        // close and clear, and get all records
//        $('#mode').val('');
//        $('#amplitude_from').val('');
//        $('#amplitude_to').val('');
//        $('#date_from').val('');
//        $('#date_to').val('');
//        types_multi_select.val([]);
//        $(".types_multiple").select2({
//            placeholder: "Select types",
//            allowClear: true
//        });
//        source_value.val('');
//        reset_request()
//    });
//
//    function reset_request() {
//        myMap.geoObjects.removeAll();
//        objectManager.removeAll();
//        myMap.geoObjects.add(objectManager);
//        fetchData(objectManager, PARAMS_URL);
//    }
    function fetchData(objectManager, url) {
        $.ajax({
            url: url
        }).done(function(data) {
            console.log(data);
            objectManager.add(data['results']);
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
