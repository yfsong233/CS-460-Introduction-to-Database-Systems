#
# CS 460: Lab 2, Task 2
#

#
# Sample query
#
sample = """
    SELECT name
    FROM Course
    WHERE room_id IS NULL;
"""

#
# Query 1. 
# finds the names and capacities 
# of all rooms in the CAS and CGS buildings
# 
# notes:
# LIKE is for pattern matching; = is for exact matching 
#
query1 = """
SELECT name, capacity
FROM Room
WHERE name LIKE 'CAS%' or name LIKE 'CGS%';
"""

#
# Query 2. 
# finds the number of students 
# who are enrolled in a course for undergraduate ('ugrad') credit.
# 
# notes:
# students can be enrolled in more than one course,
# which means a student may appear multiple times in the relationship set Enrolled
# therefore DISTINCT is required
#
query2 = """
SELECT DISTINCT name
FROM Student, Enrolled
WHERE id = student_id AND credit_status = 'ugrad';
"""

#
# Query 3. finds the earliest (i.e., smallest) start time of any CS course
#
query3 = """ 
SELECT MIN(start_time)
FROM Course
WHERE name LIKE 'CS%';
"""

#
# Query 4. Modify your previous query to find the name and start time 
# of the CS course with the earliest start time. 
# In order to adhere to standard SQL, you will need to use a subquery.
#
# notes:
# 1. the conditions in the subquery may need to be restated in the main query's WHERE
# 2. remember to remove the ; at the end of subquery 
#    and include ; at the end of main query
# 
query4 = """
SELECT name, start_time
FROM Course
WHERE name LIKE 'CS%' AND start_time = (SELECT MIN(start_time)
				FROM Course
				WHERE name LIKE 'CS%'
				);
"""

#
# Query 5. 
# finds, for each type of credit status, the number of students 
# who are enrolled in a course with that credit status.
# notes: 
# 1. COUNT(DISTINCT <attribute>) vs COUNT(*)
# 2. cannot do COUNT(DISTINCT *)
#
query5 = """
SELECT credit_status, COUNT(DISTINCT student_id) AS num_students
FROM Enrolled
WHERE credit_status IS NOT NULL
GROUP BY credit_status;
"""

#
# Query 6. finds the names of all students majoring in 'computer science'
# Hint: Don’t forget to include an appropriate join condition.
# 
query6 = """
SELECT name
FROM Student, MajorsIn
WHERE id = student_id and dept_name = 'computer science';
"""

#
# Query 7. finds the names of all students who are not enrolled in CS 460. 
# Hint: You will need a subquery.
# notes: when joining >= 2 tables, remember to include (n-1) join conditions
#
query7 = """
SELECT DISTINCT name
FROM Student, Enrolled
WHERE id = student_id AND name NOT IN (
		select name
		from Student, Enrolled
		where id = student_id and course_name = 'CS 460');
"""
