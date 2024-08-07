import json
import logging
import os
import yaml
import calendar
from dotenv import load_dotenv
import textwrap 
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from langchain_openai import ChatOpenAI
from typing import List
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel, Field 

from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics 
pdfmetrics.registerFont(TTFont('Calibri-Bold', '/Users/scholar/Downloads/calibri-bold.ttf'))
pdfmetrics.registerFont(TTFont('Calibri', '/Users/scholar/Downloads/calibri.ttf'))
pdfmetrics.registerFont(TTFont('Calibri-Italic', '/Users/scholar/Downloads/calibri-italic.ttf'))

from openai import OpenAI
import langchain
from langchain import LLMChain
from langchain.chains.openai_functions import create_structured_output_chain

from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import create_qa_with_sources_chain
from langchain.chains import ConversationalRetrievalChain

openai_api_key= os.getenv("OPEN_API_KEY")



# Open and read the JSON file
with open('results.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


def FirstName_LastName(data):
    # Extract the first key, which is the LinkedIn URL
    profile_key = next(iter(data.keys()))
    profile_data = data[profile_key][0]  # Access the first item in the list under this key

    # Ensure these keys exist in the profile data
    if 'firstName' in profile_data and 'lastName' in profile_data:
        return profile_data['firstName'] + ' ' + profile_data['lastName']
    else:
        return "Key(s) not found in the data"

resume_FirstName_LastName = FirstName_LastName(data).upper()

# Extract the LinkedIn URL from the data keys
fullLinkedinURL= list(data.keys())[0]

# Remove the 'https://www.' part from the URL
resume_LinkedInURL = fullLinkedinURL.replace('https://www.', '')


""" EDUCATION SECTION DETAILS """
def extract_educations(data):
    profile_key = next(iter(data.keys()))
    profile_data = data[profile_key]
    
    educations = []
    for profile in profile_data:
        education_list = profile.get('educations', [])
        educations.extend(education_list)

    return educations

educations_data = extract_educations(data)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
# Define the functions that we want the model to perform
function_descriptions_multiple = [
    {
        "name": "college_name",
        "description": "Only provide the full name of the university the student most recently attended.",
    },
    {
        "name": "college_major",
        "description": "Provide only the most recent degree and its major. Use the format 'Bachelor of Science, Major'. Do not include abbreviations like BBA, BS, or BA. ",
    }
]

responses = {}
for function in function_descriptions_multiple:
    function_name = function["name"]
    description = function["description"]

    # Prepare the prompt
    prompt_for_function = f"{description}\n\n{educations_data}\n"
    
    response = llm.invoke(
        [
            HumanMessage(content=prompt_for_function),
        ]
    )

    response_content = response.content.strip()
    responses[function_name] = response_content 

education_section_details = {function_name: content for function_name, content in responses.items()}

college_name = education_section_details['college_name']
college_major = education_section_details['college_major']

"""Generating Minor & Certificate details"""

def generate_education_info(data):
    prompt = f"With the following input:\n\n{data}\n\:, search for any mention of a 'minor' and 'certificate' and return only what each of those may be for the user. (should be in the format Minor: 'minor name' and on a separate line Certificate: 'certificate name') it should be capitalized. If either the word 'minor' or the word 'certificate' is not found in the text at all, return Not Applicable for that word."
    openai_client = OpenAI()
    chat_completion = openai_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
  )
    return chat_completion.choices[0].message


courseworkinfo = generate_education_info(data).content
if "Not Applicable" not in courseworkinfo:
    print(courseworkinfo)


'''GRADUATION DATE'''
education_entry = educations_data[0]

end_date = education_entry.get("timePeriod", {}).get("endDate", {})
month_number = end_date.get("month")
year = end_date.get("year")

# Format the graduation date using the calendar module
if month_number and year:
    graduation_date = f"{calendar.month_name[month_number]} {year}"
else:
    graduation_date = "Date not available"

'''Relevant coursework'''
def extract_classes(data):
    classwork_key = next(iter(data.keys()))
    classwork_data = data[classwork_key]
    classestaken = []

    for classes in classwork_data:
        coursesexist = classes.get("courses", [])
        if not coursesexist:
            continue

        names = [course.get("name", "") for course in coursesexist]
        classestaken.extend(names)

    relevant_coursework = ", ".join(classestaken)
    return relevant_coursework

relevant_courswork = extract_classes(data)

""""EXPERIENCE SECTION DETAILS"""
def extract_experiences(data):
    profile_key = next(iter(data.keys()))
    profile_data = data[profile_key]
    
    experiences = []
    for profile in profile_data:
        education_list = profile.get('positions', [])
        experiences.extend(education_list)

    return experiences


experiences_data = extract_experiences(data)


companies_worked_at = []

# Extracting company names
for experience in experiences_data:
    company_name = experience.get("companyName")
    if company_name:
        companies_worked_at.append(company_name)

print(companies_worked_at)

'''DESCRIPTIONS'''
descriptions = []
for experience in experiences_data:
    description_info = experience.get("description")
    descriptions.append(description_info)

print(descriptions)

openai_model_name = "gpt-3.5-turbo"

llm_kwargs = dict(
    model_name=openai_model_name,
    temperature = 0.3,
    model_kwargs=dict(
        # top_p=0.6, 
        frequency_penalty=0.1
    ),
)
chat_model = ChatOpenAI(**llm_kwargs)

prompt_msgs = [
    SystemMessage(
        content=(
            "You are an expert critic. "
            "Your goal is to strictly follow all the provided <Steps> and meet all the given <Criteria>."
        )
    ),
    HumanMessagePromptTemplate.from_template(
        "<Descriptions>"
        "\n{descriptions}\n"
    ),
    HumanMessagePromptTemplate.from_template(
        "<Writing Bullets>"
        "Rewrite this information into seperate bullet point sentences, starting with this character •. Each bullet point should be seperated by task, starting with a strong ACTION VERB followed by Description of the ACTIVITY OR SKILL followed by the end result or accomplishment and/or purpose"
    ),

    # HumanMessage(
    #     content="<Instruction> Critique <Writing Bullets>, and [Use a variety of strong action verbs at the beginning of bullets and avoid repetition (e.g., Led, Managed, etc.)—do not begin a bullet with a weak/missing verb (e.g., Responsible for… Assisted with… Worked on… Helped…)."
    # ),
    HumanMessage(
        content=(
            "<Steps>"
            "\n - Critique <Writing Bullets>, and [Use a variety of strong action verbs at the beginning of bullets and avoid repetition (e.g., Led, Managed, etc.)—do not begin a bullet with a weak/missing verb (e.g., Responsible for… Assisted with… Worked on… Helped…)."
            "\n- Critique <Writing Bullets> so that it includes specific actions and measurable results—specify how many people you managed, amount of money saved, earned, or managed, percent of sales gained, or savings gained by process improvements. Also make sure no words are fully capitalized.]."
            "\n- Critique <Writing Bullets> Resume bullets are not sentences—remove pronouns (I, me, my, we, us, our) and limit articles (a, an, the) and helping verbs (had, have, may, might, forms of “to be”: am, is, are, was, were) when writing resume bullets; reader assumes these words. Remove any period punctuation as well.] "
            "\n- Follow all steps one by one. "
            
        )
    ),
]
improver_prompt = ChatPromptTemplate(messages=prompt_msgs)
prompt_imputs = dict(

    descriptions = descriptions
)
from langchain import LLMChain
better_improver_chain = LLMChain(
    llm=chat_model,
    prompt=improver_prompt,
    verbose=True
)
improved_descriptions_by_company = {}

for i, description in enumerate(descriptions):
    if description:  # Ensure the description is not None
        prompt_inputs = {"descriptions": description}
        improved_description = better_improver_chain.predict(**prompt_inputs)
        company_name = experiences_data[i].get("companyName", f"Company_{i + 1}")
        improved_descriptions_by_company[company_name] = improved_description

for company, desc in improved_descriptions_by_company.items():
    print(f"Company: {company}")
    print(f"Improved Description:\n{desc}\n")

titleincompany = []
for experience in experiences_data:
    title = experience.get("title")
    titleincompany.append(title)

print(titleincompany)

locationnames = []
for experience in experiences_data:
    location = experience.get("locationName")
    if location is None:
        locationnames.append("Remote")
    else:
        locationnames.append(location)

datesforpositions = []
for experience in experiences_data:
    time_period = experience.get("timePeriod", {})
    start_dateforposition = time_period.get("startDate", {})
    start_month_number = start_dateforposition.get("month")
    start_year = start_dateforposition.get("year")
    
    if time_period.get("endDate") is None:
        if start_month_number and start_year:
            role_start_date = f"{calendar.month_name[start_month_number]} {start_year}"
            datesforpositions.append(f'{role_start_date} - Present')
        else:
            datesforpositions.append('Dates not provided')
    else:
        end_dateforposition = time_period.get("endDate", {})
        end_month_number = end_dateforposition.get("month")
        end_year = end_dateforposition.get("year")
        
        if start_month_number and start_year and end_month_number and end_year:
            role_start_date = f"{calendar.month_name[start_month_number]} {start_year}"
            role_end_date = f"{calendar.month_name[end_month_number]} {end_year}"
            datesforpositions.append(f'{role_start_date} - {role_end_date}')
        else:
            datesforpositions.append('Dates not provided')


# # Format the graduation date using the calendar module
# if month_number and year:
#     graduation_date = f"{calendar.month_name[month_number]} {year}"
# else:
#     graduation_date = "Date not available"

"""Leadership Experiences and Activities"""

"""HONORS SECTION DETAILS"""

def extract_honors(data):
    # Assuming data is a dictionary and the first key contains the relevant section
    honors_key = next(iter(data.keys()))
    data_honors_section = data[honors_key]

    if isinstance(data_honors_section, list):
        # If it's a list, check if the first element contains the honors data
        if len(data_honors_section) > 0 and isinstance(data_honors_section[0], dict):
            honors_data = data_honors_section[0].get("honors", [])
        else:
            honors_data = []
    elif isinstance(data_honors_section, dict):
        # If it's a dict, directly get the honors data
        honors_data = data_honors_section.get("honors", [])
    else:
        honors_data = []

    resume_honorsdates = []
    all_honors_descriptions = []
    honors_titles = []

    for honor in honors_data:
        honor_title = honor.get("title", "")
        honor_description = honor.get("description", "")
        issue_date = honor.get("issueDate", {})
        month_number = issue_date.get("month")
        year = issue_date.get("year")

        if month_number and year:
            date_of_honors = f"{calendar.month_name[month_number]} {year}"
        else:
            date_of_honors = "Date not available"

        resume_honorsdates.append(date_of_honors)
        all_honors_descriptions.append(honor_description)
        honors_titles.append(honor_title)

    return resume_honorsdates, all_honors_descriptions, honors_titles

def honors_revised(all_honors_descriptions):
    revised_honors = []
    
    for honors_description in all_honors_descriptions:
        prompt = f"With the following input:\n\n{honors_description}\n\n, condense the information in the data to one bullet point sentence, in a way that captures all the important points in the data."
        openai_client = OpenAI()
        chat_completion = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        answer = chat_completion.choices[0].message
        revised_honors.append(answer.content)

    return revised_honors


resume_honors_dates, all_honors_descriptions, honors_titles = extract_honors(data)

gpt_revised_honors = honors_revised(all_honors_descriptions)

# ''''Extra sections'''
# def additional_sections(data):
#     prompt = f"With the following input:\n\n{data}\n\:, search for any mention of a 'PROJECTS' section or 'VOLUNTEERING' section or 'ORGANIZATIONS' section, and return only what each of those may be for the user. (should be in the format Minor: 'minor name' and on a separate line Certificate: 'certificate name') it should be capitalized. If either the word 'minor' or the word 'certificate' is not found in the text at all, return Not Applicable for that word."
#     openai_client = OpenAI()
#     chat_completion = openai_client.chat.completions.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt,
#             }
#         ],
#         model="gpt-3.5-turbo",
#   )
#     return chat_completion.choices[0].message


# courseworkinfo = generate_education_info(data).content
# if "Not Applicable" not in courseworkinfo:
#     print(courseworkinfo)

"""    EXPORTING TO PDF   """
class linesection:
    def __init__(self, canvas, width, margin=50):
        self.canvas = canvas
        self.width = width
        self.margin = margin
        self.current_y = 0

    def add_header(self, text, font_name="Calibri-Bold", font_size=9, y_position=None):
        self.canvas.setFont(font_name, font_size)
        if y_position is not None:
            self.current_y = y_position
        else:
            self.current_y -= 9 

        self.canvas.drawString(self.margin, self.current_y, text)
        self.add_line()

    def add_line(self):
        line_y = self.current_y - 5
        self.canvas.setLineWidth(0.2)
        self.canvas.line(self.margin, line_y, self.width - self.margin, line_y)
        self.current_y = line_y - 9

    def time(self, text, font_name="Calibri", font_size=9):
        self.canvas.setFont(font_name, font_size)
        text_width = self.canvas.stringWidth(text, font_name, font_size)
        x_position = self.width - self.margin - text_width
        self.canvas.drawString(x_position, self.current_y, text)
            
    def add_university(self, text, font_name="Calibri-Bold", font_size=9, y_position=None):
        self.canvas.setFont(font_name, font_size)
        if y_position is not None:
            self.current_y = y_position
        else:
            self.current_y -= 0.01  # Default spacing for text lines

        self.canvas.drawString(self.margin, self.current_y, text)
        # Store the width of the university name text for positioning the position role
        self.university_text_width = self.canvas.stringWidth(text, font_name, font_size)
        # Adjust spacing after text
        #self.current_y -= 9  

    def add_relevant_coursework(self, text, font_name="Calibri", font_size=9, x_offset=None, line_spacing=12):
        self.canvas.setFont(font_name, font_size)
        max_width = self.width - 2 * self.margin

        if x_offset is None:
            x_offset = self.margin + self.university_text_width + self.canvas.stringWidth(" ", font_name, font_size)

        lines = self.wrap_text(text.strip(), max_width - self.margin)

        for line in lines:
            self.canvas.drawString(x_offset, self.current_y, line)
            self.current_y -= line_spacing

    def position_role(self, text, font_name="Calibri-Italic", font_size=9, x_offset=None):
        self.canvas.setFont(font_name, font_size)
        if x_offset is None:
            x_offset = self.margin + self.university_text_width + self.canvas.stringWidth(" ", font_name, font_size)
        self.canvas.drawString(x_offset, self.current_y, text)
        self.position_role_text_width = self.canvas.stringWidth(text, font_name, font_size)

    def location_role(self, text, font_name="Calibri", font_size=9, x_offset=None):
        self.canvas.setFont(font_name, font_size)
        if x_offset is None:
            x_offset = self.margin + self.university_text_width + self.position_role_text_width + self.canvas.stringWidth(" ", font_name, font_size)
        self.canvas.drawString(x_offset, self.current_y, text)
        self.current_y -= 3  # Adjust spacing after text

    def education_studies_info(self, text, font_name="Calibri", font_size=9, x_offset=210):
        self.canvas.setFont(font_name, font_size)
        lines = text.split('\n')  # Split the text into lines
        for line in lines:
            self.canvas.drawString(x_offset, self.current_y, line)
            self.current_y -= 11

    def description_section_info(self, text, font_name="Calibri", font_size=9, line_spacing=12):
        self.canvas.setFont(font_name, font_size)
        max_width = self.width - 2 * self.margin
        bullet = "• "
        bullet_width = self.canvas.stringWidth(bullet)
        indent_width = self.margin + bullet_width

        self.current_y -= line_spacing

        # Split the text by the bullet point symbol
        bullet_points = text.split('• ')
        for point in bullet_points:
            if point.strip():
                lines = self.wrap_text(bullet + point.strip(), max_width)
                for i, line in enumerate(lines):
                    if i==0:
                        self.canvas.drawString(self.margin, self.current_y, line)
                    else:
                        self.canvas.drawString(indent_width, self.current_y, line)
                    self.current_y -= line_spacing

    def wrap_text(self, text, max_width):
        # Set the font for calculating text width
        lines = []
        words = text.split(' ')
        line = ''
        
        for word in words:
            test_line = line + word + ' '
            if self.canvas.stringWidth(test_line) <= max_width:
                line = test_line
            else:
                lines.append(line.strip())
                line = word + ' '
        if line:
            lines.append(line.strip())
        return lines
    

    def add_space(self,space_amount):
        self.current_y -= space_amount

    
wrapped_name = textwrap.fill(resume_FirstName_LastName, width=75)
wrapped_linkedin = textwrap.fill(resume_LinkedInURL, width=50)
c = canvas.Canvas("exportedresume.pdf", pagesize=letter)
width, height = letter

# Initialize lineSection
sectionline = linesection(c, width)

# Title
font_name = "Calibri-Bold"
font_size = 16
c.setFont(font_name, font_size)
text_width = c.stringWidth(wrapped_name, font_name, font_size)
x_position = (width - text_width) / 2 
y_title = height - 50
c.drawString(x_position, y_title, wrapped_name)

# LinkedIn URL
c.setFont("Calibri", 9)
y_url = y_title - 10
c.drawString(x_position, y_url, wrapped_linkedin)

sectionline.add_header("EDUCATION", y_position=y_url - 9)

sectionline.add_university(college_name)
sectionline.time(graduation_date)

sectionline.education_studies_info(college_major)
sectionline.education_studies_info(courseworkinfo)
sectionline.add_university("Relevant Coursework:")
sectionline.add_relevant_coursework(relevant_courswork)

sectionline.add_header("EXPERIENCES")
for i in range(len(companies_worked_at)):
    sectionline.time(datesforpositions[i])
    sectionline.add_university(companies_worked_at[i] + " -")
    sectionline.position_role(titleincompany[i] + ";")
    sectionline.location_role(" " + locationnames[i])
    if improved_descriptions_by_company.get(f"{companies_worked_at[i]}") is None:
        sectionline.description_section_info("No description given") 
    else:
        sectionline.description_section_info(improved_descriptions_by_company.get(f"{companies_worked_at[i]}"))   
    sectionline.add_space(5) 
                             

# for i in range(0,4):
#     sectionline.add_university(companies_worked_at[i])
#     i+=1
#sectionline.add_header("LEADERSHIP EXPERIENCE AND ACTIVITIES")
sectionline.add_header("HONORS")
for t in range(len(honors_titles)):
    sectionline.time(resume_honors_dates[t])
    sectionline.add_university(honors_titles[t])
    sectionline.description_section_info(gpt_revised_honors[t])


sectionline.add_header("ADDITIONAL INFORMATION")

# sectionline.add_university("Computer Skills:")

# sectionline.add_university("Certifications:")
# sectionline.add_university("Languages:")

sectionline.add_university("Work Eligibility:")
sectionline.add_relevant_coursework("Eligible to work in the U.S. with no restrictions")


#sectionline.time(resume_honors_dates)

#sectionline.add_header("ADDITIONAL INFORMATION")


c.save()



