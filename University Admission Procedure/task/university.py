def calculate_score(depart, physres, chemres, mathres, compres, admisres):
    if depart == 'Biotech':
        return max((float(physres) + float(chemres)) / 2, float(admisres))
    elif depart == 'Chemistry':
        return max(float(chemres), float(admisres))
    elif depart == 'Engineering':
        return max((float(compres) + float(mathres)) / 2, float(admisres))
    elif depart == 'Mathematics':
        return max(float(mathres), float(admisres))
    else:
        return max((float(physres) + float(mathres)) / 2, float(admisres))


def create_applicant(firstname, lastname, physres, chemres, mathres, compres, admisres, fpdepart, spdepart, tpdepart):
    applicants.append(dict())
    applicants[-1]['first name'] = firstname
    applicants[-1]['last name'] = lastname
    applicants[-1]['phys'] = float(physres)
    applicants[-1]['chem'] = float(chemres)
    applicants[-1]['math'] = float(mathres)
    applicants[-1]['comp'] = float(compres)
    applicants[-1]['admis'] = float(admisres)
    applicants[-1]['score_fp'] = calculate_score(fpdepart, physres, chemres, mathres, compres, admisres)
    applicants[-1]['score_sp'] = calculate_score(spdepart, physres, chemres, mathres, compres, admisres)
    applicants[-1]['score_tp'] = calculate_score(tpdepart, physres, chemres, mathres, compres, admisres)
    applicants[-1]['First-priority Department'] = fpdepart
    applicants[-1]['Second-priority Department'] = spdepart
    applicants[-1]['Third-priority Department'] = tpdepart


def determine_sort(keyword):
    if keyword == 'First-priority Department':
        return 'score_fp'
    elif keyword == 'Second-priority Department':
        return 'score_sp'
    elif keyword == 'Third-priority Department':
        return 'score_tp'


def adding_to_list(prior_department, maxpeople):
    for key1 in disciplines:
        # print(key1)
        sorting_alg = determine_sort(prior_department)
        # print(sorting_alg)
        applicants.sort(key=lambda x: (x[prior_department], -x[sorting_alg], x['first name'], x['last name']))
        j = 0
        # print(applicants[:12])
        while len(disciplines[key1]) < maxpeople and len(applicants) != 0:
            if applicants[j][prior_department] == key1:
                good_applicant = applicants.pop(j)
                good_applicant = good_applicant['first name'], good_applicant['last name'], good_applicant[sorting_alg]
                disciplines[key1].append(good_applicant)
            elif j < len(applicants) - 1:
                j += 1
            if j == len(applicants) - 1:
                if applicants[j][prior_department] == key1:
                    good_applicant = applicants.pop(j)
                    good_applicant = good_applicant['first name'], good_applicant['last name'], good_applicant[sorting_alg]
                    disciplines[key1].append(good_applicant)
                break


def printing_into_file(faculty, students):
    students.sort(key=lambda x: (-x[2], x[0], x[1]))
    faculty = faculty.lower()
    current_file = open(f'{faculty}.txt', 'w')
    for stud in students:
        current_file.write(stud[0].rstrip() + ' ' + stud[1].rstrip() + ' ' + str(stud[2]).rstrip() + '\n')
    current_file.close()


applicant_file = open('applicants.txt', 'r')
applicants = []
disciplines = dict()
disciplines['Biotech'] = []
disciplines['Chemistry'] = []
disciplines['Engineering'] = []
disciplines['Mathematics'] = []
disciplines['Physics'] = []
for line in applicant_file:
    first_name, last_name, phys_res, chem_res, math_res, comp_res, admis_res, fp_depart, sp_depart, tp_depart = line.split()
    create_applicant(first_name, last_name, phys_res, chem_res, math_res, comp_res, admis_res, fp_depart, sp_depart, tp_depart)
applicant_file.close()

max_applicants = int(input())

adding_to_list('First-priority Department', max_applicants)
adding_to_list('Second-priority Department', max_applicants)
adding_to_list('Third-priority Department', max_applicants)

for key in disciplines:
    printing_into_file(key, disciplines[key])
