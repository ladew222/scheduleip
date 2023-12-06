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
import random
import numpy as np
import random
from datetime import datetime, timedelta
from collections import Counter
import uuid
import os
from flask import make_response
from ics import Calendar, Event
from datetime import datetime, timedelta
import re
import pandas as pd
from io import StringIO


global_settings = {}
results_storage = {}

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


def create_individual(failed_sections,combined_expanded_schedule, mutation_rate=0.3):
    individual = []
    day_assignment = {}  # Dictionary to track day assignments for each course
    full_meeting_times = create_full_meeting_times()

    for cls in combined_expanded_schedule:
        # Copy class section detailså
        new_class_section = cls.copy()
        course_identifier = cls['section'].split('_')[0]
        
        
        first_elements_list = [item[0] for item in failed_sections]
        # Check if the current class section is in the list of failed sections
        if course_identifier in first_elements_list or 1==1:
            # Randomly decide whether to mutate this class section
            if random.random() < mutation_rate:
                # Determine the current pattern (MWF or TuTh) of the class
                current_pattern = 'MWF' if 'M' in cls['timeslot'] or 'W' in cls['timeslot'] or 'F' in cls['timeslot'] else 'TuTh'
                
                # Filter timeslots based on the pattern and avoid clashes on the same day
                available_timeslots = [
                    ts for ts in full_meeting_times
                    if ts['days'] in cls['timeslot'] and
                       ts['days'] not in day_assignment.get(course_identifier, set())
                ]

                # If available timeslots are found, choose one randomly
                if available_timeslots:
                    chosen_timeslot = random.choice(available_timeslots)
                    new_class_section['timeslot'] = f"{chosen_timeslot['days']} - {chosen_timeslot['start_time']}"
                    # Update day assignment for the course
                    day_assignment.setdefault(course_identifier, set()).add(chosen_timeslot['days'])

        # Add the class section to the individual schedule regardless of mutation
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


def group_and_update_schedule(schedule_info):
    updated_schedules = []


    # Divide each schedule into groups of 3-credit and remaining classes
    three_credit_classes, remaining_classes = divide_schedules_by_credit(schedule_info['schedule'])

    # Group 3-credit classes based on common time patterns
    grouped_three_credit_classes = []
    for cls in three_credit_classes:
        # Use 'get_most_common_start_times' if necessary
        # mwf_time, tuth_time = get_most_common_start_times([cls]) # If this function is needed

        # Directly use the timeslot info from the class section
        grouped_three_credit_classes.append({
            'section': cls['section'],
            'timeslot': cls['timeslot'],
            'minCredit': cls['minCredit'],
            'secCap': cls['secCap'],
            'faculty1': cls['faculty1'],
            'room': cls['room'],
            'bldg': cls['bldg']
        })

    # Combine the grouped 3-credit classes with remaining classes
    updated_schedule = grouped_three_credit_classes + remaining_classes

    # Update the schedule in the schedule_info dictionary
    updated_schedules.append({
        'schedule': updated_schedule,
        'score': schedule_info['score'],
        'algorithm': schedule_info['algorithm'],
        'slot_differences': schedule_info['slot_differences']
    })

    return updated_schedules



def get_most_common_start_times(sections):
    # Separate MWF and TuTh timeslots
    mwf_start_times = [cls['timeslot'].split(' - ')[1] for cls in sections if 'M' in cls['timeslot'] or 'W' in cls['timeslot'] or 'F' in cls['timeslot']]
    tuth_start_times = [cls['timeslot'].split(' - ')[1] for cls in sections if 'Tu' in cls['timeslot'] or 'Th' in cls['timeslot']]

    # Find the most common start times
    most_common_mwf_time = Counter(mwf_start_times).most_common(1)[0][0] if mwf_start_times else None
    most_common_tuth_time = Counter(tuth_start_times).most_common(1)[0][0] if tuth_start_times else None

    return most_common_mwf_time, most_common_tuth_time



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
                    'faculty1': cls['faculty1'],
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
                    'faculty1': get_value(cls, 'faculty1'),
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

def annotate_failure_reasons(schedule, failure_report):
    # Check if failure_report[1] has values
    if  failure_report and  len(failure_report)>0:
        failure_details = {section_info[0]: section_info[1] for section_info in failure_report}
        for section in schedule:
            if section['section'] in failure_details:
                section['failure_reason'] = failure_details[section['section']]
            else:
                section['failure_reason'] = None  # No failure for this section
    else:
        # If failure_report[1] is empty, there are no failures
        for section in schedule:
            section['failure_reason'] = None  # No failure for this section

    return schedule

from ics import Calendar, Event
from datetime import datetime, timedelta

def process_calendar_data_to_ics(expanded_schedule):
    cal = Calendar()

    reference_date = datetime.today()
    while reference_date.weekday() != 2:  # Adjust to the nearest Wednesday
        reference_date += timedelta(days=1)

    weekday_map = {'M': 0, 'Tu': 1, 'W': 2, 'Th': 3, 'F': 4}

    for result in expanded_schedule:
        section_name = result['section']
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

        # Create an event
        event = Event()
        event.name = f"{section_name} Class"
        event.begin = start_datetime
        event.end = end_datetime
        event.location = result['room']
        event.description = f"Class with {result['faculty1']}"

        # Add event to calendar
        cal.events.add(event)

    # Convert the calendar to a string
    return str(cal)

def get_weekday_date(reference_date, weekday_offset):
    """
    Get the date for a specific weekday based on a reference date.
    """
    target_weekday = (reference_date.weekday() + weekday_offset) % 7
    return reference_date + timedelta(days=target_weekday - reference_date.weekday())

# Example usage:
# expanded_schedule = [...]  # Your expanded schedule data here
# ics_calendar_str = process_calendar_data_to_ics(expanded_schedule)
# with open("schedule.ics", "w") as file:
#     file.write(ics_calendar_str)



def process_calendar_data_expanded(expanded_schedule):
    calendar_data = []
    color_cache = {}

    reference_date = datetime.today()
    while reference_date.weekday() != 2:  # Adjust to the nearest Wednesday
        reference_date += timedelta(days=1)

    weekday_map = {'M': 0, 'Tu': 1, 'W': 2, 'Th': 3, 'F': 4}

    for result in expanded_schedule:
        section_name = result['section']
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
            'faculty1': result['faculty1'],
            'room': result['room'],
            'color': color
        }
        calendar_data.append(calendar_event)

    return calendar_data


def process_calendar_data(three_credit_results, remaining_class_results):
    calendar_data = []
    color_cache = {}

    # Assume the current week's Monday as a reference date
    reference_date = datetime.today()
    while reference_date.weekday() != 0:  # Adjust to the nearest Monday
        reference_date -= timedelta(days=1)

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
                # Determine the duration based on the days
                duration = timedelta(hours=1.5 if day in ['Tu', 'Th'] else 1)
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
                    'faculty1': result['faculty1'],
                    'room': result['room'],
                    'bldg': result['bldg'],
                    'color': color
                }
                calendar_data.append(calendar_event)

    return calendar_data

def get_weekday_date(reference_date, target_weekday):
    """
    Get the date for the target weekday based on the reference date (which is a Monday).
    """
    reference_weekday = reference_date.weekday()  # Monday is 0, Sunday is 6
    days_difference = target_weekday - reference_weekday
    return reference_date + timedelta(days=days_difference)

def combine_and_expand_schedule(three_credit_results, remaining_class_results, meeting_times, class_sections):
    combined_schedule = []

    # Expand and add three-credit class schedules
    for result in three_credit_results['scheduled_sections']:
        cls = next((c for c in class_sections if c.section== result['section']), None)
        if cls:
            # Extract days from the optimized timeslot
            optimized_days = result['timeslot'].split(' - ')[0].split()
            optimized_time = result['timeslot'].split(' - ')[1]
            # Expand each three-credit class into individual time slots based on its meeting days
            for day in optimized_days:
                day_specific_slot = f"{day} - {optimized_time}"
                combined_schedule.append({
                    'section': cls.section,
                    'timeslot': day_specific_slot,
                    'faculty1': cls.faculty1,
                    'room': cls.room,
                    'minCredit': cls.minCredit,
                    'unwanted_timeslots': cls.unwanted_timeslots,
                    'secCap': cls.secCap,
                    'bldg': cls.bldg,
                    'avoid_classes': cls.avoid_classes,
                    'hold_value': cls.holdValue
                })

    # Add one-credit class schedules with proper timeslot format
    # Continue to process each result in 'remaining_class_results'
    for result in remaining_class_results['scheduled_sections']:
        section_name = result['section']

        # Check if the section name ends with '_one_credit'
        if section_name.endswith('_one_credit'):
            # Remove the '_one_credit' suffix to match with 'class_sections'
            base_section_name = section_name[:-11]  # 11 characters in '_one_credit'
        else:
            base_section_name = section_name

        # Find the corresponding class section in 'class_sections'
        cls = next((c for c in class_sections if c.section == base_section_name), None)
        
        # Check if a corresponding class section was found
        if cls:
            # Append the formatted class section to 'combined_schedule'
            combined_schedule.append({
                'section': section_name,  # Keep the original section name
                'timeslot': result['timeslot'],
                'faculty1': cls.faculty1,
                'room': cls.room,
                'minCredit': cls.minCredit,
                'unwanted_timeslots': cls.unwanted_timeslots,
                'hold_value': cls.holdValue,
                'secCap': cls.secCap,
                'bldg': cls.bldg,
                'avoid_classes': cls.avoid_classes,
                'hold_value': cls.holdValue
            })

    # 'combined_schedule' now contains the formatted schedule including the remaining class results

    return combined_schedule


def format_for_pulp(schedule):
    formatted_schedule = []

    for class_section in schedule:
        formatted_class = {
            'section': class_section['section'],
            'timeslot': class_section['timeslot'],
            'faculty1': class_section['faculty1'],
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
            'faculty1': class_section.faculty1,
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
                'faculty1': scheduled_section.get('faculty1'),
                'room': scheduled_section.get('room'),
                'sec_cap': scheduled_section.get('sec_cap', 'Unknown'),
                'bldg': scheduled_section.get('bldg', 'Unknown'),
                # Include any other relevant attributes you need from the Pulp results
            }
            extracted_schedule.append(formatted_section)

    return extracted_schedule



def create_timeslot_availability(individual):
    
    full_meeting_times = create_full_meeting_times()
    # Initialize dictionaries for availability
    timeslot_availability = {
        'M': {'MWF': [], 'other': []},
        'W': {'MWF': [], 'other': []},
        'F': {'MWF': [], 'other': []},
        'Tu': {'TuTh': [], 'other': []},
        'Th': {'TuTh': [], 'other': []}
    }
    room_availability = {}
    instructor_availability = {}

    # Populate timeslot availability based on full_meeting_times
    for timeslot in full_meeting_times:
        day = timeslot['days']
        time = f"{timeslot['start_time']} - {timeslot['end_time']}"
        if 'M' in day and 'W' in day and 'F' in day:
            timeslot_availability['M']['MWF'].append(time)
            timeslot_availability['W']['MWF'].append(time)
            timeslot_availability['F']['MWF'].append(time)
        elif 'Tu' in day and 'Th' in day:
            timeslot_availability['Tu']['TuTh'].append(time)
            timeslot_availability['Th']['TuTh'].append(time)
        else:
            if 'M' in day: timeslot_availability['M']['other'].append(time)
            if 'W' in day: timeslot_availability['W']['other'].append(time)
            if 'F' in day: timeslot_availability['F']['other'].append(time)
            if 'Tu' in day: timeslot_availability['Tu']['other'].append(time)
            if 'Th' in day: timeslot_availability['Th']['other'].append(time)

    # Populate room and instructor availability based on current individual schedule
    for cls in individual:
        timeslot = cls['timeslot']
        room_availability.setdefault(timeslot, set()).add(cls['room'])
        instructor_availability.setdefault(timeslot, set()).add(cls['faculty1'])

    return timeslot_availability, room_availability, instructor_availability

       

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
                'faculty1': scheduled_section.get('faculty1'),
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
    merged_result['faculty1'] = class_section.faculty1
    merged_result['room'] = class_section.room
    merged_result['minCredit'] = class_section.minCredit
    merged_result['unwanted_timeslots'] = class_section.unwanted_timeslots

    if day:
        # Adjust the timeslot for the specific day if provided
        merged_result['timeslot'] = f"{day} - {schedule_result['timeslot'].split(' ')[1]}"
    
    return merged_result




def determine_class_pattern(course_timeslots):
    # Count occurrences of each day in the timeslots
    day_count = {'M': 0, 'W': 0, 'F': 0, 'Tu': 0, 'Th': 0}
    for ts in course_timeslots:
        day = ts['timeslot'].split(' - ')[0]
        if day in day_count:
            day_count[day] += 1

    # Determine the pattern based on the counts
    if day_count['M'] > 0 and day_count['W'] > 0 and day_count['F'] > 0:
        return 'MWF'
    elif day_count['Tu'] > 0 and day_count['Th'] > 0:
        return 'TuTh'
    else:
        return 'Other'

def group_by_pattern(individual):
    # Group classes by their section and determine the overall pattern
    grouped_classes = {}
    for cls in individual:
        course_identifier = cls['section'].split('_')[0]
        grouped_classes.setdefault(course_identifier, []).append(cls)

    # Separate classes into MWF, TuTh, and Others based on their determined pattern
    mwf_classes = []
    tuth_classes = []
    other_classes = []

    for course_identifier, course_timeslots in grouped_classes.items():
        pattern = determine_class_pattern(course_timeslots)
        if pattern == 'MWF':
            mwf_classes.extend(course_timeslots)
        elif pattern == 'TuTh':
            tuth_classes.extend(course_timeslots)
        else:
            other_classes.extend(course_timeslots)

    return mwf_classes, tuth_classes, other_classes




def is_valid_individual(individual):
    full_meeting_times = create_full_meeting_times()
    room_assignments = {}
    instructor_assignments = {}
    failure_sections = []
    section_day_assignments = {}
    valid_timeslots = {f"{ts['days']} - {ts['start_time']}" for ts in full_meeting_times}

    # Group classes by their base section name for pattern adherence
    section_groupings = {}
    for cls in individual:
        base_section_name = cls['section'].split('_')[0]  # Use base name for pattern adherence
        section_groupings.setdefault(base_section_name, []).append(cls)

    for cls in individual:
        # Check if the class timeslot is valid
        if cls['timeslot'] not in valid_timeslots:
            failure_sections.append((cls['section'],"invalid timeslot"),cls)  # Use full section name

        # Check for multiple timeslot assignments on the same day for each section
        day = cls['timeslot'].split(' - ')[0]
        if day in section_day_assignments.get(cls['section'], set()):  # Use full section name
            failure_sections.append((cls['section'], "multiple timeslots on same day",cls))
        section_day_assignments.setdefault(cls['section'], set()).add(day)
        full_room = cls.get('bldg','') + ' ' + cls['room']
        # Check for room and instructor conflicts
        if cls['timeslot'] in room_assignments:
            if full_room in room_assignments[cls['timeslot']]:
                 # Check for room conflicts
                failure_sections.append((cls['section'],"room conflict"))
            elif cls['faculty1'] in instructor_assignments[cls['timeslot']]:
                # Check for instructor conflicts
                failure_sections.append((cls['section'],"instructor conflict",cls))
        room_assignments.setdefault(cls['timeslot'], set()).add(full_room)
        instructor_assignments.setdefault(cls['timeslot'], set()).add(cls['faculty1'])

        # Group classes by their base section name for pattern adherence
        section_groupings = {}
        for cls in individual:
            base_section_name = cls['section'].split('_')[0]  # Use base name for pattern adherence
            section_groupings.setdefault(base_section_name, []).append(cls)

        # ... (rest of the checks for invalid timeslot, multiple timeslots, room and instructor conflicts)

        # Check for pattern adherence for groups of sections
        for base_section_name, sections in section_groupings.items():
            pattern_sections = [cls for cls in sections if not cls['section'].endswith('_one_credit')]
            if any(int(cls['minCredit']) >= 3 for cls in pattern_sections):
                days = set(cls['timeslot'].split(' - ')[0] for cls in pattern_sections)
                times = set(cls['timeslot'].split(' - ')[1] for cls in pattern_sections)

                is_mwf = days.issubset({'M', 'W', 'F'}) and len(times) == 1
                is_tuth = days.issubset({'Tu', 'Th'}) and len(times) == 1

                if not (is_mwf or is_tuth):
                    failure_sections.append((base_section_name, "pattern adherence", pattern_sections[0]))  # Include an example class for reference

        # Return a tuple with a boolean for overall validity and a list of sections that failed validation
        return failure_sections




def follows_pattern(timeslot, pattern):
    """Check if a timeslot follows a specific pattern (MWF or TuTh)."""
    days = timeslot.split(' - ')[0]
    if pattern == 'MWF':
        return all(day in days for day in ['M', 'W', 'F'])
    elif pattern == 'TuTh':
        return all(day in days for day in ['Tu', 'Th'])
    return False




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
    pulp_sections = {section['section']: section['timeslot'] for section in pulp_schedule}
    
    for section in ga_schedule:
        section_name = section['section']
        if pulp_sections.get(section_name) != section['timeslot']:
            differences += 1

    return differences


@app.route('/get_ical', methods=['GET'])
def get_ical():
    key = request.args.get('key')
    file_path = f'optimization_results/{key}.json'
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'Invalid or missing key'}), 400

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        schedule = data['sorted_schedule']

    ical_content = convert_schedule_to_ical(schedule)

    response = make_response(ical_content)
    response.headers["Content-Disposition"] = f"attachment; filename=schedule_{key}.ics"
    response.headers["Content-Type"] = "text/calendar"
    return response


def weekday_to_date(start_date, weekday):
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    start_weekday = start_date_obj.weekday()
    target_weekday = weekdays.index(weekday)
    days_to_add = (target_weekday - start_weekday) % 7
    return (start_date_obj + timedelta(days=days_to_add)).date()

def convert_schedule_to_ical(schedules, start_date=None, end_date=None):
    cal = Calendar()
    schedule = schedules[0]['schedule']

    days_map = {'M': 'Monday', 'Tu': 'Tuesday', 'W': 'Wednesday', 'Th': 'Thursday', 'F': 'Friday'}
    day_durations = {'Tu': timedelta(hours=1, minutes=30), 'Th': timedelta(hours=1, minutes=30), 'M': timedelta(hours=1), 'W': timedelta(hours=1), 'F': timedelta(hours=1)}

    if not start_date:
        start_date = datetime.today().strftime("%Y-%m-%d")
    if not end_date:
        end_date = (datetime.today() + timedelta(weeks=16)).strftime("%Y-%m-%d")

    for entry in schedule:
        days, time_str = entry['timeslot'].split(' - ')
        start_time = datetime.strptime(time_str, '%I:%M%p').time()
        for day_code in days.split():
            day_name = days_map.get(day_code)
            if day_name:
                duration = day_durations.get(day_code, timedelta(hours=1))
                end_time = (datetime.combine(datetime.today(), start_time) + duration).time()
                first_event_date = weekday_to_date(start_date, day_name)

                event = Event()
                event.name = f"{entry['section']}"
                event.begin = datetime.combine(first_event_date, start_time)
                event.end = datetime.combine(first_event_date, end_time)
                event.location = entry['bldg'] + " " + entry['room']
                subject = entry['section'].split('-')[0]
                event.categories = subject
                event.classification = subject
                event.organizer = entry['faculty1']
                event.description = f"Instructor:{entry['faculty1']} Capacity: {entry['secCap']} with Min-credits: {entry['minCredit']}"

                event.recurring = True
                event.recurrences = f"FREQ=WEEKLY;UNTIL={end_date.replace('-', '')}"

                cal.events.add(event)

    return str(cal)

def validate_csv_for_class_section(csv_data):
    required_columns = ['section', 'title', 'minCredit', 'secCap', 'room', 'bldg', 'weekDays', 'csmStart', 'csmEnd', 'faculty1']
    optional_columns = ['hold', 'restrictions', 'blockedTimeSlots', 'weekDays']

    # Check if the list is not empty and is a list of dictionaries
    if not csv_data or not isinstance(csv_data, list) or not all(isinstance(item, dict) for item in csv_data):
        return "CSV data is empty or not in the expected format (list of dictionaries).", False

    # Check if there's at least one row in the data
    if not csv_data:
        return "CSV data is empty.", False

    # Check the keys in the first row (dictionary) of csv_data
    first_row_keys = csv_data[0].keys()
    missing_columns = [col for col in required_columns if col not in first_row_keys]
    
    if missing_columns:
        return f"Missing required columns: {', '.join(missing_columns)}", False

    return "CSV data is valid for ClassSection.", True



@app.route('/get_csv', methods=['GET'])
def get_csv():
    key = request.args.get('key')
    file_path = f'optimization_results/{key}.json'
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'Invalid or missing key'}), 400

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        schedule = data['sorted_schedule']

    csv_content = convert_schedule_to_csv(schedule)

    response = make_response(csv_content)
    response.headers["Content-Disposition"] = f"attachment; filename=schedule_{key}.csv"
    response.headers["Content-Type"] = "text/csv"
    return response

def convert_schedule_to_csv(schedule):
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Section', 'Timeslot', 'Faculty', 'Room', 'Building'])  # Add other headers as needed
    for entry in schedule:
        cw.writerow([entry['section'], entry['timeslot'], entry['faculty1'], entry['room'], entry['bldg']])  # Match with your data structure
    return si.getvalue()


@app.route('/optimize', methods=['POST'])
def optimize():
    try:
    
        global global_settings
        data = request.get_json()
        
        unique_key = str(uuid.uuid4())
        
        global_settings['class_sections_data'] = data.get('classData', [])
        global_settings['class_penalty'] = data.get('classPenalty', 0)
        global_settings['move_penalty'] = data.get('movePenalty', 0)
        global_settings['blocked_slot_penalty'] = data.get('blockedSlotPenalty', 0)
        global_settings['hold_penalty'] = data.get('holdPenalty', 0)
        
        
        message, is_valid = validate_csv_for_class_section(global_settings['class_sections_data'])
        
        if not is_valid:
            return jsonify({'message':  message }), 400

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
        
        pulp_score = "Successfully optimized"

        
        #marked_combined_expanded_schedule
        all_schedules = ({'schedule': combined_expanded_schedule, 'score': pulp_score, 'algorithm': 'PuLP', 'slot_differences': 0})

        #all_schedules_sorted = sorted(all_schedules, key=lambda x: x['score'])
        all_schedules_sorted = all_schedules
        final_schedule = group_and_update_schedule(all_schedules_sorted)


        
        final_results = {
            'unique_key': unique_key,
            'sorted_schedule': final_schedule,
            'calendar_events': calendar_events,
            
            'message': 'Optimization completed'
        }
        
        write_results_to_json(unique_key, final_results)

        return jsonify(final_results)

    except Exception as e:
            # Handle specific exceptions or general exceptions
            error_message = f"Error: {str(e)}"  # Format the message based on the exception type
            return jsonify({'message': error_message}), 400



def write_results_to_json(key, results):
    # Define a directory to store the JSON files
    directory = 'optimization_results'
    if not os.path.exists(directory):
        os.makedirs(directory)

    filepath = os.path.join(directory, f"{key}.json")
    with open(filepath, 'w') as json_file:
        json.dump(results, json_file, indent=4)


def divide_schedules_by_credit(schedule, credit_threshold=3):
    three_credit_classes = []
    remaining_classes = []
    section_groupings = {}

    for class_section in schedule:
        base_section_name = class_section['section'].split('_')[0]
        section_groupings.setdefault(base_section_name, []).append(class_section)

    for base_section_name, sections in section_groupings.items():
        if any(int(cls['minCredit']) >= credit_threshold for cls in sections):
            mwf_time, tuth_time = get_most_common_start_times(sections)
            if mwf_time:
                mwf_sections = [cls for cls in sections if 'M' in cls['timeslot'] or 'W' in cls['timeslot'] or 'F' in cls['timeslot']]
                if mwf_sections:
                    three_credit_classes.append({
                        'section': base_section_name,
                        'timeslot': 'M W F - ' + mwf_time,
                        'minCredit': mwf_sections[0]['minCredit'],
                        'faculty1': mwf_sections[0]['faculty1'],
                        'room': mwf_sections[0]['room'],
                        'bldg': mwf_sections[0]['bldg'],
                        'secCap': mwf_sections[0]['secCap']
                    })
            if tuth_time:
                tuth_sections = [cls for cls in sections if 'Tu' in cls['timeslot'] or 'Th' in cls['timeslot']]
                if tuth_sections:
                    three_credit_classes.append({
                        'section': base_section_name,
                        'timeslot': 'Tu Th - ' + tuth_time,
                        'minCredit': tuth_sections[0]['minCredit'],
                        'faculty1': mwf_sections[0]['faculty1'],
                        'room': mwf_sections[0]['room'],
                        'bldg': mwf_sections[0]['bldg'],
                        'secCap': mwf_sections[0]['secCap']
                    })
        else:
            remaining_classes.extend(sections)

    return three_credit_classes, remaining_classes


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
