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
    var fieldShortName = $(document).find('.field-short_name');
    var fieldDescription = $(document).find('.field-description');
    var fieldConfLink = $(document).find('.field-conf_link');
    var fieldConfCheckbox = $(document).find('.field-conf_checkbox');
    var fieldFiles = $(document).find('#files-group');

    if (value == JOURNAL) {
        fieldConfType.hide();
        fieldDateStart.hide();
        fieldDateStop.hide();
        fieldPlace.hide();
        fieldOrganizer.hide();
        fieldShortName.hide();
        fieldDescription.hide();
        fieldConfLink.hide();
        fieldConfCheckbox.hide();
        fieldFiles.hide()
    } else {
        fieldConfType.show();
        fieldDateStart.show();
        fieldDateStop.show();
        fieldPlace.show();
        fieldOrganizer.show();
        fieldShortName.show();
        fieldDescription.show();
        fieldConfLink.show();
        fieldConfCheckbox.show();
        fieldFiles.show()
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