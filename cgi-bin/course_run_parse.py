import urllib
from course_run_url_finder import find_urls
from CourseRunObjects import Course,Seminar
from seminar_parse import similar

class PageNotFound(Exception):
    pass


def parse_calendar(page, universal_course_dict, program_name):

    str_page = page.read()
    # Check if page is found correctly
    # if not then raise the pagenotfound error
    if '404 Not Found' in str_page:
        raise PageNotFound('program %s not found' % program)
    cur_course_index = 0
    while True:
        next_course_details = find_next_course_index(str_page, cur_course_index)
        if not next_course_details:
            break
        cur_course_index, cur_course_code = next_course_details
        # finds the html info of the course
        course_description = find_course_description(str_page, cur_course_index, cur_course_code)
        if not course_description:
            cur_course_index += 1
            continue
        else:
            course_description = refine_desc(course_description)
        if course_description.count('<strong>') != course_description.count('</strong>'):
            strongless.append(cur_course_code)
        breadth_category_list = find_breadth_categories(course_description)
        distribution_category_list = find_distribution_categories(course_description)
        
        course_program = cur_course_code[:3]
        #////// extra checking stuff
        if course_program not in all_programs:
            all_programs.append(course_program)
        
        actual_course = True
        if cur_course_code in universal_course_dict:
            already_present_course = universal_course_dict[cur_course_code][0]
            if similar(already_present_course.course_description, course_description):
                already_present_course.program_names += (" + " +  program_name)
                already_present_course.lower_pns.append(program_name.lower())
                print '--------------------', cur_course_code, program_name, already_present_course.program_names
                actual_course = False
            elif len(already_present_course.course_description) > len(course_description)*5:
                actual_course = False
        if actual_course:
            course_memory = Course(cur_course_code,course_description, program_name)
            universal_course_dict[cur_course_code] = [course_memory,
                                                  breadth_category_list,
                                                  distribution_category_list,
                                                  []]

        cur_course_index += 1




def find_next_course_index(str_page, cur_course_index):
    
    not_sure_index = str_page.find("<a name=", cur_course_index)
    if not_sure_index == -1: #end of page
        return False
    
    open_quote_index = not_sure_index + 8
    # side-line test
    if str_page[open_quote_index] != '"':
        print 'cry: open quote index not "'
        
    close_quote_index = str_page.find('"', open_quote_index + 1)
    
    # side-line test
    if open_quote_index - close_quote_index > 20:
        print 'cry: open quote index and close quote index part apart'
        
    quote_content = str_page[(open_quote_index + 1) : close_quote_index]
    
    if not valid_course_code(quote_content):
        return find_next_course_index(str_page, close_quote_index)
    
    else:
        return (not_sure_index, quote_content)
    
    
def valid_course_code(quote_content):
    
    if len(quote_content) == 8:
        if quote_content[0:3].isalpha() and quote_content[0:3].isupper():
            if quote_content[3:6].isdigit():
                if quote_content[6] == "H" or quote_content[6] == "Y":
                    if quote_content[7] == '1' or quote_content[7] == '0':
                        return True
                    else:     # not a st.george course
                        print 'cry: not a st.george course', quote_content
                        
         
                       
def find_course_description(str_page, cur_course_index, cur_course_code):
    
    breadth_location_index = str_page.find('Breadth Requirement:', cur_course_index)
    distribution_location_index = str_page.find('Distribution Requirement Status:', cur_course_index)
    if breadth_location_index != -1 and distribution_location_index != -1:
        if distribution_location_index > breadth_location_index:
            print 'cry: distribution mentioned after breadth', cur_course_code
    if breadth_location_index == -1:
        print 'cry: course head but without a breadth requirement left in the file', cur_course_code
    # Now we'll check for the course which occurs after our current
    # course and see if the found breadth requirement doesn't belong to it.
    
    next_course_details = find_next_course_index(str_page, cur_course_index + 1)
        
    if next_course_details:
        next_course_index, next_course_code = next_course_details
        # if we have our found breadth not beloonging to our current course
        if next_course_index < breadth_location_index:
            if next_course_index < distribution_location_index:
                print 'cry: our found breadth AND DISTRIBUTION not beloonging to our current course', cur_course_code
                return False
            
            else:
                print 'cry: our found breadth not beloonging to our current course***************************', cur_course_code
                end_of_course_index = str_page.find('<', distribution_location_index)
                course_content = str_page[cur_course_index : end_of_course_index]
        
        else:
            end_of_course_index = str_page.find('<', breadth_location_index)
            course_content = str_page[cur_course_index : end_of_course_index]
        
        
    else:
        if breadth_location_index != -1:
            end_of_course_index = str_page.find('<', breadth_location_index)
            course_content = str_page[cur_course_index : end_of_course_index]
        elif distribution_location_index != -1:
            end_of_course_index = str_page.find('<', distribution_location_index)
            course_content = str_page[cur_course_index : end_of_course_index]
        
        else:
            print 'cry: LAST our found breadth AND DISTRIBUTION not beloonging to our current course', cur_course_code
            return False
    
    return course_content


def refine_desc(desc):
    desc = desc.replace('href="', 'href="http://www.artsandscience.utoronto.ca/ofr/calendar/')
    desc = desc.replace("href='", 'href="http://www.artsandscience.utoronto.ca/ofr/calendar/')
    desc = desc.replace('<p> </p>', '')
    desc = desc.replace('<p></p>', '')
    desc = desc.replace('<p>&nbsp;</p>', '')
    desc = desc.replace('font-size:', '')
    desc = desc.replace('font-family:', '')
    desc = desc.replace('background-color:', '')

    return desc

    
def find_breadth_categories(course_description):
    
    breadth_category_list = []
    breadth_location_index = course_description.find('Breadth Requirement:') 
    if breadth_location_index != -1:
        end_of_breadth_index = course_description.find('<br>', breadth_location_index)
        breadth_content = course_description[breadth_location_index : end_of_breadth_index].lower()

        #side-line-error
        if len(breadth_content) > 120:
            print 'cry: breadth_content too long', breadth_content, course_description

        if 'creative' in breadth_content:
            breadth_category_list.append('1')

        if 'thought' in breadth_content:
            breadth_category_list.append('2')

        if 'society' in breadth_content:
            breadth_category_list.append('3')

        if 'living' in breadth_content:
            breadth_category_list.append('4')

        if 'physical' in breadth_content:
            breadth_category_list.append('5')

        if 'none' in breadth_content or not breadth_category_list:
            breadth_category_list.append('6')

    return breadth_category_list


def find_distribution_categories(course_description):
    
    distribution_category_list = []
    distribution_location_index = course_description.find('Distribution Requirement Status:')
    if distribution_location_index != -1:
        end_of_distribution_index = course_description.find('<br>', distribution_location_index)
        distribution_content = course_description[distribution_location_index : end_of_distribution_index].lower()
        
        #side-line-error
        if len(distribution_content) > 91:
            print 'cry: distribution_content too long', distribution_content,course_description
        
        if 'humanities' in distribution_content:
            distribution_category_list.append('7')
            
        if 'social science' in distribution_content:
            distribution_category_list.append('8')
        
        if 'a science' in distribution_content or 'or science' in distribution_content:
            distribution_category_list.append('9')
        
        if not distribution_category_list:
            distribution_category_list.append('0')
            
    return distribution_category_list
    
    
def parse_timetable(page, universal_course_dict):
    

    str_page = page.read().replace('&nbsp;', '')
    # Check if page is found correctly
    # if not then raise the pagenotfound error
    if '404 Not Found' in str_page:
        raise PageNotFound('program %s not found' % program)

    table_list = extract_table(str_page)

    table_index = 0    
    for tr in table_list:
        if valid_course_code(tr[0]):
            break
        table_index += 1

    table_length = len(table_list)
        
    # precondition - the loop will start off with
    # a course code in the row.
    while table_index < table_length:
        emergency = False
        cancel = False
        current_row = table_list[table_index]
        course_code = current_row[0].strip()
        
        first_iteration_done = False
        session = current_row[1]

        while table_index < table_length:
            current_row = table_list[table_index]
    
            if current_row[0] and first_iteration_done:
                emergency = True
                break

            #side-line test
            if current_row[3]:
                if first_iteration_done and not cancel:
                    update_course(course_code, session, section_code, collected_time,
                                  collected_location, collected_profs, collected_eis, universal_course_dict)

                if 'cancel' in current_row or 'Cancel' in current_row or (len(current_row) < 8 and 'Cancel' in str(current_row)):
                    #//print "cancel row list", current_row
                    collected_time, collected_location, collected_profs, collected_eis = [], [], [], []
                    cancel = True
                    table_index += 1
                    first_iteration_done = True
                    continue
                else:
                    cancel = False
                    section_code = current_row[3][0]
                    
                    time = correct_uoft(clean_up(current_row[5]))
                    location = clean_up(current_row[6])
                    prof = clean_up(current_row[7])
                    ei = clean_up(current_row[8])
                
                    collected_time = [time]
                    collected_location = [location]
                    collected_profs = [prof]
                    collected_eis = [ei]
                    

                    table_index += 1
                    first_iteration_done = True
                    continue

            time = correct_uoft(clean_up(current_row[5]))
            location = clean_up(current_row[6])
            prof = clean_up(current_row[7])
            ei = clean_up(current_row[8])
    
            collected_time.append(time)
            collected_location.append(location)
            collected_profs.append(prof)
            collected_eis.append(ei)
            
            if not first_iteration_done:
                print "duck"
            table_index += 1

        if collected_time:
            update_course(course_code, session, section_code, collected_time,
                              collected_location, collected_profs, collected_eis,  universal_course_dict)
        if not emergency:
            table_index += 1


def clean_up(raw):
    raw = raw.replace('<br/>', ' ')
    raw = raw.replace('<br>', ' ')
    raw = raw.replace('<br />', ' ')
    raw = raw.replace('<br >', ' ')
    if "<" in raw:
        if raw.index('<') == 0:
            raise zeroindexerror
        raw = raw[0:raw.index('<')]
    return raw.strip()

def correct_uoft(time):

    full_list = time.split()
    try:
        first = full_list[0].strip()
        second = full_list[1].strip()
        if is_days(first) and no_numbers(first):
            checko = second.replace('-', '')
            checko = checko.replace(':', '')
            if checko.isdigit():
                print 'woohoo', first + second
                full_list = [full_list[0] + full_list[1]] + full_list[2:]                
    except:
        pass
            
    ans = ""
    for i in full_list:
        ans += (i + ' ')
    return ans.strip()

def is_days(s):
    if '(' in s or (not s.isupper()):
        return False
    days = 'MTWRF'
    for char in s:
        if char not in days:
            return False
    return True
        
        
def no_numbers(sub_section):
    nums = '0123456789'
    for char in sub_section:
        if char in nums:
            return False
    return True


def update_course(course_code, session, section_code, collected_time, collected_location,
                  collected_profs, collected_eis, universal_course_dict):

    if course_code not in universal_course_dict:
        print "OMGGGGGGG course %s found in timetable not in universal dict" % course_code
        return
    
    if not collected_time:
        raise zeroindexerror
    universal_course_dict[course_code][3].append(session)
    universal_course_dict[course_code][0].set_timing_and_location(session, [collected_time, collected_location, collected_profs, collected_eis],
                                                                    section_code)
    


               
def extract_table(str_page):
    
    table_list = []
    start_tr = 0
    end_tr = 0
    table_end = find_next(str_page, "</table>", 0);
    while 1:
        start_tr = find_next(str_page, "<tr", end_tr)
        if start_tr > table_end:
            break
        if start_tr == -1:
            break

        end_tr = find_next(str_page, "</tr>", start_tr)
        tr_content = str_page[start_tr : end_tr]
        table_list.append(extract_tr(tr_content))
        
        start_tr =  end_tr 
        
    return table_list

        
def extract_tr(tr_content):
    
    td_list = []
    
    start_td = 0
    end_td = 0
    
    while 1:
        start_td = find_next(tr_content, "<td", end_td)

        if start_td == -1:
            break
        end_td = find_next(tr_content, "</td>", start_td) + 4

        td_content = tr_content[start_td : end_td + 1]
        td_list.append(non_html_content(td_content.strip()))
        start_td = end_td   
    return td_list


def non_html_content(html_content):


    if not html_content.startswith("<"):
        return html_content.strip()

    else:   #there is presence of html tags
        close_html = html_content.index(">")
        open_html = html_content.rfind("<")
        trimmed_html_content = html_content[close_html + 1: open_html]
        return non_html_content(trimmed_html_content)



def find_next(str_page, to_search, cur_index):

    lower_ind = str_page.find(to_search, cur_index)
    upper_ind = str_page.find(to_search.upper(), cur_index)

    if lower_ind != -1:
        if upper_ind != -1:
            return min(lower_ind, upper_ind)
        return lower_ind
    return upper_ind
            

    

def generate_unified_course_dict():                
    universal_course_dict = {}
    
    calendar_programs, calendar_program_names = find_urls(calendar=True)
    print calendar_program_names
    count = 0
    for program in calendar_programs:
        program_name = calendar_program_names[count]
        print 'CURRENT PROGRAM -> %s' % program
        page = urllib.urlopen("http://www.artsandscience.utoronto.ca/ofr/calendar/%s" % (program))
        parse_calendar(page, universal_course_dict, program_name)
        count += 1
      
      
    timetable_programs = find_urls(calendar=False)[0]
    
    for program in timetable_programs:
        print 'CURRENT PROGRAM -> %s' % program
        page = urllib.urlopen("http://www.artsandscience.utoronto.ca/ofr/timetable/winter/%s" % (program))
        parse_timetable(page, universal_course_dict)
    
    return universal_course_dict

all_programs = []
timetable_courses = []
calendar_courses = []
strongless = []

if __name__ == "__main__":
    
    generate_unified_course_dict()

print all_programs, '\n'  
print strongless