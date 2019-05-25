"use strict";

var myMap;
var RECORDS_URL = 'http://localhost:8000/api/v1/records/?api_key=d837d31970deb03ee35c416c5a66be1bba9f56d3';
var SOURCE_URL = 'http://localhost:8000/api/v1/sources/?api_key=d837d31970deb03ee35c416c5a66be1bba9f56d3';
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
        /*console.log(event.target.checked);
        console.log(typeof event.target.checked);
        console.log(event.target.checked == true);
        if (event.target.checked == true) {
            date_value.hide();
            date_from_value.show();
            date_to_value.show();
        }*/
       date_value.hide();
       date_from_value.hide();
       date_to_value.hide();
    });
    myMap = new ymaps.Map(
        'map',
        {
            center: [53.97, 148.50],
            zoom: 5,
            type: 'yandex#satellite',
            controls: ['zoomControl', 'fullscreenControl']
        }
    );

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
        clusterize: true,
        gridSize: 32,
        clusterDisableClickZoom: true
    });
    myMap.geoObjects.add(objectManager);

    fetchData(objectManager, RECORDS_URL);

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
                    api_key: 'd837d31970deb03ee35c416c5a66be1bba9f56d3',
                    types: types,
                    date_from: $('#date_from').val(),
                    date_to: $('#date_to').val(),
                    source_text: source_value.val()
                }
            }).done(function (data) {
                objectManager.add(data['results']);
                console.log(data);
                if (data['next']) {
                    fetchSearchData(data['next'])
                }
            });
        }

        fetchSearchData('http://localhost:8000/api/v1/records/?api_key=');

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
        $.ajax({
            url: url
        }).done(function (data) {
            objectManager.add(data['results']);
            console.log(data);
            if (data['next']) {
                fetchData(objectManager, data['next'])
            }
        });
    }

    //handler right click
    myMap.events.add('click', function (e) {
        myMap.hint.open(e.get('coords'), 'Create new record');
        $("#create").modal();

        $('#id_for_source').select2({
            ajax: {
                url: SOURCE_URL,
                data: function (params) {
                    var query = {
                        query: params.term,
                        page: params.page || 1
                    }
                    return query;
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

        $("#add_record_button").click(function (event) {
            var types_value = $('#id_for_types');
            var date_value = $('#id_for_date');
            var image_value = $('#id_for_image');
            var page_value = $('#id_for_page');

            var source = $('#id_for_source').find(':selected');

            var image = image_value[0].files;
            var formData = new FormData();
            formData.append('api_key', 'd837d31970deb03ee35c416c5a66be1bba9f56d3');
            formData.append('latitude', e.get('coords')[0]);
            formData.append('longitude', e.get('coords')[1]);
            formData.append('types', types_value.val());
            formData.append('image', image[0]);
            formData.append('source', source.val());
            formData.append('page', page_value.val());
            formData.append('date', date_value.val());
            if (formData) {
                $.ajax({
                    url: 'http://localhost:8000/api/v1/records/',
                    method: 'post',
                    processData: false,
                    contentType: false,
                    data: formData,
                    enctype: 'multipart/form-data',
                    success: function (response) {
                        console.log(response)
                    }, error: function () {
                        alert("INTERNAL SERVER ERROR: please write to arybin93@gmail.com");
                    }
                });
            }
            event.preventDefault();

        });

    });
    window.alert = null
    $(document).ready(function () {
        $("#add_record_button").click(function () {
            $('#success-alert').removeClass('hidden');
        });

        $(".close").click(function () {
            $("#success-alert").addClass('hidden');
        });
    });
}


