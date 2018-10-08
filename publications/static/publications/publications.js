"use strict";

const MAIN_URL = window.location.protocol + "//" + window.location.host + "/api/v1/publication";
const KEY = 'd837d31970deb03ee35c416c5a66be1bba9f56d3';


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
    var fieldJournal = $("#div_id_journal");
    var fieldVolume = $("#div_id_volume");
    var fieldIssue = $("#div_id_issue");
    var fieldPages = $("#div_id_pages");
    var fieldNumber = $("#div_id_number");
    var fieldDOI = $("#div_id_doi");
    var fieldRINC = $("#div_id_is_rinc");
    var fieldVAK = $("#div_id_is_vak");
    var fieldWOS = $("#div_id_is_wos");
    var fieldSCOPUS = $("#div_id_is_scopus");
    var fieldOther = $("#div_id_is_other_db");
    var conferenceAuthor = $("#div_id_conference_author");

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
        conferenceAuthor.show()
    } else {
        conferenceAuthor.hide()
    }
}


$(document).ready(function() {
   console.log('Publications');

   var type = $("#id_type");
   update_form();

   type.change(function() {
       update_form();
   });
});