function studentCategory(breadth)
{
document.getElementById('all').checked = false;
if (breadth)
	{ document.getElementById("breadth-categories").style.display = "block";
	  document.getElementById("distribution-categories").style.display = "none";
	  document.getElementById("breadth-option").style.textDecoration = "underline";
	  document.getElementById("distribution-option").style.textDecoration = "none";
	  document.forms["formy"].elements["student_category"].value = "breadth";
	  
	  var distribution_id = document.getElementById('distribution-categories');
	  var distribution_list = distribution_id.getElementsByTagName('input');
	  for (var i=0; i<distribution_list.length; i++){
		distribution_list[i].checked = false;
		distribution_list[i].disabled = false;
		}  
	}
else
	{ document.getElementById("distribution-categories").style.display = "block";
	  document.getElementById("breadth-categories").style.display = "none";
	  document.getElementById("distribution-option").style.textDecoration = "underline";
	  document.getElementById("breadth-option").style.textDecoration = "none";
	  document.forms["formy"].elements["student_category"].value = "distribution";
	  
	  var breadth_id = document.getElementById('breadth-categories');
	  var breadth_list = breadth_id.getElementsByTagName('input');
	  for (var i=0; i < breadth_list.length; i++){
		breadth_list[i].checked = false;
		breadth_list[i].disabled = false;
		}
	}	
}

function allCategories(){
	var truth_val = document.getElementById('all').checked;
	var stu_cat = document.forms["formy"].elements["student_category"].value;
	var cat_list;
	if (stu_cat == 'breadth'){
		cat_list = new Array('1','2','3','4','5','6');}
	else {
		cat_list = new Array('0','7','8','9');}
	var len_cat_list = cat_list.length;
	for (var i=0; i < len_cat_list; i++){
		document.getElementById(cat_list[i]).checked = truth_val;
		/**document.getElementById(cat_list[i]).disabled = truth_val;**/}}
	

function semesterChoice()
	{	
	var truth_value = document.getElementById("half-year").checked;
	document.getElementById("fall").checked = truth_value;
	document.getElementById("winter").checked = truth_value;
	document.getElementById("fall").disabled=!truth_value;
	document.getElementById("winter").disabled=!truth_value;
	}


function morePreferredPrograms()
	{
	document.forms["formy"].elements["preferred_programs_num"].value = (parseInt(document.forms["formy"].elements["preferred_programs_num"].value) + 1);
	var preferred_programs_num = parseInt(document.forms["formy"].elements["preferred_programs_num"].value);
	var program_array = new Array('Aboriginal Studies', 'Academic Bridging Program', 'Actuarial Science', 'American Studies', 'Anatomy', 'Anthropology', 'Architecture', 'Archaeology', 'Art', 'Asia-Pacific Studies', 'Astronomy and Astrophysics', 'Biochemistry', 'Biology', 'Canadian Institute for Theoretical Astrophysics', 'Chemistry', 'Classics', 'Cognitive Science', 'Comparative Literature', 'Cell and Systems Biology', 'Centre for Environment', 'Centre for Jewish Studies', 'Computer Science', 'Drama', 'Diaspora and Transnational Studies', 'East Asian Studies', 'Economics', 'Ecology and Evolutionary Biology', 'English', 'Ethics (Centre for)',  'Estonian', 'European Studies', 'Finnish', 'First Year Seminars', 'Forest Conservation', 'French', 'German', 'Geography', 'Geology', 'History', 'Human Biology', 'History and Philosophy of Science and Technology', 'Hungarian', 'Immunology', 'Innis College', 'Italian',  'Joint Courses', 'Kinesiology & Physical Education', 'Latin American Studies', 'Life Sciences', 'Linguistics', 'Laboratory Medicine and Pathobiology', 'Mathematics', 'Modern Languages and Literatures', 'Molecular Genetics and Microbiology', 'Materials Science', 'Music', 'New College', 'Nutritional Science', 'Near and Middle Eastern Civilizations', 'Pharmacology and Toxicology', 'Peace, Conflict and Justice Studies', 'Pharmaceutical Chemistry', 'Philosophy', 'Physics', 'Planetary Science', 'Political Science', 'Portuguese', 'Physiology', 'Psychology', 'Public Health Sciences', 'Public Policy', 'Religion', 'Rotman Commerce', 'Slavic Languages and Literatures', "St. Michael's College", 'Sociology', 'South Asian Studies', 'Spanish', 'Statistics', 'Trinity College', 'University College', 'Victoria College', 'Woodsworth College', 'Women and Gender Studies');
	
	var sel = document.createElement('select');
	sel.name = 'preferred_program' + preferred_programs_num;
	sel.style.width = "115px";
	/**sel.onfocus = function() { sel.style.width = "170px"; }**/
	/** add none as first value **/
	var opt = document.createElement("option");
	opt.value = '';
	opt.text = 'None';
	try{
			sel.add(opt, sel.options[null]);
			}
		catch(e){
			sel.add(opt, null);
			}
	
	var length_program_array = program_array.length;
	for (var i=0;i<length_program_array;i++){
		var opt = document.createElement("option");
		opt.text = program_array[i];  
		opt.value = program_array[i].toLowerCase();  
		try{
			sel.add(opt, sel.options[null]);
			}
		catch(e){
			sel.add(opt, null);
			} 
		}
	var preferred_id = document.getElementById('preferred_programs');
	preferred_id.appendChild(sel);
	}

function moreTimeSlots(){

	document.forms["formy"].elements["time_slot_num"].value = (parseInt(document.forms["formy"].elements["time_slot_num"].value) + 1);
	var time_slot_num = (document.forms["formy"].elements["time_slot_num"].value);

	var time_cells = document.getElementById('time-slot-cells');
	
	var sel = document.createElement('select');
	sel.name = ("day" + time_slot_num);
	sel.id = ("day" + time_slot_num);
	sel.onchange = function() { exposeSlots(); }
	
	var days = new Array('None',"Monday", "Tuesday", "Wednesday", "Thursday", "Friday");
	var code_days = new Array('', "M", "T", "W", "R", "F");
	
	for (var i=0; i<6; i++){
		var opt = document.createElement("option");
		opt.value = code_days[i];  
		opt.text = days[i];
		try{
			sel.add(opt, sel.options[null]);
			}
		catch(e){
			sel.add(opt, null);
			}
		}
	time_cells.appendChild(sel);
	
	//Start Time part
	
	sel = document.createElement('select');
	sel.name = ("start_time" + time_slot_num);
	sel.onchange = function() { exposeSlots(); }
	
	var start_times = new Array('None',"9:00 am", "10:00 am", "11:00 am", "12:00 pm", "1:00 pm", "2:00 pm", "3:00 pm", "4:00 pm", "5:00 pm", "6:00 pm", "7:00 pm", "8:00 pm", "9:00 pm");
	var code_start_times = new Array('',"-3", "-2", "-1", "0", "1", "2", "3", "4", "5", "6", "7", "8" ,"9");
	for (var i=0;i<14;i++){
		var opt = document.createElement("option");
		opt.value = code_start_times[i];  
		opt.text = start_times[i];  
		try{
			sel.add(opt, sel.options[null]);
			}
		catch(e){
			sel.add(opt, null);
			}
		}
	time_cells.appendChild(sel);
	
	
	//End Time part
	sel = document.createElement('select');
	sel.name = ("end_time" + time_slot_num);
	sel.onchange = function() { exposeSlots(); }
	
	var end_times = new Array('None', "10:00 am", "11:00 am", "12:00 pm", "1:00 pm", "2:00 pm", "3:00 pm", "4:00 pm", "5:00 pm", "6:00 pm", "7:00 pm", "8:00 pm", "9:00 pm", "10:00 pm");
	var code_end_times = new Array( '', "-2", "-1", "0", "1", "2", "3", "4", "5", "6", "7", "8" ,"9" ,"10");
	for (var i=0;i<14;i++){
		var opt = document.createElement("option");
		opt.value = code_end_times[i];  
		opt.text = end_times[i];  
		try{
			sel.add(opt, sel.options[null]);
			}
		catch(e){
			sel.add(opt, null);
			}
		}
	time_cells.appendChild(sel);
	time_cells.appendChild(document.createElement('br'));
	}
	
	
function exposeSlots(){
	var time_slot_num = (document.forms["formy"].elements["time_slot_num"].value);
	var tba = document.getElementById('tba');
	var wants_time = false;
	for (var i=1; i <= time_slot_num; i++){
		var day = (document.forms["formy"].elements[("day" + i)].value);
		var start_time = (document.forms["formy"].elements[("start_time" + i)].value);
		var end_time = (document.forms["formy"].elements[("end_time" + i)].value);
		if (day && start_time && end_time) {wants_time = true; break;}
		}
	if (wants_time){
		tba.style.visibility = 'visible';
		}
	else{
		tba.style.visibility = 'hidden';
		}	
	}


function validateForm(){
	
	if (navigator.userAgent.indexOf('Firefox') != -1){
	return}
	var proc = document.getElementById('process');
	proc.style.width = '170px'
	proc.value = 'PROCESSING';
	}
	
	