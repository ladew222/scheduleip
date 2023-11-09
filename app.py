from flask import Flask, render_template, request, redirect, url_for, jsonify
import pulp
import re
import csv
import json
from io import StringIO
from urllib.parse import urlencode
import pandas as pd
from io import StringIO
app = Flask(__name__)


def create_meeting_times():
        your_meeting_time_data = [
        {
            'days': 'M W F',
            'start_time': '8:00AM',
            'end_time': '8:55AM',
        },
        {
            'days': 'M W F',
            'start_time': '9:05AM',
            'end_time': '10:00AM',
        },
        {
            'days': 'M W F',
            'start_time': '10:10AM',
            'end_time': '11:05AM',
        },
        {
            'days': 'M W F',
            'start_time': '11:15AM',
            'end_time': '12:10PM',
        },
        {
            'days': 'M W F',
            'start_time': '12:20PM',
            'end_time': '1:15PM',
        },
        {
            'days': 'M W F',
            'start_time': '1:25PM',
            'end_time': '2:20PM',
        },
        {
            'days': 'M W F',
            'start_time': '2:30PM',
            'end_time': '3:25PM',
        },
        {
            'days': 'M W F',
            'start_time': '3:35PM',
            'end_time': '4:30PM',
        },
        {
            'days': 'Tu Th',
            'start_time': '8:00AM',
            'end_time': '9:20AM',
        },
        {
            'days': 'Tu Th',
            'start_time': '9:30AM',
            'end_time': '10:50AM',
        },
        {
            'days': 'Tu Th',
            'start_time': '11:00AM',
            'end_time': '12:20PM',
        },
        {
            'days': 'Tu Th',
            'start_time': '12:30PM',
            'end_time': '1:50PM',
        },
        {
            'days': 'Tu Th',
            'start_time': '2:00PM',
            'end_time': '3:20PM',
        },
        {
            'days': 'Tu Th',
            'start_time': '3:30PM',
            'end_time': '4:50PM',
        },
    ]

        return your_meeting_time_data
    

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
    
    


    
class ClassSection:
    def __init__(self, sec_name, title, min_credit, sec_cap, room, bldg, week_days, csm_start, csm_end, faculty1, restrictions, blocked_time_slots, assigned_meeting_time_indices=None):
        self.sec_name = sec_name
        self.title = title
        self.min_credit = min_credit
        self.sec_cap = sec_cap
        self.room = room
        self.bldg = bldg
        self.week_days = week_days
        self.csm_start = csm_start
        self.csm_end = csm_end
        self.faculty1 = faculty1

        # List of classes to avoid
        self.avoid_classes = []

        # List of unwanted timeslots
        self.unwanted_timeslots = []

        if assigned_meeting_time_indices is None:
            # Initialize assigned meeting time indices as an empty list
            self.assigned_meeting_time_indices = []
        else:
            # Use the provided assigned meeting time indices
            self.assigned_meeting_time_indices = assigned_meeting_time_indices

        # Add restrictions and blocked_time_slots to the lists
        self.add_restrictions(restrictions)
        self.add_unwanted_timeslots(blocked_time_slots)

        # If assigned meeting time indices are not vided, calculate them
        if not assigned_meeting_time_indices:
            meeting_times_data = create_meeting_times()
            self.calculate_assigned_meeting_time_indices(meeting_times_data)


    def add_restrictions(self, restrictions):
        # Check if restrictions is not None, is a string, and is not empty before splitting
        if restrictions and isinstance(restrictions, str) and restrictions.strip():
            # Split and add restrictions to the avoid_classes list
            self.avoid_classes.extend(restrictions.split(';'))

    def add_unwanted_timeslots(self, blocked_time_slots):
        # Check if blocked_time_slots is not None, is a string, and is not empty before splitting
        if blocked_time_slots and isinstance(blocked_time_slots, str) and blocked_time_slots.strip():
            # Split and add blocked_time_slots to the unwanted_timeslots list
            self.unwanted_timeslots.extend(blocked_time_slots.split(';'))

    def calculate_assigned_meeting_time_indices(self, meeting_times_data):
        # Initialize assigned meeting time indices as an empty list
        assigned_meeting_time_indices = []

        # Iterate through meeting times data
        for index, meeting_time in enumerate(meeting_times_data):
            if set(meeting_time['days']).issubset(set(self.week_days)):
                # Check if class days contain all meeting days
                start_time = meeting_time['start_time']
                end_time = meeting_time['end_time']
                class_start_time = self.csm_start

                # Check if class start time falls within the meeting time slot
                if start_time <= class_start_time <= end_time:
                    assigned_meeting_time_indices.append(index)

        # Update the assigned meeting time indices
        self.assigned_meeting_time_indices = assigned_meeting_time_indices


        # Update the assigned meeting time indices
        self.assigned_meeting_time_indices = assigned_meeting_time_indices


        # Update the assigned meeting time indices
        self.assigned_meeting_time_indices = assigned_meeting_time_indices






# Function to create ClassSection objects from data
def create_class_sections_from_data(class_sections_data):
    class_sections = []
    for section_data in class_sections_data:
        # Extract data from 'section_data' and create a ClassSection object
        sec_name = section_data.get('section', '')  # Updated to match the new column name
        title = section_data.get('title', '')
        min_credit = section_data.get('minCredit', '')  # Updated to match the new column name
        sec_cap = section_data.get('secCap', '')  # Updated to match the new column name
        room = section_data.get('room', '')
        bldg = section_data.get('bldg', '')
        week_days = section_data.get('weekDays', '')  # Updated to match the new column name
        csm_start = section_data.get('csmStart', '')  # Updated to match the new column name
        csm_end = section_data.get('csmEnd', '')  # Updated to match the new column name
        faculty1 = section_data.get('faculty1', '')  # Updated to match the new column name
        restrictions = section_data.get('restrictions', '')
        blocked_time_slots = section_data.get('blockedTimeSlots', '')  # Updated to match the new column name
        class_section = ClassSection(sec_name, title, min_credit, sec_cap, room, bldg, week_days, csm_start, csm_end, faculty1, restrictions,blocked_time_slots)
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
    try:
        df = pd.read_csv(csv_filename)  # Read the CSV file with headers

        for index, row in df.iterrows():
            class_section = ClassSection(
                row['Term'], row['Section'], row['Title'], row['Location'], row['Meeting Info'],
                row['Faculty'], row['Available/Capacity'], row['Status'], row['Credits'],
                row['Academic Level'], row['Restrictions'], row['Blocked Time Slots'],
            )
            class_sections.append(class_section)

    except Exception as e:
        # Handle any exceptions that may occur during parsing
        print(f"Error processing CSV data: {str(e)}")

    return class_sections




def optimize_schedule(class_sections, meeting_times):
    # Extract the meeting times list from the MeetingTimes object

    # Create a binary variable for each class and time slot
    class_timeslots = pulp.LpVariable.dicts(
        "ClassTimeslot",
        ((class_section.sec_name, meeting_time['days'], meeting_time['start_time'])
         for class_section in class_sections
         for meeting_time in meeting_times
         if meeting_times.index(meeting_time) in class_section.assigned_meeting_time_indices),
        cat=pulp.LpBinary
    )

    # Additional variables for 1-credit classes if they exist
    extra_timeslots = {}
    if any(cs.min_credit == '1' for cs in class_sections):
        extra_timeslots = pulp.LpVariable.dicts(
            "ExtraTimeslot",
            ((class_section.sec_name, meeting_time['days'], meeting_time['start_time'])
             for class_section in class_sections if class_section.min_credit == '1'
             for meeting_time in meeting_times
             if meeting_times.index(meeting_time) in class_section.assigned_meeting_time_indices),
            cat=pulp.LpBinary
        )

    # Create an optimization problem
    model = pulp.LpProblem("ClassScheduling", pulp.LpMinimize)

    # Objective function
    model += pulp.lpSum([class_timeslots[class_section.sec_name, meeting_time['days'], meeting_time['start_time']]
                         for class_section in class_sections
                         for meeting_time in meeting_times
                         if meeting_times.index(meeting_time) in class_section.assigned_meeting_time_indices])

    # Penalize overlapping classes that should avoid each other
    for class_section in class_sections:
        for other_section in class_sections:
            if other_section.sec_name in class_section.avoid_classes:
                for meeting_time in meeting_times:
                    if (meeting_times.index(meeting_time) in class_section.assigned_meeting_time_indices and
                            meeting_times.index(meeting_time) in class_sections.assigned_meeting_time_indices):
                        model += 50 * (class_timeslots[class_section.sec_name, meeting_time['days'], meeting_time['start_time']] *
                                        class_timeslots[other_section.sec_name, meeting_time['days'], meeting_time['start_time']])

    # Modify constraints to work with the updated variable structure

    # Constraint 1: Each class is scheduled once and only once
    for class_section in class_sections:
        timeslots_required = 2 if class_section.min_credit == '4' else 1
        model += pulp.lpSum(class_timeslots[class_section.sec_name, meeting_time['days'], meeting_time['start_time']]
                            for meeting_time in meeting_times
                            if meeting_times.index(meeting_time) in class_section.assigned_meeting_time_indices) == timeslots_required

    # Constraint 2: Instructor constraints (each instructor can teach one class at a time)
    instructors = set(cs.faculty1 for cs in class_sections)
    for instructor in instructors:
        for meeting_time in meeting_times:
            if any(cs.faculty1 == instructor for cs in class_sections if
                   meeting_times.index(meeting_time) in cs.assigned_meeting_time_indices):
                model += pulp.lpSum(class_timeslots[class_section.sec_name, meeting_time['days'], meeting_time['start_time']]
                                    for class_section in class_sections
                                    if class_section.faculty1 == instructor) <= 1

    # Constraint 3: No class overlap
    for meeting_time in meeting_times:
        model += pulp.lpSum(class_timeslots[class_section.sec_name, meeting_time['days'], meeting_time['start_time']]
                            for class_section in class_sections
                            if meeting_times.index(meeting_time) in class_section.assigned_meeting_time_indices) <= 1

    # Constraint 4: Room constraints (no two classes can be in the same room at the same time)
    rooms = set(cs.room for cs in class_sections)
    for room in rooms:
        for meeting_time in meeting_times:
            if any(cs.room == room for cs in class_sections if
                   meeting_times.index(meeting_time) in cs.assigned_meeting_time_indices):
                model += pulp.lpSum(class_timeslots[class_section.sec_name, meeting_time['days'], meeting_time['start_time']]
                                    for class_section in class_sections
                                    if class_section.room == room) <= 1

    # Constraint for avoiding unwanted timeslots for certain classes
    for class_section in class_sections:
        for meeting_time_index in class_section.unwanted_timeslots:
            if meeting_time_index < len(meeting_times):
                model += class_timeslots[class_section.sec_name, meeting_times[meeting_time_index]['days'], meeting_times[meeting_time_index]['start_time']] == 0

    # Additional constraints for 1-credit classes
    for class_section in [cs for cs in class_sections if cs.min_credit == '1']:
        # Constraint: A 1-credit class must be scheduled an extra time slot
        model += pulp.lpSum(extra_timeslots[class_section.sec_name, meeting_time['days'], meeting_time['start_time']]
                            for meeting_time in meeting_times
                            if meeting_times.index(meeting_time) in class_section.assigned_meeting_time_indices) == 1

        # Constraint: This extra time slot must not conflict with other classes
        for meeting_time in meeting_times:
            if (meeting_times.index(meeting_time) in class_section.assigned_meeting_time_indices and
                    meeting_times.index(meeting_time) < len(meeting_times)):
                model += pulp.lpSum(extra_timeslots[class_section.sec_name, meeting_time['days'], meeting_time['start_time']] +
                                    class_timeslots.get((class_section.sec_name, meeting_time['days'], meeting_time['start_time']), 0)
                                    for cs in class_sections if cs.min_credit == '3') <= 1

    # Solve the optimization problem
    model.solve()

    # Interpret the solution
    # (You can add code here to extract and print the schedule)




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



import pandas as pd

def process_uploaded_data(uploaded_file_data):
    try:
        # Create a DataFrame from the uploaded data
        df = pd.read_csv(StringIO(uploaded_file_data))

        # Define the columns to keep
        columns_to_keep = [
            'sec name','title', 'min Credit','sec Cap', 'room',
            'bldg', 'week Days', 'CSM start', 'CSM end','faculty1','Restrictions','Blocked Time Slots'
        ]

        # Check if all required columns exist in the DataFrame
        missing_columns = set(columns_to_keep) - set(df.columns)
        if missing_columns:
            raise ValueError(f"Columns not found: {', '.join(missing_columns)}")

        # Select the desired columns
        filtered_df = df[columns_to_keep]

        # Convert the filtered DataFrame to a list of dictionaries
        class_sections_data = filtered_df.to_dict(orient='records')

        return class_sections_data

    except Exception as e:
        # Handle any exceptions that may occur during parsing
        print(f"Error processing CSV data: {str(e)}")
        return None




@app.route('/upload', methods=['GET', 'POST'])
def upload():
    uploaded_file_data = None
    class_sections = None
    file_format = None  # Initialize the format parameter

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

    return render_template('display.html', class_sections = class_sections, your_meeting_time_data=create_meeting_times())


@app.route('/load-schedule', methods=['GET'])
def load_schedule():
    # Read the CSV file and parse it into a list of dictionaries
    csv_filename = 'your_schedule.csv'  # Adjust the filename
    schedule_data = []

    with open(csv_filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            schedule_data.append(row)

    # Send the parsed data as JSON
    return jsonify(schedule_data)


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
