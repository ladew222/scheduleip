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
            'days': 'M',
            'start_time': '8:00AM',
            'end_time': '8:55AM',
        },
        {
            'days': 'M',
            'start_time': '9:05AM',
            'end_time': '10:00AM',
        },
        {
            'days': 'M',
            'start_time': '10:10AM',
            'end_time': '11:05AM',
        },
        {
            'days': 'M',
            'start_time': '11:15AM',
            'end_time': '12:10PM',
        },
        {
            'days': 'M',
            'start_time': '12:20PM',
            'end_time': '1:15PM',
        },
        {
            'days': 'M',
            'start_time': '1:25PM',
            'end_time': '2:20PM',
        },
        {
            'days': 'M',
            'start_time': '2:30PM',
            'end_time': '3:25PM',
        },
        {
            'days': 'M',
            'start_time': '3:35PM',
            'end_time': '4:30PM',
        },
        {
            'days': 'W',
            'start_time': '8:00AM',
            'end_time': '8:55AM',
        },
        {
            'days': 'W',
            'start_time': '9:05AM',
            'end_time': '10:00AM',
        },
        {
            'days': 'W',
            'start_time': '10:10AM',
            'end_time': '11:05AM',
        },
        {
            'days': 'W',
            'start_time': '11:15AM',
            'end_time': '12:10PM',
        },
        {
            'days': 'W',
            'start_time': '12:20PM',
            'end_time': '1:15PM',
        },
        {
            'days': 'W',
            'start_time': '1:25PM',
            'end_time': '2:20PM',
        },
        {
            'days': 'W',
            'start_time': '2:30PM',
            'end_time': '3:25PM',
        },
        {
            'days': 'W',
            'start_time': '3:35PM',
            'end_time': '4:30PM',
        },
        {
            'days': 'F',
            'start_time': '8:00AM',
            'end_time': '8:55AM',
        },
        {
            'days': 'F',
            'start_time': '9:05AM',
            'end_time': '10:00AM',
        },
        {
            'days': 'F',
            'start_time': '10:10AM',
            'end_time': '11:05AM',
        },
        {
            'days': 'F',
            'start_time': '11:15AM',
            'end_time': '12:10PM',
        },
        {
            'days': 'F',
            'start_time': '12:20PM',
            'end_time': '1:15PM',
        },
        {
            'days': 'F',
            'start_time': '1:25PM',
            'end_time': '2:20PM',
        },
        {
            'days': 'F',
            'start_time': '2:30PM',
            'end_time': '3:25PM',
        },
        {
            'days': 'F',
            'start_time': '3:35PM',
            'end_time': '4:30PM',
        },
        {
            'days': 'Tu',
            'start_time': '8:00AM',
            'end_time': '9:20AM',
        },
        {
            'days': 'Tu',
            'start_time': '9:30AM',
            'end_time': '10:50AM',
        },
        {
            'days': 'Tu',
            'start_time': '11:00AM',
            'end_time': '12:20PM',
        },
        {
            'days': 'Tu',
            'start_time': '12:30PM',
            'end_time': '1:50PM',
        },
        {
            'days': 'Tu',
            'start_time': '2:00PM',
            'end_time': '3:20PM',
        },
        {
            'days': 'Tu',
            'start_time': '3:30PM',
            'end_time': '4:50PM',
        },
        {
            'days': 'Th',
            'start_time': '8:00AM',
            'end_time': '9:20AM',
        },
        {
            'days': 'Th',
            'start_time': '9:30AM',
            'end_time': '10:50AM',
        },
        {
            'days': 'Th',
            'start_time': '11:00AM',
            'end_time': '12:20PM',
        },
        {
            'days': 'Th',
            'start_time': '12:30PM',
            'end_time': '1:50PM',
        },
        {
            'days': 'Th',
            'start_time': '2:00PM',
            'end_time': '3:20PM',
        },
        {
            'days': 'Th',
            'start_time': '3:30PM',
            'end_time': '4:50PM',
        },
    ]

    return your_meeting_time_data

    




    
class ClassSection:
    def __init__(self, sec_name, title, min_credit, sec_cap, room, bldg, week_days, csm_start, csm_end, faculty1, holdValue=None, restrictions=None, blocked_time_slots=None, assigned_meeting_time_indices=None):
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
        self.holdValue = holdValue
        self.hours = min_credit
        

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

    def to_dictionary(self):
        # Convert the attributes of the class instance to a dictionary
        return {
            'sec_name': self.sec_name,
            'title': self.title,
            'min_credit': self.min_credit,
            'sec_cap': self.sec_cap,
            'room': self.room,
            'bldg': self.bldg,
            'week_days': self.week_days,
            'csm_start': self.csm_start,
            'csm_end': self.csm_end,
            'faculty1': self.faculty1,
            'holdValue': self.holdValue,
            'avoid_classes': self.avoid_classes,
            'restrictions': self.unwanted_timeslots,
            'hours': self.hours,
            'blocked_time_slots': self.blocked_time_slots
        }
        
    def copy(self):
        return ClassSection(
            sec_name=self.sec_name,
            title=self.title,
            min_credit=self.min_credit,
            sec_cap=self.sec_cap,
            room=self.room,
            bldg=self.bldg,
            week_days=self.week_days,
            csm_start=self.csm_start,
            csm_end=self.csm_end,
            faculty1=self.faculty1,
            holdValue=self.holdValue,
            restrictions=self.avoid_classes.copy() if self.avoid_classes else None,
            assigned_meeting_time_indices=self.assigned_meeting_time_indices.copy() if self.assigned_meeting_time_indices else None
        )




# Function to create ClassSection objects from data
def create_class_sections_from_data(class_sections_data):
    class_sections = []
    seen_sec_names = set()  # Initialize a set to keep track of section names
    valid_days = set(['M', 'W', 'F', 'Tu', 'Th'])  # Set of valid days

    for section_data in class_sections_data:
        sec_name = section_data.get('section', '')
        week_days = section_data.get('weekDays', '').split()

        # Check if the section name is unique and week_days contain any valid days
        if sec_name not in seen_sec_names and any(day in valid_days for day in week_days):
            seen_sec_names.add(sec_name)  # Add the section name to the set

            # Extract other data from 'section_data' and create a ClassSection object
            title = section_data.get('title', '')
            min_credit = section_data.get('minCredit', '')
            sec_cap = section_data.get('secCap', '')
            room = section_data.get('room', '')
            bldg = section_data.get('bldg', '')
            csm_start = section_data.get('csmStart', '')
            csm_end = section_data.get('csmEnd', '')
            faculty1 = section_data.get('faculty1', '')
            holdValue = section_data.get('hold', '')
            restrictions = section_data.get('restrictions', '')
            blocked_time_slots = section_data.get('blockedTimeSlots', '')

            # Reconstruct week_days as a string
            week_days_str = ' '.join(week_days)
            
            class_section = ClassSection(sec_name, title, min_credit, sec_cap, room, bldg, week_days_str, csm_start, csm_end, faculty1, holdValue, restrictions, blocked_time_slots)
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





def optimize_schedule(class_sections, meeting_times, class_penalty, move_penalty, blocked_slot_penalty, hold_penalty,
                      enable_unique_class_constraint=True, 
                      enable_instructor_constraint=True, 
                      enable_avoid_classes_penalty=True,
                      enable_avoid_timeslot_penalty=True, 
                      enable_move_class_penalty=False, 
                      enable_linked_sections_penalty=False,
                      enable_single_class_instance_constraint=True):
    
    # ... (initial setup, linked_sections handling remains the same)

    instructors = set(cls.faculty1 for cls in class_sections)

    # Create time slots for each day and start time
    timeslots = [f"{day} - {mt['start_time']}" for mt in meeting_times for day in ['M', 'Tu', 'W', 'Th', 'F']]  # Adjust days as needed
    
    prob = pulp.LpProblem("Class_Scheduling", pulp.LpMinimize)
    
    # Create binary variables: x_ij = 1 if class i is in timeslot j on day d
    x = pulp.LpVariable.dicts("x", 
                            ((cls.sec_name, tsl) for cls in class_sections for tsl in timeslots),
                            cat='Binary')

    # Objective function: Minimize the total number of scheduled classes
    prob += pulp.lpSum(x[cls.sec_name, tsl] for cls in class_sections for tsl in timeslots)


    # Constraint: Only one instance of a class can be scheduled per timeslot
    if enable_single_class_instance_constraint:
        constraint_counter = 0
        sec_names = set(cls.sec_name for cls in class_sections)  # Extract unique class names
        for class_name in sec_names:
            for tsl in timeslots:
                constraint_counter += 1
                sections_of_class = [cls for cls in class_sections if cls.sec_name == class_name]
                constraint_name = f"SingleClassInstancePerTimeslot_{class_name}_{tsl}_{constraint_counter}"
                prob += pulp.lpSum(x[cls.sec_name, tsl] for cls in sections_of_class) <= 1, constraint_name

    # Modified Constraint: Each class must take exactly one timeslot per credit hour
    # Additional Rule: Classes over 3 credits schedule Tu Th for 3 credits or M W F for 3 credits
    # Modified Constraint for 3-Credit Classes
    if enable_unique_class_constraint:
        for cls in class_sections:
            if int(cls.min_credit) >= 3:
                # Separate constraints for M W F and Tu Th scheduling
                mwf_timeslots = [tsl for tsl in timeslots if tsl.split(' - ')[0] in ['M', 'W', 'F']]
                tu_th_timeslots = [tsl for tsl in timeslots if tsl.split(' - ')[0] in ['Tu', 'Th']]

                # Ensure same time scheduling for M W F or Tu Th
                for start_time in set(mt['start_time'] for mt in meeting_times):
                    prob += pulp.lpSum(x[cls.sec_name, tsl] for tsl in mwf_timeslots if start_time in tsl) <= 1, f"Class_{cls.sec_name}_MWF_SameTime_{start_time}"
                    prob += pulp.lpSum(x[cls.sec_name, tsl] for tsl in tu_th_timeslots if start_time in tsl) <= 1, f"Class_{cls.sec_name}_TuTh_SameTime_{start_time}"

                # Constraint for remaining credits if any
                if int(cls.min_credit) > 3:
                    extra_credits = int(cls.min_credit) - 3
                    prob += pulp.lpSum(x[cls.sec_name, tsl] for tsl in timeslots) == 3 + extra_credits, f"TotalCreditsConstraint_{cls.sec_name}"
            else:
                # One credit per timeslot for other classes
                for day in cls.week_days.split():
                    prob += pulp.lpSum(x[cls.sec_name, f"{day} - {mt['start_time']}"] for mt in meeting_times if day in mt['days']) == 1, f"OneClassOneSlotConstraint_{cls.sec_name}_{day}"


    # Constraint: An instructor can only teach one class per timeslot
    if enable_instructor_constraint:
        global_constraint_id = 0  # Global counter for constraint names
        for tsl in timeslots:
            for instructor in instructors:
                global_constraint_id += 1
                for cls in class_sections:
                    if cls.faculty1 == instructor:
                        constraint_name = f"OneClassPerInstructorPerSlot_{instructor}_{cls.sec_name}_{tsl}_{global_constraint_id}"
                        prob += x[cls.sec_name, tsl] <= 1, constraint_name


    # Penalty for avoiding classes in the same timeslot
    if enable_avoid_classes_penalty:
        for cls in class_sections:
            for tsl in timeslots:
                for other_cls_name in cls.avoid_classes:
                    prob += x[cls.sec_name, tsl] + x.get(other_cls_name, tsl, 0) <= 1, f"AvoidClassesPenalty_{cls.sec_name}_{other_cls_name}_{tsl}"

    # Penalty for avoiding timeslots
    if enable_avoid_timeslot_penalty:
        for cls in class_sections:
            for tsl in timeslots:
                if tsl in cls.unwanted_timeslots:
                    prob += x[cls.sec_name, tsl] == 0, f"BlockedTimeSlotPenalty_{cls.sec_name}_{tsl}"

    # Penalty for moving a class outside its known timeslot when holdValue is 1
    if enable_move_class_penalty:
        for cls in class_sections:
            if cls.holdValue == 1:
                for tsl in timeslots:
                    if tsl not in cls.assigned_meeting_times:
                        prob += x[cls.sec_name, tsl] == 0, f"MoveClassPenalty_{cls.sec_name}_{tsl}"

    linked_sections = []
    # Calculate the penalty for keeping linked sections together
    if enable_linked_sections_penalty:
        for cls_A, cls_B in linked_sections:
            for tsl in timeslots:
                prob += x[cls_A.sec_name, tsl] + x[cls_B.sec_name, tsl] <= 1, f"LinkConstraint_{cls_A.sec_name}_{cls_B.sec_name}_{tsl}"

    # Solve the problem
    prob.solve()
    
    for var in x:
        if pulp.value(x[var]) == 1:
            print(f"{var} is scheduled.")

    # Output the results and create a list to store the scheduled class sections
    scheduled_sections = []
    for cls in class_sections:
        for tsl in timeslots:
            if pulp.value(x[cls.sec_name, tsl]) == 1:
                scheduled_sections.append({
                    'section_name': cls.sec_name,
                    'timeslot': tsl,
                })

    # Create a dictionary to store optimization results
    optimization_results = {
        'message': 'Optimization complete',
        'scheduled_sections': scheduled_sections,
        'status': 'Success' if prob.status == pulp.LpStatusOptimal else 'Failure'
    }

    # Return the optimization results
    return optimization_results









# Define the '/optimize' route to handle optimization requests
@app.route('/optimize', methods=['POST'])
def optimize():
    # Get the JSON data from the request
    data = request.get_json()

    # Extract class section data from the 'data' variable
    class_sections_data = data.get('classData', [])
    
    
    # Extract additional parameters
    class_penalty = data.get('classPenalty', 0)
    move_penalty = data.get('movePenalty', 0)
    blocked_slot_penalty = data.get('blockedSlotPenalty', 0)
    hold_penalty = data.get('holdPenalty', 0)

    
    # Convert the class section data to ClassSection objects
    class_sections = create_class_sections_from_data(class_sections_data)

    # Adjust the class_sections list to create an extra 1-credit class with "_ex" appended to the section name
    adjusted_class_sections = []
    for class_section in class_sections:
        adjusted_class_sections.append(class_section)
        if int(class_section.min_credit) > 3:
            # Create an extra 1-credit class with "_ex" appended to the section name
            extra_class_section = class_section.copy()
            extra_class_section.sec_name += "_ex"
            extra_class_section.min_credit = '1'  # Set credit to 1
            adjusted_class_sections.append(extra_class_section)


    # Create a MeetingTimes object
    meeting_times = create_meeting_times()

    # Optimize the schedule based on the received data
    optimized_results = optimize_schedule(adjusted_class_sections, meeting_times, class_penalty, move_penalty, blocked_slot_penalty, hold_penalty)
    optimized_class_sections = optimized_results.get('scheduled_sections', [])

    if optimized_class_sections is not None:
        # Prepare the optimization results as a dictionary
        optimization_results = {
            'message': 'Optimization complete',
            'results': [optimized_class_sections],
        }

        # Return the results as JSON
        return jsonify(optimization_results)
    else:
        # If no optimal solution is found, return an error response
        error_response = {
            'error': 'No optimal solution found'
        }
        return jsonify(error_response), 400




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
