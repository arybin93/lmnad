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
    var maxRow = $('#max_row');

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
                        var data = response;
                        update_page(PARSE_FILE, data)
                    }, error: function(){
                        console.log("not okay");
                    }
                });
            }
        });
    } else if (current_state == PARSE_FILE) {
        console.log('Parse file');
        loadFileRow.hide();
        parseFileRow.show();
        console.log(data);
        if (data['success'] == true) {
            $.each(data['result'], function(index, value) {
                console.log(value);
                loadedDataTable.append('<tr>' + '<th scope="row">' + value +'</th>' + '</tr>');
            });
            maxRow.html('Всего строк: ' + data['max_row']);
        } else {
            maxRow.html(data['max_row']);
        }
    }
}


$(document).ready(function() {
    console.log('ready');
    var state = LOAD_FILE;
    update_page(state);
});