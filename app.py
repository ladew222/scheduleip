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
    
    for section_data in class_sections_data:
        # Extract data from 'section_data' and create a ClassSection object
        sec_name = section_data.get('section', '')  # Updated to match the new column name
        if sec_name in seen_sec_names:
            # If the section name is already in the set, skip this iteration
            continue
        seen_sec_names.add(sec_name) # Add the section name to the set
        title = section_data.get('title', '')
        min_credit = section_data.get('minCredit', '')  # Updated to match the new column name
        sec_cap = section_data.get('secCap', '')  # Updated to match the new column name
        room = section_data.get('room', '')
        bldg = section_data.get('bldg', '')
        week_days = section_data.get('weekDays', '')  # Updated to match the new column name
        csm_start = section_data.get('csmStart', '')  # Updated to match the new column name
        csm_end = section_data.get('csmEnd', '')  # Updated to match the new column name
        faculty1 = section_data.get('faculty1', '')  # Updated to match the new column name
        holdValue = section_data.get('hold', '')  # Updated to match the new column name
        restrictions = section_data.get('restrictions', '')
        blocked_time_slots = section_data.get('blockedTimeSlots', '')  # Updated to match the new column name
        class_section = ClassSection(sec_name, title, min_credit, sec_cap, room, bldg, week_days, csm_start, csm_end, faculty1, holdValue ,restrictions,blocked_time_slots)
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





def optimize_schedule(class_sections, meeting_times, class_penalty, move_penalty, blocked_slot_penalty, hold_penalty):
    #So, in simple terms, the optimization process examines each class, 
    # takes into account its properties and constraints, and tries to find 
    # the best schedule by adjusting the schedule to minimize the total number
    # of scheduled classes while satisfying all the constraints and considering 
    # any penalties or incentives you've defined.
    #
    #
    
    # Create a LP problem instance
    prob = pulp.LpProblem("Class_Scheduling", pulp.LpMinimize)

    # Create binary variables: x_ij = 1 if class i is in timeslot j
    x = pulp.LpVariable.dicts("x",
                              ((cls.sec_name, mt['days'], mt['start_time']) for cls in class_sections for mt in meeting_times),
                              cat='Binary')

    # Objective function: Minimize the total number of scheduled classes
    prob += pulp.lpSum(x[cls.sec_name, mt['days'], mt['start_time']] for cls in class_sections for mt in meeting_times)

    # Constraint: Each class must take exactly one timeslot per hour
    for cls in class_sections:
        num_credits = cls.hours  # Assuming 'hours' represents the number of credit hours
        total_credits = pulp.lpSum(x[cls.sec_name, mt['days'], mt['start_time']] for mt in meeting_times)
        
        if 'MWF' in cls.week_days:
            prob += total_credits == num_credits, f"OneClassOneSlotPerCreditConstraint_{cls.sec_name}"
        elif 'TTh' in cls.week_days:
            prob += total_credits == 1.5 * num_credits, f"OneClassOneSlotPerCreditConstraint_{cls.sec_name}"
        else:
            # Handle other cases (if necessary)
            pass


    # Constraint: An instructor can only teach one class per timeslot
    instructors = set(cls.faculty1 for cls in class_sections)
    for mt in meeting_times:
        for instructor in instructors:
            prob += pulp.lpSum(x[cls.sec_name, mt['days'], mt['start_time']] for cls in class_sections if cls.faculty1 == instructor) <= 1, f"OneClassPerInstructorPerSlot_{instructor}_{mt['days']}_{mt['start_time']}"

    # Penalty for avoiding classes in the same timeslot
    for cls in class_sections:
        for mt in meeting_times:
            for other_cls_name in cls.avoid_classes:
                prob += x[cls.sec_name, mt['days'], mt['start_time']] + x[other_cls_name, mt['days'], mt['start_time']] <= 1, f"AvoidClassesPenalty_{cls.sec_name}_{other_cls_name}_{mt['days']}_{mt['start_time']}"

    # Penalty for avoiding timeslots
    for cls in class_sections:
        for mt in meeting_times:
            if mt['days'] + ' ' + mt['start_time'] in cls.unwanted_timeslots:
                prob += x[cls.sec_name, mt['days'], mt['start_time']] == 0, f"BlockedTimeSlotPenalty_{cls.sec_name}_{mt['days']}_{mt['start_time']}"

    # Penalty for moving a class outside its known timeslot when holdValue is 1
    for cls in class_sections:
        if cls.holdValue == 1:
            for mt in meeting_times:
                if mt['days'] + ' ' + mt['start_time'] not in cls.assigned_meeting_times:
                    prob += x[cls.sec_name, mt['days'], mt['start_time']] == 0, f"MoveClassPenalty_{cls.sec_name}_{mt['days']}_{mt['start_time']}"

    # Separate 3-credit classes into MWF and TTh categories based on the number of congruent days
    credit_3_sections_MWF = []
    credit_3_sections_TTh = []

    # Assuming class_sections is a list of class sections with credit values
    credit_3_sections = [cls for cls in class_sections if int(cls.min_credit) >= 3]

    for cls in credit_3_sections:
        congruent_days = pulp.lpSum(x[cls.sec_name, mt['days'], mt['start_time']] for mt in meeting_times)
        if congruent_days == 3:
            credit_3_sections_MWF.append(cls)
        elif congruent_days == 2:
            credit_3_sections_TTh.append(cls)

    # Create constraints for MWF classes
    for cls in credit_3_sections_MWF:
        prob += pulp.lpSum(x[cls.sec_name, mt['days'], mt['start_time']] for mt in meeting_times) == 3, f"CongruentDaysConstraint_MWF_{cls.sec_name}"

    # Create constraints for TTh classes
    for cls in credit_3_sections_TTh:
        prob += pulp.lpSum(x[cls.sec_name, mt['days'], mt['start_time']] for mt in meeting_times) == 2, f"CongruentDaysConstraint_TTh_{cls.sec_name}"

    # Ensure that timeslots for 3-credit classes are consecutive on MWF
    for cls in credit_3_sections_MWF:
        # Collect the timeslots for the current class
        timeslots = [(mt['days'], mt['start_time']) for mt in meeting_times if pulp.value(x[cls.sec_name, mt['days'], mt['start_time']]) == 1]

        # Ensure that all timeslots have the same start time
        start_time_set = set(start_time for _, start_time in timeslots)

        if len(start_time_set) > 1:
            # Add a constraint to ensure all timeslots have the same start time
            prob += pulp.lpSum(x[cls.sec_name, day, start_time] for day, start_time in timeslots) == len(timeslots), f"ConsecutiveTimeSlots_MWF_{cls.sec_name}"

    # Ensure that timeslots for 3-credit classes are consecutive on TTh
    for cls in credit_3_sections_TTh:
        # Collect the timeslots for the current class
        timeslots = [(mt['days'], mt['start_time']) for mt in meeting_times if pulp.value(x[cls.sec_name, mt['days'], mt['start_time']]) == 1]

        # Ensure that all timeslots have the same start time
        start_time_set = set(start_time for _, start_time in timeslots)

        if len(start_time_set) > 1:
            # Add a constraint to ensure all timeslots have the same start time
            prob += pulp.lpSum(x[cls.sec_name, day, start_time] for day, start_time in timeslots) == len(timeslots), f"ConsecutiveTimeSlots_TTh_{cls.sec_name}"

    # Solve the problem
    prob.solve()
    
    # Check the status of the solver
    if prob.status == pulp.LpStatusOptimal:
        print("Optimal solution found.")
        # Retrieve the values of decision variables (x)
        for var in prob.variables():
            if var.varValue == 1:
                print(f"{var.name}: {var.varValue}")
    else:
        print("Solver did not find an optimal solution.")

    # Create a list to store the scheduled class sections
    # Initialize a list to store scheduled sections
    scheduled_sections = []

    # Output the results and store scheduled sections
    for cls in class_sections:
        for mt in meeting_times:
            if pulp.value(x[cls.sec_name, mt['days'], mt['start_time']]) == 1:
                scheduled_sections.append({
                    'section_name': cls.sec_name,
                    'days': mt['days'],
                    'start_time': mt['start_time'],
                })

    # Create a dictionary to store optimization results
    optimization_results = {
        'message': 'Optimization complete',
        'scheduled_sections': scheduled_sections,
    }

    # Check if optimization was successful
    if prob.status == pulp.LpStatusOptimal:
        optimization_results['status'] = 'Success'
    else:
        optimization_results['status'] = 'Optimization failed'

    # Return the optimization_results dictionary
    return jsonify(optimization_results)





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
    optimized_class_sections = optimize_schedule(adjusted_class_sections, meeting_times, class_penalty, move_penalty, blocked_slot_penalty, hold_penalty)


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
