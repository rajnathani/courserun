
function removeSearchText()
{
var search_box = document.getElementById('search-box');
if (search_box.value == 'Course Code or Program'){
	search_box.value = "";
	}
search_box.style.color="black";
search_box.style.backgroundColor = "rgb(240,240,240)";
}

function addDim()
{
var search_box = document.getElementById('search-box');
search_box.style.color="grey";
if (!search_box.value){
	search_box.value = "Course Code or Program";
	}
search_box.style.backgroundColor = "rgb(230,230,230)";
}

var open = false;

function popUp(typ){
	if (open){ return false;}
	open = true;
	document.getElementById('container').style.opacity = "0.5";
    var popup = document.createElement('div');
    popup.className = 'popup';
    popup.id = "test";
    var cancel = document.createElement('div');
    cancel.className = 'cancel';
    cancel.innerHTML = 'x';
    cancel.onclick = function (e) {open = false;popup.parentNode.removeChild(popup); document.getElementById('container').style.opacity = "1.0"; };
    var message = document.createElement('span');
    message.style.margin = "10px";
	
	if (typ == "bug"){
	message.innerHTML = "<p>Any bugs found to be reported to admin@courserun.ca</p>"}
	else if (typ == "feedback"){
	message.innerHTML = "<p>Your feedback is highly appreciated.</p> <p>You can post your feedback to Course Run's <a href='https://twitter.com/CourseRun'>twitter</a> or <a href='http://www.facebook.com/pages/Course-Run-University-of-Toronto/392789940783083'>facebook</a> page.</p><p>In case you want your feedback to remain private, e-mail it over to feedback@courserun.ca</p>"}
	else if (typ == "about") {
	message.innerHTML = "<p>This is a project done by University of Toronto students and not University of Toronto. Logos done by Sangah Han, the remaining by Relfor.</p><p>Special thanks to Doanld Boere (Assistant Principal of Innis College) for his enthusiasm and motivation right from the start.</p>"}
	else {
		message.innerHTML = "<p>Course Run's database is valid for year 2012-2013. The project has been officially abandoned as of late 2012. The university now has their own course search tool with features highly similar to those of Course Run's, its available at <a href='http://coursefinder.utoronto.ca'>coursefinder.utoronto.ca</a> please use that instead.</p><p>Over 70,000 hits were received by Course Run.<br/>Thank you for being a part of it.</p>"
	}
	
	popup.appendChild(cancel);
    popup.appendChild(message);                                    

	var h = (parseFloat(window.innerHeight));
	var w = (parseFloat(window.innerWidth));
	var scrolledDown = window.scrollY;
	
	if (!h){  
		var h = (parseFloat(document.body.offsetHeight));
		var w = (parseFloat(document.body.offsetWidth));}
	if (!scrolledDown){
		var scrolledDown = document.body.scrollTop;}
	popup.style.top = (0.24 * h) + scrolledDown + "px";
	popup.style.left = 0.5*(w - 200) + "px";
    document.body.appendChild(popup);
	
    }