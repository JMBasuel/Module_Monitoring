import json
import os
import pandas as pd
from datetime import datetime

inventory_filepath = 'data/inventory_data.json'
student_filepath = 'data/student_data.json'
inventory_backup_filepath = 'backup/inventory_data_backup.json'
student_backup_filepath = 'backup/student_data_backup.json'
inventory_data = {}
student_data = {}
inventory_data_backup = {}
student_data_backup = {}
zfill = 0
date = ''

def ensure_directory(filepath):
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)

ensure_directory(inventory_filepath)
ensure_directory(student_filepath)
ensure_directory(inventory_backup_filepath)
ensure_directory(student_backup_filepath)

def set_zfill():
    global zfill
    data_size = 0
    for _, ids in student_data.items():
        data_size += len(ids)
    zfill = len(str(data_size))


# GET ALL MODULE DATA                                                                   ADMIN
def get_inventory_data():
    data = []
    for pen, value in inventory_data.items():
        for title, quantity in value.items():
            data.append((pen, title, quantity))
    return data


# ADD NEW MODULE DATA                                                                   ADMIN
def add_inventory(pen, title, quantity):
    if pen not in inventory_data:
        inventory_data[pen] = {title: quantity}
    else:
        return True


# MODIFY MODULE (PEN CODE OR SUBJECT TITLE) AND QUANTITY                                ADMIN
def modify_inventory(pen, title, quantity):
    global inventory_data
    if pen in inventory_data:
        inventory_data[pen] = {title: quantity}
    else:
        for _pen, _title in inventory_data.items():
            if title == _title:
                del inventory_data[_pen]
                inventory_data[pen] = {title: quantity}
            else:
                return True


# INCREMENT QUANTITY TO MODULE                                                          ADMIN
def add_inventory_data(pen, quantity):
    if pen in inventory_data:
        inventory_data[pen][next(iter(inventory_data[pen]))] += quantity
    else:
        return True


# REMOVE MODULE FROM INVENTORY                                                          ADMIN
def delete_inventory(pen):
    global inventory_data_backup
    for key, value in inventory_data.items():
        if key == pen:
            inventory_data_backup[pen] = value
    del inventory_data[pen]


# DELETE ALL INVENTORY DATA
def clear_inventory():
    for pen, value in inventory_data.items():
        inventory_data_backup[pen] = value
    inventory_data.clear()


# RESTORE DELETED DATA FROM INVENTORY                                                   ADMIN
def restore_inventory_data():
    global inventory_data
    for key, value in inventory_data_backup.items():
        if key not in inventory_data:
            inventory_data[key] = value
    inventory_data_backup.clear()


# GET STUDENT DATA                                                                      ADMIN
def get_student_data():
    data = []
    ctr = 0
    for course, student_id in student_data.items():
        for _id, names in student_id.items():
            ctr += 1
            claims = []
            dates = []
            name = ''
            for name, subjects in names.items():
                for subject, status in subjects.items():
                    for _date, claimed in status.items():
                        claim = f"{subject} - {'Claimed' if claimed else 'Unclaimed'}"
                        claims.append(claim)
                        dates.append(_date)
            data.append((str(ctr).zfill(zfill), course, _id, name, tuple(claims), tuple(dates)))
    return data


# ADD DATE LOGGING TO DATA
def add_date(values):
    data = {}
    for subject, claimed in values.items():
        data[subject] = {date: claimed}
    return data


# ADD NEW STUDENT DATA                                                                  DISTRIBUTION
def add_student(course, _id, name, values):
    if course not in student_data:
        student_data[course] = {_id: {name: add_date(values)}}
    elif _id not in student_data[course]:
        student_data[course][_id] = {name: add_date(values)}
    else:
        modify_status(course, _id, name, values)
    set_zfill()


# MODIFY THE MODULE DISTRIBUTION STATUS                                                 DISTRIBUTION
def modify_status(course, _id, name, values):
    global student_data
    for _name, subjects in student_data[course][_id].copy().items():
        for _subject, _claimed in values.items():
            for subject in list(subjects):
                if _subject == subject:
                    student_data[course][_id][name][subject] = {date: _claimed}
                else:
                    student_data[course][_id][name][_subject] = {date: _claimed}


# DELETE DISTRIBUTION DATA                                                              ADMIN
def delete_distribution(keyword):
    global student_data_backup
    for course, student_ids in student_data.items():
        for _id, names in student_ids.items():
            if keyword == course:
                student_data_backup[course] = student_ids
                del student_data[course]
                return
            elif keyword == _id:
                student_data_backup[course] = {_id: names}
                del student_data[course][_id]
                return


# DELETE ALL DISTRIBUTION DATA                                                          ADMIN
def clear_distribution():
    for key, value in student_data.items():
        student_data_backup[key] = value
    student_data.clear()


# RESTORE DELETED MODULE DISTRIBUTION DATA                                              ADMIN
def restore_distribution_data():
    global student_data
    for course, student_ids in student_data_backup.items():
        for _id, names in student_ids.items():
            if student_data:
                for _course, _student_ids in student_data.items():
                    if _id not in _student_ids:
                        student_data[course][_id] = names
            else:
                student_data[course] = {_id: names}
    student_data_backup.clear()


# CHECKER IF ITEM IS IN DICTIONARY
def inDict(dictionary, target):
    for val in dictionary.values():
        if target in dictionary:
            return True
        elif isinstance(val, dict):
            if inDict(val, target):
                return True
    return False


# MODIFY STUDENT ID OR NAME                                                             ADMIN
def modify_student_data(course, _id, name):
    for _course, student_ids in student_data.items():
        for __id, names in student_ids.items():
            for _name, subjects in names.items():
                if __id == _id:
                    student_data[course][_id] = {name: subjects}
                    return
                elif name == _name:
                    del student_data[course][__id]
                    student_data[course][_id] = {_name: subjects}
                    return
    return True


# GET STUDENT ID OR NAME                                                                DISTRIBUTION
def get_student_name_id(keyword):
    data = {}
    for course, student_ids in student_data.items():
        for _id, names in student_ids.items():
            if keyword == _id:
                data[course] = {keyword: names}
                return data
            else:
                for name, subjects in names.items():
                    if keyword == name:
                        data[course] = {_id: {keyword: subjects}}
                        return data


# FILTER STUDENT DATA                                                                   ADMIN
def filter_student_data(keyword):
    data = []
    ctr = 0
    claims = []
    dates = []
    # COURSE
    if keyword in student_data:
        for _id, names in student_data[keyword].items():
            ctr += 1
            for name, subjects in names.items():
                claims.clear()
                dates.clear()
                for subject, status in subjects.items():
                    for _date, claimed in status.items():
                        claim = f"{subject} - {'Claimed' if claimed else 'Unclaimed'}"
                        claims.append(claim)
                        dates.append(_date)
                data.append((ctr, keyword, _id, name, tuple(claims), tuple(dates)))
        return data
    # STUDENT ID
    else:
        for course, student_ids in student_data.items():
            if keyword in student_ids:
                ctr += 1
                for name, subjects in student_ids[keyword].items():
                    for subject, status in subjects.items():
                        for _date, claimed in status.items():
                            claim = f"{subject} - {'Claimed' if claimed else 'Unclaimed'}"
                            claims.append(claim)
                            dates.append(_date)
                    data.append((ctr, course, keyword, name, tuple(claims), tuple(dates)))
                return data
            # NAME
            else:
                for _id, names in student_ids.items():
                    if keyword in names:
                        ctr += 1
                        for subject, status in names[keyword].items():
                            for _date, claimed in status.items():
                                claim = f"{subject} - {'Claimed' if claimed else 'Unclaimed'}"
                                claims.append(claim)
                                dates.append(_date)
                        data.append((ctr, course, _id, keyword, tuple(claims), tuple(dates)))
                        return data
                    # PEN CODE
                    else:
                        for name, subjects in names.items():
                            if keyword in subjects:
                                ctr += 1
                                for _date, claimed in subjects[keyword].items():
                                    claim = f"{keyword} - {'Claimed' if claimed else 'Unclaimed'}"
                                    data.append((ctr, course, _id, name, claim, _date))
                            # DATE
                            else:
                                for subject, status in subjects.items():
                                    claims.clear()
                                    dates.clear()
                                    ctr += 1
                                    if keyword in status:
                                        for _date, claimed in status.items():
                                            claim = f"{subject} - {'Claimed' if claimed else 'Unclaimed'}"
                                            claims.append(claim)
                                            dates.append(keyword)
                                    data.append((ctr, course, _id, name, tuple(claims), tuple(dates)))
                return data


# GET MODULE PEN CODES                                                                  DISTRIBUTION
def get_pen():
    return list(inventory_data.keys())


# DECREMENT MODULE QUANTITY                                                             DISTRIBUTION
def subtract_inventory_data(pen):
    if inventory_data[pen][next(iter(inventory_data[pen]))] - 1 > -1:
        inventory_data[pen][next(iter(inventory_data[pen]))] -= 1
    else:
        return True


# WRITE DATA TO FILE                                                                    DATA STORAGE
def write_data():
    with open(inventory_filepath, 'w') as json_fil:
        json.dump(inventory_data, json_fil, indent=2)
    with open(student_filepath, 'w') as json_fil:
        json.dump(student_data, json_fil, indent=2)


def write_data_backup():
    with open(inventory_backup_filepath, 'w') as json_fil:
        json.dump(inventory_data_backup, json_fil, indent=2)
    with open(student_backup_filepath, 'w') as json_fil:
        json.dump(student_data_backup, json_fil, indent=2)


# READ DATA FROM FILE                                                                   DATA STORAGE
def read_data():
    global inventory_data
    global student_data
    global date
    date = str(datetime.now().date())
    if not (os.path.exists(inventory_filepath) and os.path.exists(student_filepath)):
        with open(inventory_filepath, 'w') as json_fil:
            json.dump(inventory_data, json_fil, indent=2)
        with open(student_filepath, 'w') as json_fil:
            json.dump(student_data, json_fil, indent=2)

    else:
        with open(inventory_filepath, 'r') as json_file:
            inventory_data = json.load(json_file)
        with open(student_filepath, 'r') as json_file:
            student_data = json.load(json_file)
        set_zfill()


def read_data_backup():
    global inventory_data_backup
    global student_data_backup
    if not (os.path.exists(inventory_backup_filepath) and os.path.exists(student_backup_filepath)):
        with open(inventory_backup_filepath, 'w') as json_fil:
            json.dump(inventory_data_backup, json_fil, indent=2)
        with open(student_backup_filepath, 'w') as json_fil:
            json.dump(student_data_backup, json_fil, indent=2)
    else:
        with open(inventory_backup_filepath, 'r') as json_file:
            inventory_data_backup = json.load(json_file)
        with open(student_backup_filepath, 'r') as json_file:
            student_data_backup = json.load(json_file)


# WRITE DATA TO EXCEL                                                                   DATA STORAGE
def inventory_to_excel(filepath):
    inventory_data_excel = []
    for code, titles in inventory_data.items():
        for title, quantity in titles.items():
            inventory_data_excel.append({"PEN Code": code, "Title": title, "Quantity": quantity})
    df = pd.DataFrame(inventory_data_excel)
    if not df.to_excel(filepath, index=False, engine='openpyxl'):
        return True


def student_to_excel(filepath):
    student_data_excel = []
    for course, students in student_data.items():
        for student_id, names in students.items():
            for name, codes in names.items():
                for code, dates in codes.items():
                    for _date, status in dates.items():
                        student_data_excel.append({
                            "Course": course,
                            "Student ID": student_id,
                            "Name": name,
                            "PEN Code": code,
                            "Status": 'Claimed' if status else 'Unclaimed',
                            "Date": _date
                        })
    df = pd.DataFrame(student_data_excel)
    if not df.to_excel(filepath, index=False, engine='openpyxl'):
        return True
