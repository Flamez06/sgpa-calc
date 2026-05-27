import pdfplumber
import json
import re

path = r"backend/test_pdf/ugcurriculum08.pdf"

#Extract sem number from header rows. Handle both "3rd year 1st semester" and "Semester 5" formats.
def is_semester_header(row):
    text = " ".join(i for i in row if i).lower()
    year_sem_match = re.search(
        r"(\d+)(st|nd|rd|th)?\s*year\s*(\d+)(st|nd|rd|th)?\s*semester",
        text,
        re.I
    )
    direct_sem_match = re.search(
        r"semester\s*(\d+)",
        text,
        re.I
    )
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
    
    if row[1] is None:
        return False
    
    title = str(row[1]).strip()
    
    if len(title) < 3:
        return False
    numeric_count = 0
    for i in row:
        try:
            float(i)
            numeric_count += 1
        except:pass

    return numeric_count >= 3

def is_header_row(row):
    text = " ".join(i for i in row if i).lower()
    keywords = ["course","subject","title","credit"]
    for word in keywords:
        if word in text:
            return True

def build_column_map(row):
    column_map = {}
    for index, cell in enumerate(row):
        if not cell:
            continue

        text = str(cell).strip().lower()

        if "number" in text or "code" in text:
            column_map["code"] = index
            
        elif "course" in text or "subject" in text:
            column_map["title"] = index

        elif text == "c" or "credit" in text:
            column_map["credits"] = index        
    return column_map


subjects = []
current_semester = None
column_map = {}


with pdfplumber.open(path) as pdf:
    for page in pdf.pages:
        tables = page.extract_tables(
            table_settings={
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines",
                "snap_tolerance": 3,
            }
        )

        if not tables:
            continue

        for table in tables:
            if not table:
                continue
            for row in table:
                if not row:
                    continue
                
                semester = is_semester_header(row)

                if semester:
                    current_semester = semester
                    print("Semester:", semester)
                    continue
                    
                #Create a map to identify the column indices for code, title and credits.
                if is_header_row(row):
                    new_column_map = build_column_map(row)
                    if(len(new_column_map) > len(column_map)):
                        column_map = new_column_map
                        print("Column Map:", column_map)
                    continue

                if is_subject_row(row):
                    title_index = column_map.get("title")
                    credit_index = column_map.get("credits")
                    code_index = column_map.get("code")

                    subject = {
                        "semester": current_semester,
                        "code": row[code_index] if code_index is not None else None,
                        "title": row[title_index] if title_index is not None else None,
                        "credits": row[credit_index] if credit_index is not None else None
                    }
                    subjects.append(subject)

with open("data.json", "w+") as file:
    json.dump(subjects, file, indent=2)