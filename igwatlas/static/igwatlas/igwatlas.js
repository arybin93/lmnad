"use strict";

var myMap;

// Waiting for the API to load and DOM to be ready.
ymaps.ready(init);

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
        url: "http://lmnad.nntu.ru/api/v1/records/?api_key=d837d31970deb03ee35c416c5a66be1bba9f56d3"
     }).done(function(data) {
        objectManager.add(data);
     });

     // search form
     $('.datepicker').datepicker();

    var types_multi_select = $(".types_multiple").select2({
        placeholder: "Select types",
        allowClear: true
    });
    var source_value = $('#id_label_sources');

    $("#search_btn").click(function(event) {

        var types_array = types_multi_select.val();

        var types = '';
        for(var i = 0; i < types_array.length; i++) {
            if (types_array.length == 1) {
                types = types_array[i]
            } else {
                types += types_array[i] + ',';
            }
        }

        // send request with params
        $.ajax({
            url: "http://lmnad.nntu.ru/api/v1/records/?api_key=",
            type: 'get',
            data: {
                api_key: 'd837d31970deb03ee35c416c5a66be1bba9f56d3',
                types: types,
                date_from: $('#date_from').val(),
                date_to: $('#date_to').val(),
                source_text: source_value.val()
            }
        }).done(function(data) {
            console.log('done');
            myMap.geoObjects.removeAll();
            objectManager.removeAll();
            console.log(data);
            myMap.geoObjects.add(objectManager);
            objectManager.add(data);
        });

        event.preventDefault();
    });

    $("#search_cancel").click(function(event) {
        console.log('reset');
        // close and clear, and get all records
        $('#date_from').val('');
        $('#date_to').val('');
        types_multi_select.val([]);
        $(".types_multiple").select2({
            placeholder: "Select types",
            allowClear: true
        });
        source_value.val('');
        reset_request()
    });

    function reset_request() {
        $.ajax({
            url: "http://lmnad.nntu.ru/api/v1/records/?api_key=d837d31970deb03ee35c416c5a66be1bba9f56d3"
        }).done(function(data) {
            myMap.geoObjects.removeAll();
            objectManager.removeAll();
            myMap.geoObjects.add(objectManager);
            objectManager.add(data);
        });
    }
}
