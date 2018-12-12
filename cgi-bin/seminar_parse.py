import urllib
from CourseRunObjects import Seminar

class PageNotFound(Exception):
    pass


def parse_calendar(page, seminar_dict, seminar_code, seminar_breadth):

    str_page = page.read()
    end_of_table = str_page.rfind('</table>')
    str_page = str_page[end_of_table : ]
    # Check if page is found correctly
    # if not then raise the pagenotfound error
    if '404 Not Found' in str_page:
        raise PageNotFound('seminar program %s not found' % seminar_program)
    
    ind = 0

    while 1:
        seminar_head, ind = find_next_course_head(str_page, ind)
        if not seminar_head:
            break
        seminar_desc = '<p>' + collect_course_desc(str_page, ind)
        if seminar_code == "XBC199Y1":
            seminar_breadth = find_cross_breadth_categories(seminar_desc)
        
        seminar_dict[seminar_head] = [Seminar(seminar_code, seminar_desc, seminar_head), seminar_breadth, []]
        
        ind += 1
    
    return seminar_dict
        

def collect_course_desc(str_page, ind):
    
    start_desc = ind
    end_desc = str_page.find('<hr', ind)
    if end_desc == -1:
        total_desc = str_page[ind:]
    else:
        total_desc = str_page[ind:end_desc]
    total_desc = total_desc.replace('\xc2','')
    return total_desc


def find_next_course_head(str_page, ind):
    
    while 1:
        strong_start = str_page.find('<strong>', ind)
        if strong_start == -1:
            return (False,False)

        strong_end = str_page.find('</strong>', strong_start)
        head_content = str_page[strong_start + 8 : strong_end].strip()
        

        if head_content in all_seminar_heads:
            return (head_content, strong_start)
        ans_similar = similar_in_list(head_content, all_seminar_heads)
        if ans_similar:
            return (ans_similar,strong_start)
        else:
            ind = strong_start + 1


def similar_in_list(s, L):
    if s == "Baguette S":
        return "Baguette Served With Poutine and a Hint of Zombies: French and Francophone Cultures Beyond Stereotypes"
    if s.startswith("Tragically Unhip"):
        return 'Tragically Unhip: Great Thinkers of the Late 19th and Early 20th Centuries'
    if not s:
        return False
    open_tag = s.find('<')
    if open_tag == 0:
        open_tag = s.find('<', 1)
    if open_tag != -1:
        s = s[:open_tag]
    
    open_par = s.find('(')
    if open_par != -1:
        s = s[:open_par]
    
    s = s.replace('&quot;', '')
    s = s.replace('&rdquo;', '"')
    s = s.replace('&ldquo;', '"')
    s = s.replace('&rsquo;', '"')
    

    for ele in L:
        if similar(s, ele):
            return ele
    
    
def similar(s1, s2):
    
    if s1 == s2:
        return True

    ls1 = list(s1)
    ls2 = list(s2)
    s1_match = 0
    for s in s1:
        if s in ls2:
            s1_match += 1
            ls2.remove(s)
            
    s1_to_s2_perc = s1_match / float(len(s1))
    
    s2_match = 0
    for s in s2:
        if s in ls1:
            s2_match += 1
            ls1.remove(s)
    s2_to_s1_perc = s2_match / float(len(s2))
    
    if s1_to_s2_perc > 0.80 and s2_to_s1_perc > 0.80:
        return s2
   
    
def find_cross_breadth_categories(course_description):
    
    breadth_category_list = []
    lower_course_dec = course_description.lower()
    
    if 'creative and cultural representation' in lower_course_dec or 'creative and cultural  representation' in lower_course_dec:
        breadth_category_list.append('1')

    if 'thought, belief, and behaviour' in lower_course_dec or 'thought, belief,  and behaviour' in lower_course_dec:
        breadth_category_list.append('2')

    if 'society and its institutions' in lower_course_dec or 'society and  its institutions' in lower_course_dec or 'society and its  institutions' in lower_course_dec:
        breadth_category_list.append('3')

    if 'living things and their environment' in lower_course_dec or 'living things and  their environment' in lower_course_dec or 'living things  and their environment' in lower_course_dec:
        breadth_category_list.append('4')

    if 'the physical and mathematical universes' in lower_course_dec or 'the physical and  mathematical universes' in lower_course_dec:
        breadth_category_list.append('5')

    if len(breadth_category_list) != 2:
        print 'NOCROSSBREADTH', lower_course_dec, breadth_category_list
    
    
    return breadth_category_list
        
        
        
def parse_timetable(page, seminar_dict):
    
    
    proper_seminar_dict = {}
    str_page = page.read().replace('&nbsp;', '')
    # Check if page is found correctly
    # if not then raise the pagenotfound error
    if '404 Not Found' in str_page:
        raise PageNotFound('program %s not found' % program)

    table_list = extract_table(str_page)

    table_index = 2    
    table_length = len(table_list)
        
    while table_index < table_length:
    
        current_row = table_list[table_index]
        
        if 'H1F' in current_row[0]:
            session = "F"
            table_index += 1
            continue
        if 'H1S' in current_row[0]:
            session = "S"
            table_index += 1
            continue
        if 'Y1Y' in current_row[0]:
            session = "Y"
            table_index += 1
            continue
          
        if len(current_row) == 1:
            table_index += 1
            continue
        
        seminar_name = current_row[1]
        if 'Cancel' in current_row or 'cancel' in current_row:
            table_index += 1
            continue
        
        
        time = correct_uoft(clean_up(current_row[3]))
        location = ""
        prof = clean_up(current_row[5])
        ei = ""
        
        update_course(seminar_name, session, 'L', [time], [location], [prof], [ei], seminar_dict)
        
        table_index += 1
    return seminar_dict    


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

def update_course(seminar_name, session, section_code, collected_time, collected_location,
                  collected_profs, eis, universal_course_dict):

    if seminar_name in universal_course_dict:
        if not collected_time:
            raise zeroindexerror
        universal_course_dict[seminar_name][2].append(session)
        universal_course_dict[seminar_name][0].set_timing_and_location(session, [collected_time, collected_location, collected_profs, eis],section_code)
        return

    ans_similar = similar_in_list(seminar_name, all_seminar_heads)
    if ans_similar:
        if not collected_time:
            raise zeroindexerror
        universal_course_dict[ans_similar][2].append(session)
        universal_course_dict[ans_similar][0].set_timing_and_location(session, [collected_time, collected_location, collected_profs, eis], section_code)
    else:
        print "rijgtrjt", seminar_name


def correct_uoft(time):

    full_list = time.split()
    try:
        first = full_list[0].strip()
        second = full_list[1].strip()
        if is_days(first) and no_numbers(first):
            checko = second.replace('-', '')
            checko = checko.replace(':', '')
            if checko.isdigit():
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
            

def generate_seminar_dict():
    
    for seminar_code_and_breadth in seminar_programs:
        seminar_code = seminar_code_and_breadth[0]
        seminar_breadth = seminar_code_and_breadth[1]
        page = urllib.urlopen("http://www.artsandscience.utoronto.ca/ofr/1213_199/%s.html" % seminar_code.lower())
        parse_calendar(page, seminar_dict, seminar_code, seminar_breadth)
        
    
    timetable_page = urllib.urlopen('http://www.artsandscience.utoronto.ca/ofr/timetable/winter/assem.html')
    proper_seminar_dict = parse_timetable(timetable_page, seminar_dict)
        
    return proper_seminar_dict
    
    
    
seminar_dict = {}
    
seminar_programs = [['CCR199H1', ['1']], ['CCR199Y1', ['1']], ['TBB199H1', ['2']], ['TBB199Y1',['2']],
                        ['SII199H1', ['3']], ['SII199Y1', ['3']], ['LTE199H1',['4']], ['LTE199Y1',['4']],
                        ['PMU199H1',['5']], ['PMU199Y1',['5']], ['XBC199Y1', ['']]]
        
all_seminar_heads = ['The "New" Visual Culture', 'Words, Rhythm, and Music: What Makes a Song?', 'Sport as Culture, Sport in Culture', 'The Anthropology of Brands', 'Traditional Chinese Culture and Modernity', 'When Species Meet', 'French Perspectives on War and Identity', 'Our Vampires, Ourselves: Of Mirrors, Shadows and ', 'Technology and the Human', 'Iranian Women Write Their Lives: The First Generation', 'The Mummy: Technology and Transformation', 'Multiculturalism, Philosophy, and Film', 'From Achilles to Zorba: continuity in Greek literature', 'Chinese Gastronomy and Beyond', 'Fictions of the US-Canadian Border', 'Language and Translation', 'The Age of Reason and the New World', 'Iranian Women Write Their Lives: The Young Generation', 'Nationalism and Ethnic Contest in the Biblical World', 'The Experience of Music', 'Pushkin and Russian Opera', 'The Slavic Grecian Formula: From Ancient Rhapsode to Modern Rap Song', 'The Criminal Mind', 'The Cossacks', 'Roots of Western Ideas',
'The Earth\'s Body', 'Language and Advertising', 'Language and the Internet', 'Ethics and Fiction', 'From Gibraltar to the Ganges', 'Tragically Unhip: Great Thinkers of the Late 19th and Early 20th Centuries', 'Innovative Teaching Methods in Chemistry', 'Korea at War, 1950-53', 'Dialectics of Dialects', 'Sustaining Languages', 'Science and Religion', 'A History of Knowledge', '"Reading" Toronto, the First 12,000 Years', 'Teams, Bands and Gangs: A study of small group processes', 'Ethics and You: Challenging Issues Facing University Students', 'Youth in Global Financial Crisis', 'Religion and Archaeology', "Greece's Wonderland", 'Computer Networks and Society', 'Contemporary Economic Systems', 'Debating and Understanding Current Environmental Issues', 'Political Spaces', 'Cities and Everyday Life', 'Globalization and it Discontents: Germany as Case Study', 'Pacifists and Peaceniks: Canadian Peace Movements in Transnational Context', 'The Process of Archaeological Discovery', 'Environmental Change: Producing New Natures', 'Biotechnology and Society', 'Human Development', 'Environmental Change: Drivers and Interactions', 'Human and Biological Viruses', 'Genes, Genomes and Us', 'Great Astronomical Issues', 'Astronomy at the Frontier', 'The Quantum World and Its Classical Limit', 'The Chemistry of Cleaning: From Basic Science to Innovation and Wealth Creation', 'Video Game Design', 'Aha! Mathematical Discovery and Creative Problem Solving', 'The Poetry of Physics and the Physics of Poetry', 'DNA and the Chemistry of Heredity', 'Mathematical Explorations', 'Seeing and Believing: Patterns of Visual Communication', 'The Fine Art of Murder: Reading Detective Fiction', 'Raiders, Traders, and Invaders: the Vikings and Their Descendents', 'Rhetoric: Theory, Criticism, Practice', 'Reading and Writing Poetry', 'Visual Culture: Understanding Images', 'More Than Just a Dinner Party: High Style and Serious Attitude in the Literary Salon of 1830s Paris.',
'Baguette Served With Poutine and a Hint of Zombies: French and Francophone Cultures Beyond Stereotypes', 'The Fine Art of Murder: Reading Detective Fiction', 'Sorrows and Joys of the Immigrant Experience and the Myth of America', 'Classics of the Italian Cinema: Obsession, Passion, Dreams and Death', 'Italian Tales from the Age of Shakespeare', 'Fatal Attraction: The Lure of the Villain in Literature', 'Autobiography and the Making of the Self in Western Culture', 'Great Ideas in Social and Political Thought', 'Language and the Internet', 'Christianity: A Religion?', 'The Nature of Psychological Enquiry', 'Embarrassment of Scriptures', 'Abraham, Moses, Jesus and Muhammad: Sociology of the Monotheistic Religions', 'Knowing and Not Knowing', 'Schools and Communities', 'The Development of Economic Ideas', 'World War II France: Resistors, Bystanders, Collaborators and Nazis', 'Public, Private, and the Liberal State', 'China in the World', 'Explaining Political Transitions', 'How We Use Time in Everyday Life', 'Plants As We See Them', 'Ecology of Trees and Forests', 'Time', 'Climate Change: Software, Science and Society', 'Mathematics in Current Events', 'Mathematics: At Work, Home and Play', 'Modern Physics in Perspective', 'How To Gamble If You Must', 'Statistics For Life', 'Machiavelli and the Power Game', 'Visual Culture in the Ancient World', 'How To Study Everyday Life', 'The Past Within The Present', 'Roll Over, Beethoven: Music, Media and the Marketplace', 'Society, Religion and Architecture in the Ancient Mediterranean', 'Interpretation of History in Society, War, Family and Religion', 'Schools, Culture & Society', 'Medieval Medicine', 'Imperialism and Nationalism', "Ideologies and Social Movements in China's Modern Transformation", 'Science and Social Choice', 'Life and Death in the Solar System', 'Thinking About Planet Earth']


if __name__ == "__main__":    
    generate_seminar_dict()
        