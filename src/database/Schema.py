SCHEMA_HINT = """
activemembers (cost DECIMAL, duration_in_months INT, email VARCHAR, full_name VARCHAR, member_id INT, membership_end DATE, membership_start DATE, phone VARCHAR, plan_name VARCHAR)
class (class_id INT, class_name VARCHAR, end_time TIME, max_participants INT, start_time TIME, trainer_id INT)
classtrainerinfo (class_id INT, class_name VARCHAR, end_time TIME, specialty VARCHAR, start_time TIME, trainer_name VARCHAR)
member (dob DATE, email VARCHAR, first_name VARCHAR, gender VARCHAR, last_name VARCHAR, member_id INT, membership_end DATE, membership_start DATE, phone VARCHAR, subscription_id INT)
memberclassenrollment (class_id INT, enrollment_date DATE, enrollment_id INT, member_id INT)
membersubscriptioninfo (cost DECIMAL, duration_in_months INT, email VARCHAR, full_name VARCHAR, member_id INT, phone VARCHAR, plan_name VARCHAR)
subscription (cost DECIMAL, duration_in_months INT, features TEXT, plan_name VARCHAR, subscription_id INT)
trainer (availability VARCHAR, email VARCHAR, experience INT, first_name VARCHAR, last_name VARCHAR, phone VARCHAR, salary DECIMAL, specialty VARCHAR, trainer_id INT)
trainerclassschedule (class_name VARCHAR, end_time TIME, enrolled_members BIGINT, start_time TIME, trainer_id INT, trainer_name VARCHAR)
"""