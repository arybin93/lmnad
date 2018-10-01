"use strict";

const ARTICLE = 'Article';
const MONOGRAPH = 'Monograph';
const GROUP_MONOGRAPH = 'Group Monograph';
const PROCEEDINGS = 'Proceedings';
const THESES_CONFERENCE = 'Theses conference';
const TEACHING_MATERIALS = 'Teaching materials';
const PATENT = 'Patent';
const PATENT_BD = 'Patent_BD';


function update_form() {
    var value = $("#id_type").find(":selected").val();
    var fieldJournal = $(document).find('.field-journal');
    var fieldVolume = $(document).find('.field-volume');
    var fieldIssue = $(document).find('.field-issue');
    var fieldPages = $(document).find('.field-pages');
    var fieldNumber = $(document).find('.field-number');
    var fieldDOI = $(document).find('.field-doi');
    var fieldRINC = $(document).find('.field-is_rinc');
    var fieldVAK = $(document).find('.field-is_vak');
    var fieldWOS = $(document).find('.field-is_wos');
    var fieldSCOPUS = $(document).find('.field-is_scopus');
    var fieldOther = $(document).find('.field-is_other_db');
    var inlineConference = $(document).find('#conference-group');


    if (value == PATENT || value == PATENT_BD ) {
        fieldJournal.hide();
        fieldVolume.hide();
        fieldIssue.hide();
        fieldPages.hide();
        fieldNumber.show();
        fieldDOI.hide();
        fieldRINC.hide();
        fieldVAK.hide();
        fieldWOS.hide();
        fieldSCOPUS.hide();
        fieldOther.hide();
    } else {
        fieldJournal.show();
        fieldVolume.show();
        fieldIssue.show();
        fieldPages.show();
        fieldNumber.hide();
        fieldDOI.show();
        fieldRINC.show();
        fieldVAK.show();
        fieldWOS.show();
        fieldSCOPUS.show();
        fieldOther.show();
    }

    if (value == PROCEEDINGS || value == THESES_CONFERENCE) {
        inlineConference.show();
    } else {
        inlineConference.hide();
    }
}

$(document).ready(function() {
   console.log('Publications Admin');
   var type = $("#id_type");
   update_form();

   type.change(function() {
       update_form();
   });
});