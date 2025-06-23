import datetime
import math

def check_valid_date(year: int, month: int, day: int):
    '''
    Checks if year, month, day is a valid date
    '''
    if year <= 0:
        # Year must be positive
        return False
    
    if not (1 <= month <= 12):
        # Month must be between 1 to 12
        return False

    # Initialise a list that stores the number of days in each month
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        # Year is a leap year, days in February should be 29
        days_in_month[1] = 29

    # Since year and month have already been checked before, if the day is valid
    # the date would be valid
    return 1 <= day <= days_in_month[month-1]


class Participant:
    def __init__(self, name: str, idi: int, birth_year: int, birth_month: int,
                 birth_day: int, gender: str):
        '''
        Constructs a Participant object
        Attributes other than name and idi have been made private.
        '''
        self.name = name
        self.idi = idi
        self.__birth_year = birth_year
        self.__birth_month = birth_month
        self.__birth_day = birth_day
        self.__gender = gender

    def get_values(self) -> None:
        '''Returns all attributes of the participant as a tuple'''
        return (self.name, self.idi, self.__birth_year, self.__birth_month,
                self.__birth_day, self.__gender)

    def show_values(self)  -> None:
        '''Prints all details of Participant for easy human-readable display'''
        print(f"Name:\t\t{self.name}")
        print(f"ID:\t\t{self.idi}")
        print(f"Birth Year:\t{self.__birth_year}")
        print(f"Birth Month:\t{self.__birth_month}")
        print(f"Birth Day:\t{self.__birth_day}")
        print(f"Gender:\t\t{self.__gender}")

    def set_values(self, data_attributes: dict) -> None:
        '''
        Sets attributes
        
        First checks if all the attributes provided in data_attributes are valid.
        Once their validity is confirmed, we set those attributes.

        According to Piazza discussion, @414_f9, if there are other attributes in
        data_attributes that are not inside the class, they can be ignored.

        Hence, other data_attributes have been ignored.
        '''
        check_name = ("name" not in data_attributes
                         or type(data_attributes["name"]) == str)
                         
        check_idi = ("idi" not in data_attributes
                        or type(data_attributes["idi"]) == int)

        # To check valid birth date, first the types of the inputs are checked
        check_birth_year = ("birth_year" not in data_attributes
                               or type(data_attributes["birth_year"]) == int)

        check_birth_month = ("birth_month" not in data_attributes
                                or type(data_attributes["birth_month"]) == int)

        check_birth_day = ("birth_day" not in data_attributes
                                or type(data_attributes["birth_day"]) == int)

        # Check if birth date has been changed
        check_birth_date_changed = ("birth_year" in data_attributes
                                    or "birth_month" in data_attributes
                                    or "birth_day" in data_attributes)
        
        # Initially assume that new birth date is valid
        check_valid_birth_date = True
        
        if check_birth_date_changed:
            # Birth date has been changed. Construct new birth date and check if
            # it is valid
            new_birth_year = data_attributes.get("birth_year", self.__birth_year)
            new_birth_month = data_attributes.get("birth_month", self.__birth_month)
            new_birth_day = data_attributes.get("birth_day", self.__birth_day)
            check_valid_birth_date = check_valid_date(new_birth_year, new_birth_month, new_birth_day)

        check_gender = ("gender" not in data_attributes
                        or (type(data_attributes["gender"]) == str
                            and (data_attributes["gender"].lower() == "male"
                                or data_attributes["gender"].lower() == "female")))

        if not all([check_name, check_idi, check_birth_year, check_birth_month,
                    check_birth_day, check_valid_birth_date, check_gender]):
            # Invalid input
            return -1

        # Update values
        self.name = data_attributes.get("name", self.name)
        self.idi = data_attributes.get("idi", self.idi)
        self.__birth_year = data_attributes.get("birth_year", self.__birth_year)
        self.__birth_month = data_attributes.get("birth_month", self.__birth_month)
        self.__birth_day = data_attributes.get("birth_day", self.__birth_day)
        self.__gender = data_attributes.get("gender", self.__gender)

    def calculate_age(self, curr_day: int, curr_month: int, curr_year: int):
        '''Computes age using the current date. Returns age in years.'''
        
        # First check if the date supplied is a valid date
        if not check_valid_date(curr_year, curr_month, curr_day):
            return -1

        # Now if the date supplied occurs before the current date, it is invalid
        current_date = datetime.date(curr_year, curr_month, curr_day)
        birth_date = datetime.date(self.__birth_year, self.__birth_month, self.__birth_day)
        
        if current_date < birth_date:
            # Invalid input
            return -1

        # According to Piazza discussion @414_f21, the suggested way for
        # calculating age is using datetime and mathfloor
        
        # Calculate the number of days a person has been alive
        age_in_days = (current_date - birth_date).days

        # Return the age in years using math.floor (Each year has 365.25 days)
        # Comparing months, days and years would give a more accurate age in the
        # traditional sense. However, this is a acceptable approximation.
        # Also, the assignment specifies that we have to use math.floor
        return math.floor(age_in_days/365.25)


class Student(Participant):
    def __init__(self, name: str, idi: int, birth_year: int, birth_month: int,
                 birth_day: int, gender: str, grade_level: int,
                 class_assigned: str, gpa: float, selected_activity: str,
                 talent_score: float, athletic_score: float,
                 leadership_score: float):
        # Construct using parent class first
        super().__init__(name, idi, birth_year, birth_month, birth_day, gender)

        # Add the new variables
        self.__grade_level = grade_level
        self.__class_assigned = class_assigned
        self.__gpa = gpa
        self.__selected_activity = selected_activity
        self.__talent_score = talent_score
        self.__athletic_score = athletic_score
        self.__leadership_score = leadership_score

        # Add the derived variables
        self.__age = self.calculate_age(1, 1, 2025)
        self.is_eligible()

    def is_eligible(self) -> bool:
        '''Calculates eligibility based on GPA and updates eligible feature'''
        # Determine if student is eligible
        eligible = self.__gpa >= 5.0

        # Update the eligible feature
        self.__eligible = eligible

        # Return the eligibility
        return eligible

    def get_values(self) -> tuple:
        '''Returns all inherited and new attributes as a tuple'''

        # Get the inherited_attributes
        inherited_attributes = super().get_values()

        # Make a tuple of new attributes
        new_attributes = (self.__age, self.__grade_level, self.__class_assigned,
                          self.__gpa, self.__selected_activity,
                          self.__talent_score, self.__athletic_score,
                          self.__leadership_score, self.__eligible)

        # Return the combined attributes
        return inherited_attributes + new_attributes

    def show_values(self) -> None:
        '''Prints all the student details, including those from Participant'''

        # Print student details from Participant
        super().show_values()

        # Print the new attributes
        print(f"Age:\t\t{self.__age}")
        print(f"Grade Level:\t{self.__grade_level}")
        print(f"Class Assigned:\t{self.__class_assigned}")
        print(f"GPA:\t\t{self.__gpa}")
        print(f"Selected Activity:\t{self.__selected_activity}")
        print(f"Talent Score:\t{self.__talent_score}")
        print(f"Athletic Score:\t{self.__athletic_score}")
        print(f"Leadership Score:\t{self.__leadership_score}")
        print(f"Eligible:\t{self.__eligible}")

    def set_values(self, data_attributes: dict) -> None:
        '''Sets both inherited and new attributes and updates derived attributes.'''
        # According to Piazza discussion @414_f27 contradicting values won't be
        # passed in data_attributes, so we can just ignore if any "age"
        # or "eligible" parameter is passed and hence the below code is no
        # longer needed.
        # if "age" in data_attributes or "eligible" in data_attributes:
        #     # age and eligible are derived attributes calculated using
        #     # calculate_age and is_eligible respectively and cannot be just set
        #     # using set_values
        #     return -1

        # First check if the new attributes are valid attributes or not
        
        # Grade level should be between 1 and 12
        check_grade_level = ("grade_level" not in data_attributes
                             or (type(data_attributes["grade_level"]) == int
                                 and 1 <= data_attributes["grade_level"] <= 12))

        check_class_assigned = ("class_assigned" not in data_attributes
                                or type(data_attributes["class_assigned"]) == str)

        # GPA cannot be more than 10 or less than 0
        check_gpa = ("gpa" not in data_attributes
                     or (type(data_attributes["gpa"]) == float
                         and 0.0 <= data_attributes["gpa"] <= 10.0))

        # selected_activity must be one of "Sports", "Talent", "Academic"
        check_selected_activity = ("selected_activity" not in data_attributes
                                   or (type(data_attributes["selected_activity"]) == str
                                       and (data_attributes["selected_activity"] == "Sports"
                                            or data_attributes["selected_activity"] == "Talent"
                                            or data_attributes["selected_activity"] == "Academic")))

        check_talent_score = ("talent_score" not in data_attributes
                              or type(data_attributes["talent_score"]) == float)

        check_athletic_score = ("athletic_score" not in data_attributes
                                or type(data_attributes["athletic_score"]) == float)

        check_leadership_score = ("leadership_score" not in data_attributes
                                  or type(data_attributes["leadership_score"]) == float)

        if not all([check_grade_level, check_class_assigned, check_gpa,
                    check_selected_activity, check_talent_score,
                    check_athletic_score, check_leadership_score]):
            # Invalid input
            return -1

        # Set inherited values. If this returns -1, then new values for inherited
        # values are not correct
        if super().set_values(data_attributes) == -1:
            return -1

        # If code reaches here, it means that inherited values have been set
        # Now set the new attributes
        self.__grade_level = data_attributes.get("grade_level", self.__grade_level)
        self.__class_assigned = data_attributes.get("class_assigned", self.__class_assigned)
        self.__gpa = data_attributes.get("gpa", self.__gpa)
        self.__selected_activity = data_attributes.get("selected_activity", self.__selected_activity)
        self.__talent_score = data_attributes.get("talent_score", self.__talent_score)
        self.__athletic_score = data_attributes.get("athletic_score", self.__athletic_score)
        self.__leadership_score = data_attributes.get("leadership_score", self.__leadership_score)

        # Update the derived attributes age and eligible
        self.__age = self.calculate_age(1, 1, 2025)
        self.is_eligible()


class Teacher(Participant):
    def __init__(self, name: str, idi: int, birth_year: int, birth_month: int,
                 birth_day: int, gender: str, subject: str, mentor_grade: int,
                 mentor_class: str, judge: bool):
        # Construct using parent class first
        super().__init__(name, idi, birth_year, birth_month, birth_day, gender)

        # Add the new variables
        self.__subject = subject
        self.__mentor_grade = mentor_grade
        self.__mentor_class = mentor_class
        self.__judge = judge

    def get_values(self) -> tuple:
        '''
        Retrieves all the teacher’s details along with inherited
        participant details
        '''

        # Get the inherited_attributes
        inherited_attributes = super().get_values()

        # Make a tuple of new attributes
        new_attributes = (self.__subject, self.__mentor_grade,
                          self.__mentor_class, self.__judge)

        # Return the combined attributes
        return inherited_attributes + new_attributes

    def show_values(self) -> None:
        '''Displays all the teacher’s details in a user-friendly format.'''

        # Print teacher details from Participant
        super().show_values()

        # Print the new attributes
        print(f"Subject:\t{self.__subject}")
        print(f"Mentor Grade:\t{self.__mentor_grade}")
        print(f"Mentor Class:\t{self.__mentor_class}")
        print(f"Judge:\t\t{self.__judge}")

    def set_values(self, data_attributes: dict) -> None:
        '''Sets both inherited and new attributes'''

        # First check if the new attributes are valid attributes or not

        check_subject = ("subject" not in data_attributes
                         or type(data_attributes["subject"]) == str)

        # Mentor grade should be between 1 and 12
        check_mentor_grade = ("mentor_grade" not in data_attributes
                              or (type(data_attributes["mentor_grade"]) == int
                                  and 1 <= data_attributes["mentor_grade"] <= 12))

        check_mentor_class = ("mentor_class" not in data_attributes
                              or type(data_attributes["mentor_class"]) == str)

        check_judge = ("judge" not in data_attributes
                        or type(data_attributes["judge"]) == bool)

        if not all([check_subject, check_mentor_grade, check_mentor_class,
                    check_judge]):
            # Invalid input
            return -1

        # Set inherited values. If this returns -1, then new values for inherited
        # values are not correct
        if super().set_values(data_attributes) == -1:
            return -1

        # If code reaches here, it means that inherited values have been set
        # Now set the new attributes
        self.__subject = data_attributes.get("subject", self.__subject)
        self.__mentor_grade = data_attributes.get("mentor_grade", self.__mentor_grade)
        self.__mentor_class = data_attributes.get("mentor_class", self.__mentor_class)
        self.__judge = data_attributes.get("judge", self.__judge)


class Artist(Student):
    def __init__(self, name: str, idi: int, birth_year: int, birth_month: int,
                 birth_day: int, gender: str, grade_level: int,
                 class_assigned: str, gpa: float, selected_activity: str,
                 talent_score: float, athletic_score: float,
                 leadership_score: float, talent: str):
        # Construct using parent class first
        super().__init__(name, idi, birth_year, birth_month, birth_day, gender,
                         grade_level, class_assigned, gpa, selected_activity,
                         talent_score, athletic_score, leadership_score)

        # Add the new attributes
        # It is given that performance_level is same as talent_score
        self.__performance_level = talent_score
        self.__talent = talent

    def compute_scores(self) -> float:
        '''Returns the score of the student if the student is eligible'''
        
        if self.is_eligible():
            # Student is eligible. Their score is their performance level.
            return self.__performance_level
        else:
            # Student is not eligible. Fail condition
            return -1
        
    def is_eligible(self) -> bool:
        '''
        Calculates eligibility based on GPA and age and sets the value of data
        member eligible.
        '''
        # Determine if student is eligible
        eligible = self._Student__gpa > 6.0 and self._Student__age >= 16

        # Update the eligible feature
        self._Student__eligible = eligible

        # Return the eligibility
        return eligible

    def get_values(self) -> tuple:
        '''
        Retrieves all artist details along with inherited participant details.
        '''
        # Get the inherited_attributes
        inherited_attributes = super().get_values()

        # Make a tuple of new attributes
        new_attributes = (self.__performance_level, self.__talent)

        # Return the combined attributes
        return inherited_attributes + new_attributes

    def show_values(self) -> None:
        '''Displays all attributes details in a user-friendly format.'''
        # Print artist details from Student
        super().show_values()

        # Print the new attributes
        print(f"Performance level:\t{self.__performance_level}")
        print(f"Talent:\t\t{self.__talent}")

    def set_values(self, data_attributes: dict) -> None:
        '''Sets both inherited and new attributes.'''
        # First make sure contradicting values are not given
        if ("talent_score" in data_attributes
            and "performance_level" in data_attributes
            and data_attributes["talent_score"] != data_attributes["performance_level"]):
            # Invalid input
            return -1

        # This new_data_attributes will be passed along to the parent class and hence
        # if the performance_level changes, the talent_score should change accordingly
        new_data_attributes = data_attributes.copy()
        if "talent_score" in data_attributes:
            new_data_attributes["performance_level"] = data_attributes["talent_score"]
        elif "performance_level" in data_attributes:
            new_data_attributes["talent_score"] = data_attributes["performance_level"]

        
        # Now check if the new attributes are valid attributes or not
        check_performance_level = ("performance_level" not in new_data_attributes
                              or type(new_data_attributes["performance_level"]) == float)
        
        check_talent = ("talent" not in new_data_attributes
                        or type(new_data_attributes["talent"]) == str)

        # Also, for Artist, the selected_activity should be Talent
        check_selected_activity = ("selected_activity" not in new_data_attributes
                                   or new_data_attributes["selected_activity"] == "Talent")
        
        if not all([check_performance_level, check_talent, check_selected_activity]):
            # Invalid input
            return -1

        # Set inherited values. If this returns -1, then new values for
        # inherited values are not correct
        if super().set_values(new_data_attributes) == -1:
            return -1

        # If code reaches here, it means that inherited values have been set
        # Now set the new attributes
        self.__performance_level = new_data_attributes.get("performance_level", self.__performance_level)
        self.__talent = new_data_attributes.get("talent", self.__talent)
        

class Athlete(Student):
    def __init__(self, name: str, idi: int, birth_year: int, birth_month: int,
                 birth_day: int, gender: str, grade_level: int,
                 class_assigned: str, gpa: float, selected_activity: str,
                 talent_score: float, athletic_score: float,
                 leadership_score: float, sports_category: str,
                 fitness_score: float):
        # Construct using parent class first
        super().__init__(name, idi, birth_year, birth_month, birth_day, gender,
                         grade_level, class_assigned, gpa, selected_activity,
                         talent_score, athletic_score, leadership_score)

        # Add the new attributes
        self.__sports_category = sports_category
        self.__fitness_score = fitness_score

        # It is given that performance_level is same as athletic_score
        self.__performance_level = athletic_score

    def compute_scores(self) -> float:
        '''Returns the score of the student if the student is eligible'''
        
        if self.is_eligible():
            # Student is eligible. Their score is their fitness_score times the
            # performance_level.
            return self.__fitness_score * self.__performance_level
        else:
            # Student is not eligible. Fail condition
            return -1
        
    def is_eligible(self) -> bool:
        '''
        Calculates eligibility based on GPA and age and sets the value of data
        member eligible.
        '''
        # Determine if student is eligible
        eligible = self._Student__gpa > 5.5 and self._Student__age >= 12

        # Update the eligible feature
        self._Student__eligible = eligible

        # Return the eligibility
        return eligible

    def get_values(self) -> tuple:
        '''
        Retrieves all athlete details along with inherited participant details.
        '''
        # Get the inherited_attributes
        inherited_attributes = super().get_values()

        # Make a tuple of new attributes
        new_attributes = (self.__sports_category, self.__fitness_score,
                          self.__performance_level)

        # Return the combined attributes
        return inherited_attributes + new_attributes

    def show_values(self) -> None:
        '''Displays all attributes details in a user-friendly format.'''
        # Print athlete details from Student
        super().show_values()

        # Print the new attributes
        print(f"Sports Category:\t{self.__sports_category}")
        print(f"Fitness Score:\t{self.__fitness_score}")
        print(f"Performance level:\t{self.__performance_level}")

    def set_values(self, data_attributes: dict) -> None:
        '''Sets both inherited and new attributes.'''
        # First make sure contradicting values are not given
        if ("athletic_score" in data_attributes
            and "performance_level" in data_attributes
            and data_attributes["athletic_score"] != data_attributes["performance_level"]):
            # Invalid input
            return -1

        # This new_data_attributes will be passed along to the parent class and hence
        # if the performance_level changes, the athletic_score should change accordingly
        new_data_attributes = data_attributes.copy()
        if "athletic_score" in data_attributes:
            new_data_attributes["performance_level"] = data_attributes["athletic_score"]
        elif "performance_level" in data_attributes:
            new_data_attributes["athletic_score"] = data_attributes["performance_level"]

        
        # Now check if the new attributes are valid attributes or not
        check_sports_category = ("sports_category" not in new_data_attributes
                        or type(new_data_attributes["sports_category"]) == str)

        check_fitness_score = ("fitness_score" not in new_data_attributes
                              or type(new_data_attributes["fitness_score"]) == float)
        
        check_performance_level = ("performance_level" not in new_data_attributes
                              or type(new_data_attributes["performance_level"]) == float)
        

        # Also, for Athlete, the selected_activity should be Sports
        check_selected_activity = ("selected_activity" not in new_data_attributes
                                   or new_data_attributes["selected_activity"] == "Sports")
        
        if not all([check_sports_category, check_fitness_score,
                    check_performance_level, check_selected_activity]):
            # Invalid input
            return -1

        # Set inherited values. If this returns -1, then new values for
        # inherited values are not correct
        if super().set_values(new_data_attributes) == -1:
            return -1

        # If code reaches here, it means that inherited values have been set
        # Now set the new attributes
        self.__sports_category = new_data_attributes.get("sports_category", self.__sports_category)
        self.__fitness_score = new_data_attributes.get("fitness_score", self.__fitness_score)
        self.__performance_level = new_data_attributes.get("performance_level", self.__performance_level)
        

class Scholar(Student):
    def __init__(self, name: str, idi: int, birth_year: int, birth_month: int,
                 birth_day: int, gender: str, grade_level: int,
                 class_assigned: str, gpa: float, selected_activity: str,
                 talent_score: float, athletic_score: float,
                 leadership_score: float, subject_specialization: str,
                 olympiad_scores: list[float]):
        self.__olympiad_scores = olympiad_scores
        
        # Construct using parent class
        super().__init__(name, idi, birth_year, birth_month, birth_day, gender,
                         grade_level, class_assigned, gpa, selected_activity,
                         talent_score, athletic_score, leadership_score)

        # Add the new attributes
        self.__subject_specialization = subject_specialization

        # It is given that performance_level is defined as GPA * 10
        self.__performance_level = gpa * 10

    def compute_scores(self) -> float:
        '''Returns the score of the student if the student is eligible'''
        if self.is_eligible():
            # Student is eligible. Their score is their olympiad_scores times
            # the performance_level.
            return sum(self.__olympiad_scores) * self.__performance_level
        else:
            # Student is not eligible. Fail condition
            return -1
        
    def is_eligible(self) -> bool:
        '''
        Calculates eligibility based on GPA, olympiad_scores and age and sets
        the value of data member eligible.
        '''
        # Determine if student is eligible
        eligible = (self._Student__gpa > 8.0 and self._Student__age >= 10
                    and any([score > 80 for score in self.__olympiad_scores]))

        # Update the eligible feature
        self._Student__eligible = eligible

        # Return the eligibility
        return eligible

    def get_values(self) -> tuple:
        '''
        Retrieves all academic details along with inherited participant details.
        '''
        # Get the inherited_attributes
        inherited_attributes = super().get_values()

        # Make a tuple of new attributes
        new_attributes = (self.__subject_specialization, self.__olympiad_scores,
                          self.__performance_level)

        # Return the combined attributes
        return inherited_attributes + new_attributes

    def show_values(self) -> None:
        '''Displays all attributes details in a user-friendly format.'''
        # Print scholar details from Student
        super().show_values()

        # Print the new attributes
        print(f"Subject Specialization:\t{self.__subject_specialization}")
        print(f"Olympiad Scores:\t{self.__olympiad_scores}")
        print(f"Performance level:\t{self.__performance_level}")

    def set_values(self, data_attributes: dict) -> None:
        '''Sets both inherited and new attributes.'''
        # First make sure contradicting values are not given
        if ("gpa" in data_attributes
            and "performance_level" in data_attributes
            and data_attributes["gpa"] * 10 != data_attributes["performance_level"]):
            # Invalid input
            return -1

        # This new_data_attributes will be passed along to the parent class and hence
        # if the performance_level changes, the gpa should change accordingly
        new_data_attributes = data_attributes.copy()
        if "gpa" in data_attributes:
            new_data_attributes["performance_level"] = data_attributes["gpa"] * 10
        elif "performance_level" in data_attributes:
            new_data_attributes["gpa"] = data_attributes["performance_level"] / 10

        
        # Now check if the new attributes are valid attributes or not
        check_subject_specialization = ("subject_specialization" not in new_data_attributes
                        or type(new_data_attributes["subject_specialization"]) == str)

        check_olympiad_scores = ("olympiad_scores" not in new_data_attributes
                              or (type(new_data_attributes["olympiad_scores"]) == list
                                  and all([type(i) == float for i in new_data_attributes["olympiad_scores"]])))
        
        
        check_performance_level = ("performance_level" not in new_data_attributes
                              or type(new_data_attributes["performance_level"]) == float)
        

        # Also, for Scholar, the selected_activity should be Academic
        check_selected_activity = ("selected_activity" not in new_data_attributes
                                   or new_data_attributes["selected_activity"] == "Academic")
        
        if not all([check_subject_specialization, check_olympiad_scores,
                    check_performance_level, check_selected_activity]):
            # Invalid input
            return -1

        # Set inherited values. If this returns -1, then new values for
        # inherited values are not correct
        if super().set_values(new_data_attributes) == -1:
            return -1

        # If code reaches here, it means that inherited values have been set
        # Now set the new attributes
        self.__subject_specialization = new_data_attributes.get("subject_specialization", self.__subject_specialization)
        self.__olympiad_scores = new_data_attributes.get("olympiad_scores", self.__olympiad_scores)
        self.__performance_level = new_data_attributes.get("performance_level", self.__performance_level)
        

class Activity:
    def __init__(self, activity_id: int, activity_name: str, activity_type: str,
                 max_participants: int, grade_level: int, is_active: bool,
                 participants: list[Student], organizers: list[Teacher]):
        '''
        Constructs the Activity object.
        Attributes other than activity_id and activity_name have been made
        private.
        '''
        self.activity_id = activity_id
        self.activity_name = activity_name
        self.__activity_type = activity_type
        self.__max_participants = max_participants
        self.__grade_level = grade_level
        self.__is_active = is_active
        self.__participants = participants
        self.__organizers = organizers

    def get_values(self) -> tuple:
        '''Return all attributes of the activity as a tuple.'''

        # Converts the students and teachers to their names for readability
        return (self.activity_id, self.activity_name, self.__activity_type,
                self.__max_participants, self.__grade_level, self.__is_active,
                [st.name for st in self.__participants],
                [te.name for te in self.__organizers])

    def show_values(self) -> None:
        '''
        Prints all the activity details in a user-friendly format.
        '''
        print(f"Activity ID:\t\t{self.activity_id}")
        print(f"Activity Name:\t\t{self.activity_name}")
        print(f"Activity Type:\t\t{self.__activity_type}")
        print(f"Max Participants:\t{self.__max_participants}")
        print(f"Grade Level:\t\t{self.__grade_level}")
        print(f"Active:\t\t\t{self.__is_active}")
        print(f"Participants:\t\t{[st.name for st in self.__participants]}")
        print(f"Organizers:\t\t{[te.name for te in self.__organizers]}")

    def set_values(self, data_attributes: dict) -> None:
        '''Sets attributes'''
        # First check if the attributes provided are correct
        check_activity_id = ("activity_id" not in data_attributes
                             or type(data_attributes["activity_id"]) == int)

        check_activity_name = ("activity_name" not in data_attributes
                             or type(data_attributes["activity_name"]) == str)

        check_activity_type = ("activity_type" not in data_attributes
                                or (type(data_attributes["activity_type"]) == str
                                    and (data_attributes["activity_type"] == "Sports"
                                        or data_attributes["activity_type"] == "Talent"
                                        or data_attributes["activity_type"] == "Academic")))

        check_max_participants = ("max_participants" not in data_attributes
                             or type(data_attributes["max_participants"]) == int)

        check_grade_level = ("grade_level" not in data_attributes
                             or type(data_attributes["grade_level"]) == int)

        check_is_active = ("is_active" not in data_attributes
                         or type(data_attributes["is_active"]) == bool)

        check_participants = ("participants" not in data_attributes
                             or (type(data_attributes["participants"]) == list
                                 and all([isinstance(p, Student) for p in data_attributes["participants"]])))

        check_organizers = ("organizers" not in data_attributes
                             or (type(data_attributes["organizers"]) == list
                                 and all([isinstance(o, Teacher) for o in data_attributes["organizers"]])))


        if not all([check_activity_id, check_activity_name, check_activity_type,
                    check_max_participants, check_grade_level, check_is_active,
                    check_participants, check_organizers]):
            # Invalid input
            return -1

        # Update Values
        self.activity_id = data_attributes.get("activity_id", self.activity_id)
        self.activity_name = data_attributes.get("activity_name", self.activity_name)
        self.__activity_type = data_attributes.get("activity_type", self.__activity_type)
        self.__max_participants = data_attributes.get("max_participants", self.__max_participants)
        self.__grade_level = data_attributes.get("grade_level", self.__grade_level)
        self.__is_active = data_attributes.get("is_active", self.__is_active)
        self.__participants = data_attributes.get("participants", self.__participants)
        self.__organizers = data_attributes.get("organizers", self.__organizers)
        

class SportsTournament(Activity):
    def __init__(self, activity_id: int, activity_name: str, activity_type: str,
                 max_participants: int, grade_level: int, is_active: bool,
                 participants: list[Athlete], organizers: list[Teacher],
                 game_type: str, duration_minutes: int):
        # Construct using parent class first
        super().__init__(activity_id, activity_name, activity_type,
                         max_participants, grade_level, is_active, participants,
                         organizers)

        # Add the new variables
        self.__game_type = game_type
        self.__duration_minutes = duration_minutes

    def determine_winner(self) -> Athlete:
        participants = self._Activity__participants
        if len(participants) == 0:
            # Fail Condition
            return -1
        
        if self.__game_type == "Individual":
            valid_participants = [p for p in participants if p.is_eligible()]
            if len(valid_participants) == 0:
                # Fail condition
                return -1
            
            return max(valid_participants, key = lambda p: [p.compute_scores(), -p.idi])
        
        elif self.__game_type == "Team":
            teams = {}
            for athlete in participants:
                if athlete.is_eligible():
                    teams.setdefault(athlete._Student__class_assigned, [])
                    teams[athlete._Student__class_assigned].append(athlete)

            if len(teams) == 0:
                # Fail Condition
                return -1
            
            best_team = None
            best_team_avg = None
            for team_name in teams:
                team = teams[team_name]

                # Compute the team average
                team_avg = sum([p.compute_scores() for p in team])/len(team)

                # Update the best team if this team has better average
                if best_team_avg is None or team_avg > best_team_avg:
                    best_team = team
                    best_team_avg = team_avg

            # Return the athlete with highest score in the winning team
            return max(best_team, key = lambda p: [p.compute_scores(), -p.idi])

        else:
            # Invalid game type
            return -1

    def get_values(self) -> None:
        '''Returns all inherited and new attributes as a tuple'''

        # Get the inherited_attributes
        inherited_attributes = super().get_values()

        # Make a tuple of new attributes
        new_attributes = (self.__game_type, self.__duration_minutes)

        # Return the combined attributes
        return inherited_attributes + new_attributes

    def show_values(self) -> None:
        '''Prints all the activity details in a user-friendly format.'''
        # Print SportsTournament details from Activity
        super().show_values()

        # Print the new attributes
        print(f"Game Type:\t\t{self.__game_type}")
        print(f"Duration (in min):\t{self.__duration_minutes}")

    def set_values(self, data_attributes: dict) -> None:
        '''Sets both inherited and new attributes'''
        # First check if the attributes provided are correct
        check_game_type = ("game_type" not in data_attributes
                            or (type(data_attributes["game_type"]) == str
                                and (data_attributes["game_type"] == "Team"
                                    or data_attributes["game_type"] == "Individual")))

        check_duration_minutes = ("duration_minutes" not in data_attributes
                             or type(data_attributes["duration_minutes"]) == int)

        # All participants should be Athletes
        check_participants = ("participants" not in data_attributes
                             or (type(data_attributes["participants"]) == list
                                 and all([isinstance(p, Athlete) for p in data_attributes["participants"]])))

        # Activity type should be Sports
        check_activity_type = ("activity_type" not in data_attributes
                             or data_attributes["activity_type"] == "Sports")

        if not all([check_game_type, check_duration_minutes, check_participants,
                   check_activity_type]):
            # Invalid input
            return -1

        # Set inherited values. If this returns -1, then new values for
        # inherited values are not correct
        if super().set_values(data_attributes) == -1:
            return -1

        # If code reaches here, it means that inherited values have been set
        # Now set the new attributes
        self.__game_type = data_attributes.get("game_type", self.__game_type)
        self.__duration_minutes = data_attributes.get("duration_minutes", self.__duration_minutes)
        

class TalentShow(Activity):
    def __init__(self, activity_id: int, activity_name: str, activity_type: str,
                 max_participants: int, grade_level: int, is_active: bool,
                 participants: list[Artist], organizers: list[Teacher],
                 talent_categories: list):
        # Construct using parent class first
        super().__init__(activity_id, activity_name, activity_type,
                         max_participants, grade_level, is_active, participants,
                         organizers)

        # Add the new variables
        self.__talent_categories = talent_categories

    def evaluate_talent(self) -> Artist:
        participants = self._Activity__participants
        valid_participants = [p for p in participants if p.is_eligible()]
        if len(valid_participants) == 0:
                # Fail condition
                return -1

        return max(valid_participants, key = lambda p: [p.compute_scores(), -p.idi])

    def determine_winner(self) -> Artist:
        return self.evaluate_talent()
        
    def get_values(self) -> None:
        '''Returns all inherited and new attributes as a tuple'''

        # Get the inherited_attributes
        inherited_attributes = super().get_values()

        # Make a tuple of new attributes
        new_attributes = (self.__talent_categories,)

        # Return the combined attributes
        return inherited_attributes + new_attributes

    def show_values(self) -> None:
        '''Prints all the activity details in a user-friendly format.'''
        # Print TalentShow details from Activity
        super().show_values()

        # Print the new attributes
        print(f"Talent Categories:\t{self.__talent_categories}")

    def set_values(self, data_attributes: dict) -> None:
        '''Sets both inherited and new attributes'''
        # First check if the attributes provided are correct
        check_talent_categories = ("talent_categories" not in data_attributes
                            or (type(data_attributes["talent_categories"]) == list
                                and all([type(i) == str for i in data_attributes["talent_categories"]])))

        # All participants should be Artists
        check_participants = ("participants" not in data_attributes
                             or (type(data_attributes["participants"]) == list
                                 and all([isinstance(p, Artist) for p in data_attributes["participants"]])))

        # Activity type should be Talent
        check_activity_type = ("activity_type" not in data_attributes
                             or data_attributes["activity_type"] == "Talent")

        if not all([check_talent_categories, check_participants,
                    check_activity_type]):
            # Invalid input
            return -1

        # Set inherited values. If this returns -1, then new values for
        # inherited values are not correct
        if super().set_values(data_attributes) == -1:
            return -1

        # If code reaches here, it means that inherited values have been set
        # Now set the new attributes
        self.__talent_categories = data_attributes.get("talent_categories", self.__talent_categories)
        

class AcademicCompetition(Activity):
    def __init__(self, activity_id: int, activity_name: str, activity_type: str,
                 max_participants: int, grade_level: int, is_active: bool,
                 participants: list[Scholar], organizers: list[Teacher],
                 subjects: list, max_marks: float):
        # Construct using parent class first
        super().__init__(activity_id, activity_name, activity_type,
                         max_participants, grade_level, is_active, participants,
                         organizers)

        # Add the new variables
        self.__subjects = subjects
        self.__max_marks = max_marks

    def determine_winner(self) -> Scholar:
        participants = self._Activity__participants
        valid_participants = [p for p in participants if p.is_eligible()]
        if len(valid_participants) == 0:
                # Fail condition
                return -1

        return max(valid_participants, key = lambda p: [p.compute_scores(), -p.idi])
        
    def get_values(self) -> None:
        '''Returns all inherited and new attributes as a tuple'''

        # Get the inherited_attributes
        inherited_attributes = super().get_values()

        # Make a tuple of new attributes
        new_attributes = (self.__subjects, self.__max_marks)

        # Return the combined attributes
        return inherited_attributes + new_attributes

    def show_values(self) -> None:
        '''Prints all the activity details in a user-friendly format.'''
        # Print AcademicCompetition details from Activity
        super().show_values()

        # Print the new attributes
        print(f"Subjects:\t\t{self.__subjects}")
        print(f"Max Marks:\t\t{self.__max_marks}")

    def set_values(self, data_attributes: dict) -> None:
        '''Sets both inherited and new attributes'''
        # First check if the attributes provided are correct
        check_subjects = ("subjects" not in data_attributes
                        or (type(data_attributes["subjects"]) == list
                            and all([type(i) == str for i in data_attributes["subjects"]])))

        check_max_marks = ("max_marks" not in data_attributes
                           or type(data_attributes["max_marks"]) == float)
        
        # All participants should be Scholars
        check_participants = ("participants" not in data_attributes
                             or (type(data_attributes["participants"]) == list
                                 and all([isinstance(p, Scholar) for p in data_attributes["participants"]])))

        # Activity type should be Academic
        check_activity_type = ("activity_type" not in data_attributes
                             or data_attributes["activity_type"] == "Academic")

        if not all([check_subjects, check_max_marks,
                    check_participants, check_activity_type]):
            # Invalid input
            return -1

        # Set inherited values. If this returns -1, then new values for
        # inherited values are not correct
        if super().set_values(data_attributes) == -1:
            return -1

        # If code reaches here, it means that inherited values have been set
        # Now set the new attributes
        self.__subjects = data_attributes.get("subject", self.__subjects)
        self.__max_marks = data_attributes.get("max_marks", self.__max_marks)
###############################################################################

import csv

def load_participant_data(filepath: str):
    '''
    Loads the participant data and returns a tuple of lists of Students and
    Teachers
    '''
    with open(filepath, 'r') as f:
        # Makes a DictReader. This takes the first line (header) of the csv
        # file and converts it into keys of the dictionary
        reader = csv.DictReader(f)

        # Initialise students and teachers to empty lists
        students = []
        teachers = []
        
        for participant in reader:
            idi = int(participant["idi"])
            name = participant["name"]
            birth_year = int(participant["birth_year"])
            birth_month = int(participant["birth_month"])
            birth_day = int(participant["birth_day"])
            gender = participant["gender"]
            
            if participant["gpa"]:
                # participant is a Student
                athletic_score = float(participant["athletic_score"])
                leadership_score = float(participant["leadership_score"])
                talent_score = float(participant["talent_score"])
                gpa = float(participant["gpa"])
                class_assigned = participant["class_assigned"]
                selected_activity = participant["selected_activity"]
                grade_level = int(participant["grade_level"])

                student = Student(name, idi, birth_year, birth_month, birth_day,
                              gender, grade_level, class_assigned, gpa,
                              selected_activity, talent_score, athletic_score,
                              leadership_score)
                students.append(student)

            else:
                # participant is a Teacher
                subject = participant["subject"]
                mentor_grade = int(participant["mentor_grade"])
                mentor_class = participant["mentor_class"]
                judge = participant["judge"]

                if judge.strip().upper() == "TRUE":
                    judge = True
                elif judge.strip().upper() == "FALSE":
                    judge = False
                else:
                    # Invalid input
                    return -1

                teacher = Teacher(name, idi, birth_year, birth_month, birth_day,
                                  gender, subject, mentor_grade, mentor_class,
                                  judge)

                teachers.append(teacher)

    # Return in the specified form
    return (students, teachers)

def load_activities_data(filepath: str):
    '''
    Loads the activities data and returns a tuple of lists of SportsTournament,
    TalentShow and AcademicCompetition.
    '''
    with open(filepath, 'r') as f:
        # Makes a DictReader. This takes the first line (header) of the csv
        # file and converts it into keys of the dictionary
        reader = csv.DictReader(f)

        # Initialise sports_tournaments, talent_shows and academic_competitions
        # to empty lists
        sports_tournaments = []
        talent_shows = []
        academic_competitions = []
        
        for activity in reader:
            activity_id = int(activity["activity_id"])
            activity_name = activity["activity_name"]
            activity_type = activity["activity_type"]
            max_participants = int(activity["max_participants"])
            grade_level = int(activity["grade_level"])

            # Default values for is_active, participants and organizers
            is_active = False
            participants = []
            organizers = []

            if activity_type == "Sports":
                # It is a SportsTournament
                game_type = activity["game_type"]
                duration_minutes = int(activity["duration_minutes"])

                sports_tournament = SportsTournament(activity_id, activity_name,
                    activity_type, max_participants, grade_level, is_active,
                    participants, organizers, game_type, duration_minutes)

                sports_tournaments.append(sports_tournament)

            elif activity_type == "Talent":
                # It is a TalentShow
                talent_categories = activity["talent_categories"].split("-")

                talent_show = TalentShow(activity_id, activity_name,
                    activity_type, max_participants, grade_level, is_active,
                    participants, organizers, talent_categories)

                talent_shows.append(talent_show)

            elif activity_type == "Academic":
                # It is a AcademicCompetition
                subjects = activity["subjects"].split("-")
                max_marks = float(activity["max_marks"])

                academic_competition = AcademicCompetition(activity_id,
                    activity_name, activity_type, max_participants, grade_level,
                    is_active, participants, organizers, subjects, max_marks)

                academic_competitions.append(academic_competition)

            else:
                # Invalid input
                return -1
            
    return (sports_tournaments, talent_shows, academic_competitions)
                                                     
            
        
                    
                    
                
                
                
                
                
