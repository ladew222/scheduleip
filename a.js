const pageList = [
    {
        name: 'business-degree-completion',
        selector:'#elcn_academicprogramofinterestid',
        options: ["Accounting Degree Completion", "Business Leadership Degree Completion", "Health Care Management Degree Completion", "Degree Completion Undecided"],
    },
    {
        name: 'education-degree-completion',
        selector:'#elcn_academicprogramofinterestid',
        options: ["Elementary Education Degree Completion", "Elementary Education Degree Completion (MPS only)", "Degree Completion Undecided"],
    },
    {
        name: 'bachelor-science-nursing-completion',
        selector:'#elcn_academicprogramofinterestid',
        options: ["BSN Degree Completion", "BSN Degree Completion (WTC Dual Enrollment)", "Nursing Professional Pathways","Degree Completion Undecided"],
    },
    {
        name: 'social-work-degree-completion',
        selector:'#elcn_academicprogramofinterestid',
        options: ["Social Work Degree Completion", "Degree Completion Undecided"],
    },
]



function  get_url_title(url){
    return url.match(/[^\/]*$/);
}


function updateDrops(page_name) {
    var item=pageList.find(x => x.name == page_name);
    if (item){
        var cnt =0;
        $(item.selector).children('option').each(function(index, element) {
            // var curr_val = element.value;
            console.log(index);
            if (item.options.includes(element.text)){
                $(this).show();
                cnt++;
            }
            else{
                $(this).hide();
            }
        });
    }
}

function getUrlParameters(parameter, staticURL, decode){

    if (staticURL.length>1 && staticURL.indexOf("utm_source") ==-1){
        return false;
    }

    var currLocation = (staticURL.length)? staticURL : window.location.search,
        parArr = currLocation.split("?")[1].split("&"),
        returnBool = true;

    for(var i = 0; i < parArr.length; i++){
        parr = parArr[i].split("=");
        if(parr[0] == parameter){
            return (decode) ? decodeURIComponent(parr[1]) : parr[1];
            returnBool = true;
        }else{

            returnBool = true;
        }
    }

    if(!returnBool) return true;
}
/// redirect to visit calendar from Event link in recruit WFE
    if(window.location.href=="https://viterbo.elluciancrmrecruit.com/Apply/Events"){
        window.location.replace("https://www.viterbo.edu/visit");
    }

function getParentParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function getParentURLLast(url) {
    newres= url.lastIndexOf("/");
    console.log(newres);
    return newres;

}


function load_ga(){
    (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
        (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
        m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

    ga('create', 'UA-43891006-1', 'auto');
    ga('send', 'pageview');
}

function mod_css_shortform(){   // CAL and GRAD Shortform formatting
    $('.navbar').hide();
    //style
 //   $('#v45_ga_source').hidhttps://clguip.exchange.viterbo.edu:453/UI/home/index.htmle();
    ('#v45_ga_source').hide
    $('#footer').hide();


    $('h1').hide();
    $('h3').css("padding", '0px');
    $('h3').css("margin", '0px');
    $('#datatel_emailaddress1_confirm').hide();
    $('.elcn-container').css("margin-top", '0px');
    $('.elcn-content').css("padding-top", '0px');
	

    $('#submitCreateAccount').css("padding", '3px 5px');
    $('#submitCreateAccount').css("font-size", '16px');
    $('.validation-summary-container').css("padding", '0px');
    $('#69ebdc80-48bc-8107-5243-755edd580212').hide();
    $('form#createForm>div.crm-form>div.tab>div.section.container>div.row').css("padding-top", '0px');
    $('.elcn-container').attr('style', 'margin-top: 0px !important;padding-top: 0px !important;box-shadow:none');
	
    $('input, .form-control').css("margin-bottom", '0em');
	

		
    $('.submit-createaccount-button').css("padding-top", '0px');
	
   // $('#address1_telephone2').hide();
    $('#v45_ga_refid').hide();
    $('#v45_ga_refid2').hide();
	
	$('form#createForm>div.crm-form>div.tab>div.section.container>h3').css("padding-bottom", '0em');

  
    ///make labels placeholders    elcn_academicprogramofinterestid
  $("form :input").each(function(index, elem) {
       var eId = $(elem).attr("id");
        var label = null;

      if (eId && (label = $(elem).parents("form").find("label[for="+eId+"]")).length == 1) {
	//if (eId && eId !== "elcn_academicprogramofinterestid" && (label = $(elem).parents("form").find("label[for="+eId+"]")).length == 1) {
				
         if($(elem).is("select")  ){
               $(elem).find('option').get(0).remove();
              $(elem).prepend("<option value disabled selected hidden>"+$(label).html()+"</option>");
	
            }
           else $(elem).attr("placeholder", $(label).html());
           $(label).hide();
			
       }

		
   });

}
function  get_url_title(url){
    return url.match(/[^\/]*$/);
}

function mod_css_eventform(){
    getParentURLLast(document.referrer);
    ga(function(tracker){
        var clientId = tracker.get('clientId');
        $('#v45_ga_refid2').val(clientId);
        $('#v45_ga_refid').val(clientId);
    });
    $('#v45_ga_refid').hide();
    $('#v45_ga_refid2').hide();

}

function mod_css_longform(){   // RFI Longform formatting

    getParentURLLast(document.referrer);
    ga(function(tracker){
        var clientId = tracker.get('clientId');
        $('#v45_ga_refid2').val(clientId);
        $('#v45_ga_refid').val(clientId);
    });

 //   $('.navbar').hide();
    //style
    $('#v45_ga_source').hide();
    $('#footer').hide();


 //   $('h1').hide();
    $('h3').css("padding", '0px');
    $('h3').css("margin", '0px');
    ///$('#datatel_emailaddress1_confirm').hide();
    $('.elcn-container').css("margin-top", '0px');
    $('.elcn-content').css("padding-top", '0px');

    $('#submitCreateAccount').css("padding", '6px 10px');
    $('#submitCreateAccount').css("font-size", '16px');
    $('.validation-summary-container').css("padding", '0px');
    $('#69ebdc80-48bc-8107-5243-755edd580212').hide();
    $('form#createForm>div.crm-form>div.tab>div.section.container>div.row').css("padding-top", '0px');
    $('.elcn-container').attr('style', 'margin-top: 0px !important;padding-top: 0px !important;box-shadow:none');
    $('input, .form-control').css("margin-bottom", '.25em');
    $('.submit-createaccount-button').css("padding-top", '0px');
   // $('#address1_telephone2').hide();
    $('#v45_ga_refid').hide();
    $('#v45_ga_refid2').hide();

}
    //***************************************************///
    //******************* Main Section *******************///
    //***************************************************///

	//**$(window).load(function() {​​
        // this code will run after all other $(document).ready() scripts// have completely finished, AND all page elements are fully loaded.
		   ///make labels placeholders
  //**  $("form :input").each(function(index, elem) {
  //**      var eId = $(elem).attr("id");
  //**      var label = null;

   //**     if (eId && (label = $(elem).parents("form").find("label[for="+eId+"]")).length == 1) {
			
    //**        if($(elem).is("select")){
    //**            $(elem).find('option').get(0).remove();
    //**           $(elem).prepend("<option value disabled selected hidden>"+$(label).html()+"</option>");
	//**
    //**        }
    //**        else $(elem).attr("placeholder", $(label).html());
    //**        $(label).hide();
			
    //**    }

		
   //** });
		
   //** }​​);




var utm = getParentParameterByName('utm_content', document.referrer); // "lorem"

$(document).ready(function() {
	


    var page_name = get_url_title(document.referrer);

   // if (pageList.find(x >= x.name == page_name[0]))
 //   {
  //      var res = updateDrops(page_name[0]);
 //   }
    //changed to above mbm 4/20/20
    //console.log(pageList.find(x => x.name == page_name[0])

   // );

    if (pageList.find(x => x.name == page_name[0])
        )
    {
        var res = updateDrops(page_name[0]);
    }

    //online applications date picker hiding for dob
    $("#datatel_birthdate.date-picker").on('focus blur click', function () {
        $(".ui-datepicker-calendar").hide();
        $(".ui-datepicker-month").hide();
        $(".ui-datepicker-day").hide();
        $(".ui-datepicker-year").hide();
        $(".ui-datepicker-header").hide();
        $(".ui-widget-header").hide();
        $(".ui-helper-clearfix").hide();
        $(".ui-corner-all").hide();
    });

    //create acct and person forms date picker hiding for dob
    $("#birthdate.date-picker").on('focus blur click', function () {
        $(".ui-datepicker-calendar").hide();
        $(".ui-datepicker-month").hide();
        $(".ui-datepicker-day").hide();
        $(".ui-datepicker-year").hide();
        $(".ui-datepicker-header").hide();
        $(".ui-widget-header").hide();
        $(".ui-helper-clearfix").hide();
        $(".ui-corner-all").hide();
    });


    //eventforms date picker hiding for dob
    $("#v45_dateofbirth.date-picker").on('focus blur click', function () {
        $(".ui-datepicker-calendar").hide();
        $(".ui-datepicker-month").hide();
        $(".ui-datepicker-day").hide();
        $(".ui-datepicker-year").hide();
        $(".ui-datepicker-header").hide();
        $(".ui-widget-header").hide();
        $(".ui-helper-clearfix").hide();
        $(".ui-corner-all").hide();
    });


//find signin page and put more text on it
  //  $('div').find('h1:contains("Sign In")').html("<table><tr><td>Sign In</td></tr><tr><td><font size='2'>" +
  //      "If you have already created an application account, you can access it by providing your email and password. " +
  //      "If you have not yet created an account you can do so with the Create Account link below.</font></td></tr>" +
  //      "<tr><td><font size='1'>(Note: This account is not the same as the Viterbo University provided account you'll " +
  //      "receive once you are accepted as a student to the University.)</font></td></tr></table>");
		
		

    $('div').find('h1:contains("Sign In")').html("<table><tr><td>Sign In</td></tr><tr><td><font size='2'>" +
        "Sign in below to submit a new application for admission, " +
       " continue your application, or check the status of your application. </br>First time visitor? " +
       " Click on Create Account below.</font></td></tr></table>");
		

    $('h1').css({"line-height": ".6"});

    load_ga();

    //  var urlParams = new URLSearchParams(window.location.search);
    var form_param = getParentParameterByName('f', "", true); // "lorem"
    // console.log(urlParams.has('f')); // true

    // below for events
    //  var urlParams = new URLSearchParams(window.location.search);
    var form_param_event = getParentParameterByName('eventId', "", true); // "lorem"
    // console.log(urlParams.has('f')); // true

    // mbm 5/7/20 get param for trad ug tab4
    var form_tab = getParentParameterByName('newTab', "", true);


    $('input#firstname, input#datatel_firstname, input#datatel_middlename, input#datatel_lastname, input#v45_birthlastname, input#datatel_alternate_lastname, input#lastname, input#v45_preferredorchosenfirstname,input#v45_preferredorchosenlastname, input#address1_line1,input#address1_city, input#v45_preferredfirstname, input#v45_preferredlastname, input#datatel_address1_line1, input#datatel_address1_city, input#datatel_addressline1, input#datatel_city').on('keyup', function (e) {
        var txt = $(this).val();
        $(this).val(txt.replace(/^(.)|\s(.)/g, function ($1) {
            return $1.toUpperCase();
        }));
    });

    $("#emailaddress1").blur(function () {
        console.log('blur');
        $('#datatel_emailaddress1_confirm').val($(this).val());
    });

//check if intl student selected when coming into the form
  //changed fields  var intlstudent = $("#v45_internationalstudent").val();
	 var intlstudent = $("#v45_areyouaninternationalstudent").val();

  //  if (intlstudent == "1") {
		   if (intlstudent == "Yes") {

        $("#v45_academicarea option[value='d385b417-1808-e711-80f8-12d74673ef26']").remove();
        $("#v45_academicarea option[value='afb99a24-1808-e711-80f8-12d74673ef26']").remove();
    }
    //

    //hide Letter of Recommendation section on app where supp items are
  //  $("[id$='supplemental-lor']").hide(); -- commented out 2/28/22 mbm to enable

//for 2020FA Coming to Vit/viterbobound hide header stuff and run function to populate params
    if (form_param_event == '842a423d-bd51-ea11-a970-b0fe1f238ad3') {
        $('#elcn-nav-main').hide();

        // var idEventParameter = getUrlParameters("id", "", true);   //form id
        var fname = getUrlParameters("firstname", "", true);
        var lname = getUrlParameters("lastname", "", true);
        var email = getUrlParameters("email", "", true);
        var program = getUrlParameters("program", "", true);


        $('#datatel_firstname').val(fname);
        $('#datatel_lastname').val(lname);
        $('#datatel_emailaddress').val(email);
        //default both to first and only selected item
        $("#elcn_prospect_studenttypeid").get(0).selectedIndex = 1;
        $("#elcn_anticipatedentrytermid").get(0).selectedIndex = 1;

        // below is setting the program value
     //   $("#elcn_academicprogramofinterestid > option").each(function () {
            //alert(this.text + ' ' + this.value);
      //      if (this.text == program) {
      //          $('#elcn_academicprogramofinterestid').val(this.value);
      //      }
     //   });

    }


//*******************
//check if intl student selected on change trigger
//*******************
  // mbm 12/17/21 changed fields  $("#v45_internationalstudent").change(function () {   //see if intl student
	   $("#v45_areyouaninternationalstudent").change(function () {   //see if intl student

     //   console.log(this.value);

 //if (this.value == "1") {
        if (this.value == "Yes") {

            $("#v45_academicarea option[value='d385b417-1808-e711-80f8-12d74673ef26']").remove();
            $("#v45_academicarea option[value='afb99a24-1808-e711-80f8-12d74673ef26']").remove();
        }
        if (this.value == "No") {

            $('#v45_academicarea').append('<option value="d385b417-1808-e711-80f8-12d74673ef26">Graduate Education - Iowa</option>');
            $('#v45_academicarea').append('<option value="afb99a24-1808-e711-80f8-12d74673ef26">Graduate Education - Wisconsin</option>');


        }
    });
//********************

//*******************
//check if admit type freshman or ugreentry to hide 2021FA term for initial app screen before app
 //   save below for next fall, turning off 6/30/20
//*******************

        if (form_tab == '4') {


        $("#new_admittype").change(function () {   //see if intl student

            //UGFR remove 2022FA
			//  3da63a86-a611-e811-80cc-0af369f4a1dc --2022FA
			//  f036d895-8879-e811-80d6-0ece12de0f90 2023FA
			// d92745bc-0b64-e311-aca0-0050569038f8  UGFR
			// df2745bc-0b64-e311-aca0-0050569038f8  UGTR
            if (this.value == "d92745bc-0b64-e311-aca0-0050569038f8") {
             // $("#datatel_anticipatedentrytermid option[value='f036d895-8879-e811-80d6-0ece12de0f90']").remove();
                         }
            else
            {
                // $("#datatel_anticipatedentrytermid option[value='0d3f1299-c037-e611-80f3-12d74673ef26']").show();
             //   $('#datatel_anticipatedentrytermid').append('<option value="f036d895-8879-e811-80d6-0ece12de0f90">2023 Fall</option>');
            }

        });
    }
   
   //**** get create acccount form data - hide 2023 Fall from create acct 2/8/21
    var createacctpage =  window.location.href;
    if (createacctpage == 'https://viterbo.elluciancrmrecruit.com/Apply/Account/Create' || createacctpage == 'https://viterbo.elluciancrmrecruit.com/Apply/Account/Create?returnUrl=%2FApply') {
		
		 $("#elcn_prospect_studenttypeid").change(function () {  
		 
		 //  f036d895-8879-e811-80d6-0ece12de0f90 2023FA
		  //UGFR remove 2023Fall
            if (this.value == "d92745bc-0b64-e311-aca0-0050569038f8") {
              //  $("#elcn_anticipatedentrytermid option[value='f036d895-8879-e811-80d6-0ece12de0f90']").remove();
            }
			//UGRE
            if (this.value == "dd2745bc-0b64-e311-aca0-0050569038f8") {
              //  $("#elcn_anticipatedentrytermid option[value='3da63a86-a611-e811-80cc-0af369f4a1dc']").remove();
            }
            //UGTR show
            if (this.value == "df2745bc-0b64-e311-aca0-0050569038f8") {
               // $('#elcn_anticipatedentrytermid').append('<option value="f036d895-8879-e811-80d6-0ece12de0f90">2023 Fall</option>');
            }
            //EXLG Bach Comp
            if (this.value == "d12745bc-0b64-e311-aca0-0050569038f8") {
              //  $('#elcn_anticipatedentrytermid').append('<option value="3da63a86-a611-e811-80cc-0af369f4a1dc">2022 Fall</option>');
            }
            //GRDS
            if (this.value == "d32745bc-0b64-e311-aca0-0050569038f8") {
              //  $('#elcn_anticipatedentrytermid').append('<option value="3da63a86-a611-e811-80cc-0af369f4a1dc">2022 Fall</option>');
            }
            //GRND
            if (this.value == "d52745bc-0b64-e311-aca0-0050569038f8") {
             //   $('#elcn_anticipatedentrytermid').append('<option value="3da63a86-a611-e811-80cc-0af369f4a1dc">2022 Fall</option>');
            }
            //GREE
            if (this.value == "d72745bc-0b64-e311-aca0-0050569038f8") {
              //  $('#elcn_anticipatedentrytermid').append('<option value="3da63a86-a611-e811-80cc-0af369f4a1dc">2022 Fall</option>');
            }
	});
   
	}

//****** save below for next fall, turning off 6/28/21
       var tradappinitpage = getUrlParameters("type", "", true);
    if (tradappinitpage == 'datatel_traditionalundergraduateapplication') {

//d92745bc-0b64-e311-aca0-0050569038f8 --UGFR
//df2745bc-0b64-e311-aca0-0050569038f8  -- UGTR
// dd2745bc-0b64-e311-aca0-0050569038f8 --UGRE

//3da63a86-a611-e811-80cc-0af369f4a1dc - 2022 Fall
        $("#elcn_prospect_studenttypeid").change(function () {   //see if intl student
            // console.log(this.value);
            //UGFR remove
            if (this.value == "d92745bc-0b64-e311-aca0-0050569038f8") {
            //    $("#elcn_anticipatedentrytermid option[value='f036d895-8879-e811-80d6-0ece12de0f90']").remove();
            }
            //UGRE
            if (this.value == "dd2745bc-0b64-e311-aca0-0050569038f8") {
             //   $("#elcn_anticipatedentrytermid option[value='3da63a86-a611-e811-80cc-0af369f4a1dc']").remove();
            }
            //UGTR show
            if (this.value == "df2745bc-0b64-e311-aca0-0050569038f8") {
              //  $('#elcn_anticipatedentrytermid').append('<option value="f036d895-8879-e811-80d6-0ece12de0f90">2023 Fall</option>');
            }
            //EXLG Bach Comp
            if (this.value == "d12745bc-0b64-e311-aca0-0050569038f8") {
             //   $('#elcn_anticipatedentrytermid').append('<option value="3da63a86-a611-e811-80cc-0af369f4a1dc">2022 Fall</option>');
            }
            //GRDS
            if (this.value == "d32745bc-0b64-e311-aca0-0050569038f8") {
              //  $('#elcn_anticipatedentrytermid').append('<option value="3da63a86-a611-e811-80cc-0af369f4a1dc">2022 Fall</option>');
            }
            //GRND
            if (this.value == "d52745bc-0b64-e311-aca0-0050569038f8") {
             //   $('#elcn_anticipatedentrytermid').append('<option value="3da63a86-a611-e811-80cc-0af369f4a1dc">2022 Fall</option>');
            }
            //GREE
            if (this.value == "d72745bc-0b64-e311-aca0-0050569038f8") {
             //   $('#elcn_anticipatedentrytermid').append('<option value="3da63a86-a611-e811-80cc-0af369f4a1dc">2022 Fall</option>');
            }
        });
    }
 //end comment out

    //*******************
    //   app goal trigger
    //********************

    $( "#elcn_prospect_studenttypeid" ).change(function() {//see where applying
        console.log(this.value);
        switch(this.value) {
            case 'd92745bc-0b64-e311-aca0-0050569038f8':
                //set ga UG FR
                ga('send', 'event', 'recruiter', 'app_start', 'ugfr',1);
                break;
            case 'df2745bc-0b64-e311-aca0-0050569038f8':
                //set ga UG TR
                ga('send', 'event', 'recruiter', 'app_start', 'ugtr',1);
                break;
            case 'db2745bc-0b64-e311-aca0-0050569038f8':
                //set ga UG NON
                ga('send', 'event', 'recruiter', 'app_start', 'ugnon',1);
                break;
            case 'd12745bc-0b64-e311-aca0-0050569038f8':
                //set ga CAL
                ga('send', 'event', 'recruiter', 'app_start', 'ugcal',1);
                break;
            case 'dd2745bc-0b64-e311-aca0-0050569038f8':
                //set ug reentry
                ga('send', 'event', 'recruiter', 'app_start', 'ugreentry',1);
                break;
            case 'd32745bc-0b64-e311-aca0-0050569038f8':
                //set grad degree
                ga('send', 'event', 'recruiter', 'app_start', 'uggrad',1);
                break;
            case 'd52745bc-0b64-e311-aca0-0050569038f8':
                //set grad non
                ga('send', 'event', 'recruiter', 'app_start', 'uggrad_non',1);
                break;
            case 'd72745bc-0b64-e311-aca0-0050569038f8':
                //set grad reentry
                ga('send', 'event', 'recruiter', 'app_start', 'uggrad_reentry',1);
                break;
            case 'fb9ad6e8-36e7-e611-80ef-0a31e000b763':
                //set senior
                ga('send', 'event', 'recruiter', 'app_start', 'senior',1);
                break;
            case '150a4f20-36e7-e611-80ef-0a31e000b763':
                //set youth
                ga('send', 'event', 'recruiter', 'app_start', 'youth',1);
                break;
            default:
        }
    });



    //*******************
    //   form switches
    //********************
    if (form_param_event){
        mod_css_eventform();


        //UG Transfer Registration Form hide header stuff
        if (form_param_event && form_param_event=='10c21203-8f8e-e811-80d6-0ece12de0f90') { //transfer reg form
            $('.navbar').hide();
            //style
            $('#footer').hide();

//here are some comments
            $('h1').hide();
            $('h3').css("padding", '0px');
            $('h3').css("margin", '0px');
            $('.elcn-container').css("margin-top", '0px');
            $('.elcn-content').css("padding-top", '0px');

            $('#submitCreateAccount').css("padding", '6px 10px');
            $('#submitCreateAccount').css("font-size", '16px');
            $('.validation-summary-container').css("padding", '0px');
            $('#69ebdc80-48bc-8107-5243-755edd580212').hide();
            $('form#createForm>div.crm-form>div.tab>div.section.container>div.row').css("padding-top", '0px');
            $('.elcn-container').attr('style', 'margin-top: 0px !important;padding-top: 0px !important;box-shadow:none');
            $('input, .form-control').css("margin-bottom", '.25em');
            $('.submit-createaccount-button').css("padding-top", '0px');

          //hide thankyou submit
            $('div').find('span:contains("Thank you for your interest.")').html("<center><Br><br><p><h2>Thank you for making your commitment to attend Viterbo University this spring semester! </h2></p><p>In order to be eligible to register, please make sure you've met the following requirements:</br>Are you Accepted for Admission?</br>Have you made your Enrollment Deposits ($100 Tuition or $200 Tuition/Housing)?</br></br>Your file will be turned over to our Academic Advising Office and you'll hear from them to schedule a registration appointment! Please let us know if you have any questions, as we are happy to assist.</br>The Admissions Office at Viterbo University - 608-796-3010 or admissions@viterbo.edu</p></center>");

        }


    }

    //*******************
    //   RFI LONG Form
    //********************

    if (form_param && form_param=='1e51dbd8-110f-42d7-bc80-aed23b4251d7') { //quickform  RFI LONG Form
        mod_css_longform();

        //set goal for long form
      //  $( "#elcn_academicprogramofinterestid" ).change(function() {//see whAT PROGRAM
            //  alert('tesing');
      //      console.log(this.value);
      //      ga('send', 'event', 'recruiter', 'request', 'long',1);
      //  });

    }

    //*******************
    //   Grad Short Form
    //********************

    if (form_param && form_param=='2b1a9707-c08d-409c-87a1-ced33f4266f4') { //quickform  GRAD SHORT FORM
        mod_css_shortform();
$('#elcn_academicprogramofinterestid').hide();

        //set ga source field
        if(utm && utm.indexOf('phase') !== -1){
            //2b1a4951-a1e3-e811-80d6-0a840c002efa
            $('#v45_ga_source').val("2b1a4951-a1e3-e811-80d6-0a840c002efa");
        }
        $('#v45_ga_source').hide();

        //set goal for grad
       // $( "#elcn_academicprogramofinterestid" ).change(function() {//see whAT PROGRAM
            //  alert('tesing');
       //     console.log(this.value);
       //     ga('send', 'event', 'recruiter', 'request', 'grad',1);
       // });


///------

        $("#v45_academicarea").change(function () {   //see acad area
		
 $('#elcn_academicprogramofinterestid').show();
  var eId = $("#elcn_academicprogramofinterestid").attr("id");

  label = $("#elcn_academicprogramofinterestid").parents("form").find("label[for="+eId+"]");
 $(label).show();	
	
		//	$("#elcn_academicprogramofinterestid").prepend("<option value selected>"+$(label).html()+"</option>");
			
// $(elem).prepend("<option value disabled selected hidden>"+$(label).html()+"</option>");			
        
 
 
		});



///-----






    }

    //*******************
    //   Cal Quick Form
    //********************

    if (form_param && form_param=='63ed9cfe-d8b9-4510-a87a-86bc417c54dc'){ //quickform - CAL SHORT FORM
        mod_css_shortform();

        //set goal for cal
      //  $( "#elcn_academicprogramofinterestid" ).change(function() {//see whAT PROGRAM
            //  alert('tesing');
       //     console.log(this.value);
      //      ga('send', 'event', 'recruiter', 'request', 'cal',1);
     //   });


        //set ga source field
        if(utm && utm.indexOf('phase') !== -1){
            //2b1a4951-a1e3-e811-80d6-0a840c002efa
            $('#v45_ga_source').val("2b1a4951-a1e3-e811-80d6-0a840c002efa");
        }
        $('#v45_ga_source').hide();

    }



});



//*******************
//   Event listener to transfer client id to quickforms in iframes
//********************

window.addEventListener('message', function(event) {
    console.log('in sub');
    //if (message.data.indexOf('clientId:') === 0) {
    ga('create', 'UA-43891006-1', 'auto', {
            'clientId': event.data
        },
        {allowLinker: true}
    );
    //      ^^^^^^^^^^^^^^^^^^^^^^^^^
    //       Manually sets Client ID due to time delay and linker fails
    ga('send', 'pageview');
    //set and hide
    $('input#v45_ga_refid2').val(event.data);
    $('input#v45_ga_refid').val(event.data);
});
