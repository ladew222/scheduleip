from flask import Flask, render_template, request, redirect, url_for
import pulp
import re
import csv


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




# Define your ClassSection class here (with attributes and methods)
class ClassSection:
    def __init__(self, term, section, title, location, meeting_info, faculty, capacity, status, credits, academic_level, restrictions):
        self.term = term
        self.section = section
        self.title = title
        self.location = location
        self.meeting_info = meeting_info
        self.faculty = faculty
        self.capacity = int(capacity.split('/')[0].strip())  # Extract the capacity as an integer
        self.status = status
        self.credits = float(credits)
        self.academic_level = academic_level
        self.restrictions = restrictions.strip().split(', ') if restrictions else []  # Extract restrictions as a list

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
        if days == "MWF" and credits <= 3:
            time_blocks = ["8:00AM - 8:55AM", "9:05AM - 10:00AM", "10:10AM - 11:05AM", "11:15AM - 12:10PM", "12:20PM - 1:15PM", "1:25PM - 2:20PM", "2:30PM - 3:25PM", "3:35PM - 4:30PM"]
        elif days == "MWF" and credits > 3:
            time_blocks = ["11:15AM - 12:10PM", "12:20PM - 1:15PM", "1:25PM - 2:20PM", "2:30PM - 3:25PM", "3:35PM - 4:30PM"]
        elif days == "TTh" and credits <= 3:
            time_blocks = ["8:00AM - 9:20AM", "9:30AM - 10:50AM", "11:00AM - 12:20PM", "12:30PM - 1:50PM", "2:00PM - 3:20PM", "3:30PM - 4:50PM"]
        elif days == "TTh" and credits > 3:
            time_blocks = ["11:00AM - 12:20PM", "12:30PM - 1:50PM", "2:00PM - 3:20PM", "3:30PM - 4:50PM"]

        return time_blocks


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
                          for day in ["MWF", "TTh"]
                          for start_time in meeting_times.choose_time_blocks(class_section.days, class_section.credits)),
        cat=pulp.LpBinary
    )

    # Create an optimization problem
    model = pulp.LpProblem("ClassScheduling", pulp.LpMinimize)

    # Define constraints (You need to specify your constraints here)
    # Constraint 1: Each class is scheduled once and only once
    for class_section in class_sections:
        model += pulp.lpSum(class_timeslots[class_section.section, day, start_time]
                            for day in ["MWF", "TTh"]
                            for start_time in meeting_times.choose_time_blocks(class_section.days, class_section.credits)) == 1

    # Constraint 2: Instructor constraints (each instructor can teach one class at a time)
    instructors = set(class_section.faculty for class_section in class_sections)
    for instructor in instructors:
        model += pulp.lpSum(class_timeslots[class_section.section, day, start_time]
                            for class_section in class_sections
                            for day in ["MWF", "TTh"]
                            for start_time in meeting_times.choose_time_blocks(class_section.days, class_section.credits)
                            if class_section.faculty == instructor) <= 1

    # Constraint 3: Avoid class overlaps (hard constraint)
    for day in ["MWF", "TTh"]:
        for start_time in meeting_times.choose_time_blocks("MWF", 3):
            model += pulp.lpSum(class_timeslots[class_section.section, day, start_time] for class_section in class_sections) <= 1

    # Constraint 4: Penalize having too many classes in the same time block (encourage distribution)
    for day in ["MWF", "TTh"]:
        for start_time in meeting_times.choose_time_blocks("MWF", 3):
            model += pulp.lpSum(class_timeslots[class_section.section, day, start_time] for class_section in class_sections) <= 2


    # Constraint 5: Penalize classes that intersect and have one of each other in avoid_classes
    for class_section in class_sections:
        for other_class_section in class_sections:
            if class_section != other_class_section and class_section.section in other_class_section.avoid_classes:
                for day in ["MWF", "TTh"]:
                    for start_time in meeting_times.choose_time_blocks(class_section.days, class_section.credits):
                        model += class_timeslots[class_section.section, day, start_time] + class_timeslots[other_class_section.section, day, start_time] <= 1
    
    # Constraint 6: Avoid unwanted timeslots
    for class_section in class_sections:
        for day in ["MWF", "TTh"]:
            for start_time in class_section.unwanted_timeslots:
                model += pulp.lpSum(class_timeslots[class_section.section, day, start_time] for day in [day]) == 0


    # Solve the optimization problem
    model.solve()
    
    # Interpret the results and generate the final schedule
    update_class_sections_with_schedule(class_sections, class_timeslots, meeting_times)

    # Interpret the results and generate the final schedule
    for class_section in class_sections:
        for day in ["MWF", "TTh"]:
            for start_time in meeting_times.choose_time_blocks(class_section.days, class_section.credits):
                if class_timeslots[class_section.section, day, start_time].varValue == 1:
                    # This class_section is scheduled for the specified day and time slot
                    # You can update class_section properties accordingly
                    pass

    # Now, class_sections contain the final schedule information based on the optimization results.
    return class_sections

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        # Check if the file is empty
        if file.filename == '':
            return redirect(request.url)

        if file:
            # Save the uploaded file to a temporary location (you can change this as needed)
            file_path = '/tmp/uploaded_schedule.csv'
            file.save(file_path)

            # Read CSV and create ClassSection objects
            class_sections = read_csv_and_create_class_sections(file_path)

            # Create a MeetingTimes object based on your meeting time data
            # Replace the following line with your actual meeting time data
            your_meeting_time_data = create_meeting_times()  # Replace with your meeting time data
            meeting_times = MeetingTimes(create_meeting_times())
    return render_template('index.html')

def index():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        # Check if the file is empty
        if file.filename == '':
            return redirect(request.url)

        if file:
            # Save the uploaded file to a temporary location (you can change this as needed)
            file_path = '/tmp/uploaded_schedule.csv'
            file.save(file_path)

            # Read CSV and create ClassSection objects
            class_sections = read_csv_and_create_class_sections(file_path)

            # Create a MeetingTimes object based on your meeting time data
            # Replace the following line with your actual meeting time data
            your_meeting_time_data = create_meeting_times()  # Replace with your meeting time data
            meeting_times = MeetingTimes(create_meeting_times())

            # Call the optimization function
            optimize_schedule(class_sections, meeting_times)

            # You can render a template to display the results or return them in JSON format, etc.
            # For now, let's return a simple message
            return "Optimization complete. Check the results!"

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
