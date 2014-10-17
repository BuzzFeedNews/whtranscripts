# -*- coding: utf-8 -*-
import sys
import re
import datetime as dt
import lxml.html

#These helper functions are designed to clean up super awkward portions of the text
def fix_27878(text):
    chart = re.compile(r"\[At this point[^7]*\.3")
    clean_text = re.sub(chart, "", text)
    return clean_text

def fix_15805(text):
    proclamation = re.compile(r"\(Reading\)[\n\"A-Z ,a-z.()0-9;:\[\]]*purposes.\"")
    clean_text = re.sub(proclamation, "", text)
    return clean_text

def fix_26405(text):
    armed_forces = re.compile(r"The breakdown by Departments is:[^T]*")
    clean_text = re.sub(armed_forces, "", text)
    return clean_text

def fix_28469(text):
    budget = re.compile(r"Enacted[^?]*\$21\. 6")
    clean_text = re.sub(budget, "", text)
    return clean_text

def fix_15601(text):
    statement = re.compile(r"Wile says:[^\(]+\(Laughter\)")
    clean_text = re.sub(statement, "", text)
    return clean_text

def fix_16238(text):
    roman_statement = re.compile(r"\(Reading\)[^\.]*")
    clean_text = re.sub(roman_statement, "", text)
    return clean_text

def fix_27116(text):
    clean_text = text.replace("WHY WE ARE IN VIET-NAM ", "")
    return clean_text

def fix_26859(text):
    opening_statement = re.compile(r"THE UNEMPLOYMENT RECORD FOR MARCH ")
    pre_question = re.compile(r"[A-Z ]*\[[0-9]\.\] ")
    no_statement = re.sub(opening_statement, "", text)
    clean_text = re.sub(pre_question, "", no_statement)
    return clean_text

def fix_27196(text):
    opening_statement = re.compile(r"THE MESSAGE- ON AGRICULTURE ")
    pre_question = re.compile(r"[A-Z ]*\[[0-9]\.\] ")
    no_statement = re.sub(opening_statement, "", text)
    clean_text = re.sub(pre_question, "", no_statement)
    return clean_text

def fix_4515(text):
    opening_statement = re.compile(r"APPOINTMENTS IN THE ENERGY PROGRAM ")
    pre_question = re.compile(r"[A-Z ]*\[[0-9]\.\] ")
    no_statement = re.sub(opening_statement, "", text)
    clean_text = re.sub(pre_question, "", no_statement)
    return clean_text    

def fix_60166(text):
    weird_questions = re.compile(r"(Q)([A-Z][a-z ])")
    clean_text = re.sub(weird_questions, r"\1: \2", text)
    return clean_text

def fix_8246(text):
    clean_text = text.replace("THE PRESDENT", "THE PRESIDENT")
    return clean_text

def fix_4600(text):
    to_replace = [ "OPENING STATEMENT ", "QUESTIONS " ]
    for r in to_replace:
        text = text.replace(r, "")
    return text    

def fix_27398(text):
    to_replace = [
        "OPENING STATEMENT ",
        "RECENT POWER FAILURES ",
        "QUESTIONS ",
        "DISCUSSION WITH MEMBERS OF THE QUADRIAD [2.] ",
        "THE PRESIDENT'S CLOSING REMARKS AND QUESTIONS "
    ]
    for r in to_replace:
        text = text.replace(r, "")
    pres_replace = [
        "MR. MARTIN THE PRESIDENT.",
        "MR. ACKLEY THE PRESIDENT."
    ]
    for p in pres_replace:
        text = text.replace(p, "THE PRESIDENT.")
    return text

def fix_64039(text):
    bush = re.compile(r"^President Bush")
    clean_text = re.sub(bush, "President Bush:", text)
    return clean_text

def fix_63786(text):
    bush = re.compile(r"^President Bush")
    clean_text = re.sub(bush, "President Bush:", text)
    return clean_text
    
def fix_63820(text):
    bush = re.compile(r"^President Bush")
    clean_text = re.sub(bush, "President Bush:", text)
    return clean_text

def fix_17762(text):
    text = text.replace("Well, good morning.", "The President: Well, good morning.")
    return text
    
def fix_4497(text):
    pre_question = re.compile(r"[A-Z ]*\[[0-9]\.\] ")
    clean_text = re.sub(pre_question, "", text)
    return clean_text

def fix_10409(text):
    header = re.compile(r"\[This[\w\.\' ]*brackets\.\]")
    clean_text = re.sub(header, "", text)
    return clean_text

def fix_17714(text):
    text = text.replace("First a statement,", "The President: First a statement,")
    return text

def fix_23332(text):
    text = text.replace("APPOINTMENTS ", "")
    return text

def fix_26881(text):
    to_replace = [
        "PLANS FOR THE DEVELOPMENT OF SOUTHEAST ASIA ",
        "QUESTIONS "
    ]
    for r in to_replace:
        text = text.replace(r, "")
    return text

def fix_16980(text):
    text = text.replace("Well, I have a brief statement", "The President: Well, I have a brief statement")
    return text

def fix_23492(text):
    text = text.replace("FEDERAL EXPENDITURES ", "")
    return text

def fix_5319(text):
    text = text.replace("Thank you very much, Mr. Barnes,", "THE PRESIDENT. Thank you very much, Mr. Barnes,")
    return text

def fix_6420(text):
    text = text.replace("Thank you very much, Joe McGovern,", "THE PRESIDENT. Thank you very much, Joe McGovern,")
    return text

def fix_5780(text):
    text = text.replace("THANK YOU very much", "THE PRESIDENT. THANK YOU very much")
    return text

def fix_5703(text):
    text = text.replace("AT THE outset", "THE PRESIDENT. AT THE outset")
    return text

def fix_5828(text):
    text = text.replace("GOOD MORNING", "THE PRESIDENT. GOOD MORNING")
    return text

def fix_15982(text):
    text = text.replace("I am delighted", "THE PRESIDENT: I am delighted")
    return text

def fix_15107(text):
    text = text.replace("So to manage", "THE PRESIDENT: So to manage")
    return text

def fix_28782(text):
    to_replace = [
        "INTENTION TO NOMINATE CLARK M.",
        "CLIFFORD AS SECRETARY OF DEFENSE"
    ]
    for r in to_replace:
        text = text.replace(r, "")
    return text

def fix_46377(text):
    text = text.replace('U. S. S. "Theodore Roosevelt"', "")
    return text

def fix_22066(text):
    text = text.replace("RESIGNATION OF WILLIAM P. MACCRACKEN, JR.", "")
    return text

def fix_15743(text):
    text = text.replace("Appeals for peace sent to Hitler and Mussolini.", "")
    return text

def fix_15401(text):
    text = text.replace("Held on the President's train en route Galveston, Tex., to Washington, D. C.", "")
    return text

def fix_15328(text):
    text = text.replace("Held at Herring Beach, Campobello Island, N. B.", "")
    return text

def fix_5931(text):
    text = text.replace("GOOD MORNING.", "THE PRESIDENT: GOOD MORNING.")
    return text

def fix_4979(text):
    text = text.replace("STATEMENT ANNOUNCING RELEASE OF REPORT OF THE COMMISSION ON CIA ACTIVITIES WITHIN THE UNITED STATES", "")
    return text

def fix_10418(text):
    text = text.replace("at that time.", "at that time.]")
    return text

fixers = {
    "27878": fix_27878,
    "26405": fix_26405,
    "28469": fix_28469,
    "15601": fix_15601,
    "16238": fix_16238,
    "15805": fix_15805,
    "60166": fix_60166,
    "26859": fix_26859,
    "27196": fix_27196,
    "27116": fix_27116,
    "27398": fix_27398,
    "64039": fix_64039,
    "63786": fix_63786,
    "17762": fix_17762,
    "17714": fix_17714,
    "16980": fix_16980,
    "10409": fix_10409,
    "23332": fix_23332,
    "23492": fix_23492,
    "26881": fix_26881,
    "15982": fix_15982,
    "63820": fix_63820,
    "15107": fix_15107,
    "28782": fix_28782,
    "46377": fix_46377,
    "22066": fix_22066,
    "15743": fix_15743,
    "15401": fix_15401,
    "15328": fix_15328,
    "10418": fix_10418,
    "8246": fix_8246,
    "4600": fix_4600,
    "4515": fix_4515,
    "4497": fix_4497,
    "5319": fix_5319,
    "6420": fix_6420,
    "5780": fix_5780,
    "5703": fix_5703,
    "5828": fix_5828,
    "5931": fix_5931,
    "4979": fix_4979
}