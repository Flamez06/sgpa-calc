import pdfplumber
import re
path = r"backend\test_pdf\ugcurriculum08.pdf"

def is_semester_header(row):
    text = " ".join([
        str(i)
        for i in row
        if i
    ])
    year_sem_match = re.search(r"(\d+)(st|nd|rd|th)?\s*Year\s*(\d+)(st|nd|rd|th)?\s*Semester",text,re.I)
    direct_sem_match = re.search(r"Semester\s*(\d+)",text,re.I)
    
    if year_sem_match:
        year = int(year_sem_match.group(1))
        sem = int(year_sem_match.group(3))
        global_sem = (year - 1) * 2 + sem
        return global_sem
    elif direct_sem_match:
        global_sem = int(direct_sem_match.group(1))
        return global_sem
    return False

def is_subject_row(row):
    if len(row) < 6:
        return False
    title = str(row[1]).strip()
    if len(title) < 3 or title=="None":
        return False
    numeric_count = 0
    for i in row[2:]:
        try:
            float(i)
            numeric_count += 1
        except:
            pass
    return numeric_count >= 3

with pdfplumber.open(path) as pdf:
    for page in pdf.pages:
        tableinfo=page.extract_table(table_settings={"vertical_strategy": "lines",
    "horizontal_strategy": "lines",
    "snap_tolerance": 3,})
        try:
            for i in tableinfo:
                check = is_semester_header(i)
                if (check!=False):
                    print("Semester :", check)
                if (is_subject_row(i)):
                    print(i)
        except:pass

   

  