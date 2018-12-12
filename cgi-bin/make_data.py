#!/usr/bin/python2.7

from course_run_parse import generate_unified_course_dict
from seminar_parse import generate_seminar_dict
from CourseRunObjects import Course, Seminar
import cPickle


def make_search_friendly_dict(rough_course_dict, seminar_dict):

    d = {}
    all_pns = {}

    for (course_code, details) in rough_course_dict.iteritems():
        
        for lower_pn in details[0].lower_pns:
            if lower_pn not in all_pns:
                all_pns[lower_pn] = []
            all_pns[lower_pn].append(details[0])

        d[course_code] = details[0]

    all_pns['first year seminars'] = []
    for (course_name, details) in seminar_dict.iteritems():
        seminar_code = details[0].course_code
        if seminar_code not in d:
            d[seminar_code] = []
        else:
            d[seminar_code].append(details[0])
        all_pns['first year seminars'].append(details[0])
        
    return (d, all_pns)


def index_course_dict(rough_course_dict, categories_specified, sem_dict, is_breadth):
        
    d = {}
    for category in categories_specified:
        for year in ['1','2','3','4','5']:
            for credit in ['H', 'Y']:
                for session in ['F','S','Y','N']:     
                    d[category + year + credit + session] = set()

    for (course_code, details) in rough_course_dict.iteritems():
        year = course_code[3]
        credit = course_code[6]
        sessions = details[3]
        if not sessions:
            sessions = ['N']            
        if is_breadth:
            categories = details[1]
        else:
            categories = details[2]

        for category in categories:
            for session in sessions:
                d[category + year + credit + session].add(details[0])
                
    if is_breadth:
        for (course_name, details) in sem_dict.iteritems():
            course_code = details[0].course_code
            year = course_code[3]
            credit = course_code[6]
            sessions = details[2]
            if not sessions:
                sessions = ['N']            
            categories = details[1]
    
            for category in categories:
                for session in sessions:
                    d[category + year + credit + session].add(details[0])
        
    return d
                    
    

if __name__ == "__main__":
    
    unified_course_dict = generate_unified_course_dict()
    seminar_dict = generate_seminar_dict()
    
    for (crs, det) in unified_course_dict.iteritems():
        det[0].generate_display()
    
    for (crs, det) in seminar_dict.iteritems():
        det[0].generate_display()
        
    breadth_dict = index_course_dict(unified_course_dict, ['1','2','3','4','5','6'], seminar_dict, is_breadth=True)
    distribution_dict = index_course_dict(unified_course_dict, ['7', '8', '9', '0'], {}, is_breadth=False)
    
    breadth_dict_file = open('breadth_dict.data', 'w')
    distribution_dict_file = open('distribution_dict.data', 'w')
    cPickle.dump(breadth_dict, breadth_dict_file)
    cPickle.dump(distribution_dict, distribution_dict_file)
    breadth_dict_file.close()
    distribution_dict_file.close()

    search_dict, program_dict = make_search_friendly_dict(unified_course_dict, seminar_dict)
    search_dict_file = open('search_dict.data', 'w')
    cPickle.dump(search_dict, search_dict_file)
    search_dict_file.close()
    
    program_dict_file = open('program_dict.data', 'w')
    cPickle.dump(program_dict, program_dict_file)
    program_dict_file.close()
    
    