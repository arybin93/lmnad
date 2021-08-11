"use strict";

var myMap;

const API_KEY = 'd837d31970deb03ee35c416c5a66be1bba9f56d3'

var RECORDS_URL = `/api/v1/records/?api_key=${API_KEY}`;
var SOURCE_URL = `/api/v1/sources/?api_key=${API_KEY}`;
var ADD_RECORD_URl = `/api/v1/records/${API_KEY}`;
var current_coordinates = null;

// Waiting for the API to load and DOM to be ready.
ymaps.ready(init);


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function init() {
    $("#checkbox_for_date_range").click(function (event) {
        var date_value = $('#id_control_date');
        var date_from_value = $('#id_control_date_from');
        var date_to_value = $('#id_control_date_to');
        if (event.target.checked) {
            date_value.hide();
            date_from_value.show();
            date_to_value.show();
        } else {
            date_value.show();
            date_from_value.hide();
            date_to_value.hide();
        }
    })

    myMap = new ymaps.Map('map', {
            center: [53.97, 148.50],
            zoom: 5,
            type: 'yandex#satellite',
            controls: ['zoomControl', 'fullscreenControl', 'rulerControl']
        });

    var coord_lat = $("#coords_lat")
    var coord_lon = $("#coords_lon")
    var source_id = $('#source_link_id');
    myMap.events.add('mousemove', function (e) {
        coord_lat.text(Number.parseFloat(e.get('coords')[0]).toPrecision(5))
        coord_lon.text(Number.parseFloat(e.get('coords')[1]).toPrecision(5))
    });

    //set CSRF token
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var objectManager = new ymaps.ObjectManager({
        clusterize: document.getElementById("cluster-checkbox").checked,
        gridSize: 32,
        geoObjectOpenBalloonOnClick: false,
        clusterDisableClickZoom: false,
        clusterIconLayout: 'default#pieChart',
        clusterIconPieChartRadius: 25,
        clusterIconPieChartCoreRadius: 10,
        clusterIconPieChartStrokeWidth: 3,
    });
    objectManager.objects.options.set({
        preset: 'islands#blueCircleIcon'
    });

    myMap.geoObjects.add(objectManager);

    fetchData(objectManager, RECORDS_URL);

    // Function that emulates a request for data to the server.
    function loadBalloonData (objectId) {
        $.ajax({
            url: '/api/v1/records/' + objectId + '/',
            type: 'get',
            data: {
                api_key: API_KEY,
                is_yandex_map_labels: document.getElementById("labels-checkbox").checked | 0
            }
        }).done(function (data) {
            console.log(data);
            var obj = objectManager.objects.getById(objectId);
            obj.properties.balloonContentHeader = data['properties']['balloonContentHeader'];
            obj.properties.balloonContentBody = data['properties']['balloonContentBody'];
            obj.properties.balloonContentFooter = data['properties']['balloonContentFooter'];
            obj.properties.clusterCaption = data['properties']['clusterCaption'];
            objectManager.objects.balloon.open(objectId);
        });
    }

    function hasBalloonData (objectId) {
        var object = objectManager.objects.getById(objectId);
        return objectManager.objects.getById(objectId).properties.balloonContent;
    }
    // Upload data by click
    objectManager.objects.events.add('click', function (e) {
        var objectId = e.get('objectId');
        if (hasBalloonData(objectId)) {
            objectManager.objects.balloon.open(objectId);
        } else {
            loadBalloonData(objectId);
        }
    });


    // search form
    $('.datepicker').datepicker();

    var types_multi_select = $(".types_multiple").select2({
        placeholder: "Select types",
        allowClear: true
    });
    var source_value = $('#id_label_sources');

    $("#search_btn").click(function (event) {

        var types_array = types_multi_select.val();

        var types = '';
        for (var i = 0; i < types_array.length; i++) {
            if (types_array.length == 1) {
                types = types_array[i]
            } else {
                types += types_array[i] + ',';
            }
        }

        myMap.geoObjects.removeAll();
        objectManager.removeAll();
        myMap.geoObjects.add(objectManager);

        function fetchSearchData(url) {
            // send request with params
            $.ajax({
                url: url,
                type: 'get',
                data: {
                    api_key: API_KEY,
                    types: types,
                    date_from: $('#date_from').val(),
                    date_to: $('#date_to').val(),
                    source_text: source_value.val(),
                    source_id: source_id.val(),
                    is_yandex_map_labels: document.getElementById("labels-checkbox").checked | 0
                }
            }).done(function (data) {
                objectManager.add(data['results']);
                console.log(data);
                if (data['next']) {
                    fetchSearchData(data['next'])
                }
            });
        }

        fetchSearchData('/api/v1/records/?api_key=');

        event.preventDefault();
    });

    $("#search_cancel").click(function (event) {
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
        myMap.geoObjects.removeAll();
        objectManager.removeAll();
        myMap.geoObjects.add(objectManager);
        fetchData(objectManager, RECORDS_URL);
    }

    function fetchData(objectManager, url) {
        var info = $("#info")
        info.text('Please wait. Points are loading...')
        $.ajax({
            url: url,
            data: {
                source_id: source_id.val(),
                is_yandex_map_labels: document.getElementById("labels-checkbox").checked | 0
            }
        }).done(function (data) {
            objectManager.add(data['results']);
            console.log(data);
            if (data['next']) {
                fetchData(objectManager, data['next'])
            } else {
                info.text('')
            }
        });
    }

    function clearFormCreate(){
        var types_el = $('#id_for_types');
        types_el.val([]);
        types_el.select2({
            placeholder: "Select types",
            allowClear: true
        });
        $('#id_for_date').val('');
        $('#id_for_image').val('');
        $('#id_for_page').val('');
        $('#id_for_date_from').val('');
        $('#id_for_date_to').val('');
        $('#id_for_source').val('');
        $('#checkbox_for_date_range').removeAttr('checked');
    }

    // handler left click
    myMap.events.add('click', function (e) {
        $("#create").modal();
        console.log('Open modal dialog');
        current_coordinates = e.get('coords');

        $('#id_for_source').select2({
            ajax: {
                url: SOURCE_URL,
                data: function (params) {
                    return {
                        query: params.term,
                        page: params.page || 1
                    }
                },
                processResults: function (data, params) {
                    // parse the results into the format expected by Select2
                    // since we are using custom formatting functions we do not need to
                    // alter the remote JSON data, except to indicate that infinite
                    // scrolling can be used
                    params.page = params.page || 1;
                    console.log(data);
                    var results = $.map(data.results, function (obj) {
                        obj.text = obj.source; // replace name with the property used for the text
                        return obj;
                    });
                    return {
                        results: results,
                        pagination: {
                            more: (params.page * 30) < data.total_count
                        }
                    };
                }
            }
        });
    });

    // Handler for Add New Record
    $("#add_record_button").click(function (event) {
        console.log('Click add record button');
        event.preventDefault();
        var types_value = $('#id_for_types');
        var date_value = $('#id_for_date');
        var image_value = $('#id_for_image');
        var page_value = $('#id_for_page');
        var date_from_value = $('#id_for_date_from');
        var date_to_value = $('#id_for_date_to');
        var checkbox_value = $('#checkbox_for_date_range');

        var source = $('#id_for_source').find(':selected');

        var image = image_value[0].files;
        var formData = new FormData();
        formData.append('api_key', API_KEY);
        formData.append('latitude', current_coordinates[0]);
        formData.append('longitude', current_coordinates[1]);
        formData.append('types', types_value.val());
        formData.append('image', image[0]);
        formData.append('source', source.val());
        formData.append('page', page_value.val());
        if (checkbox_value[0].checked) {
            formData.append('date_start', date_from_value.val());
            formData.append('date_stop', date_to_value.val());
        }
        else {
            formData.append('date', date_value.val());
        }

        if (formData) {
            $.ajax({
                url: ADD_RECORD_URl,
                method: 'post',
                processData: false,
                contentType: false,
                data: formData,
                enctype: 'multipart/form-data',
                success: function (response) {
                    console.log(response);
                    if (response['success']) {
                        $('#success-alert').removeClass('hidden');
                        clearFormCreate();
                    } else {
                        alert(response['reason'])
                    }
                    current_coordinates = null;
                }, error: function (response) {
                    alert("INTERNAL SERVER ERROR: please write to arybin93@gmail.com");
                }
            });
        }
    });

    $(".close").click(function () {
        $("#success-alert").addClass('hidden');
    });

    $("#cluster-checkbox").click(function (event) {
        var url = window.location.href;

        if (url.indexOf('?') > -1){
            if (url.indexOf('clusterize') !== -1) {
                if (event.target.checked) {
                    url = url.replace('clusterize=false','clusterize=true');
                } else {
                    url = url.replace('clusterize=true','clusterize=false');
                }
            } else {
                url += `&clusterize=${event.target.checked}`
            }
        } else {
           url += `?clusterize=${event.target.checked}`
        }

        location.replace(url)
    });

    $("#labels-checkbox").click(function (event) {
        // Update all items
        reset_request()
    });
}
