"use strict";

const MAIN_URL = window.location.protocol + "//" + window.location.host + "/api/v1/";
const KEY = 'd837d31970deb03ee35c416c5a66be1bba9f56d3';
const LOAD_FILE = 'LOAD_FILE';
const PARSE_FILE = 'PARSE_FILE';


function update_page(current_state, data) {
    var loadFileRow = $('#load-file-row');
    var parseFileRow = $('#parse-file-row');
    var inputFile = $('#load-file-input');
    var loadedDataTable = $('#loaded-data-table');
    var separator = $('#separator');
    var name = $('#name-calculation');
    var maxRow = $('#max_row');
    var mappingFields = $('#mapping-data-table');

    if (current_state == LOAD_FILE) {
         // load file to server
        loadFileRow.show();
        parseFileRow.hide();
        $("#submit-load-file").click(function(event) {
            event.preventDefault();
            // Get the selected files from the input.
            var files = inputFile[0].files;
            // Create a new FormData object.
            var formData = new FormData();
            formData.append('file', files[0]);
            formData.append('separator', separator.val());
            formData.append('name', name.val());
            formData.append('api_key', KEY);
            if (formData) {
                $.ajax({
                    url: MAIN_URL + 'calculation/load_file/',
                    method: 'post',
                    processData: false,
                    contentType: false,
                    cache: false,
                    data: formData,
                    enctype: 'multipart/form-data',
                    success: function(response){
                        console.log("file successfully submitted");
                        update_page(PARSE_FILE, response);
                    }, error: function(){
                        alert("INTERNAL SERVER ERROR: please write to arybin93@gmail.com");
                    }
                });
            }
        });
    } else if (current_state == PARSE_FILE) {
        console.log('Parse file');
        loadFileRow.hide();
        parseFileRow.show();
        var first_row = '';
        if (data['success'] == true) {
            $.each(data['result'], function(index, value) {
                if (index == 0) {
                    first_row = value;
                }
                var tr = $(document.createElement('tr'));
                $.each(value, function(index, value) {
                    tr.append('<th scope="row">' + value +'</th>');
                });
                loadedDataTable.append(tr);
            });
            maxRow.html('Всего строк: ' + data['max_row']);

            // mappingFields
            $.each(first_row, function(index, value) {
                var tr = $(document.createElement('tr'));
                tr.append('<td scope="row"><h4>' + value +'</h4></td>');
                var id = 'field-' + index;
                tr.append('<td scope="row"><div class="form-group">' +
                    '<div class="form-group">' +
                    '<select class="form-control" id='+ id + '>' +
                    '<option value="lon">Longitude</option>' +
                    '<option value="lat">Latitude</option>' +
                    '<option value="max_depth">Max depth</option>' +
                    '<option value="depth">Depth</option>' +
                    '<option value="tempterature">Tempterature</option>' +
                    '<option value="salinity">Salinity</option>' +
                    '<option value="density">Density</option>' +
                    '<option value="bvf">Brant-Vaisala Frequency</option>' +
                    '</select></div></div></td>');
                mappingFields.append(tr);

                $("#submit-parse-file").click(function(event) {
                    event.preventDefault();
                    loadFileRow.hide();
                    parseFileRow.hide();
                });
            });
        } else {
            maxRow.html(data['max_row']);
        }
    }
}


$(document).ready(function() {
    console.log('ready');
    var state = LOAD_FILE;

    var loadTab = $('#load-file-tab');
    var parseTab = $('#parse-file-tab');
    var startTab = $('#start-tab');
    var resultsTab = $('#results-tab');
    console.log(loadTab);
    loadTab.click(function(event) {
        event.preventDefault();
        console.log('Load tab');
    });
    parseTab.click(function(event) {
        event.preventDefault();
        console.log('Parse tab');
    });
    startTab.click(function(event) {
        event.preventDefault();
        console.log('Start tab');
    });
    resultsTab.click(function(event) {
        event.preventDefault();
        console.log('Result tab');
    });

    update_page(state);
});