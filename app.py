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
import pandas as pd
from deap import base, creator, tools, algorithms
import random
import numpy as np
import random

# Define the problem class
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

global_settings = {}


def string_to_color(s):
    # Use a hash function to convert the string to a hexadecimal color code
    hash_object = hashlib.md5(s.encode())
    return '#' + hash_object.hexdigest()[:6]


import random
from deap import creator

import random

import random

def follows_pattern(timeslot, pattern):
    """Check if a timeslot follows a specific pattern (MWF or TuTh)."""
    days = timeslot.split(' - ')[0]
    if pattern == 'MWF':
        return all(day in days for day in ['M', 'W', 'F'])
    elif pattern == 'TuTh':
        return all(day in days for day in ['Tu', 'Th'])
    return False

def create_individual(combined_expanded_schedule, full_meeting_times, mutation_rate=0.1):
    """
    Create an individual schedule by using the PuLP optimized schedule and 
    introducing variations to some class sections while respecting the MWF/TuTh pattern
    and one section per day requirements.

    Args:
        combined_expanded_schedule (list): List of class sections with PuLP optimized details.
        full_meeting_times (list): List of all available meeting times.
        mutation_rate (float): Probability of mutating a given class section's timeslot.

    Returns:
        An individual schedule for the GA.
    """
    individual = []
    day_assignment = {}  # Dictionary to track day assignments for each course

    for cls in combined_expanded_schedule:
        # Copy class section details
        new_class_section = cls.copy()
        course_identifier = cls['section'].split('_')[0]

        # Randomly decide whether to mutate this class section
        if random.random() < mutation_rate:
            # Filter timeslots based on the pattern and day constraints
            pattern = 'MWF' if follows_pattern(cls['timeslot'], 'MWF') else 'TuTh'
            available_timeslots = [ts for ts in full_meeting_times 
                                   if follows_pattern(f"{ts['days']} - {ts['start_time']}", pattern)
                                   and ts['days'] not in day_assignment.get(course_identifier, set())]

            # If available timeslots are found, choose one randomly
            if available_timeslots:
                chosen_timeslot = random.choice(available_timeslots)
                new_class_section['timeslot'] = f"{chosen_timeslot['days']} - {chosen_timeslot['start_time']}"
                # Update day assignment for the course
                day_assignment.setdefault(course_identifier, set()).update(chosen_timeslot['days'].split())

        # Add the class section to the individual schedule
        individual.append(new_class_section)

    return creator.Individual(individual)





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
    def __init__(self, sec_name, title, minCredit, sec_cap, room, bldg, week_days, csm_start, csm_end, faculty1, holdValue=None, restrictions=None, blocked_time_slots=None, assigned_meeting_time_indices=None):
        self.section = sec_name
        self.title = title
        self.minCredit = minCredit
        self.secCap = sec_cap
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
            'section': self.section,
            'title': self.title,
            'minCredit': self.minCredit,
            'secCap': self.secCap,
            'room': self.room,
            'bldg': self.bldg,
            'week_days': self.week_days,
            'csm_start': self.csm_start,
            'csm_end': self.csm_end,
            'faculty1': self.faculty1,
            'holdValue': self.holdValue,
            'avoid_classes': self.avoid_classes,
            'restrictions': self.unwanted_timeslots,
        }
        
    def copy(self):
        return ClassSection(
            section=self.section,
            title=self.title,
            minCredit=self.minCredit,
            secCap=self.secCap,
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
        minCredit = section_data.get('minCredit', '')  # Updated to match the new column name
        secCap = section_data.get('secCap', '')  # Updated to match the new column name
        room = section_data.get('room', '')
        bldg = section_data.get('bldg', '')
        week_days = section_data.get('weekDays', '').strip() # Updated to match the new column name
        csm_start = section_data.get('csmStart', '')  # Updated to match the new column name
        csm_end = section_data.get('csmEnd', '')  # Updated to match the new column name
        faculty1 = section_data.get('faculty1', '')  # Updated to match the new column name
        holdValue = section_data.get('hold', '')  # Updated to match the new column name
        restrictions = section_data.get('restrictions', '')
        blocked_time_slots = section_data.get('blockedTimeSlots', '')  # Updated to match the new column name
        class_section = ClassSection(sec_name, title, minCredit, secCap, room, bldg, week_days, csm_start, csm_end, faculty1, holdValue ,restrictions,blocked_time_slots)
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


def divide_schedules_by_credit(schedule, credit_threshold=3):
    """
    Divide the schedule into two groups based on credit hours and time patterns.

    Args:
        schedule (list): The list of scheduled classes.
        credit_threshold (int): The threshold for dividing classes by credit.

    Returns:
        tuple: Two lists, one for classes with credits greater than or equal to the threshold, and one for the rest.
    """
    three_credit_classes = []
    remaining_classes = []
    section_groupings = {}

    # Group classes by their base section name
    for class_section in schedule:
        base_section_name = class_section['section_name'].split('_')[0]
        section_groupings.setdefault(base_section_name, []).append(class_section)

    # Process each group to form 3-credit or remaining classes
    for base_section_name, sections in section_groupings.items():
        if any(int(cls['min_credit']) >= credit_threshold for cls in sections):
            # Determine the most common start times for TuTh and MWF patterns
            mwf_times, tuth_times = get_most_common_start_times(sections)

            # Form the 3-credit class pattern
            three_credit_class = form_three_credit_pattern(sections, mwf_times, tuth_times, credit_threshold)

            three_credit_classes.extend(three_credit_class['patterned_classes'])
            remaining_classes.extend(three_credit_class['remaining_classes'])
        else:
            # All sections are less than the credit threshold
            remaining_classes.extend(sections)

    return three_credit_classes, remaining_classes

def get_most_common_start_times(sections):
    mwf_start_times = [cls['timeslot'].split(' - ')[1] for cls in sections if 'M' in cls['timeslot'] and 'W' in cls['timeslot'] and 'F' in cls['timeslot']]
    tuth_start_times = [cls['timeslot'].split(' - ')[1] for cls in sections if 'Tu' in cls['timeslot'] and 'Th' in cls['timeslot']]

    most_common_mwf_time = max(set(mwf_start_times), key=mwf_start_times.count) if mwf_start_times else None
    most_common_tuth_time = max(set(tuth_start_times), key=tuth_start_times.count) if tuth_start_times else None

    return most_common_mwf_time, most_common_tuth_time

def form_three_credit_pattern(sections, mwf_time, tuth_time, credit_threshold):
    patterned_classes = []
    remaining_classes = []
    mwf_count = tuth_count = 0

    for cls in sections:
        if cls['min_credit'] == '4' and len(patterned_classes) < 3:
            # Prioritize filling the pattern for 4-credit classes
            if 'M' in cls['timeslot'] and 'W' in cls['timeslot'] and 'F' in cls['timeslot'] and (mwf_time is None or cls['timeslot'].endswith(mwf_time)):
                patterned_classes.append(cls)
                mwf_count += 1
            elif 'Tu' in cls['timeslot'] and 'Th' in cls['timeslot'] and (tuth_time is None or cls['timeslot'].endswith(tuth_time)):
                patterned_classes.append(cls)
                tuth_count += 1
            else:
                remaining_classes.append(cls)
        elif int(cls['min_credit']) >= credit_threshold:
            # Fill in the pattern for 3-credit classes
            if (mwf_count < 3 and 'M' in cls['timeslot'] and 'W' in cls['timeslot'] and 'F' in cls['timeslot']) or (tuth_count < 2 and 'Tu' in cls['timeslot'] and 'Th' in cls['timeslot']):
                patterned_classes.append(cls)
            else:
                remaining_classes.append(cls)
        else:
            remaining_classes.append(cls)

    # If the pattern is incomplete, fill it with the most common start times
    if len(patterned_classes) < 3 and mwf_time:
        patterned_classes.extend([cls for cls in remaining_classes if cls['timeslot'].endswith(mwf_time)])
        remaining_classes = [cls for cls in remaining_classes if not cls['timeslot'].endswith(mwf_time)]
    elif len(patterned_classes) < 2 and tuth_time:
        patterned_classes.extend([cls for cls in remaining_classes if cls['timeslot'].endswith(tuth_time)])
        remaining_classes = [cls for cls in remaining_classes if not cls['timeslot'].endswith(tuth_time)]

    return {'patterned_classes': patterned_classes, 'remaining_classes': remaining_classes}



# Function to get all datetime slots for a class based on its week days and start time
def get_class_datetime_slots(week_days, start_time_str):
    start_time = datetime.strptime(start_time_str, '%I:%M%p').time()
    weekdays_map = {'M': 0, 'Tu': 1, 'W': 2, 'Th': 3, 'F': 4}
    datetime_slots = []
    for day in week_days.split():
        weekday = weekdays_map[day]
        class_datetime = datetime.combine(datetime.today(), start_time)
        days_ahead = (weekday - class_datetime.weekday()) % 7
        class_datetime += timedelta(days=days_ahead)
        datetime_slots.append(class_datetime)
    return datetime_slots

# Find the closest time slot for the 1-credit class
def find_closest_slot(cls_1_slots, cls_3_slots):
    min_diff = float('inf')
    for cls_1_slot in cls_1_slots:
        for cls_3_slot in cls_3_slots:
            diff = abs((cls_1_slot - cls_3_slot).total_seconds() / 3600)  # Difference in hours
            min_diff = min(min_diff, diff)
    return min_diff


def optimize_remaining_classes(class_sections, remaining_timeslots,used_timeslots):
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
                              ((cls['section'], tsl) for cls in class_sections for tsl in available_timeslots),
                              cat='Binary')

    # Objective function: Minimize the total number of scheduled classes
    prob += pulp.lpSum(x[cls['section'], tsl] for cls in class_sections for tsl in available_timeslots)

    # Constraint: Each class must be scheduled once
    for idx, cls in enumerate(class_sections):
        constraint_name = f"OneClassOneSlot_{cls['section']}_{idx}"
        prob += pulp.lpSum(x[cls['section'], tsl] for tsl in available_timeslots) == 1, constraint_name



    # Create a set of unique rooms
    rooms = set(cls['room'] for cls in class_sections if cls['room'].strip())

    # Constraint: No two classes can be in the same room at the same timeslot
    for tsl in available_timeslots:
        for room in rooms:
            prob += pulp.lpSum(x[cls['section'], tsl] for cls in class_sections if cls['room'] == room) <= 1, f"OneClassPerRoomPerSlot_{room}_{tsl}"

    # Transform weekly unwanted timeslots to individual daily timeslots
    def transform_unwanted_timeslots(unwanted_timeslots):
        transformed_timeslots = set()
        for timeslot in unwanted_timeslots:
            days, time = timeslot.split(' - ')
            for day in days.split():
                transformed_timeslots.add(f"{day} - {time}")
        return transformed_timeslots

    # Constraint: Penalize classes assigned to blocked timeslots
    for cls in class_sections:
        # Check if 'unwanted_timeslots' key exists and is not empty
        if 'unwanted_timeslots' in cls and cls['unwanted_timeslots']:
            transformed_unwanted_timeslots = transform_unwanted_timeslots(cls['unwanted_timeslots'])
            for tsl in available_timeslots:
                if tsl in transformed_unwanted_timeslots:
                    # Apply a penalty for scheduling a class in a blocked timeslot
                    constraint_name = f"BlockedTimeslotPenalty_{cls['section']}_{tsl}"
                    prob += global_settings['blocked_slot_penalty'] * x[cls['section'], tsl], constraint_name



    # Constraint: An instructor can only teach one class per timeslot
    instructors = set(cls['faculty1'] for cls in class_sections)
    for instructor in instructors:
        for tsl in available_timeslots:
            prob += pulp.lpSum(x[cls['section'], tsl] for cls in class_sections if cls['faculty1'] == instructor) <= 1, f"OneInstructorOneSlot_{instructor}_{tsl}"

    # Constraint: Avoid class overlaps
    for tsl in available_timeslots:
        prob += pulp.lpSum(x[cls['section'], tsl] for cls in class_sections) <= 1, f"AvoidOverlap_{tsl}"

    # Constraint: Avoid unwanted timeslots
    for cls in class_sections:
        # Initialize transformed_unwanted_timeslots as an empty set
        transformed_unwanted_timeslots = set()

        # Check if 'unwanted_timeslots' exists and is not empty
        if 'unwanted_timeslots' in cls and cls['unwanted_timeslots']:
            # Transform unwanted timeslots for this class
            for tslot in cls['unwanted_timeslots']:
                days, time = tslot.split(' - ')
                for day in days.split():
                    transformed_unwanted_timeslots.add(f"{day} - {time}")

        # Apply constraint for each unwanted timeslot
        for tsl in transformed_unwanted_timeslots:
            if tsl in available_timeslots:
                prob += x[cls['section'], tsl] == 0, f"AvoidUnwanted_{cls['section']}_{tsl}"


    # Mapping for 3-credit classes and their time slots
    three_credit_slots = {}
    for cls in class_sections:
        if cls['minCredit'] == '3':
            three_credit_slots[cls['section']] = get_class_datetime_slots(cls['week_days'], cls['csm_start'])

    # Penalty for 1-credit classes not being close to their 3-credit counterparts
    for cls in class_sections:
        if cls['minCredit'] == '1' and cls['section'].endswith("_one_credit"):
            base_sec_name = cls['section'][:-11]  # Remove "_one_credit"
            if base_sec_name in three_credit_slots:
                cls_1_slots = get_class_datetime_slots(cls['week_days'], cls['csm_start'])
                time_diff = find_closest_slot(cls_1_slots, three_credit_slots[base_sec_name])
                for tsl in available_timeslots:
                    prob += global_settings['move_penalty'] * time_diff * x[cls['section'], tsl]


    # Solve the problem
    prob.solve()

    # Create a list to store the scheduled class sections
    scheduled_sections = []

    # Check the values of the decision variables and create the schedule
    for cls in class_sections:
        for tsl in remaining_timeslots:
            if pulp.value(x[cls['section'], tsl]) == 1:
                scheduled_sections.append({
                    'section': cls['section'],
                    'timeslot': tsl,
                    'instructor': cls['faculty1'],
                    'room': cls['room'],
                    'bldg': cls['bldg'],
                    'secCap' : cls['secCap'],
                })

    # Create a dictionary to store optimization results
    optimization_results = {
        'message': 'Optimization for remaining classes complete',
        'scheduled_sections': scheduled_sections,
        'status': 'Success' if prob.status == pulp.LpStatusOptimal else 'Failure'
    }

    return optimization_results


def optimize_schedule(class_sections):
    linked_sections = []
    meeting_times = create_meeting_times()

    # Helper function to get attribute or key value
    def get_value(item, key, default=None):
        return item.get(key, default) if isinstance(item, dict) else getattr(item, key, default)

    for class_section in class_sections:
        sec_name = get_value(class_section, 'section')


    instructors = set(get_value(cls, 'faculty1') for cls in class_sections)
    timeslots = [f"{mt['days']} - {mt['start_time']}" for mt in meeting_times]

    prob = pulp.LpProblem("Class_Scheduling", pulp.LpMinimize) 
    
    x = pulp.LpVariable.dicts("x", ((cls['section'], tsl) for cls in class_sections for tsl in timeslots), cat='Binary')

    prob += pulp.lpSum(x[cls['section'], tsl] for cls in class_sections for tsl in timeslots)

     # Constraint: Each class must take exactly one timeslot
    for cls in class_sections:
        unique_constraint_name = f"OneClassOneSlotConstraint_{cls['section']}"  # Generate a unique constraint name
        prob += pulp.lpSum(x[cls['section'], tsl] for tsl in timeslots if (cls['section'], tsl) in x) == 1, unique_constraint_name

    # Create a set of unique rooms
    rooms = set(cls['room'] for cls in class_sections if cls['room'].strip())

    # Constraint: No two classes can be in the same room at the same timeslot
    for tsl in timeslots:
        for room in rooms:
            prob += pulp.lpSum(x[cls['section'], tsl] for cls in class_sections if cls['room'] == room and (cls['section'], tsl) in x) <= 1, f"OneClassPerRoomPerSlot_{room}_{tsl}"

    # Assuming 'instructors' is a list of all unique instructors
    instructors = set(cls['faculty1'] for cls in class_sections)


    # Constraint: An instructor can only teach one class per timeslot
    for tsl in timeslots:
        for instructor in instructors:
            prob += pulp.lpSum(x[cls['section'], tsl] for cls in class_sections if cls['faculty1'] == instructor and (cls['section'], tsl) in x) <= 1, f"OneClassPerInstructorPerSlot_{instructor}_{tsl}"
            
    # Penalty for avoiding classes in the same timeslot
    penalty = global_settings['class_penalty']  # Adjust the penalty weight as needed
    constraint_counter = 0  # Initialize a counter for constraint names
    for cls in class_sections:
        for tsl in timeslots:
            # Check if 'restrictions' list is not empty
            if cls['restrictions']:
                for other_cls_name in cls['restrictions']:
                    if (other_cls_name, tsl) in x:
                        constraint_counter += 1
                        constraint_name = f"AvoidClassesPenalty_{cls['section']}_{tsl}_{constraint_counter}"
                        prob += x[cls['section'], tsl] + x[other_cls_name, tsl] <= 1, constraint_name

    

    # Penalty for avoiding timeslots
    constraint_counter = 0  # Initialize a counter for constraint names

    # Penalty for moving a class outside its known timeslot when holdValue is 1
    for cls in class_sections:
        # Check if the holdValue of the class section is 1
        if cls.get('holdValue', 0) == 1:
            for tsl in timeslots:
                # Check if the class is not scheduled in this timeslot and if the timeslot is not in the assigned meeting time indices
                if (cls['section'], tsl) not in x:
                    tsl_index = int(tsl.split("_")[-1])
                    if tsl_index not in cls.get('assigned_meeting_time_indices', []):
                        constraint_counter += global_settings['hold_penalty']
                        constraint_name = f"MoveClassPenalty_{cls['section']}_{tsl}_{constraint_counter}"
                        prob += x[cls['section'], tsl] == 0, constraint_name


    # Additional penalty for blocked_time_slots
    for cls in class_sections:
        for tsl in timeslots:
            # Check if the timeslot is in the unwanted timeslots for the class section
            if tsl in cls.get('unwanted_timeslots', []):
                prob += global_settings['blocked_slot_penalty'] * x[cls['sec_name'], tsl], f"BlockedTimeSlotPenalty_{cls['sec_name']}_{tsl}"


    
    # Calculate the penalty for keeping linked sections together
    linked_sections_penalty = 0  # Initialize the penalty
    for cls_A, cls_B in linked_sections:
        for tsl in timeslots:
            # Calculate the absolute difference in indexes of cls_A and cls_B
            index_diff = abs(class_sections.index(cls_A) - class_sections.index(cls_B)) * global_settings['move_penalty']
            index_diff = int(index_diff)
            # Add the penalty to the objective function
            prob += x[cls_A['section'], tsl] + x[cls_B.sec_name, tsl] <= 1 + index_diff, f"LinkConstraint_{cls_A.sec_name}_{cls_B['section']}_{tsl}"

            # Update the linked_sections_penalty based on the index_diff
            linked_sections_penalty += index_diff * x[cls_A.sec_name, tsl] + index_diff * x[cls_B.sec_name, tsl]

        
    # Solve the problem
    prob.solve()
    
    
     # Print the status of the problem
    print("Status:", pulp.LpStatus[prob.status])

    # Debugging: Check if any variables are set to 1
    is_any_variable_set = any(pulp.value(var) == 1 for var in x.values())
    print("Is any variable set to 1:", is_any_variable_set)

    # Create a list to store the scheduled class sections
    scheduled_sections = []
    for cls in class_sections:
        for tsl in timeslots:
            if pulp.value(x[get_value(cls, 'section'), tsl]) == 1:
                scheduled_sections.append({
                    'section': get_value(cls, 'section'),
                    'timeslot': tsl,
                    'instructor': get_value(cls, 'faculty1'),
                    'room': get_value(cls, 'room'),
                    'secCap': get_value(cls, 'secCap', 'Unknown'),
                    'bldg': get_value(cls, 'bldg', 'Unknown'),
                })

    # Create a dictionary to store optimization results
    optimization_results = {
        'message': 'Optimization complete',
        'scheduled_sections': scheduled_sections,
        'status': 'Success' if prob.status == pulp.LpStatusOptimal else 'Failure'
    }

    return optimization_results



def get_weekday_date(reference_date, target_weekday):
    """
    Get the date for the target weekday based on the reference date (which is a Wednesday).
    """
    reference_weekday = reference_date.weekday()  # Monday is 0, Sunday is 6
    days_difference = target_weekday - reference_weekday
    return reference_date + timedelta(days=days_difference)

def process_calendar_data_expanded(expanded_schedule):
    calendar_data = []
    color_cache = {}

    reference_date = datetime.today()
    while reference_date.weekday() != 2:  # Adjust to the nearest Wednesday
        reference_date += timedelta(days=1)

    weekday_map = {'M': 0, 'Tu': 1, 'W': 2, 'Th': 3, 'F': 4}

    for result in expanded_schedule:
        section_name = result['section_name']
        timeslot = result['timeslot']
        day, start_time = timeslot.split(' - ')
        
        # Check if day is 'nan' or not in weekday_map
        if day == 'nan' or day not in weekday_map:
            print(f"Skipping invalid day '{day}' in timeslot: {timeslot}")
            continue

        class_date = get_weekday_date(reference_date, weekday_map[day])
        start_datetime = datetime.combine(class_date, datetime.strptime(start_time, '%I:%M%p').time())
        duration = timedelta(hours=1)
        end_datetime = start_datetime + duration

        course_prefix = section_name.split('-')[0]
        if course_prefix not in color_cache:
            color_cache[course_prefix] = str(string_to_color(course_prefix))
        color = color_cache[course_prefix]

        calendar_event = {
            'section_name': section_name,
            'start': start_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
            'end': end_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
            'instructor': result['instructor'],
            'room': result['room'],
            'color': color
        }
        calendar_data.append(calendar_event)

    return calendar_data


def process_calendar_data(three_credit_results, remaining_class_results):
    calendar_data = []
    color_cache = {}

    # Assume the current week's Wednesday as a reference date
    reference_date = datetime.today()
    while reference_date.weekday() != 2:  # Adjust to the nearest Wednesday
        reference_date += timedelta(days=1)

    # Define a weekday map
    weekday_map = {'M': 0, 'Tu': 1, 'W': 2, 'Th': 3, 'F': 4}

    # Process classes
    for results in [three_credit_results['scheduled_sections'], remaining_class_results['scheduled_sections']]:
        for result in results:
            section_name = result['section']
            timeslot = result['timeslot']
            days, start_time = timeslot.split(' - ')
            start_time_obj = datetime.strptime(start_time, '%I:%M%p')

            for day in days.split():
                class_date = get_weekday_date(reference_date, weekday_map[day])
                start_datetime = datetime.combine(class_date, start_time_obj.time())
                duration = timedelta(hours=1) if len(days.split()) == 3 else timedelta(hours=1, minutes=30)
                end_datetime = start_datetime + duration

                # Extract the course prefix and assign color
                course_prefix = section_name.split('-')[0]
                if course_prefix not in color_cache:
                    color_cache[course_prefix] = str(string_to_color(course_prefix))
                color = color_cache[course_prefix]

                calendar_event = {
                    'section_name': section_name,
                    'start': start_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
                    'end': end_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
                    'instructor': result['instructor'],
                    'room': result['room'],
                    'bldg': result['bldg'],
                    'color': color
                }
                calendar_data.append(calendar_event)

    return calendar_data


def combine_and_expand_schedule(three_credit_results, remaining_class_results, meeting_times, class_sections):
    combined_schedule = []

    # Expand and add three-credit class schedules
    for result in three_credit_results['scheduled_sections']:
        cls = next((c for c in class_sections if c.section== result['section']), None)
        if cls:
            # Expand each three-credit class into individual time slots based on its meeting days
            for day in cls.week_days.split():
                day_specific_slot = f"{day} - {result['timeslot'].split(' - ')[1]}"
                combined_schedule.append({
                    'section': cls.section,
                    'timeslot': day_specific_slot,
                    'instructor': cls.faculty1,
                    'room': cls.room,
                    'minCredit': cls.minCredit,
                    'unwanted_timeslots': cls.unwanted_timeslots,
                    'secCap': cls.secCap,
                    'bldg': cls.bldg,
                    'avoid_classes': cls.avoid_classes,
                    'hold_value': cls.holdValue
                })

    # Add one-credit class schedules with proper timeslot format
    for result in remaining_class_results['scheduled_sections']:
        cls = next((c for c in class_sections if c.section == result['section']), None)
        if cls:
            combined_schedule.append({
                'section': cls.section,
                'timeslot': result['timeslot'],
                'instructor': cls.faculty1,
                'room': cls.room,
                'minCredit': cls.minCredit,
                'unwanted_timeslots': cls.unwanted_timeslots,
                'hold_value': cls.holdValue,
                'secCap': cls.secCap,
                'avoid_classes': cls.avoid_classes
            })

    return combined_schedule


def format_for_pulp(schedule):
    formatted_schedule = []

    for class_section in schedule:
        formatted_class = {
            'section': class_section['section'],
            'timeslot': class_section['timeslot'],
            'faculty1': class_section['instructor'],
            'room': class_section.get('room', 'Unknown'),
            'secCap': class_section.get('secCap', 'Unknown'),
            'bldg': class_section.get('bldg', 'Unknown'),
            'avoid_classes': class_section.get('avoid_classes', []),
            'unwanted_timeslots': class_section.get('unwanted_timeslots', []),
            'holdValue': class_section.get('holdValue', 0)
        }

        # Additional attributes might be needed depending on your Pulp functions
        # For example, if minCredit or week_days are needed, add them here.

        formatted_schedule.append(formatted_class)

    return formatted_schedule


def expand_three_credit_class(class_result, meeting_times, class_section):
    # Logic to expand a three-credit class into individual time slots
    expanded_slots = []
    days = class_result['timeslot'].split(' ')[0].split()
    for day in days:
        expanded_slot = {
            'section_name': class_result['section_name'],
            'timeslot': f"{day} - {class_result['timeslot'].split(' ')[1]}",
            'instructor': class_section.faculty1,
            'room': class_section.room,
            'minCredit': class_section.minCredit,
            'unwanted_timeslots': class_section.unwanted_timeslots
        }
        expanded_slots.append(expanded_slot)
    return expanded_slots

import random

def merge_schedules(schedule_1, schedule_2):
    merged_schedule = schedule_1.copy()  # Start with a copy of the first schedule

    # Iterate over the second schedule and add unique sections
    for section_2 in schedule_2:
        if section_2 not in merged_schedule:
            # Add the section from schedule_2 if it's not already in merged_schedule
            merged_schedule.append(section_2)

    return merged_schedule


def repair_schedule(individual):
    # Divide the schedule into 3-credit and other classes
    three_credit_classes, other_classes = divide_schedules_by_credit(individual)

    # Format the schedules for Pulp optimization
    formatted_three_credit_classes = format_for_pulp(three_credit_classes)
    formatted_other_classes = format_for_pulp(other_classes)

    # Optimize the 3-credit classes with Pulp
    optimized_three_credit_results = optimize_schedule(formatted_three_credit_classes)
    
    # Create used_timeslots based on the optimized 3-credit class results
    used_timeslots = set()
    for section in optimized_three_credit_results['scheduled_sections']:
        used_timeslots.add(section['timeslot'])

    # Calculate remaining timeslots
    all_timeslots = [f"{day} - {mt['start_time']}" for mt in create_full_meeting_times() for day in mt['days'].split()]
    remaining_timeslots = [ts for ts in all_timeslots if ts not in used_timeslots]

    # Optimize the remaining classes with Pulp
    optimized_other_classes_results = optimize_remaining_classes(
        formatted_other_classes, 
        remaining_timeslots, 
        used_timeslots
    )


    # Extract the optimized schedules from the Pulp results
    optimized_three_credit_classes = extract_schedule_from_pulp_results(optimized_three_credit_results)
    optimized_other_classes = extract_schedule_from_pulp_results(optimized_other_classes_results)

    # Merge the optimized schedules back into one
    repaired_individual = merge_schedules(optimized_three_credit_classes, optimized_other_classes)

    return repaired_individual

# Implement the additional helper functions as needed

def extract_schedule_from_pulp_results(pulp_results):
    extracted_schedule = []

    # Check if optimization was successful
    if pulp_results.get('status') == 'Success':
        scheduled_sections = pulp_results.get('scheduled_sections', [])

        for scheduled_section in scheduled_sections:
            # Extract and format each scheduled section
            formatted_section = {
                'section_name': scheduled_section.get('section_name'),
                'timeslot': scheduled_section.get('timeslot'),
                'instructor': scheduled_section.get('instructor'),
                'room': scheduled_section.get('room'),
                'sec_cap': scheduled_section.get('sec_cap', 'Unknown'),
                'bldg': scheduled_section.get('bldg', 'Unknown'),
                # Include any other relevant attributes you need from the Pulp results
            }
            extracted_schedule.append(formatted_section)

    return extracted_schedule


def custom_mutate(individual, full_meeting_times, mutpb):
    section_timeslots_map = {}
    for class_section in individual:
        section_name = class_section['section']
        section_timeslots_map.setdefault(section_name, []).append(class_section)

    for i in range(len(individual)):
        if random.random() < mutpb:
            class_section = individual[i]
            minCredit = int(class_section['minCredit'])
            section_name = class_section['section']

            pattern_timeslots = []
            mwf_timeslots = []
            tuth_timeslots = []

            if minCredit >= 3:
                all_timeslots = section_timeslots_map[section_name]
                is_mwf = all(['M' in ts['timeslot'] and 'W' in ts['timeslot'] and 'F' in ts['timeslot'] for ts in all_timeslots])
                is_tuth = all(['Tu' in ts['timeslot'] and 'Th' in ts['timeslot'] for ts in all_timeslots])

                if random.random() < 0.5:  # Change timeslot within the same pattern
                    if is_mwf:
                        pattern_timeslots = [ts for ts in full_meeting_times if 'M' in ts['days'] and 'W' in ts['days'] and 'F' in ts['days']]
                    elif is_tuth:
                        pattern_timeslots = [ts for ts in full_meeting_times if 'Tu' in ts['days'] and 'Th' in ts['days']]

                    if pattern_timeslots:
                        new_timeslot = random.choice(pattern_timeslots)
                        for ts in all_timeslots:
                            ts['timeslot'] = f"{new_timeslot['days']} - {new_timeslot['start_time']}"
                else:  # Switch pattern
                    if is_mwf:
                        tuth_timeslots = [ts for ts in full_meeting_times if 'Tu' in ts['days'] and 'Th' in ts['days']]
                    elif is_tuth:
                        mwf_timeslots = [ts for ts in full_meeting_times if 'M' in ts['days'] and 'W' in ts['days'] and 'F' in ts['days']]

                    if (is_mwf and tuth_timeslots) or (is_tuth and mwf_timeslots):
                        new_timeslot = random.choice(tuth_timeslots if is_mwf else mwf_timeslots)
                        for ts in all_timeslots:
                            ts['timeslot'] = f"{new_timeslot['days']} - {new_timeslot['start_time']}"

            else:
                current_day = class_section['timeslot'].split(' - ')[0]
                same_day_timeslots = [ts for ts in full_meeting_times if current_day in ts['days']]
                if same_day_timeslots:
                    new_timeslot = random.choice(same_day_timeslots)
                    class_section['timeslot'] = f"{new_timeslot['days']} - {new_timeslot['start_time']}"
                    

    # After mutation, repair the individual
    repaired_individual = repair_schedule(individual)
    # Update the individual with the repaired schedule
    individual[:] = repaired_individual

    return individual,

def extract_schedule_from_pulp_results(pulp_results):
    extracted_schedule = []

    # Check if optimization was successful
    if pulp_results.get('status') == 'Success':
        scheduled_sections = pulp_results.get('scheduled_sections', [])

        for scheduled_section in scheduled_sections:
            # Extract and format each scheduled section
            formatted_section = {
                'section_name': scheduled_section.get('section_name'),
                'timeslot': scheduled_section.get('timeslot'),
                'instructor': scheduled_section.get('instructor'),
                'room': scheduled_section.get('room'),
                'sec_cap': scheduled_section.get('sec_cap', 'Unknown'),
                'bldg': scheduled_section.get('bldg', 'Unknown'),
                # Include any other relevant attributes you need from the Pulp results
            }
            extracted_schedule.append(formatted_section)

    return extracted_schedule




def merge_class_details(schedule_result, class_section, day=None):
    # Merge details from class_section into the schedule result
    merged_result = schedule_result.copy()
    merged_result['instructor'] = class_section.faculty1
    merged_result['room'] = class_section.room
    merged_result['minCredit'] = class_section.minCredit
    merged_result['unwanted_timeslots'] = class_section.unwanted_timeslots

    if day:
        # Adjust the timeslot for the specific day if provided
        merged_result['timeslot'] = f"{day} - {schedule_result['timeslot'].split(' ')[1]}"
    
    return merged_result


def custom_crossover(ind1, ind2):
    full_meeting_times = create_full_meeting_times()
    size = min(len(ind1), len(ind2))
    cxpoint1 = random.randint(1, size - 1)
    cxpoint2 = random.randint(1, size - 1)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else:
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    # Perform the crossover
    ind1[cxpoint1:cxpoint2], ind2[cxpoint1:cxpoint2] = ind2[cxpoint1:cxpoint2], ind1[cxpoint1:cxpoint2]

    # Adjust timeslots for all classes to maintain constraints
    for ind in [ind1, ind2]:
        # Process each class section in the individual
        for class_section in ind:
            minCredit = int(class_section['minCredit'])
            course_identifier = class_section['section'].split('_')[0]
            course_timeslots = [cs for cs in ind if cs['section'].startswith(course_identifier)]

            # Check if the pattern is maintained for 3+ credit classes
            if minCredit >= 3:
                mwf_count = sum(['M' in ts['timeslot'] and 'W' in ts['timeslot'] and 'F' in ts['timeslot'] for ts in course_timeslots])
                tuth_count = sum(['Tu' in ts['timeslot'] and 'Th' in ts['timeslot'] for ts in course_timeslots])

                # Determine the desired pattern based on the existing count
                desired_pattern = 'MWF' if mwf_count >= tuth_count else 'TuTh'

                # Adjust timeslots to match the desired pattern
                for ts in course_timeslots:
                    # Choose timeslots based on the desired pattern
                    if desired_pattern == 'MWF':
                        suitable_timeslots = [time for time in full_meeting_times if 'M' in time['days'] and 'W' in time['days'] and 'F' in time['days']]
                    else:
                        suitable_timeslots = [time for time in full_meeting_times if 'Tu' in time['days'] and 'Th' in time['days']]

                    # Assign a new timeslot adhering to the pattern
                    if suitable_timeslots:
                        new_timeslot = random.choice(suitable_timeslots)
                        ts['timeslot'] = f"{new_timeslot['days']} - {new_timeslot['start_time']}"
                    else:
                        # Retain original timeslot if no suitable new timeslot is found
                        pass  # No change needed

            # For classes with less than 3 credits, ensure they have a valid timeslot
            else:
                # Extract the day part from the class section's current timeslot
                current_day = class_section['timeslot'].split(' - ')[0]

                # Filter available timeslots for the same day of the week
                same_day_timeslots = [ts for ts in full_meeting_times if current_day in ts['days']]

                # Assign a new timeslot on the same day
                if same_day_timeslots:
                    new_timeslot = random.choice(same_day_timeslots)
                    class_section['timeslot'] = f"{new_timeslot['days']} - {new_timeslot['start_time']}"
                else:
                    # Retain original timeslot if no suitable new timeslot is found
                    pass  # No change needed

    return ind1, ind2






def run_genetic_algorithm(combined_expanded_schedule, ngen=100, pop_size=50, cxpb=0.5, mutpb=0.2):
    # Create necessary data
    full_meeting_times_data = create_full_meeting_times()

    # Setup the DEAP toolbox
    toolbox = base.Toolbox()
    
    # Register individual and population creation methods
    toolbox.register("individual", create_individual, combined_expanded_schedule, full_meeting_times_data)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Register custom mutate method
    toolbox.register(
        "mutate", 
        custom_mutate, 
        full_meeting_times=full_meeting_times_data, 
        mutpb=0.3
    )
    # Register mate and select methods
    toolbox.register("mate", custom_crossover)
    toolbox.register("select", tools.selTournament, tournsize=3)

    # Adjust the evaluate function to use only the total score from evaluateSchedule's output
    def evaluate_wrapper(individual):
        evaluation_results = evaluateSchedule(individual)
        return evaluation_results['total_score'],

    toolbox.register("evaluate", evaluate_wrapper)

    # Create initial population
    population = toolbox.population(n=pop_size)

    # Evaluate initial population's fitness
    fitnesses = list(map(toolbox.evaluate, population))
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit

    # Collecting statistics
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)

    # Run genetic algorithm
    final_population, logbook = algorithms.eaSimple(population, toolbox, cxpb, mutpb, ngen, stats=stats, verbose=True)

    # Process final population
    sorted_population = sorted(population, key=lambda ind: ind.fitness.values[0])

    # Identify top unique schedules
    top_unique_schedules = []
    used_scores = set()
    for ind in sorted_population:
        fitness_score = ind.fitness.values[0]
        if fitness_score not in used_scores:
            top_unique_schedules.append((ind, fitness_score))
            used_scores.add(fitness_score)
            if len(top_unique_schedules) == 5:
                break

    return top_unique_schedules

def split_class_sections(class_sections):
    three_credit_sections = []
    remaining_class_sections = []
    #class_sections = global_settings['class_sections_data']

    for class_section in class_sections:
        if int(class_section['minCredit']) == 4:
            # Create a copy of the class_section dictionary
            three_credit_section = class_section.copy()
            three_credit_section['minCredit'] = '3'

            # Create a modified copy for the one credit section
            one_credit_section = class_section.copy()
            one_credit_section['minCredit'] = '1'
            one_credit_section['section'] += "_one_credit"

            three_credit_sections.append(three_credit_section)
            remaining_class_sections.append(one_credit_section)

        elif int(class_section['minCredit']) == 3:
            three_credit_sections.append(class_section.copy())

        else:
            remaining_class_sections.append(class_section.copy())

    return three_credit_sections, remaining_class_sections


def count_slot_differences(pulp_schedule, ga_schedule):
    differences = 0
    pulp_sections = {section['section_name']: section['timeslot'] for section in pulp_schedule}
    
    for section in ga_schedule:
        section_name = section['section_name']
        if pulp_sections.get(section_name) != section['timeslot']:
            differences += 1

    return differences

@app.route('/optimize', methods=['POST'])
def optimize():
    
    global global_settings
    data = request.get_json()
    
    global_settings['class_sections_data'] = data.get('classData', [])
    global_settings['class_penalty'] = data.get('classPenalty', 0)
    global_settings['move_penalty'] = data.get('movePenalty', 0)
    global_settings['blocked_slot_penalty'] = data.get('blockedSlotPenalty', 0)
    global_settings['hold_penalty'] = data.get('holdPenalty', 0)



    class_sections = create_class_sections_from_data(global_settings['class_sections_data'])
    
    # Convert class section instances to dictionaries
    class_sections_dictionaries = [class_section.to_dictionary() for class_section in class_sections]

    three_credit_sections, remaining_class_sections =  split_class_sections(class_sections_dictionaries)

    # Optimize the 3-credit classes with Pulp
    three_credit_results = optimize_schedule(three_credit_sections)

    # Create a set of used timeslots
    used_timeslots = set()
    for section in three_credit_results['scheduled_sections']:
        used_timeslots.add(section['timeslot'])
        
    # Calculate remaining timeslots
    all_timeslots = [f"{day} - {mt['start_time']}" for mt in create_full_meeting_times() for day in mt['days'].split()]
    remaining_timeslots = [ts for ts in all_timeslots if ts not in used_timeslots]

    # Optimize the remaining classes with Pulp
    remaining_class_results = optimize_remaining_classes(remaining_class_sections, remaining_timeslots, used_timeslots)
    calendar_events = process_calendar_data(three_credit_results, remaining_class_results)

    # Combine and expand the schedules
    combined_expanded_schedule = combine_and_expand_schedule(three_credit_results, remaining_class_results, create_full_meeting_times(), class_sections)

    # use the genetic algorithm evalutaion function to evaluate the schedule
    pulp_evaluation_results = evaluateSchedule(combined_expanded_schedule)
    pulp_score = pulp_evaluation_results['total_score']
    full_meeting_times_data = create_full_meeting_times()

    # Run the genetic algorithm to optimize the schedule further
    ga_schedules = run_genetic_algorithm(combined_expanded_schedule)

    all_schedules = [{'schedule': schedule, 'score': score, 'algorithm': 'GA', 'slot_differences': count_slot_differences(combined_expanded_schedule, schedule)} for schedule, score in ga_schedules]
    all_schedules.append({'schedule': combined_expanded_schedule, 'score': pulp_score, 'algorithm': 'PuLP', 'slot_differences': 0})

    all_schedules_sorted = sorted(all_schedules, key=lambda x: x['score'])

    calendar_events = []
    for schedule in all_schedules_sorted:
        events_for_schedule = process_calendar_data_expanded(schedule['schedule'])
        calendar_events.append({
            'schedule_info': schedule,
            'events': events_for_schedule
        })

    final_results = {
        'sorted_schedules': all_schedules_sorted,
        'calendar_events': calendar_events,
        'message': 'Optimization completed'
    }

    return jsonify(final_results)



from datetime import datetime


def evaluateSchedule(individual):
    # Define penalties
    overlap_penalty = 300
    instructor_conflict_penalty = 300
    room_conflict_penalty = 300
    proximity_penalty = 2
    unwanted_timeslot_penalty = 3
    pattern_violation_penalty = 300
    mutual_exclusion_penalty = 2
    same_day_penalty = 300

    # Initialize scoring variables
    total_score = 0
    detailed_scores = {}
    class_timings = {}
    class_days = {}

    # Function to check if the class follows the MWF or TuTh pattern
    def follows_desired_pattern(course_identifier, timeslots):
        mwf_count = sum(['M' in ts and 'W' in ts and 'F' in ts for ts in timeslots])
        tuth_count = sum(['Tu' in ts and 'Th' in ts for ts in timeslots])

        # For 3-credit classes, either 2 TuTh or 3 MWF slots are acceptable
        if course_identifier.endswith('_3'):
            return (mwf_count == 3 and len(timeslots) >= 3) or (tuth_count == 2 and len(timeslots) >= 2)
        else:
            return mwf_count == len(timeslots) or tuth_count == len(timeslots)

    # Evaluate each class meeting
    for i, meeting in enumerate(individual):
        class_score = 0
        overlap_violations = 0
        instructor_conflicts = 0
        room_conflicts = 0
        proximity_issues = 0
        unwanted_timeslot_violations = 0
        mutual_exclusion_violations = 0

        # Store timing and days for classes 3+ credits
        if int(meeting['minCredit']) >= 3:
            course_identifier = meeting['section'].split('_')[0]
            class_timings.setdefault(course_identifier, set()).add(meeting['timeslot'])
            days = meeting['timeslot'].split(' - ')[0]
            class_days.setdefault(course_identifier, set()).update(days.split())

        # Check for overlaps, conflicts, and violations
        for j, other_meeting in enumerate(individual):
            if i != j:
                if meeting['timeslot'] == other_meeting['timeslot']:
                    overlap_violations += 1
                    if meeting['room'] == other_meeting['room']:
                        room_conflicts += 1
                    if meeting['instructor'] == other_meeting['instructor']:
                        instructor_conflicts += 1

                # Mutual exclusion violations
                mutually_exclusive_sections = meeting.get('avoid_classes', [])
                if other_meeting['section'] in mutually_exclusive_sections:
                    mutual_exclusion_violations += 1

        # Proximity issues for 1-credit classes
        if meeting['minCredit'] == '1' and meeting['section'].endswith("_one_credit"):
            base_sec_name = meeting['section'][:-11]
            three_credit_class_meetings = [s for s in individual if s['section'] == base_sec_name]
            for cls_3_meeting in three_credit_class_meetings:
                time_diff = abs((datetime.strptime(meeting['timeslot'].split(' - ')[1], '%I:%M%p') - 
                                 datetime.strptime(cls_3_meeting['timeslot'].split(' - ')[1], '%I:%M%p')).total_seconds()) / 3600
                if time_diff > 2:
                    proximity_issues += 1

        # Unwanted timeslot violations
        for unwanted_timeslot in meeting.get('unwanted_timeslots', []):
            unwanted_days, unwanted_time = unwanted_timeslot.split(' - ')
            if unwanted_days in meeting['timeslot'] and unwanted_time == meeting['timeslot'].split(' - ')[1]:
                unwanted_timeslot_violations += 1

        # Calculate score for this class meeting
        class_score = (overlap_violations * overlap_penalty +
                       instructor_conflicts * instructor_conflict_penalty +
                       room_conflicts * room_conflict_penalty +
                       proximity_issues * proximity_penalty +
                       unwanted_timeslot_violations * unwanted_timeslot_penalty +
                       mutual_exclusion_violations * mutual_exclusion_penalty)

        # Update total score and details
        total_score += class_score
        detailed_scores[meeting['section']] = {
            'score': class_score,
            'overlap_violations': overlap_violations,
            'instructor_conflicts': instructor_conflicts,
            'room_conflicts': room_conflicts,
            'proximity_issues': proximity_issues,
            'unwanted_timeslot_violations': unwanted_timeslot_violations,
            'mutual_exclusion_violations': mutual_exclusion_violations
        }

    # Check for pattern matching and same day violations
    for course, timeslots in class_timings.items():
        if not follows_desired_pattern(course, timeslots):
            pattern_violation = pattern_violation_penalty * len(timeslots)
            total_score += pattern_violation
            for section in detailed_scores:
                if section.startswith(course):
                    detailed_scores[section]['pattern_violation'] = pattern_violation
        
        # Same day violations
        if len(class_days[course]) < len(timeslots):
            same_day_violation = same_day_penalty * (len(timeslots) - len(class_days[course]))
            total_score += same_day_violation
            for section in detailed_scores:
                if section.startswith(course):
                    detailed_scores[section].setdefault('same_day_violation', 0)
                    detailed_scores[section]['same_day_violation'] += same_day_violation

    return {'total_score': total_score, 'detailed_scores': detailed_scores}






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
