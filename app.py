from flask import Flask, render_template, request, redirect, url_for, jsonify
import pulp
import re
import csv
import json
from io import StringIO
from urllib.parse import urlencode
import pandas as pd

app = Flask(__name__)


def create_meeting_times():
    your_meeting_time_data = [
        {
            'days': 'MWF',
            'start_time': '8:00AM',
            'end_time': '8:55AM',
        },
        {
            'days': 'MWF',
            'start_time': '9:05AM',
            'end_time': '10:00AM',
        },
        {
            'days': 'MWF',
            'start_time': '10:10AM',
            'end_time': '11:05AM',
        },
        {
            'days': 'MWF',
            'start_time': '11:15AM',
            'end_time': '12:10PM',
        },
        {
            'days': 'MWF',
            'start_time': '12:20PM',
            'end_time': '1:15PM',
        },
        {
            'days': 'MWF',
            'start_time': '1:25PM',
            'end_time': '2:20PM',
        },
        {
            'days': 'MWF',
            'start_time': '2:30PM',
            'end_time': '3:25PM',
        },
        {
            'days': 'MWF',
            'start_time': '3:35PM',
            'end_time': '4:30PM',
        },
        {
            'days': 'TTh',
            'start_time': '8:00AM',
            'end_time': '9:20AM',
        },
        {
            'days': 'TTh',
            'start_time': '9:30AM',
            'end_time': '10:50AM',
        },
        {
            'days': 'TTh',
            'start_time': '11:00AM',
            'end_time': '12:20PM',
        },
        {
            'days': 'TTh',
            'start_time': '12:30PM',
            'end_time': '1:50PM',
        },
        {
            'days': 'TTh',
            'start_time': '2:00PM',
            'end_time': '3:20PM',
        },
        {
            'days': 'TTh',
            'start_time': '3:30PM',
            'end_time': '4:50PM',
        },
    ]

    return MeetingTimes(your_meeting_time_data)

def class_section_to_dict(class_section):
    return {
        'term': class_section.term,
        'section': class_section.section,
        'title': class_section.title,
        'location': class_section.location,
        'meeting_info': class_section.meeting_info,
        'faculty': class_section.faculty,
        'capacity': class_section.capacity,
        'status': class_section.status,
        'credits': class_section.credits,
        'academic_level': class_section.academic_level,
        'scheduled_day': getattr(class_section, 'scheduled_day', None),
        'scheduled_time': getattr(class_section, 'scheduled_time', None),
    }
    
    
def process_uploaded_data(uploaded_file_data):
    class_sections = []

    # Create a DataFrame from the uploaded data
    try:
        df = pd.read_csv(StringIO(uploaded_file_data))

        # Convert specific columns to numeric data type if needed
        numeric_columns = ['Credits']
        df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

        for index, row in df.iterrows():
            class_section = ClassSection(
                row['Term'], row['Section'], row['Title'], row['Location'], row['Meeting Info'],
                row['Faculty'], row['Available/Capacity'], row['Status'], row['Credits'],
                row['Academic Level'], row['Restrictions']
            )
            class_sections.append(class_section)

    except Exception as e:
        # Handle any exceptions that may occur during parsing
        print(f"Error processing CSV data: {str(e)}")

    return class_sections



# Define your ClassSection class here (with attributes and methods)
class ClassSection:
    def __init__(self, term, section, title, location, meeting_info, faculty, capacity, status, credits, academic_level, restrictions):
        self.term = term
        self.section = section
        self.title = title
        self.location = location
        self.meeting_info = meeting_info
        self.faculty = faculty
        #self.capacity = int(capacity)  # Extract the capacity as an integer
        try:
            # Split the capacity value by '/' and take the first part
            capacity_parts = capacity.split('/')
            self.capacity = int(capacity_parts[0].strip())  # Extract and convert to an integer
        except (ValueError, IndexError):
            # Handle the case where the conversion fails or the value is missing
            self.capacity = 0  # You can set a default value or handle it as needed

        self.status = status
        self.credits = float(credits)
        self.academic_level = academic_level


        # List of classes to avoid
        self.avoid_classes = []
        
        # List of unwanted timeslots
        self.unwanted_timeslots = []

        # Parse "Meeting Info" to extract MWF or TTh
        self.days = self.extract_days_from_meeting_info(meeting_info)
        self.time_slot = self.extract_time_slot_from_meeting_info(meeting_info)

    def extract_days_from_meeting_info(self, meeting_info):
        # Determine if it's MWF or TTh based on "Meeting Info" (you can modify this logic as needed)
        if "Monday, Wednesday, Friday" in meeting_info:
            return "MWF"
        elif "Tuesday, Thursday" in meeting_info:
            return "TTh"
        else:
            return None

    def extract_time_slot_from_meeting_info(self, meeting_info):
        # Extract the time slot from "Meeting Info" (you can modify this logic as needed)
        # Example logic: Look for a time pattern like "9:05AM - 10:00AM"
        time_pattern = re.search(r'\d{1,2}:\d{2}[APM]{2} - \d{1,2}:\d{2}[APM]{2}', meeting_info)
        if time_pattern:
            return time_pattern.group()
        else:
            return None

class MeetingTimes:
    def __init__(self, your_meeting_time_data):
        # Initialize meeting times based on your_meeting_time_data
        self.meeting_times = your_meeting_time_data

    def choose_time_blocks(self, days, credits):
        # Implement logic to choose appropriate time blocks based on days and credits
        time_blocks = []

        # Define the time slots based on the provided schedule
        if days == "MWF" or days == "TTh":
            time_blocks = [
                "8:00AM - 9:20AM",
                "9:30AM - 10:50AM",
                "11:00AM - 12:20PM",
                "12:30PM - 1:50PM",
                "2:00PM - 3:20PM",
                "3:30PM - 4:50PM",
            ]

        return time_blocks



    def get_days(self, days):
        # Implement logic to get individual days based on input (e.g., "MWF" -> ["M", "W", "F"])
        individual_days = []
        for day in days:
            if day == "M":
                individual_days.append("Monday")
            elif day == "T":
                individual_days.append("Tuesday")
            elif day == "W":
                individual_days.append("Wednesday")
            elif day == "R":
                individual_days.append("Thursday")
            elif day == "F":
                individual_days.append("Friday")
            # Add additional days as needed (e.g., "S" for Saturday, "U" for Sunday)

        return individual_days


# Function to create ClassSection objects from data
def create_class_sections_from_data(class_sections_data):
    class_sections = []
    for section_data in class_sections_data:
        # Extract data from 'section_data' and create a ClassSection object
        term = section_data.get('term', '')
        section = section_data.get('section', '')
        title = section_data.get('title', '')
        location = section_data.get('location', '')
        meeting_info = section_data.get('meetingInfo', '')
        faculty = section_data.get('faculty', '')
        capacity = section_data.get('capacity', '')
        status = section_data.get('status', '')
        credits = section_data.get('credits', '')
        academic_level = section_data.get('academicLevel', '')
        restrictions = section_data.get('restrictions', '')
        
        class_section = ClassSection(term, section, title, location, meeting_info, faculty, capacity, status, credits, academic_level, restrictions)
        class_sections.append(class_section)

    return class_sections







def update_class_sections_with_schedule(class_sections, class_timeslots, meeting_times):
    """
    Update the class sections with their scheduled day and time based on the optimization results.

    Args:
        class_sections (list): List of ClassSection objects.
        class_timeslots (dict): Dictionary of LpVariable binary variables representing class timeslots.
        meeting_times (MeetingTimes): Object containing meeting time data.
    """
    for class_section in class_sections:
        for day in ["MWF", "TTh"]:
            for start_time in meeting_times.choose_time_blocks(class_section.days, class_section.credits):
                variable = class_timeslots[class_section.section, day, start_time]
                if variable.varValue == 1:
                    # This class_section is scheduled for the specified day and time slot
                    class_section.scheduled_day = day
                    class_section.scheduled_time = start_time



# Create a list of ClassSection objects from the CSV data
def read_csv_and_create_class_sections(csv_filename):
    class_sections = []
    with open(csv_filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            class_section = ClassSection(
                row['Term'], row['Section'], row['Title'], row['Location'], row['Meeting Info'],
                row['Faculty'], row['Available/Capacity'], row['Status'], row['Credits'],
                row['Academic Level'], row['Restrictions']
            )
            class_sections.append(class_section)
    return class_sections

def optimize_schedule(class_sections, meeting_times):
    # Create a binary variable for each class and time slot
    class_timeslots = pulp.LpVariable.dicts(
        "ClassTimeslot", ((class_section.section, day, start_time)
                          for class_section in class_sections
                          for day in ["MWF", "TTh"]  # Include both "MWF" and "TTh"
                          for start_time in meeting_times.choose_time_blocks(day, class_section.credits)),  # Use choose_time_blocks
        cat=pulp.LpBinary
    )

    # Create an optimization problem
    model = pulp.LpProblem("ClassScheduling", pulp.LpMinimize)

    # Define constraints (You need to specify your constraints here)
    # Constraint 1: Each class is scheduled once and only once
    for class_section in class_sections:
        model += pulp.lpSum(class_timeslots[class_section.section, day, start_time]
                            for day in ["MWF", "TTh"]
                            for start_time in meeting_times.choose_time_blocks(day, class_section.credits)) == 1

    # Constraint 2: Instructor constraints (each instructor can teach one class at a time)
    instructors = set(class_section.faculty for class_section in class_sections)
    for instructor in instructors:
        model += pulp.lpSum(class_timeslots[class_section.section, day, start_time]
                            for class_section in class_sections
                            for day in ["MWF", "TTh"]
                            for start_time in meeting_times.choose_time_blocks(day, class_section.credits)
                            if class_section.faculty == instructor) <= 1

    # Constraint 3: Avoid class overlaps (hard constraint)
    for day in ["MWF", "TTh"]:
        for start_time in meeting_times.choose_time_blocks(day, 3):
            model += pulp.lpSum(class_timeslots[class_section.section, day, start_time] for class_section in class_sections) <= 1

    # Constraint 4: Penalize having too many classes in the same time block (encourage distribution)
    for day in ["MWF", "TTh"]:
        for start_time in meeting_times.choose_time_blocks(day, 3):
            model += pulp.lpSum(class_timeslots[class_section.section, day, start_time] for class_section in class_sections) <= 10

    # Constraint 5: Penalize classes that intersect and have one of each other in avoid_classes
    for class_section in class_sections:
        for other_class_section in class_sections:
            if class_section != other_class_section and class_section.section in other_class_section.avoid_classes:
                for day in ["MWF", "TTh"]:
                    for start_time in meeting_times.choose_time_blocks(day, class_section.credits):
                        model += class_timeslots[class_section.section, day, start_time] + class_timeslots[other_class_section.section, day, start_time] <= 3
    
    # Constraint 6: Avoid unwanted timeslots
    for class_section in class_sections:
        for day in ["MWF", "TTh"]:
            for start_time in class_section.unwanted_timeslots:
                model += pulp.lpSum(class_timeslots[class_section.section, day, start_time] for day in [day]) == 0

    # Solve the optimization problem
    model.solve()
    
    # Interpret the results and generate the final schedule
    update_class_sections_with_schedule(class_sections, class_timeslots, meeting_times)

    # Now, class_sections contain the final schedule information based on the optimization results.
    return class_sections





# Define the '/optimize' route to handle optimization requests
@app.route('/optimize', methods=['POST'])
def optimize():
    # Get the JSON data from the request
    data = request.get_json()

    # Extract class section data from the 'data' variable
    class_sections_data = data.get('classData', [])
    
    # Convert the class section data to ClassSection objects
    class_sections = create_class_sections_from_data(class_sections_data)

    # Create a MeetingTimes object
    meeting_times = create_meeting_times()

    # Optimize the schedule based on the received data
    optimized_class_sections = optimize_schedule(class_sections, meeting_times)

    # Prepare the optimization results
    optimization_results = {
        'message': 'Optimization complete',
        'results': [class_section_to_dict(cs) for cs in optimized_class_sections],
    }

    return jsonify(optimization_results)



@app.route('/upload', methods=['GET', 'POST'])
def upload():
    uploaded_file_data = None
    class_sections = None

    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        # Check if the file is empty
        if file.filename == '':
            return redirect(request.url)

        if file:
            # Save the uploaded file data
            uploaded_file_data = file.read().decode('utf-8')
            # Process the uploaded file data to create class_sections
            class_sections = process_uploaded_data(uploaded_file_data)

    return render_template('display.html', uploaded_file_data=uploaded_file_data, class_sections=class_sections, your_meeting_time_data=create_meeting_times().meeting_times)

@app.route('/', methods=['GET', 'POST'])
def index():
    uploaded_file_data = None

    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        # Check if the file is empty
        if file.filename == '':
            return redirect(request.url)

        if file:
            # Save the uploaded file data
            uploaded_file_data = file.read().decode('utf-8')

    return render_template('index.html', uploaded_file_data=uploaded_file_data)



if __name__ == "__main__":
    app.run(debug=True)
