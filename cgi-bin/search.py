#!/usr/bin/python2.7
print "Content-type: text/html\n\n";
print '''<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<title>Search Results</title>
<meta name="author" content="raj nathani">
<meta name="keywords" content="university of toronto course run, university of toronto course, university of toronto,
course run, uoft course run, uoftcourserun, calendar, timetable, course finder, utoronto">

<link rel="stylesheet" href="../css/style.css" type="text/css"/>
<link rel="stylesheet" href="../css/style_results.css" type="text/css"/>
<!--[if lt IE 9]>
	<link rel="stylesheet" type="text/css" href="../css/ienot9.css" />
<![endif]-->
<script type="text/javascript" language="Javascript" src="../js/main.js"></script>
</head>
<body>
<div id="container">
<div id="header">
	<img id="main-logo" onmouseover="document.getElementById('main-logo').style.cursor='pointer'" onclick="document.location.href = '../index.html';" src="../img/course_run_head.png" />
</div>
<div id="nav-bar">
<div id="nav-links">
<a class="link left" href="http://www.artsandscience.utoronto.ca/ofr/calendar/#">CALENDAR</a>
<a class="link left" href="http://www.artsandscience.utoronto.ca/ofr/timetable/winter/sponsors.htm">TIMETABLE</a>
<a class="link left" href="http://www.artsci.utoronto.ca/current/undergraduate/first-year-seminars/">SEMINARS</a>
<a class="link left" href="https://www.rosi.utoronto.ca/main.html">ROSI</a>
</div>
<form name="search" style="margin:0; padding:0; float:right;" action="search.py">
<input type="text" name="query" id="search-box" class="search-box" maxlength="100" autocomplete="off" value="Course Code or Program" tabindex="2" onFocus="removeSearchText();" onBlur="addDim();"/>
<input type="submit" class="search-button" value="GO" tabindex="3">
</form>
</div>
<div id="results-area">
<ul class="results">
'''

import os, sys;
import cgi, cgitb;
import cPickle;
from CourseRunObjects import Course,Seminar;

def valid_course_code(quote_content):
    
    if len(quote_content) == 8:
        if quote_content[0:3].isalpha() and quote_content[0:3].isupper():
            if quote_content[3:6].isdigit():
                if quote_content[6] == "H" or quote_content[6] == "Y":
                    if quote_content[7] == '1' or quote_content[7] == '0':
                        return True
                    
def capitalize(s):
    l = s.split()
    answer = ""
    nouns = ['in', 'or', 'and', 'for']
    for ss in l:
        if ss in nouns:
            answer += ss
        else:
            answer += ss.capitalize()
        answer += ' '
    return answer.strip()
        

cgitb.enable();
form = cgi.FieldStorage('search');



query = form.getvalue('query').strip()[:8].upper();
search_file = open("search_dict.data");
search_dict = cPickle.load(search_file);
found_courses = set()
user_wants_code = False
for (course_code, obj) in search_dict.iteritems():
    if query in course_code:
        user_wants_code = True
        if type(obj) == Course:
            found_courses.add(obj)
        else:
            for sem in obj:
                found_courses.add(sem)

if not user_wants_code and not valid_course_code(query):
    qprogram = form.getvalue('query').strip().lower();
    program_file = open("program_dict.data");
    program_dict = cPickle.load(program_file);
    for program in program_dict:
        if qprogram in program:
            found_courses = program_dict[program]
            print '<h1 class="results-head">Found Program: <span class="program-name">%s</span></h1>' % capitalize(program)
            break
    
sorted_courses = sorted(found_courses)


if not sorted_courses:
    print '<div class="no-matches">No Matches</div>'

else:
    for crs in sorted_courses:
        print '<hr/>'
        print '<li>' + str(crs) + '</li>'
    
    print '<hr style="margin:17px 0px 0px 0px;"/>'



print '''</ul></div><div id="footer">
<div class="footer-list">
<ul>
<li><span onClick="popUp('feedback');" tabindex="4">feedback</span></li>
<li><span onClick="popUp('about');" tabindex="5">about</span></li>
<li><span onClick="popUp('bug');" tabindex="6">report bug</span></li>
<li><a href="http://www.facebook.com/pages/Course-Run-University-of-Toronto/392789940783083" tabindex="7">facebook</a></li>
<li><a href="https://twitter.com/CourseRun" tabindex="8">twitter</a></li>
</ul>
</div>
Copyright &copy;2012 Gigadote | All Rights Reserved
</div>
</div>
</body>
</html>'''