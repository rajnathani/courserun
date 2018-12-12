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
'''

import os, sys;
import cgi, cgitb;
import cPickle;
import time;
from CourseRunObjects import Course, Seminar;

cgitb.enable();
form = cgi.FieldStorage('formy');

print '''<div id="filter-choice-box">'''

time1 = time.time()
#categories
student_category = form.getvalue('student_category');
if student_category == "breadth":
    cat_file = open('breadth_dict.data', 'r');
    cat_dict = cPickle.load(cat_file);
    filter_head = "BREADTH CATEGORIES";
    cat_conver = {'1':'Creative and Cultural Representations',
                  '2': 'Thought, Belief and Behaviour',
                  '3': 'Society and its Institutions',
                  '4': 'Living Things and Their Environment',
                  '5': 'The Physical and Mathematical Universes',
                  '6': 'None'};
else:
    cat_file = open('distribution_dict.data', 'r');
    cat_dict = cPickle.load(cat_file);
    filter_head = "DISTRIBUTION CATEGORIES";
    cat_conver = {'7': 'Humanities',
                  '8': 'Social Science',
                  '9': 'Science',
                  '0': 'None'};

categories = form.getlist('category');  
print '<h1 class="filter-head">%s</h1>' % filter_head;
print '''<div class="filter-list"><ul>''';
for cat in categories:
    print '<li>%s</li>' % cat_conver[cat];
print '''</ul></div>''';

#
 
    
#duration
duration = form.getlist('duration');

print '<h1 class="filter-head">DURATION</h1>';
print '''<div class="filter-list"><ul>'''

if 'F' in duration:
    if 'S' in duration:
        print '<li>Half Year (fall and winter)</li>';
    else:
        print '<li>Half Year (fall)</li>';
elif 'S' in duration:
    print '<li>Half Year (winter)</li>';
    
if 'Y' in duration:
    print '<li>Full Year</li>';

print '''</ul></div>''';

#


#credit

credit = form.getlist('credit');
print '<h1 class="filter-head">CREDITS</h1>';

print '''<div class="filter-list"><ul>''';
if 'H' in credit:
    print '<li>Half-Credit</li>';
if 'Y' in credit:
    print '<li>Full-Credit</li>';
    
print '''</ul></div>''';


#


#years
years = form.getlist('year');

print '<h1 class="filter-head">YEAR LEVEL</h1>';
print '''<div class="filter-list"><ul>''';
for year in years:
    print '<li>%s00 Level</li>' % year;
print '''</ul></div>'''
#


#preferred programs

preferred_program_num = int(form.getvalue('preferred_programs_num'));

pref = False
preferred_programs = [];
for i in xrange(1, preferred_program_num + 1):
    preferred_program = form.getvalue('preferred_program' + str(i));
    if preferred_program and not (preferred_program in preferred_programs):
        preferred_programs.append(preferred_program);
        pref = True
        
if pref:
    print '<h1 class="filter-head">PREFERRED PROGRAMS</h1>';
    print '''<div class="filter-list"><ul>''';
    for pref in preferred_programs:
        print '<li>%s</li>' % pref;
    print '''</ul></div>''';
    
            
#

#time slots


def makeTimeSet(day, start, end):
    start = int(start)
    end = int(end)
    for i in range(start, end):
        full_time_set.add(day + str(i))
        
    
def convert_time(time):
    if not ('-' in time):
        if time == "0":
            return '12 pm'
        else:
            return (time + ' pm')
    elif time == '-1':
        return '11 am'
    elif time == '-2':
        return '10 am'
    else:
        return '9 am'

def part_of(L1, L2):
    for l in L1:
        if l in L2:
            return True
    
time_slot_num = int(form.getvalue('time_slot_num'));

first_timing = True
for i in xrange(1, time_slot_num + 1):
    
    day =  form.getvalue('day' + str(i));
    start = form.getvalue('start_time' + str(i));
    end =  form.getvalue('end_time' + str(i));


    if day and start and end:
        if first_timing:
            first_timing = False
            full_time_set = set()
            user_sects = form.getlist('section')
            print '<h1 class="filter-head">TIME SELECTION</h1>';
            print '<h1 style="font-size:11px; color:rgb(40,40,40); font-family:arial; font-weight:bold; padding:0; margin:0 0 0 6px;">Matched For</h1>'
            user_sect_dict = {'L': 'Lectures', 'T': 'Tutorials', 'P': 'Practicals'}
            print '<ul style="margin-top:2px; padding-bottom:11px; border-bottom:1px solid rgb(180,180,180);">'
            for usr_sect in user_sects:
                print '<li>%s</li>' % user_sect_dict[usr_sect];
            print '</ul>'
            print '''<div class="filter-list"><ul>''';
            if 'N' in duration:
                full_time_set.add('TBA')
                undec = True
            else:
                undec = False

            convert_day = {'M': 'Monday', 'T': 'Tuesday', 'W': 'Wednesday', 'R': 'Thursday', 'F': 'Friday'}
    
        makeTimeSet(day, start, end)
        print '<li>%s %s - %s</li>' % (convert_day[day], convert_time(start), convert_time(end))
    
if not first_timing:
    print '''</ul></div>'''; 
#

print '''</div>'''

tried = []
found_courses = set()
for cat in categories:
    for year in years:
        for cre in credit:
            for dur in duration:
                for c in cat_dict[cat + year + cre + dur]:
                    if not pref or part_of(c.lower_pns,preferred_programs):
                        if not first_timing:
                            if c not in tried:
                                if c.timing_possible(duration, user_sects, full_time_set, undec):
                                    found_courses.add(c)
                                tried.append(c)
                        else:
                            found_courses.add(c)
                        

if not found_courses:
    print '<div class="no-matches">No Matches</div>'
else:
    print '<h1 class="results-head">%d results in %.2f seconds</h1>' % (len(found_courses), (time.time() - time1));
    sorted_courses = sorted(found_courses)
    
    print '<ul class="results">'
    for crs in sorted_courses:
        print '<hr/>'
        print '<li>' + str(crs) + '</li>'
        
    print '<hr style="margin:17px 0px 0px 0px;"/>'
    print '</ul>'



print '''<div id="footer">
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