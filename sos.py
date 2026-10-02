# ============================================================
#              SCHOOL OF SKILLS - MANAGEMENT SYSTEM
#                          sos.py
#
# This file has NO Streamlit code in it. It only has the
# "business logic" — the classes and rules of how the school
# works. app.py (a separate file) uses these classes to build
# the actual screens the user sees and clicks on.
# ============================================================

from abc import ABC
from datetime import date
import random
# ABC = "Abstract Base Class". We use it to say "SOS is a
# base/parent idea, not something you create directly."
# Real-life example: "Vehicle" is a concept, but you don't buy
# a "Vehicle" — you buy a "Car" or a "Bike" (which come FROM
# the Vehicle idea). SOS works the same way here.


# ============================================================
#                    1. SOS (SCHOOL) CLASS
# ============================================================

class SOS(ABC):
    # This class stores facts about the SCHOOL ITSELF.
    # Every other class (Staff, Program, Student) will inherit
    # from this class, so they all "know" these facts too.

    # ---------------- CLASS VARIABLES ----------------
    # A "class variable" is shared by EVERY object made from
    # this class. Real-life example: every ID card issued by
    # the same school has the same school name and address
    # printed on it — that's a class variable.

    school_name = "School of Skills"        # name shown everywhere in the app
    location = "Calicut"                    # city where the school is located
    established_year = 2026                 # the year the school started (edit if wrong)
    director = "Management Team"            # who is in charge (edit with real name)
    contact_number = "0495-1234567"         # school's contact number (edit if wrong)

    # ---------------- INSTANCE METHOD ----------------
    # "self" means "this particular object that called the method".
    def school_details(self):
        # This method just packs all the facts above into one
        # dictionary (a labelled box) so app.py can easily loop
        # over it and print "Label: Value" on the screen.
        return {
            "School Name": self.school_name,
            "Location": self.location,
            "Established Year": self.established_year,
            "Established": self.established_year,
            "Director": self.director,
            "Contact Number": self.contact_number,
            "Address": "Calicut, Kerala",
            "Phone": self.contact_number,
            "Email": "info@schoolofskills.com",
            "Website": "https://schoolofskills.com",
            "Affiliation": "Kerala State Skill Development"
        }


# ============================================================
#                    2. STAFF CLASS
# ============================================================

class Staff(SOS):
    # Staff INHERITS from SOS, meaning a Staff object also has
    # access to school_name, location, etc. automatically.

    # CLASS VARIABLE — shared list that remembers EVERY staff
    # member ever created, no matter their role.
    # Real-life example: think of this as the school's master
    # employee register kept in one big binder.
    staff_list = []

    # CLASS VARIABLE — a second, separate list for staff that
    # have been "removed". Real-life example: this is exactly
    # like your computer's Recycle Bin — a removed file doesn't
    # vanish immediately, it just moves to a different folder
    # where it can still be restored, or emptied out for good.
    trash_list = []

    def __init__(
        self,
        staff_id,        # unique code for this employee, e.g. "S101"
        name,            # employee's full name
        role,            # job title, e.g. "Teacher", "Accountant"
        phone,           # phone number
        email,           # email address
        department,      # which department they work in
        joining_date     # the date they joined the school
    ):
        # __init__ runs automatically the moment you create a
        # new Staff (or Teacher/Accountant/etc.) object.
        # It is like filling out a brand-new employee form.

        # ---------------- INSTANCE VARIABLES ----------------
        # "Instance variable" = belongs to THIS ONE employee only,
        # unlike class variables which are shared by everyone.
        self.staff_id = staff_id
        self.name = name
        self.role = role
        self.phone = phone
        self.email = email
        self.department = department
        self.joining_date = joining_date
        self.__attendance = []         # list of {"date": ..., "present": True/False}

        # As soon as this employee is created, automatically
        # file their form into the master register (staff_list).
        Staff.staff_list.append(self)


    # ========================================================
    # CLASS METHOD - Display All Staff
    # ========================================================
    # A "classmethod" works on the WHOLE list, not just one
    # object. "cls" here means "the Staff class itself".
    @classmethod
    def display_all_staff(cls):
        # Simply hand back the entire master register.
        return cls.staff_list


    # ========================================================
    # CLASS METHOD - Search Staff by Name
    # ========================================================
    @classmethod
    def search_staff(cls, name):
        found_staff = []                       # empty basket to collect matches

        for staff in cls.staff_list:           # look at every staff member, one by one
            if name.lower() in staff.name.lower():   # ignore uppercase/lowercase differences
                found_staff.append(staff)      # put a match into the basket

        return found_staff                     # hand back everything found


    # ========================================================
    # CLASS METHOD - Display Trash
    # ========================================================
    @classmethod
    def display_trash(cls):
        # Hand back everyone currently sitting in the Recycle Bin.
        return cls.trash_list


    # ========================================================
    # INSTANCE METHOD - Move to Trash (a "soft delete")
    # ========================================================
    def move_to_trash(self):
        # We don't erase the staff member's data at all — we just
        # take them OUT of the active register and PUT them into
        # the trash register instead. Nothing is lost, so this
        # can always be undone with restore_from_trash().
        if self in Staff.staff_list:
            Staff.staff_list.remove(self)

        Staff.trash_list.append(self)


    # ========================================================
    # INSTANCE METHOD - Restore from Trash
    # ========================================================
    def restore_from_trash(self):
        # The exact reverse of move_to_trash(): take them out of
        # the trash register and put them back into the active one.
        if self in Staff.trash_list:
            Staff.trash_list.remove(self)

        Staff.staff_list.append(self)


    # ========================================================
    # INSTANCE METHOD - Delete Permanently
    # ========================================================
    def delete_permanently(self):
        # This is the ONLY method that actually throws the data
        # away for good — like emptying the Recycle Bin. There is
        # no "undo" after this one.
        if self in Staff.trash_list:
            Staff.trash_list.remove(self)


    # ========================================================
    # INSTANCE METHOD - Staff Attendance
    # ========================================================
    def has_attendance_marked(self, att_date):
        # We check each saved record in the staff member's attendance list
        for record in self.__attendance:
            # If the record's date matches the date we are checking, return True (already marked)
            if record["date"] == att_date:
                return True
        # If the loop finishes without finding a match, return False (not yet marked)
        return False

    def mark_attendance(self, att_date, present):
        # We create a dictionary with the calendar date and a True/False boolean for present/absent
        # Then we append (add) this dictionary to the private __attendance list for this staff member
        self.__attendance.append(
            {"date": att_date, "present": present}
        )

    def get_attendance_percentage(self):
        # If no attendance has been marked yet, avoid division by zero and return 0%
        if not self.__attendance:
            return 0

        # Start a counter at zero to count how many days this staff member was present
        present_days = 0
        # Go through each attendance record in the list one by one
        for record in self.__attendance:
            # If the 'present' field is True, add 1 to our count of present days
            if record["present"]:
                present_days += 1

        # Calculate percentage: (present_days / total_days) * 100, and round to 1 decimal place
        return round(
            (present_days / len(self.__attendance)) * 100, 1
        )

    def get_attendance_summary(self):
        # Total number of days attendance was recorded for this staff member
        total_days = len(self.__attendance)
        # Count how many days had present == True
        present_days = sum(1 for record in self.__attendance if record["present"])
        # Remaining days are absent days (total minus present)
        absent_days = total_days - present_days
        # Calculate percentage, protecting against 0 total days
        percentage = round((present_days / total_days) * 100, 1) if total_days > 0 else 0
        # Pack all four stats into a clean dictionary so screens can easily show them
        return {
            "total_days": total_days,
            "present_days": present_days,
            "absent_days": absent_days,
            "percentage": percentage
        }

    def get_attendance_records(self):
        # Return the raw list of daily attendance logs for this staff member
        return self.__attendance

    # ========================================================
    # INSTANCE METHOD - Display Staff Details
    # ========================================================
    def staff_details(self):
        # Packs one employee's info into a labelled dictionary,
        # the same way school_details() did for the school.
        return {
            "Staff ID": self.staff_id,
            "Name": self.name,
            "Role": self.role,
            "Phone": self.phone,
            "Email": self.email,
            "Department": self.department,
            "Joining Date": self.joining_date,
            "Attendance %": f"{self.get_attendance_percentage()}%"
        }


# ============================================================
#              2a. STAFF SUB-CLASSES (INHERITANCE)
# ============================================================
# Real-life example: think of "Staff" as a blank employee ID
# card template. "Teacher", "Accountant" etc. are the SAME
# template, just already stamped with a specific job title, so
# you never have to type the role by hand and risk a typo.

class Teacher(Staff):
    def __init__(
        self, staff_id, name, phone, email, department, joining_date
    ):
        # "super()" means "run the parent class's __init__ for me".
        # We just slot in the fixed role "Teacher" automatically.
        super().__init__(
            staff_id, name, "Teacher",
            phone, email, department, joining_date
        )


class StudentCoordinator(Staff):
    def __init__(
        self, staff_id, name, phone, email, department, joining_date
    ):
        super().__init__(
            staff_id, name, "Student Coordinator",
            phone, email, department, joining_date
        )


class MediaTeam(Staff):
    def __init__(
        self, staff_id, name, phone, email, department, joining_date
    ):
        super().__init__(
            staff_id, name, "Media Team",
            phone, email, department, joining_date
        )


class Accountant(Staff):
    def __init__(
        self, staff_id, name, phone, email, department, joining_date
    ):
        super().__init__(
            staff_id, name, "Accountant",
            phone, email, department, joining_date
        )


# ============================================================
#                    3. PROGRAM CLASS
# ============================================================

class Program(SOS):
    # Represents one course/program the school offers,
    # e.g. "Agentic AI" or "Digital Marketing".

    # CLASS VARIABLE — the master catalog of every program.
    programs_list = []

    # CLASS VARIABLE — the Recycle Bin for removed programs.
    # Same idea as Staff.trash_list: nothing is deleted for real
    # until someone empties it out on purpose.
    trash_list = []

    def __init__(
        self,
        program_id,      # unique code, e.g. "P201"
        program_name,    # e.g. "Agentic AI"
        category,        # e.g. "Tech" or "Business"
        duration,        # e.g. "3 months"
        fees,            # the standard course fee
        teacher          # name of the teacher teaching it
    ):
        # ---------------- INSTANCE VARIABLES ----------------
        self.program_id = program_id
        self.program_name = program_name
        # Store the category under self.category
        self.category = category
        # Also assign self.department as an alias to category so both attribute names work interchangeably
        self.department = category
        # Store course duration in months/weeks
        self.duration = duration
        # Store standard course fee
        self.fees = fees
        # Store assigned faculty teacher name
        self.teacher = teacher

        # File this new program into the master catalog.
        Program.programs_list.append(self)


    # ========================================================
    # CLASS METHOD - Display All Programs
    # ========================================================
    @classmethod
    def display_all_programs(cls):
        return cls.programs_list   # hand back the whole catalog


    # ========================================================
    # CLASS METHOD - Search Program by Name
    # ========================================================
    @classmethod
    def search_program(cls, name):
        found_programs = []                          # empty basket

        for program in cls.programs_list:             # check every program
            if name.lower() in program.program_name.lower():
                found_programs.append(program)         # keep the ones that match

        return found_programs


    # ========================================================
    # CLASS METHOD - Display Trash
    # ========================================================
    @classmethod
    def display_trash(cls):
        return cls.trash_list


    # ========================================================
    # INSTANCE METHOD - Move to Trash (a "soft delete")
    # ========================================================
    def move_to_trash(self):
        if self in Program.programs_list:
            Program.programs_list.remove(self)

        Program.trash_list.append(self)


    # ========================================================
    # INSTANCE METHOD - Restore from Trash
    # ========================================================
    def restore_from_trash(self):
        if self in Program.trash_list:
            Program.trash_list.remove(self)

        Program.programs_list.append(self)


    # ========================================================
    # INSTANCE METHOD - Delete Permanently
    # ========================================================
    def delete_permanently(self):
        # No undo after this — it comes straight out of the trash.
        if self in Program.trash_list:
            Program.trash_list.remove(self)


    # ========================================================
    # INSTANCE METHOD - Count Students Enrolled in this Program
    # ========================================================
    def enrolled_count(self):
        # We look through EVERY student in the whole school and
        # count how many chose THIS program.
        count = 0

        for student in Student.students_list:
            if student.get_program() == self.program_name:
                count += 1                             # found one more match

        # Return the final tally of enrolled students
        return count

    # ========================================================
    # INSTANCE METHOD - Get List of Enrolled Student Names
    # ========================================================
    def enrolled_students(self):
        # Iterate through every student in the school master register
        # Collect and return the names of all students enrolled in this program
        return [student.name for student in Student.students_list if student.get_program() == self.program_name]


    # ========================================================
    # INSTANCE METHOD - Display Program Details
    # ========================================================
    def program_details(self):
        return {
            "Program ID": self.program_id,
            "Program Name": self.program_name,
            "Category": self.category,
            "Duration": self.duration,
            "Fees": self.fees,
            "Teacher": self.teacher,
            "Number of Students": self.enrolled_count()   # calculated live, not stored
        }


# ============================================================
#                    4. STUDENT CLASS
# ============================================================

class Student(SOS):
    # Represents one student. Every student is created as soon
    # as they walk in and give their basic details — like
    # filling an "enquiry form" at the school's front desk.
    # They may or may not have chosen a program YET.

    # CLASS VARIABLE — master register of every student.
    students_list = []

    # CLASS VARIABLE — the Recycle Bin for removed students.
    trash_list = []

    def __init__(
        self,
        student_id,   # unique code, e.g. "ST301"
        name,         # student's full name
        phone,        # phone number
        email,        # email address
        age,          # student's age
        address       # home address
    ):
        # ---------------- INSTANCE VARIABLES ----------------
        # These are basic details every student has from day one,
        # even before choosing a program.
        self.student_id = student_id
        self.name = name
        self.phone = phone
        self.email = email
        self.age = age
        self.address = address

        # ---------------- PRIVATE INSTANCE VARIABLES ----------------
        # The double-underscore (__) in front makes these PRIVATE.
        # That means code OUTSIDE this class cannot directly do
        # something like "student.__fees_paid = 999999" to cheat
        # the numbers. They can only be changed by calling the
        # proper methods below (pay_fee, enroll, etc.).
        # Real-life example: this is like a bank balance — you
        # can't just scribble a new number on your passbook,
        # you must deposit/withdraw through the counter, which
        # checks the rules first.
        self.__program = None          # which program they joined (None = not yet)
        self.__batch = None            # which batch, e.g. "2026-A"
        self.__teacher = None          # assigned teacher's name
        self.__admission_date = None   # the date they got enrolled
        self.__total_fees = 0          # total fee agreed for their program
        self.__fees_paid = 0           # how much they've paid so far
        self.__attendance = []         # a list of {"date": ..., "present": True/False}
        self.__payment_history = []    # list of receipt dicts
        self.__status = "Not Enrolled" # "Not Enrolled" until they join a program

        # File this new student into the master register.
        Student.students_list.append(self)


    # ========================================================
    # CLASS METHOD - Display All Students
    # ========================================================
    @classmethod
    def display_all_students(cls):
        return cls.students_list


    # ========================================================
    # CLASS METHOD - Search Student by Name
    # ========================================================
    @classmethod
    def search_student(cls, name):
        found_students = []

        for student in cls.students_list:
            if name.lower() in student.name.lower():
                found_students.append(student)

        return found_students


    # ========================================================
    # CLASS METHOD - Display Trash
    # ========================================================
    @classmethod
    def display_trash(cls):
        return cls.trash_list


    # ========================================================
    # INSTANCE METHOD - Move to Trash (a "soft delete")
    # ========================================================
    def move_to_trash(self):
        if self in Student.students_list:
            Student.students_list.remove(self)

        Student.trash_list.append(self)


    # ========================================================
    # INSTANCE METHOD - Restore from Trash
    # ========================================================
    def restore_from_trash(self):
        if self in Student.trash_list:
            Student.trash_list.remove(self)

        Student.students_list.append(self)


    # ========================================================
    # INSTANCE METHOD - Delete Permanently
    # ========================================================
    def delete_permanently(self):
        # No undo after this — it comes straight out of the trash.
        if self in Student.trash_list:
            Student.trash_list.remove(self)


    # ========================================================
    # CLASS METHOD - Students who ARE enrolled in a program
    # ========================================================
    @classmethod
    def get_enrolled_students(cls):
        # A list-comprehension is just a short way of writing a
        # for-loop that filters and collects in one line.
        # This line means: "give me every student, but only keep
        # the ones where is_enrolled() is True."
        return [student for student in cls.students_list if student.is_enrolled()]


    # ========================================================
    # CLASS METHOD - Enrolled students who STILL owe fees
    # ========================================================
    @classmethod
    def get_pending_fee_students(cls):
        # Real-life example: this is the list a school accountant
        # would print out to know who to follow up with.
        return [
            student for student in cls.get_enrolled_students()
            if student.get_fee_due() > 0
        ]


    # ========================================================
    # CLASS METHOD - Enrolled students who have FULLY paid
    # ========================================================
    @classmethod
    def get_fully_paid_students(cls):
        return [
            student for student in cls.get_enrolled_students()
            if student.get_fee_due() <= 0
        ]


    # ========================================================
    # INSTANCE METHOD - Enroll Student in a Program
    # ========================================================
    def enroll(
        self, program_name, batch, teacher, admission_date, total_fees
    ):
        # This is the ONLY proper way to set these private
        # fields. Filling this form = officially joining a program.
        self.__program = program_name
        self.__batch = batch
        self.__teacher = teacher
        self.__admission_date = admission_date
        self.__total_fees = total_fees
        self.__status = "Active"           # they are now an active student


    def is_enrolled(self):
        # Returns True if they have chosen a program, False if not.
        return self.__program is not None


    def get_program(self):
        # A "getter" — lets other code READ the private value
        # without being able to overwrite it directly.
        return self.__program


    def get_batch(self):
        # A getter method that safely returns the student's batch name (e.g. 'Batch A')
        # If no batch was assigned yet, it gracefully returns '-' as a placeholder
        return self.__batch or "-"


    # ========================================================
    # INSTANCE METHOD - Attendance
    # ========================================================
    def has_attendance_marked(self, att_date):
        # Loop through every attendance record in this student's history
        for record in self.__attendance:
            # If the record has the exact same date as the one requested, it is already marked
            if record["date"] == att_date:
                return True
        # If no matching date is found in the list, return False
        return False


    def mark_attendance(self, att_date, present):
        # Pack the date and the True/False presence status into a dictionary
        # Append this new attendance dictionary to the student's private __attendance list
        self.__attendance.append(
            {"date": att_date, "present": present}
        )


    def get_attendance_percentage(self):
        # If no attendance records exist yet, return 0% to avoid dividing by zero
        if not self.__attendance:
            return 0

        # Counter variable to tally days the student was marked Present
        present_days = 0
        # Iterate over each record in the student's attendance list
        for record in self.__attendance:
            # Check if this day's attendance status is True (Present)
            if record["present"]:
                # Increment the present day counter by 1
                present_days += 1

        # Calculate percentage: (present_days / total_records) * 100 and round to 1 decimal place
        return round(
            (present_days / len(self.__attendance)) * 100, 1
        )

    def get_attendance_summary(self):
        # Count total number of attendance records marked for this student
        total_days = len(self.__attendance)
        # Sum up all the entries where present is True
        present_days = sum(1 for record in self.__attendance if record["present"])
        # Calculate absent days by subtracting present days from total days
        absent_days = total_days - present_days
        # Compute the percentage (or 0 if total_days is 0 to avoid ZeroDivisionError)
        percentage = round((present_days / total_days) * 100, 1) if total_days > 0 else 0
        # Return a dictionary containing all key attendance statistics for easy UI rendering
        return {
            "total_days": total_days,
            "present_days": present_days,
            "absent_days": absent_days,
            "percentage": percentage
        }

    def get_attendance_records(self):
        # Return the complete list of daily attendance logs for this student
        return self.__attendance


    # ========================================================
    # INSTANCE METHOD - Fees
    # ========================================================
    def pay_fee(self, amount, payment_mode="Cash", receipt_id=None):
        # Add the newly collected amount onto the student's cumulative fees paid
        self.__fees_paid += amount
        # If a custom receipt ID was not passed in, auto-generate one with a random 4-digit number
        if not receipt_id:
            receipt_id = f"REC-2026-{random.randint(1000, 9999)}"
        # Build an official receipt dictionary recording the transaction details
        receipt = {
            "receipt_id": receipt_id,
            "date": str(date.today()),
            "amount": amount,
            "mode": payment_mode,
            "due_after": self.get_fee_due()
        }
        # Save this receipt in the student's private payment history register
        self.__payment_history.append(receipt)
        # Return the generated receipt dictionary so the caller can display or print it
        return receipt

    def get_payment_history(self):
        # Return the list of all payment receipts recorded for this student
        return self.__payment_history


    def get_fee_due(self):
        # Simple subtraction: what's left to pay.
        return self.__total_fees - self.__fees_paid


    def get_fee_status(self):
        due = self.get_fee_due()

        if not self.is_enrolled():
            return "Not Applicable"   # can't owe fees for a program they haven't joined
        elif due <= 0:
            return "Fully Paid"
        elif self.__fees_paid > 0:
            return "Partially Paid"
        else:
            return "Unpaid"


    # ========================================================
    # INSTANCE METHOD - Display Student Details
    # ========================================================
    def student_details(self):
        # "or" here means: if the left side is empty/None, use
        # the right side instead. So an un-enrolled student shows
        # "Not Enrolled" instead of a blank/None value.
        return {
            "Student ID": self.student_id,
            "Name": self.name,
            "Phone": self.phone,
            "Email": self.email,
            "Age": self.age,
            "Address": self.address,
            "Program": self.__program or "Not Enrolled",
            "Batch": self.__batch or "-",
            "Teacher": self.__teacher or "-",
            "Admission Date": self.__admission_date or "-",
            "Total Fees": self.__total_fees,
            "Fees Paid": self.__fees_paid,
            "Fee Due": self.get_fee_due(),
            "Fee Status": self.get_fee_status(),
            "Attendance %": self.get_attendance_percentage(),
            "Status": self.__status
        }


# ============================================================
#                    4a. NOTICE (ANNOUNCEMENT) CLASS
# ============================================================

class Notice(SOS):
    # CLASS VARIABLE — shared list that holds all active campus notices in one place
    # Every time a new Notice is created, it registers itself into this master list
    notices_list = []

    def __init__(
        self,
        notice_id,       # Unique identifier for the notice (e.g. 'N101')
        title,           # The headline or subject of the announcement
        category,        # Tag/category like 'Urgent', 'Event', 'General', or 'Exam'
        content,         # The detailed body text describing the announcement
        posted_date,     # The calendar date when this notice was published
        posted_by="Admin"# Name or role of the person or department issuing the notice
    ):
        # Assign the notice ID to this particular notice instance
        self.notice_id = notice_id
        # Assign the title headline to this notice instance
        self.title = title
        # Assign the category label to this notice instance
        self.category = category
        # Assign the full announcement text to this notice instance
        self.content = content
        # Assign the publication date to this notice instance
        self.posted_date = posted_date
        # Assign the author's name or department to this notice instance
        self.posted_by = posted_by

        # Immediately append this newly created notice to the master notices register
        Notice.notices_list.append(self)

    @classmethod
    def get_all_notices(cls):
        # Return all notices in reverse order so the newest announcements appear first at the top
        return list(reversed(cls.notices_list))

    @classmethod
    def delete_notice(cls, notice_id):
        # Filter out and remove the notice matching the given notice_id from the master list
        cls.notices_list = [n for n in cls.notices_list if n.notice_id != notice_id]


# ============================================================
#                5. SOS ACTIVITIES CLASS
# ============================================================
# This class does NOT store any data of its own. Its whole job
# is to take objects (a Student, a Program, ...) that already
# exist and perform an ACTION on them, while checking the
# rules first. Real-life example: this is like the reception
# desk — it doesn't own the student's file, it just knows the
# correct procedure to update it.

class SOSActivities:

    # ========================================================
    # INSTANCE METHOD - ENROLL STUDENT
    # ========================================================
    def enroll_student(
        self, student, program, batch, teacher, admission_date, total_fees
    ):
        # RULE 1: a student cannot join two programs at once
        # in this simple system.
        if student.is_enrolled():
            return (
                False,
                f"{student.name} is already enrolled in "
                f"'{student.get_program()}'."
            )

        # If the rule passes, actually do the enrollment.
        student.enroll(
            program.program_name,
            batch,
            teacher,
            admission_date,
            total_fees
        )

        # Return a tuple: (did it succeed?, message to display)
        return (
            True,
            f"{student.name} enrolled successfully in "
            f"'{program.program_name}'."
        )


    # ========================================================
    # INSTANCE METHOD - MARK ATTENDANCE
    # ========================================================
    def mark_attendance(self, student, att_date, present):
        # RULE 1: must be enrolled before attendance makes sense.
        if not student.is_enrolled():
            return (
                False,
                f"{student.name} is not enrolled in any "
                f"program yet."
            )

        # RULE 2: don't allow marking the same date twice.
        if student.has_attendance_marked(att_date):
            return (
                False,
                f"Attendance for {att_date} is already "
                f"marked for {student.name}."
            )

        # Rules passed — actually record it.
        student.mark_attendance(att_date, present)

        status_word = "Present" if present else "Absent"

        return (
            True,
            f"Attendance marked as {status_word} for "
            f"{student.name} on {att_date}."
        )


    # ========================================================
    # INSTANCE METHOD - MARK STAFF ATTENDANCE
    # ========================================================
    def mark_staff_attendance(self, staff, att_date, present):
        # RULE 1: Check if attendance for this employee has already been marked on this date
        if staff.has_attendance_marked(att_date):
            # If already marked, abort and return False along with a helpful warning message
            return (
                False,
                f"Attendance for {att_date} is already marked for {staff.name}."
            )

        # Rule check passed — call the staff member's internal mark_attendance method to save it
        staff.mark_attendance(att_date, present)

        # Format a friendly English word ('Present' or 'Absent') based on the boolean status
        status_word = "Present" if present else "Absent"

        # Return True for success and a clear confirmation message
        return (
            True,
            f"Attendance marked as {status_word} for staff "
            f"{staff.name} on {att_date}."
        )


    # ========================================================
    # INSTANCE METHOD - MARK BULK CLASS ATTENDANCE
    # ========================================================
    def mark_bulk_attendance(self, student_status_list, att_date):
        # Initialize a counter for how many students we successfully record attendance for
        marked_count = 0
        # Initialize a list to track any students who already had attendance on this date
        already_marked = []

        # Iterate over each (student_object, is_present) pair in the batch list
        for student, present in student_status_list:
            # Check if this student already has attendance marked for the chosen date
            if student.has_attendance_marked(att_date):
                # If so, note their name in the skipped list so we don't duplicate it
                already_marked.append(student.name)
            else:
                # Otherwise, record the attendance for this student
                student.mark_attendance(att_date, present)
                # Increment our successfully marked count by 1
                marked_count += 1

        # Return the total count of students marked and the list of any skipped names
        return marked_count, already_marked


    # ========================================================
    # INSTANCE METHOD - COLLECT FEE
    # ========================================================
    def collect_fee(self, student, amount, payment_mode="Cash"):
        # RULE 1: Ensure the student has actually enrolled in a program before accepting fees
        if not student.is_enrolled():
            return (
                False,
                None,
                f"{student.name} is not enrolled in any program yet."
            )

        # Calculate what the student currently owes
        due = student.get_fee_due()

        # RULE 2: If the outstanding balance is 0 or less, nothing needs to be collected
        if due <= 0:
            return (
                False,
                None,
                f"{student.name} has already paid the full fee."
            )

        # RULE 3: Reject payments that are zero or negative numbers
        if amount <= 0:
            return (
                False,
                None,
                "Please enter a valid amount."
            )

        # RULE 4: Reject payments that are strictly greater than what is actually owed
        if amount > due:
            return (
                False,
                None,
                f"Amount exceeds the due fee of ₹{due}."
            )

        # All validation rules passed — create a unique receipt number with a random 4-digit code
        receipt_id = f"REC-2026-{random.randint(1000, 9999)}"
        # Call the student's pay_fee method, which updates the total paid and stores this receipt
        receipt = student.pay_fee(amount, payment_mode=payment_mode, receipt_id=receipt_id)

        # Return True for success, the generated receipt dictionary, and a detailed confirmation message
        return (
            True,
            receipt,
            f"₹{amount} collected from {student.name} via {payment_mode}. "
            f"Remaining due: ₹{student.get_fee_due()}"
        )


    # ========================================================
    # INSTANCE METHOD - ASSIGN TEACHER
    # ========================================================
    def assign_teacher(self, program, teacher_name):
        # Simply overwrite the teacher field on the program.
        program.teacher = teacher_name

        return (
            True,
            f"{teacher_name} assigned as teacher for "
            f"'{program.program_name}'."
        )
