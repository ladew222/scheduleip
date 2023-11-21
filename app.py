from flask import Flask, render_template, request, redirect, url_for, jsonify
import pulp
import re
import csv
import json
from io import StringIO
from urllib.parse import urlencode
import pandas as pd
from io import StringIO
from datetime import datetime, timedelta
import calendar
app = Flask(__name__)
import hashlib

def string_to_color(s):
    # Use a hash function to convert the string to a hexadecimal color code
    hash_object = hashlib.md5(s.encode())
    return '#' + hash_object.hexdigest()[:6]


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
    

def create_full_meeting_times():
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
        for day in ["M W F", "T Th"]:
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


def optimize_remaining_classes(class_sections, remaining_timeslots,used_timeslots, class_penalty, move_penalty, blocked_slot_penalty, hold_penalty):
    # Create a new list of timeslots based on the full meeting times
    full_meeting_times = create_full_meeting_times()
    full_timeslots = [f"{mt['days']} - {mt['start_time']}" for mt in full_meeting_times]

    # Transform the used_timeslots to match the daily pattern
    transformed_used_timeslots = set()
    for used_tslot in used_timeslots:
        days, time = used_tslot.split(' - ')
        for day in days.split():
            transformed_used_timeslots.add(f"{day} - {time}")
            
    # Filter out the timeslots that are already used
    available_timeslots = [ts for ts in full_timeslots if ts not in used_timeslots]

    # Create a LP problem instance
    prob = pulp.LpProblem("Class_Scheduling_Remaining", pulp.LpMinimize)

    # Create binary variables: x_ij = 1 if class i is in timeslot j
    x = pulp.LpVariable.dicts("x", 
                              ((cls.sec_name, tsl) for cls in class_sections for tsl in available_timeslots),
                              cat='Binary')

    # Objective function: Minimize the total number of scheduled classes
    prob += pulp.lpSum(x[cls.sec_name, tsl] for cls in class_sections for tsl in available_timeslots)

    # Constraint: Each class must be scheduled once
    for cls in class_sections:
        prob += pulp.lpSum(x[cls.sec_name, tsl] for tsl in available_timeslots) == 1, f"OneClassOneSlot_{cls.sec_name}"

    # Constraint: An instructor can only teach one class per timeslot
    instructors = set(cls.faculty1 for cls in class_sections)
    for instructor in instructors:
        for tsl in available_timeslots:
            prob += pulp.lpSum(x[cls.sec_name, tsl] for cls in class_sections if cls.faculty1 == instructor) <= 1, f"OneInstructorOneSlot_{instructor}_{tsl}"

    # Constraint: Avoid class overlaps
    for tsl in available_timeslots:
        prob += pulp.lpSum(x[cls.sec_name, tsl] for cls in class_sections) <= 1, f"AvoidOverlap_{tsl}"

    # Constraint: Penalize classes that intersect and have one of each other in avoid_classes
    for cls in class_sections:
        for other_cls in class_sections:
            if other_cls.sec_name in cls.avoid_classes:
                for tsl in available_timeslots:
                    prob += x[cls.sec_name, tsl] + x[other_cls.sec_name, tsl] <= 1, f"AvoidClasses_{cls.sec_name}_{other_cls.sec_name}_{tsl}"

    # Constraint: Avoid unwanted timeslots
    for cls in class_sections:
        # Transform unwanted timeslots for this class
        transformed_unwanted_timeslots = set()
        for tslot in cls.unwanted_timeslots:
            days, time = tslot.split(' - ')
            for day in days.split():
                transformed_unwanted_timeslots.add(f"{day} - {time}")

        # Apply constraint for each unwanted timeslot
        for tsl in transformed_unwanted_timeslots:
            if tsl in available_timeslots:
                prob += x[cls.sec_name, tsl] == 0, f"AvoidUnwanted_{cls.sec_name}_{tsl}"


    # Solve the problem
    prob.solve()

    # Create a list to store the scheduled class sections
    scheduled_sections = []

    # Check the values of the decision variables and create the schedule
    for cls in class_sections:
        for tsl in remaining_timeslots:
            if pulp.value(x[cls.sec_name, tsl]) == 1:
                scheduled_sections.append({
                    'section_name': cls.sec_name,
                    'timeslot': tsl,
                })

    # Create a dictionary to store optimization results
    optimization_results = {
        'message': 'Optimization for remaining classes complete',
        'scheduled_sections': scheduled_sections,
        'status': 'Success' if prob.status == pulp.LpStatusOptimal else 'Failure'
    }

    return optimization_results


def optimize_schedule(class_sections, meeting_times, class_penalty, move_penalty, blocked_slot_penalty, hold_penalty):
    
        
    
    linked_sections = []

    for class_section in class_sections:
        sec_name = class_section.sec_name

        # Check if the section name ends with "_ex"
        if sec_name.endswith("_ex"):
            # Extract the base section name (without "_ex")
            base_sec_name = sec_name[:-3]

            # Find the corresponding "_ex" section, if it exists
            corresponding_ex_section = next((cls for cls in class_sections if cls.sec_name == base_sec_name), None)

            if corresponding_ex_section:
                linked_sections.append((corresponding_ex_section, class_section))
        
    
    
    instructors = set(cls.faculty1 for cls in class_sections)
    # Create a LP problem instance
    timeslots = [f"{mt['days']} - {mt['start_time']}" for mt in meeting_times]
    
    # Create a LP problem instance
    prob = pulp.LpProblem("Class_Scheduling", pulp.LpMinimize) 
    
    
    # Create binary variables: x_ij = 1 if class i is in timeslot j 
    x = pulp.LpVariable.dicts("x", 
                            ((cls.sec_name, tsl) for cls in class_sections for tsl in timeslots),
                            cat='Binary')

    # Objective function: Minimize the total number of scheduled classes
    prob += pulp.lpSum(x[cls.sec_name,tsl] for cls in class_sections for tsl in timeslots)
    
    
     # Constraint: Each class must take exactly one timeslot
    for cls in class_sections:
        unique_constraint_name = f"OneClassOneSlotConstraint_{cls.sec_name}"  # Generate a unique constraint name
        prob += pulp.lpSum(x[cls.sec_name, tsl] for tsl in timeslots if (cls.sec_name, tsl) in x) == 1, unique_constraint_name


    # Create a set of unique rooms
    rooms = set(cls.room for cls in class_sections if cls.room.strip())

    # Constraint: No two classes can be in the same room at the same timeslot
    for tsl in timeslots:
        for room in rooms:
            prob += pulp.lpSum(x[cls.sec_name, tsl] for cls in class_sections if cls.room == room and (cls.sec_name, tsl) in x) <= 1, f"OneClassPerRoomPerSlot_{room}_{tsl}"

    # Assuming 'instructors' is a list of all unique instructors
    instructors = set(cls.faculty1 for cls in class_sections)


    # Constraint: An instructor can only teach one class per timeslot
    for tsl in timeslots:
        for instructor in instructors:
            prob += pulp.lpSum(x[cls.sec_name, tsl] for cls in class_sections if cls.faculty1 == instructor and (cls.sec_name, tsl) in x) <= 1, f"OneClassPerInstructorPerSlot_{instructor}_{tsl}"
            
   # Penalty for avoiding classes in the same timeslot
    penalty = class_penalty  # Adjust the penalty weight as needed
    constraint_counter = 0  # Initialize a countexr for constraint names
    for cls in class_sections:
        for tsl in timeslots:
            for other_cls_name in cls.avoid_classes:
                if (other_cls_name, tsl) in x:
                    constraint_counter += 1
                    constraint_name = f"AvoidClassesPenalty_{cls.sec_name}_{tsl}_{constraint_counter}"
                    prob += x[cls.sec_name, tsl] + x[other_cls_name, tsl] <= 1, constraint_name


    # Penalty for avoiding timeslots
    constraint_counter = 0  # Initialize a counter for constraint names
    #hold_penalty = hold_penalty # Adjust the penalty weight as needed
    
    # Penalty for moving a class outside its known timeslot when holdValue is 1
    for cls in class_sections:
        if cls.holdValue == 1:
            for tsl in timeslots:
                if (cls.sec_name, tsl) not in x and int(tsl.split("_")[-1]) not in cls.assigned_meeting_time_indices:
                    constraint_counter += hold_penalty
                    constraint_name = f"MoveClassPenalty_{cls.sec_name}_{tsl}_{constraint_counter}"
                    prob += x[cls.sec_name, tsl] == 0, constraint_name


     # Additional penalty for blocked_time_slots
    blocked_slot_penalty = blocked_slot_penalty  # Adjust the penalty weight as needed
    for cls in class_sections:
        for tsl in timeslots:
            if tsl in cls.unwanted_timeslots:
                prob += x[cls.sec_name, tsl] == 0, f"BlockedTimeSlotPenalty_{cls.sec_name}_{tsl}"

    
    # Calculate the penalty for keeping linked sections together
    linked_sections_penalty = 0  # Initialize the penalty
    for cls_A, cls_B in linked_sections:
        for tsl in timeslots:
            # Calculate the absolute difference in indexes of cls_A and cls_B
            index_diff = abs(class_sections.index(cls_A) - class_sections.index(cls_B)) * move_penalty
            index_diff = int(index_diff)
            # Add the penalty to the objective function
            prob += x[cls_A.sec_name, tsl] + x[cls_B.sec_name, tsl] <= 1 + index_diff, f"LinkConstraint_{cls_A.sec_name}_{cls_B.sec_name}_{tsl}"

            # Update the linked_sections_penalty based on the index_diff
            linked_sections_penalty += index_diff * x[cls_A.sec_name, tsl] + index_diff * x[cls_B.sec_name, tsl]

        
    # Solve the problem
    prob.solve()


    # Create a list to store the scheduled class sections
    scheduled_sections = []

    # Output the results and store scheduled sections
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
    }

    # Check if optimization was successful
    if prob.status == pulp.LpStatusOptimal:
        optimization_results['status'] = 'Success'
    else:
        optimization_results['status'] = 'Optimization failed'

    # Return the optimization results
    return optimization_results


def get_weekday_date(weekday):
    """
    Get the date of the next occurrence of the given weekday.
    """
    today = datetime.today()
    today_weekday = today.weekday()  # Monday is 0 and Sunday is 6
    days_ahead = (weekday - today_weekday) % 7
    return today + timedelta(days=days_ahead)

def process_calendar_data(three_credit_results, remaining_class_results):
    calendar_data = []
    color_cache ={ }

    # Process three-credit classes
    for result in three_credit_results['scheduled_sections']:
        section_name = result['section_name']
        timeslot = result['timeslot']
        days, start_time = timeslot.split(' - ')
        start_time_obj = datetime.strptime(start_time, '%I:%M%p')

        for day in days.split():
            weekday_map = {'M': 0, 'Tu': 1, 'W': 2, 'Th': 3, 'F': 4}
            class_date = get_weekday_date(weekday_map[day])
            start_datetime = datetime.combine(class_date, start_time_obj.time())
            duration = timedelta(hours=1)  # Three-credit classes last for 1 hour
            end_datetime = start_datetime + duration
            # Extract the course prefix
            course_prefix = section_name.split('-')[0]
            # Assign color based on the course prefix
            if course_prefix not in color_cache:
                color_cache[course_prefix] = str(string_to_color(course_prefix))
            color = color_cache[course_prefix]


            calendar_event = {
                'section_name': section_name,
                'start': start_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
                'end': end_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
                'color': color
            }
            calendar_data.append(calendar_event)

    # Process remaining one-credit classes
    for result in remaining_class_results['scheduled_sections']:
        section_name = result['section_name']
        timeslot = result['timeslot']
        day, start_time = timeslot.split(' - ')
        start_time_obj = datetime.strptime(start_time, '%I:%M%p')
        
        weekday_map = {'M': 0, 'Tu': 1, 'W': 2, 'Th': 3, 'F': 4}
        class_date = get_weekday_date(weekday_map[day])
        start_datetime = datetime.combine(class_date, start_time_obj.time())
        duration = timedelta(hours=1, minutes=30)  # One-credit classes last for 1.5 hours
        end_datetime = start_datetime + duration
        if course_prefix not in color_cache:
            color_cache[course_prefix] = str(string_to_color(course_prefix))
        color = color_cache[course_prefix]


        calendar_event = {
            'section_name': section_name,
            'start': start_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
            'end': end_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
            'color': color
        }
        calendar_data.append(calendar_event)

    return calendar_data



@app.route('/optimize', methods=['POST'])
def optimize():
    # Get the JSON data from the request
    data = request.get_json()

    # Extract class section data and additional parameters
    class_sections_data = data.get('classData', [])
    class_penalty = data.get('classPenalty', 0)
    move_penalty = data.get('movePenalty', 0)
    blocked_slot_penalty = data.get('blockedSlotPenalty', 0)
    hold_penalty = data.get('holdPenalty', 0)

    # Convert the class section data to ClassSection objects
    class_sections = create_class_sections_from_data(class_sections_data)

    # Split 4-credit classes and prepare for 3-credit optimization
    three_credit_sections = []
    remaining_class_sections = []
    for class_section in class_sections:
        if int(class_section.min_credit) == 4:
            # Split into two sections: one with 3 credits, another with 1 credit
            three_credit_section = class_section.copy()
            three_credit_section.min_credit = '3'
            one_credit_section = class_section.copy()
            one_credit_section.min_credit = '1'
            one_credit_section.sec_name += "_one_credit"
            three_credit_sections.append(three_credit_section)
            remaining_class_sections.append(one_credit_section)
        elif int(class_section.min_credit) == 3:
            three_credit_sections.append(class_section)
        else:
            remaining_class_sections.append(class_section)

    # Create a MeetingTimes object
    meeting_times = create_meeting_times()

    # Optimize the schedule for 3-credit classes
    three_credit_results = optimize_schedule(three_credit_sections, meeting_times, class_penalty, move_penalty, blocked_slot_penalty, hold_penalty)

    # Extract used timeslots from the results
    used_timeslots = set()
    for section in three_credit_results['scheduled_sections']:
        used_timeslots.add(section['timeslot'])

    # Determine remaining available timeslots
    all_timeslots = [f"{day} - {mt['start_time']}" for mt in create_full_meeting_times() for day in mt['days'].split()]
    remaining_timeslots = [ts for ts in all_timeslots if ts not in used_timeslots]

    # Optimize the schedule for remaining classes
    remaining_class_results = optimize_remaining_classes(remaining_class_sections, remaining_timeslots,used_timeslots, class_penalty, move_penalty, blocked_slot_penalty, hold_penalty)

    calendar_events = process_calendar_data(three_credit_results, remaining_class_results)
    
    # Combine results from both optimizations
    combined_scheduled_sections = three_credit_results['scheduled_sections'] + remaining_class_results['scheduled_sections']

    # Sort the combined list by section name
    combined_scheduled_sections.sort(key=lambda x: x['section_name'])

    # Prepare the combined results dictionary
    combined_results = {
        'scheduled_sections': combined_scheduled_sections,
        'calendar_events': calendar_events,
        'message': 'Success' if (three_credit_results['status'] == 'Success' and remaining_class_results['status'] == 'Success') else 'Partial Success'
    }

    
    # Check if optimization was successful
    if combined_results:
        return jsonify(combined_results)
    else:
        error_response = {
            'error': 'Optimization failed or no classes provided'
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
