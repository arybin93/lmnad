"use strict";

const JOURNAL = 'journal';
const CONFERENCE = 'conference';


function update_form() {
    var value = $("#id_type").find(":selected").val();
    var fieldConfType = $(document).find('.field-conf_type');
    var fieldDateStart = $(document).find('.field-date_start');
    var fieldDateStop = $(document).find('.field-date_stop');
    var fieldPlace = $(document).find('.field-place');
    var fieldOrganizer = $(document).find('.field-organizer');

    if (value == JOURNAL) {
        fieldConfType.hide();
        fieldDateStart.hide();
        fieldDateStop.hide();
        fieldPlace.hide();
        fieldOrganizer.hide()
    } else {
        fieldConfType.show();
        fieldDateStart.show();
        fieldDateStop.show();
        fieldPlace.show();
        fieldOrganizer.show()
    }
}


$(document).ready(function() {
   console.log('Journals Admin');
   var type = $("#id_type");
   update_form();

   type.change(function() {
       update_form();
   });
});