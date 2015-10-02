#!/usr/bin/python
# coding=utf-8

from random import randint
import openpyxl
import copy
import os
import sys
import datetime

data_filename = "enkater.xlsx"
mission_filename = "missions.txt"
classes_filename = "klasslista.txt"
class_sorting_filename = "klasssortering.txt"
questions_filename = "questions.txt"
sorting_filename = "sorting.txt"
nollan_filename = "nollan.txt"

columns_about_nollan = [
    u"Tidstämpel",
    u"Förnamn",
    u"Efternamn",
    u"Personnummer",
    u"Adress",
    u"Telefonnr",
    u"Kön",
    u"Program",
    ]

columns_one2five = [
    u"1. Hur bra är Ø:an egentligen på att... [...snickra/bygga]",
    u"1. Hur bra är Ø:an egentligen på att... [...konstruera]",
    u"1. Hur bra är Ø:an egentligen på att... [...måla/teckna]",
    u"1. Hur bra är Ø:an egentligen på att... [...sy]",
    u"1. Hur bra är Ø:an egentligen på att... [...designa]",
    u"1. Hur bra är Ø:an egentligen på att... [...pyssla]",
    u"1. Hur bra är Ø:an egentligen på att... [...heja]",
    u"1. Hur bra är Ø:an egentligen på att... [...samla saker]",
    u"1. Hur bra är Ø:an egentligen på att... [...lösa gåtor]",
    u"1. Hur bra är Ø:an egentligen på att... [...smyga]",
    u"1. Hur bra är Ø:an egentligen på att... [...spionera]",
    u"1. Hur bra är Ø:an egentligen på att... [...uppträda]",
    u"1. Hur bra är Ø:an egentligen på att... [...sjunga]",
    u"1. Hur bra är Ø:an egentligen på att... [...skriva låtar]",
    u"1. Hur bra är Ø:an egentligen på att... [...dansa]",
    u"1. Hur bra är Ø:an egentligen på att... [...hålla tal]",
    u"1. Hur bra är Ø:an egentligen på att... [...leka/busa]",
    u"1. Hur bra är Ø:an egentligen på att... [...peppa folk]",
    u"1. Hur bra är Ø:an egentligen på att... [...tävla]",
    u"1. Hur bra är Ø:an egentligen på att... [...ge smicker]",
    u"1. Hur bra är Ø:an egentligen på att... [...samla poäng]",
    u"1. Hur bra är Ø:an egentligen på att... [...laga mat]",
    u"1. Hur bra är Ø:an egentligen på att... [...göra egna recept]",
    u"1. Hur bra är Ø:an egentligen på att... [...baka]",
    u"1. Hur bra är Ø:an egentligen på att... [...äta kakor]",
    u"1. Hur bra är Ø:an egentligen på att... [...servera]",
    u"1. Hur bra är Ø:an egentligen på att... [...arrangera fester]",
    u"1. Hur bra är Ø:an egentligen på att... [...använda sociala nätverk]",
    u"1. Hur bra är Ø:an egentligen på att... [...videofilma]",
    u"1. Hur bra är Ø:an egentligen på att... [...skriva artiklar]",
    u"1. Hur bra är Ø:an egentligen på att... [...redigera film]",
    u"1. Hur bra är Ø:an egentligen på att... [...blogga]",
    u"1. Hur bra är Ø:an egentligen på att... [...fotografera]",
    u"1. Hur bra är Ø:an egentligen på att... [...ta selfies]",
    u"1. Hur bra är Ø:an egentligen på att... [...snapchatta]",
    u"1. Hur bra är Ø:an egentligen på att... [...skrika]",
    u"1. Hur bra är Ø:an egentligen på att... [...spela fotboll]",
    u"1. Hur bra är Ø:an egentligen på att... [...hålla uppvärmning]",
    u"1. Hur bra är Ø:an egentligen på att... [...köra bil]",
    u"1. Hur bra är Ø:an egentligen på att... [...pricka rätt]",
    ]

columns_attributes = [
    u"2. Spelar Ø:an gitarr, maracas, banjo, orgel eller något annat instrument kanske?",
    u"3. Isåfall, vad ∅:an?",
    u"4. Kommer Ø:an ta med det till Linköping?",
    u"5. Känner Ø:an någon eller några som blivit upphöjd till etta på Linköpings Tekniska Högskola?",
    u"6. Isåfall, Vem/vilka? Klass? Program?  Massa frågor ∅:an!",
    u"7. Har Ø:an någon slags allergi eller specialkost?",
    u"8. Vilka egenskapsord passa in på Ø:an?",
    u"9. Vad har Ø:an i Linköping?",
    u"10. Har Ø:an erfarenhet av något av följande yrken?",
    u"Annat yrke:",
    u"11. Vilka sporter utövar Ø:an?",
    u"Annan sport:",
    u"12. Kan Ø:an tänka sig att uppträda inför publik?",
    ]

columns_extra = [
    u"13. Har Ø:an varit på gymnasiebesök på Maskinteknologsektionen på LiTH?",
    u"14. Har ∅:an studerat på universitet/högskola tidigare?",
    u"15. Vad tycker Ø:an att det allsmäktiga Phadderiet mer bör veta om Ø:an?",
    u"16. Vad är ∅:ans visdomsord?",
    ]

class Nollan:
    def __init__(self, firstname, familyname, sex, id_nr, program, one2five, attr):
        self.firstname = firstname
        self.familyname = familyname
        self.name = firstname + ' ' + familyname
        self.sex = sex
        self.program = program
        self.school_class = "N/A"
        self.id_nr = id_nr
        self.match = {}
        self.match_relative = {}
        self.assigned = None
        self.one2five = one2five
        self.attr = attr
        self.dealbreaker = []
        self.question_post = "N/A"
        self.question_random = "N/A"

    def __str__(self):
        s = "Nollan: "
        if self.name is not None:
            s += self.name
        # if self.id_nr is not None:
        #   s += ", " + unicode(self.id_nr)
        if self.program is not None:
            s += ", " + self.program

        s += '\n'
        return s


    def print_all(self):
        s = "Nollan: "
        if self.name is not None:
            s += self.name + ", "
        else:
            s += "N/A, "

        if self.assigned is not None:
            s += self.assigned + ", "
        else:
            s += "N/A, "

        return s

    def set_match(self, mission, score):
        self.match[mission] = score

    def set_match_relative(self, mission, score):
        self.match_relative[mission] = score

class Mission:
    def __init__(self, name):
        self.name = name
        self.priority = 2
        self.count = 0
        self.boys = 0
        self.girls = 0
        self.instrument = 0
        self.dpu = 0
        self.dpu_a = 0
        self.dpu_b = 0
        self.m = 0
        self.m_a = 0
        self.m_b = 0
        self.m_c = 0
        self.m_d = 0
        self.emm = 0
        self.emm_a = 0
        self.emm_b = 0

        self.one2five = ""
        self.attr = ""
        self.dealbreaker = []
        self.assigned = []
        self.questions = []
        self.sex = '-'
        self.school_class = '-'
        self.program = '-'
        self.id = id(self)

    def is_valid(self):
        if self.name is None:
            print "ERROR: Could not create mission without name."
            return False

        if self.count == 0:
            print "ERROR: Could not create mission without any nollan."
            return False

        if self.one2five == "" and self.attr == "":
            print "ERROR: Could not create mission without any attributes or 1 to 5 questions."
            return False

        if self.questions == []:
            print "ERROR: Could not create mission without any questions."
            return False

        return True

    def __str__(self):
        return "Name: " + str(self.name) \
                + "\nPriority: " + str(self.priority) \
                + "\nNollan: " + str(self.count)

def read_missions(path):
    missions = []
    current_mission = None

    if not os.path.exists(path):
        print "ERROR: Could not find " + path
        sys.exit(0)

    print "Reading missions from", mission_filename

    with open(path) as f:
        try:
            for line in f:
                if line != "\n" and line[0] != '#':
                    line = line.translate(None, '\n')
                    line = line.replace(': ', ':')
                    if line[0] == '%':
                        if current_mission is not None:
                            add_missions(current_mission, missions)
                        current_mission = Mission(line[2:])
                    else:
                        key = line.split(':')[0].lower()
                        arg = line.split(':')[1]
                        
                        klasser = ["m_a", "m_b", "m_c", "m_d", "emm_a", "emm_b", "dpu_a", "dpu_b"]
                        tot_klasser = 0


                        if key == "prio":
                            current_mission.priority = int(arg)

                        elif key == "fraga" or key == "fråga":
                            current_mission.questions.append(arg)
                        
                        elif key == "totalt antal" or key == "antal":
                            if int(arg) > current_mission.boys + current_mission.girls:
                                current_mission.count = int(arg)

                        # instrument, gyckel
                        elif key == "instrument":
                            current_mission.instrument = int(arg)
                            if int(arg) > current_mission.count:
                                current_mission.count = int(arg)

                        # Kon
                        elif key == "killar" or key == "pojkar":
                            current_mission.boys = int(arg)
                            if current_mission.boys + current_mission.girls > current_mission.count:
                                current_mission.count = current_mission.boys + current_mission.girls

                        elif key == "flickor" or key == "tjejer":
                            current_mission.girls = int(arg)
                            if current_mission.boys + current_mission.girls > current_mission.count:
                                current_mission.count = current_mission.boys + current_mission.girls

                        # Program
                        elif key == "m":
                            current_mission.m = int(arg)
                            if current_mission.m + current_mission.dpu + current_mission.emm > current_mission.count:
                                current_mission.count = current_mission.m + current_mission.dpu + current_mission.emm

                        elif key == "emm":
                            current_mission.emm = int(arg)
                            if current_mission.m + current_mission.dpu + current_mission.emm > current_mission.count:
                                current_mission.count = current_mission.m + current_mission.dpu + current_mission.emm

                        elif key == "dpu":
                            current_mission.dpu = int(arg)
                            if current_mission.m + current_mission.dpu + current_mission.emm > current_mission.count:
                                current_mission.count = current_mission.m + current_mission.dpu + current_mission.emm

                        # Klasser
                        elif key in klasser:
                            if key == "m_a":
                                current_mission.m_a = int(arg)
                            
                            elif key == "m_b":
                                current_mission.m_b = int(arg)

                            elif key == "m_c":
                                current_mission.m_c = int(arg)

                            elif key == "m_d":
                                current_mission.m_d = int(arg)

                            elif key == "emm_a":
                                current_mission.emm_a = int(arg)

                            elif key == "emm_b":
                                current_mission.emm_b = int(arg)

                            elif key == "dpu_a":
                                current_mission.dpu_a = int(arg)

                            elif key == "dpu_b":
                                current_mission.dpu_b = int(arg)

                            tot_klasser = tot_klasser + int(arg)
                            if tot_klasser > current_mission.count:
                                current_mission.count = tot_klasser

                        # Enkatsvar
                        elif key == "fragor" or key == "frågor" or key == "1-5":
                            tmp = arg.replace(', ', ',')
                            if tmp[-1] == ',':
                                tmp = tmp[:-1]

                            tmp = tmp.split(',')
                            current_mission.one2five = tmp

                        elif key == "egenskaper":
                            if tmp[-1] == ',':
                                tmp = tmp[:-1]

                            tmp = arg.replace(', ', ',')
                            tmp = tmp.split(',')
                            current_mission.attr = tmp

                        elif key == "deal-breaker":
                            current_mission.dealbreaker = arg.split()

                        else:
                            print "ERROR: Unknown keyword " + key
        except:
            print "ERROR: Failed to parse " + line

        # Add last one to list
        if current_mission is not None:
            add_missions(current_mission, missions)
        f.close()

    return missions

def add_missions(new, missions):
    if new.is_valid():

        if new.m > 0:
            new.program = 'M'
        elif new.dpu > 0:
            new.program = 'DPU'
        elif new.emm > 0:
            new.program = 'EMM'

        # Instrument
        if new.instrument > 0:
            tmp = copy.deepcopy(new)
            tmp.count = tmp.instrument
            tmp.dealbreaker.append("instrument")
            tmp.id = id(tmp)
            missions.append(tmp)
            new.count -= new.instrument

        # Gender 
        if new.boys > 0:
            tmp = copy.deepcopy(new)
            tmp.count = tmp.boys
            tmp.sex = 'M'
            tmp.id = id(tmp)
            missions.append(tmp)
            new.count -= new.boys

        if new.girls > 0:
            tmp = copy.deepcopy(new)
            tmp.count = tmp.boys
            tmp.sex = 'F'
            tmp.id = id(tmp)
            missions.append(tmp)
            new.count -= new.girls

        # Class
        if new.m_a > 0:
            tmp = copy.deepcopy(new)
            tmp.count = tmp.m_a
            tmp.school_class = 'M_A'
            tmp.id = id(tmp)
            missions.append(tmp)
            new.count -= new.m_a

        if new.m_b > 0:
            tmp = copy.deepcopy(new)
            tmp.count = tmp.m_b
            tmp.school_class = 'M_B'
            tmp.id = id(tmp)
            missions.append(tmp)
            new.count -= new.m_b

        if new.m_c > 0:
            tmp = copy.deepcopy(new)
            tmp.count = tmp.m_c
            tmp.school_class = 'M_C'
            tmp.id = id(tmp)
            missions.append(tmp)
            new.count -= new.m_c

        if new.m_d > 0:
            tmp = copy.deepcopy(new)
            tmp.count = tmp.m_d
            tmp.school_class = 'M_D'
            tmp.id = id(tmp)
            missions.append(tmp)
            new.count -= new.m_d

        if new.emm_a > 0:
            tmp = copy.deepcopy(new)
            tmp.count = tmp.emm_a
            tmp.school_class = 'EMM_A'
            tmp.id = id(tmp)
            missions.append(tmp)
            new.count -= new.emm_a

        if new.emm_b > 0:
            tmp = copy.deepcopy(new)
            tmp.count = tmp.emm_b
            tmp.school_class = 'EMM_B'
            tmp.id = id(tmp)
            missions.append(tmp)
            new.count -= new.emm_b

        if new.dpu_a > 0:
            tmp = copy.deepcopy(new)
            tmp.count = tmp.dpu_a
            tmp.school_class = 'DPU_A'
            tmp.id = id(tmp)
            missions.append(tmp)
            new.count -= new.dpu_a

        if new.dpu_b > 0:
            tmp = copy.deepcopy(new)
            tmp.count = tmp.dpu_b
            tmp.school_class = 'DPU_B'
            tmp.id = id(tmp)
            missions.append(tmp)
            new.count -= new.dpu_b

        if new.count > 0:
            missions.append(new)

    else:
        print "ERROR: Failed to add incomplete mission " + new.name

def read_questions(path):
    if not os.path.exists(path):
        print "ERROR: Could not find " + path
        sys.exit(0)

    questions = []

    with open(path) as f:
        for line in f:
            if line != "\n" and line[0] != '#':
                line = line.translate(None, '\n')
                
                questions.append(line)
        f.close()
    return questions

def set_classes(path, nollan):
    # Sould be run AFTER setting program. 
    # Program is used as sanity check as there can be people with the same name.
    # Undefined if there are people in the same program with the same name.

    if not os.path.exists(path):
        print "ERROR: Could not find " + path
        sys.exit(0)

    classes = {}
    current_class = None
    only_in_klasslista = []
    only_in_nollan = []


    with open(path) as f:
        for line in f:
            if line != "\n" and line[0] != '#':
                line = line.translate(None, '\n')

                if line[0] == '%':
                    line = line.translate(None, ' ')
                    current_class = line[1:]
                    classes[current_class] = []

                elif current_class is not None:
                    tmp = line.split()
                    tmp = tmp[1] + ' ' + tmp[0]
                    classes[current_class].append(tmp)
                else:
                    print "WARNING: Trying to read nollan from " + path + " before setting class!"
        f.close()

    for n in nollan:
        # Some nollan are confused about what their first/last names are...
        found = False
        for c in classes:
            for name in classes[c]:
                tmp_name = name.split()[1] + ' ' + name.split()[0]
                if name.upper().decode('utf-8') == n.name.upper() or tmp_name.upper().decode('utf-8') == n.name.upper():
                    n.school_class = c
                    found = True
                    break
            if found:
                break
        if not found:
            only_in_nollan.append(n)



    if len(only_in_nollan) > 0:
        print "WARNING: " + str(len(only_in_nollan)) + " of " + str(len(nollan)) + " nollan not found in " + path
        for n in only_in_nollan:
            print unicode(n.name)

def read_nollan(path):
    global columns_one2five
    global columns_attributes
    global columns_dealbreakers
    global columns_about_nollan

    ans_to_int = [
    u"zero-not-used!",
    u"va?!?",
    u"sissodär...",
    u"lagom..!",
    u"helt ok!",
    u"braaa!",
    ]

    if not os.path.exists(path):
        print "ERROR: Could not find " + path
        sys.exit(0)

    print "Reading Nollan from", data_filename

    nollan = []
    incorrect_entries = []
    ids = []
    names = []

    workbook = openpyxl.load_workbook(filename = path, use_iterators = True)
    worksheet = workbook.get_sheet_by_name(workbook.get_sheet_names()[0])

    first_row = True

    for row in worksheet.iter_rows():
        # Sanity check, same number of columns in document and lists
        if first_row:
            first_row = False
            total_columns = len(columns_one2five) + len(columns_about_nollan) + \
                len(columns_attributes) + len(columns_extra)
            actual_columns = 0
            while True:
                cont = row[actual_columns].value
                if cont is None:
                    break
                actual_columns += 1
            if actual_columns != total_columns:
                print "WARNING: Document contains " + str(actual_columns) + " columns, expected " + str(total_columns) +'!'
            print "Total number of columns: " + str(actual_columns)
        else:
            try:
                one2five_attributes = []
                for item in range(len(columns_one2five)):
                    one2five_attributes.append( ans_to_int.index(row[item + len(columns_about_nollan)].value))

                attributes = []
                tmp = row[columns_attributes.index(u"8. Vilka egenskapsord passa in på Ø:an?") \
                    + len(columns_about_nollan) + len(columns_one2five)].value
                if tmp is not None:
                    attributes += tmp.split(', ')
                
                tmp = row[columns_attributes.index(u"9. Vad har Ø:an i Linköping?") \
                     + len(columns_about_nollan) + len(columns_one2five)].value
                if tmp is not None:
                    attributes += tmp.split(', ')
                
                tmp = row[columns_attributes.index(u"10. Har Ø:an erfarenhet av något av följande yrken?") \
                    + len(columns_about_nollan) + len(columns_one2five)].value
                if tmp is not None:
                    attributes += tmp.split(', ')

                tmp = row[columns_attributes.index(u"11. Vilka sporter utövar Ø:an?") \
                    + len(columns_about_nollan) + len(columns_one2five)].value
                if tmp is not None:
                    attributes += tmp.split(', ')


                kon_val = row[columns_about_nollan.index(u"Kön")].value
                if kon_val == "Man":
                    kon = 'M'
                elif kon_val == "Kvinna":
                    kon = 'F'
                else:
                    kon = '-'

                new_nollan = Nollan(row[columns_about_nollan.index(u"Förnamn")].value,
                    row[columns_about_nollan.index(u"Efternamn")].value,
                    # row[columns_about_nollan.index(u"Kön")].value,
                    # "-",
                    kon,
                    row[columns_about_nollan.index(u"Personnummer")].value,
                    row[columns_about_nollan.index(u"Program")].value,
                    one2five_attributes, attributes)

                # instrument
                val1 = row[columns_attributes.index(u"2. Spelar Ø:an gitarr, maracas, banjo, orgel eller något annat instrument kanske?") \
                    + len(columns_about_nollan)  + len(columns_one2five)].value
                val2 = row[columns_attributes.index(u"4. Kommer Ø:an ta med det till Linköping?") \
                    + len(columns_about_nollan)  + len(columns_one2five)].value
                if val1 == u"Ja!" and val2 == u"Ja!":
                    new_nollan.attr.append(u"instrument")

                # studied before
                val = row[columns_extra.index(u"14. Har ∅:an studerat på universitet/högskola tidigare?") + len(columns_attributes) \
                    + len(columns_about_nollan)  + len(columns_one2five)].value
                if val == u"Ja!":
                    new_nollan.attr.append(u"pluggat tidigare")

                # can perform on stage
                val = row[columns_attributes.index(u"12. Kan Ø:an tänka sig att uppträda inför publik?") \
                    + len(columns_about_nollan)  + len(columns_one2five)].value
                if val == u"Ja!":
                    new_nollan.attr.append(u"Uppträda")

                # Has to be run AFTER "studied before"
                # For any mission at vikinga, make sure nollan is suitable
                if is_viking(new_nollan):
                    new_nollan.attr.append(u"Viking")

                if not new_nollan.id_nr in ids:
                    nollan.append(new_nollan)
                    ids.append(new_nollan.id_nr)

            except:
                incorrect_entries.append(row[0].row)
                print "WARNING: Failed to read line " + unicode(row[0].row) + " in " + path

    return nollan

def is_viking(nollan):
    # Nollan participating at vikinga should be more "experienced"
    # Nollan is suitable if nollan either has studied before or is old enough
    age = 21

    try:
        # Studied before
        if "pluggat tidigare" in nollan.attr:
            return True

        # Age
        t = datetime.date.today().strftime("%Y%m%d")
        latest_born = int(str(datetime.date.today() - datetime.timedelta(days=age*365)).translate(None, '-'))

        if int(str(nollan.id_nr)[:2]) > int(t[2:4]):
            born = int(str('19' + nollan.id_nr)[:8])
        else:
            born = int(str('20' + nollan.id_nr)[:8])

        if born < latest_born:
            return True

    except:
        print "ERROR: could not determine if nollan is a true Viking :( "
        return False
    return False

def write_nollan(nollan, missions, path):
    print "Writing nollans attributes to ", path

    nollan.sort(key=lambda x: x.name)

    mission_map = {}
    for m in missions:
        mission_map[m.id] = unicode(m.name, "utf-8")

    f = open(path,'w')

    for item in nollan:
        printed = []
        try:
            s = item.name + ', ' + item.sex + ', ' + item.program 
            if item.assigned is not None:
                s += ' (' + unicode(item.assigned.name, "utf-8") + ')\n'
            f.write(s.encode('utf8'))
            f.write(item.question_post + '\n')
            f.write(item.question_random + '\n')

            for a in item.match:
                if item.match_relative[a] != 0 and mission_map[a] not in printed:
                    s = mission_map[a] + ": " + unicode(item.match_relative[a]) + u'%\n'
                    f.write(s.encode('utf8'))
                    
                    printed.append(mission_map[a])
            f.write('\n')
        except:
            print "ERROR: Failed to write " + unicode(item)[:-1]
            
    f.close() 

def write_sorting(sorting, path):
    print "Writing sorting to", path
    f = open(path,'w')
    prev_item = None

    sorting.sort(key=lambda x: x.name)

    for item in sorting:
        try:
            if prev_item != item.name:
                f.write('\n' + item.name.upper() + '\n')
                
            item.assigned.sort(key=lambda x: x.name)
            for a in item.assigned:
                s = a.name + ": " + str(a.school_class) + '\n'
                f.write(s.encode('utf8'))
            
            prev_item = item.name
        except:
            print "ERROR: failed to write " + item.name + " to " + path
            
    f.close() 

def write_class_sorting(nollan, path):
    print "Writing sorting to", path

    # Sort nollan by class and by name
    nollan.sort(key=lambda x: x.name)
    nollan.sort(key=lambda x: x.school_class)

    f = open(path,'w')
    prev_class = None
    for item in nollan:
        try:
            if prev_class != item.school_class:
                f.write('\n' + item.school_class.upper() + '\n')
            s = item.name + " (" + unicode(item.assigned.name, "utf-8") + ') ' + unicode(item.question_post, "utf-8") \
                + ', ' + unicode(item.question_random, "utf-8") + '\n'
            f.write(s.encode('utf8'))
            
            prev_class = item.school_class
        except:
            print "ERROR: failed to write " + item.name + " to " + path
            
    f.close() 

def match(nollan, mission):
    global columns_one2five

    # set 0 for wrong sex/class/program
    if mission.sex != "-":
        if mission.sex != nollan.sex:
            return 0

    if mission.program != "-":
        if mission.program != nollan.program:
            return 0

    if mission.school_class != "-":
        if mission.school_class.upper() != nollan.school_class.upper():
            return 0


    # match 1-5 questions
    res_1 = 0
    for f in mission.one2five:
        try:
            tmp = u"1. Hur bra är Ø:an egentligen på att... [..." + unicode(f, "utf-8").lower() + u']'
            res_1 += nollan.one2five[columns_one2five.index(tmp)]
        except:
            print "ERROR: Could not find question " + tmp

    # match attribute
    res_2 = 0
    for a in mission.attr:
        if unicode(a, "utf-8") in nollan.attr:
            res_2 += 1

    # dealbreakers
    res_3 = 1
    for d in mission.dealbreaker:
        if not unicode(d, "utf-8") in nollan.attr:
            res_3 = 0

    # Math for determining how suitable a nollan is
    return (res_1 + 5*res_2) * res_3

def normalize(nollan, mission):
    for m in mission:
        tot = 0
        maximum = 0
        for n in nollan:
            tot += n.match[m.id]
            maximum = max(n.match[m.id], maximum)

        for n in nollan:
            if maximum == 0:
                print "ERROR: Maximum match is 0 for " + m.name
                n.set_match_relative(m.id, 0)
            else:   
                n.set_match_relative(m.id, n.match[m.id]*100/maximum)

def most_urgent(mission):
    # Priority groups
    # 1 = high, 2 = low, 3 = optional, 9 = unset
    top_prio = 9
    high_prio_missions = []

    for m in mission:
        if m.count > len(m.assigned):
            if m.priority < top_prio:
                top_prio = m.priority
                high_prio_missions = []
            
            if m.priority <= top_prio:
                high_prio_missions.append(m)

    most_empty = None
    emptyness = float(2)

    for hpm in high_prio_missions:
        tmp_empty = float(1 + len(hpm.assigned))/float(hpm.count)
        if tmp_empty < emptyness:
            emptyness = tmp_empty
            most_empty = hpm

    return most_empty

def best_nollan(nollan, mission):
    bn = None
    maximum = 0

    for n in nollan:
        if nollan[n].match_relative[mission.id] > maximum:
            maximum = nollan[n].match_relative[mission.id]
            bn = nollan[n]
    if bn is None:
        print "ERROR: No matching nollan found for " + mission.name
    return bn

def select(nollan, mission):
    unassigned = {}
    total_empty = 0

    for n in nollan:
        unassigned[n.id_nr] = n

    while len(unassigned) != 0:
        mamma_mu = most_urgent(mission)
        if mamma_mu is None:
            print "WARNIGN: No posts left to fill! " + str(len(unassigned)) + " Nollan with no misson assigned."
            break
        bn = best_nollan(unassigned, mamma_mu)
        if bn is not None:
            mamma_mu.assigned.append(bn)
            bn.assigned = mamma_mu
            del unassigned[bn.id_nr]
        else:
            print "ERROR: No suitable nollan found for mission!"
            break

        # Count the number of empty spots
        total_empty = []
        for m in mission:
            while m.priority >= len(total_empty):
                total_empty.append(0)

            total_empty[m.priority] += m.count - len(m.assigned)
    if total_empty > 0:
        s = "WARNING: Total " + str(sum(total_empty))  + " unfilled positions. ("
        for i in range(len(total_empty)):
            if total_empty[i] != 0:
                s += " prio " + str(i) + ': ' + str(total_empty[i]) + '. '
        s += ')'
        print s

def set_questions(nollan):
    random_questions = read_questions(questions_filename)
    for n in nollan:
        if n.assigned is not None:
            try:
                if n.assigned == None:
                    print "WARNING: Could not set questions. No mission assigned to " + unicode(n.print_all())
                else:
                    l = n.assigned.questions
                    n.question_post = l[randint(0,len(l)-1)]
                    n.question_random = random_questions[randint(0,len(random_questions)-1)]
            except:
                print "ERROR: Failed to set questions for " + unicode(n)[:-1]
            
if __name__ == "__main__":
    missions = read_missions(mission_filename)

    nollan = read_nollan(data_filename)

    set_classes(classes_filename, nollan)

    for n in nollan:
        for m in missions:
            n.set_match(m.id, match(n,m))

    normalize(nollan, missions)

    select(nollan, missions)

    set_questions(nollan)

    write_sorting(missions, sorting_filename)

    write_nollan(nollan, missions, nollan_filename)

    write_class_sorting(nollan, class_sorting_filename)

    print "\n I am the Lord, thy God:\n \
        1: Thou shalt remember DVBF. \n \
        2: Thou shalt honor thy elders.\n \
        3: Thou shalt understand and be in awe of the meaning of Inri.\n \
        4: Thou shalt turn water into wine (and give to your elders)\n \
        5: Thou shalt worship no false Idols (beside Barbara). \n \
        6: Thou shalt show thankfullness [sv: Tackfestfullhet, red. anm.]\n \
        7: Thou shalt look at my horse, my horse is amazing. \n \
        8: Thou shalt not covet thy neighbors ass (the animal, stupid!)\n \
        9: Thou shalt covet thy neighbor (the one on the left).\n \
        10: Thou shalt show respect when thou calleth tech support.\n \
        "


