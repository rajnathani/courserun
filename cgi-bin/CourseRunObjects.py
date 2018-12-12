class Course(object):

    def __init__(self, course_code, course_description, program_name):
        self.course_code = course_code
        self.course_description = course_description.strip()
        self.course_program = course_code[:3]
        self.program_names = program_name
        self.lower_pns = [program_name.lower()]

        self.fall_timings = {'L': [], 'T': [], 'P': []}
        self.winter_timings = {'L': [], 'T': [], 'P': []}
        self.full_year_timings = {'L': [], 'T': [], 'P': []}

        self.fall_time_frame = {'L': [], 'T': [], 'P': []}
        self.winter_time_frame = {'L': [], 'T': [], 'P': []}
        self.full_year_time_frame = {'L': [], 'T': [], 'P': []}

        self.no_session = True
        self.fall = False
        self.winter = False
        self.full_year = False

    def set_timing_and_location(self,session_type, section_timing_location_prof, section_type):

        merged_timing_location_prof = merge_timing_location_prof(section_timing_location_prof)

        if session_type == "F":            
            self.fall = True
            self.no_session = False
            self.fall_timings[section_type].append(merged_timing_location_prof)
            time_span = get_full_section_time_span(section_timing_location_prof[0])
            if time_span not in self.fall_time_frame[section_type]:
                self.fall_time_frame[section_type].append(time_span)

        elif session_type == "S":
            self.winter = True
            self.no_session = False
            self.winter_timings[section_type].append(merged_timing_location_prof)
            time_span = get_full_section_time_span(section_timing_location_prof[0])
            if time_span not in self.winter_time_frame[section_type]:
                self.winter_time_frame[section_type].append(time_span)

        else:
            self.full_year = True
            self.no_session = False
            self.full_year_timings[section_type].append(merged_timing_location_prof)
            time_span = get_full_section_time_span(section_timing_location_prof[0])
            if time_span not in self.full_year_time_frame[section_type]:
                self.full_year_time_frame[section_type].append(time_span)


    def generate_display(self):
        desc = self.course_description
        if type(self) == Course or not self.course_description.endswith('</p>'):
            desc += "<br/>"
        if desc.count('<p') != desc.count('</p>'):
            desc += "</p>"
            if desc.count('<p') != desc.count('</p>'):
                print "OOOOOOOOO", self.course_code
        if self.program_names:
            desc += "<div id='pn'>Program: %s</div>" % self.program_names
        desc += '<table>' 
        if self.fall or self.winter:
            desc += '<tr>'
            desc += '<td id="f"><h1>Fall Timings</h1>'
            desc += time_display_helper(self.fall_timings, 'Fall')
            desc += '</td>'
            
            desc += '<td id="s"><h1>Winter Timings</h1>'
            desc += time_display_helper(self.winter_timings, 'Winter')
            desc += '</td>'
            desc += '</tr>'

        if self.full_year:
            desc += '<tr>'
            if self.fall or self.winter:
                desc += '<td id="y" colspan="2"><h1>Full Year Timings</h1>'
            else:                
                desc += '<td id="y"><h1>Full Year Timings</h1>'
            desc += time_display_helper(self.full_year_timings, 'Full Year')
            desc += '</td>'
            desc += '</tr>'
            
        if self.no_session:
            desc += '<tr>'
            desc += '<td id="n">Timings Undeclared</td>'
            desc += '</tr>'
        
        desc += '</table>'
        self.display = desc


    def timing_possible(self, user_sessions, user_sections, user_times, user_no_session):

        if self.no_session:
            if user_no_session:
                return True
            else:
                return False
        full_match = False
        session_frame_dict = {'F': self.fall_time_frame, 'S': self.winter_time_frame,
                               'Y': self.full_year_time_frame}
        empty = {'L': [], 'T': [], 'P': []}
        for user_session in user_sessions:
            if user_session == 'N':
                continue
            session_frame = session_frame_dict[user_session]
            if session_frame == empty:
                continue
            session_match = True
            for user_section in user_sections:
                section_match = False
                course_section_timings = session_frame[user_section]
                if not course_section_timings:
                    section_match = True
                else:
                    for class_time in course_section_timings:
                        if class_time.issubset(user_times):
                            section_match = True
                            break
                if not section_match:
                    session_match = False
                    break
            if session_match:
                return True #break
        return full_match

    def __str__(self):
        return self.display
    
    def __cmp__(self, other):
        if self.course_code < other.course_code:
            return -1
        elif self.course_code > other.course_code:
            return 1
        else:
            return 0


class Seminar(Course):
  
    def __init__(self, course_code, course_description, course_name):
        Course.__init__(self,course_code,course_description, 'First Year Seminars')
        self.course_name = course_name
    
    def generate_display(self):
        Course.generate_display(self)
        put_index = self.display.index('<strong>') + 8
        new_display = self.display[0:put_index] + self.course_code + ' ' + self.display[put_index:]
        self.display = new_display    
        
def merge_timing_location_prof(section_timing_location_prof_ei):
    
    timings = section_timing_location_prof_ei[0]
    locations = section_timing_location_prof_ei[1]
    profs = section_timing_location_prof_ei[2]
    eis = section_timing_location_prof_ei[3]
    merged_answer = ""
    for i in range(len(timings)):
        time = timings[i]
        location = locations[i]
        prof = profs[i]
        ei = eis[i]
        extra_det = "("
        if location:
            extra_det += "<i>location</i>: %s" % location
        if prof:
            if location:
                extra_det += " "
            extra_det += "<i>instructor</i>: %s" % prof
        if ei:
            if location or prof:
                extra_det += " "
            extra_det += "<i>EI</i>: %s" % ei
        extra_det += ")"
            
        if extra_det != "()":
            merged_part = "%s %s " % (time, extra_det)
        else:
            merged_part = time + " "
        merged_answer += merged_part
    return merged_answer.strip()
        
        

def time_display_helper(timings_dict, session):
    time_l = timings_dict['L']
    time_t = timings_dict['T']
    time_p = timings_dict['P']
    
    
    desc = ""    
    if not (time_l or time_t or time_p):
        if session == "Full Year":
            raise zeroindexerror
        desc += 'Not offered in this session' 
    else:
        
        #lectures
        desc += '<span id="und">Lectures:</span>'
        if not time_l:
            desc += 'None'
            print '///YOOOOOOO///OOOOOOOOOOOOOOOOOOOO/////0000000000O'
        else:
            desc += '<ul>'
            for lec in time_l:
                desc += '<li>%s</li>' % lec
            desc += '</ul>'
            
            
        if time_t:
            desc += '<span id="und">Tutorials:</span>'
            desc += '<ul>'
            for tut in time_t:
                desc += '<li>%s</li>' % tut
            desc += '</ul>'
            
        if time_p:
            desc += '<span id="und">Practicals:</span>'
            desc += '<ul>'
            for prac in time_p:
                desc += '<li>%s</li>' % prac
            desc += '</ul>'
    
    return desc        
        
                        
def get_full_section_time_span(full_section_list):
    
    full_section_time_span = set()
    
    for section_str in full_section_list:
        section_list = section_str.split() 
        for sub_section in section_list:
            if sub_section.upper() == "TBA":
                full_section_time_span.add("TBA")
            elif "(" in sub_section or not sub_section.isupper() or no_numbers(sub_section):
                continue
            else:
                sub_section_time_span = get_time_span(sub_section)
                full_section_time_span = full_section_time_span.union(sub_section_time_span)

    return full_section_time_span

        

def no_numbers(sub_section):
    nums = '0123456789'
    for char in sub_section:
        if char in nums:
            return False
    return True
            
            

  
def get_time_span(given_time):
    '''string -> Set
    Return a tuple containing the start time (string) as the first item
    and end time (string) as the second time, obtained from string 'given_time'.
    '''

    time_span = set()

    day_span = get_day_span(given_time)
    if not day_span:
        print "YELL NO DAY SPAN!"

    hyphen_position = given_time.find("-")
    if hyphen_position == -1:
        rough_start_time = extract_number(given_time)
        start_time = convert_standard(rough_start_time,True)
        for day in day_span:
            time_span.add(day + start_time)
        return time_span

    rough_start_time = extract_number(given_time[:hyphen_position])
    start_time = convert_standard(rough_start_time, True)
    rough_end_time = given_time[hyphen_position + 1:]
    end_time = extract_number(rough_end_time)
    end_time = str(int(end_time) + (":" in rough_end_time) - 1)
    end_time = convert_standard(end_time, False)
    hour_span =  range(int(start_time), int(end_time) + 1)

    for day in day_span:
        for hour in hour_span:
            time_span.add(day + str(hour))
    return time_span


def get_day_span(given_time):
    all_days = []
    if 'M' in given_time:
        all_days.append('M')
    if 'T' in given_time:
        all_days.append('T')
    if 'W' in given_time:
        all_days.append('W')
    if 'R' in given_time:
        all_days.append('R')
    if 'F' in given_time:
        all_days.append('F')
        
    return all_days



def convert_standard(s,start):
    '''string -> string
    Return the 'CR' standard form of the string 's'.
    If bool 'start' is True then record 9 as 9 AM, else
    record it as 9 PM.
    '''
    
    if s == "9" and start:
        return "-3"
    elif s == "10":
        return "-2"
    elif s == "11":
        return "-1"
    elif s == "12":
        return "0"
    else:
        return s


def extract_number(s):
    '''string -> string
    Return a new string which contains all the substrings from string 's'
    which are digits, till the first occurence of a non digit.
    '''

    # We have on our mind that there
    # could be a ":" or an alphabet
    # occuring.
    extracted_digits = ""
    numbers_started = False
    for substring in s:
        if substring.isdigit():
            numbers_started = True
            extracted_digits += substring
        elif not numbers_started:
            continue
        else:
            break
    return extracted_digits.strip()

    