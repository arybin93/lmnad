"use strict";

const JOURNAL = 'journal';
const CONFERENCE = 'conference';

function update_form() {
    var value = $("#id_type").find(":selected").val();
    var confType = $("#div_id_conf_type");
    var dateStart = $("#div_id_date_start");
    var dateStop = $("#div_id_date_stop");
    var place = $("#div_id_place");
    var organizer = $("#div_id_organizer");

    if (value == JOURNAL) {
        confType.hide();
        dateStart.hide();
        dateStop.hide();
        place.hide();
        organizer.hide();
    } else {
        confType.show();
        dateStart.show();
        dateStop.show();
        place.show();
        organizer.show();
    }
}


$(document).ready(function() {
   console.log('Journals');

   var type = $("#id_type");
   update_form();

   type.change(function() {
       update_form();
   });
});