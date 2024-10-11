#
# CS 460: Lab 3, Task 2
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
# finds the major(s) of each student in the database. 
# results: tuples of (student name, dept name).
#
query1 = """
    SELECT S.name, M.dept_name
    FROM Student S LEFT OUTER JOIN MajorsIn M ON S.id = M.student_id
"""

#
# Query 2. 
# revise the previous query so that its results will include students who don’t have a major. 
# Hint: You will need to perform a LEFT OUTER JOIN, with the join condition moved to the ON clause.
#
query2 = """

"""

#
# Query 3. Put your SQL command between the triple quotes found below.
#
query3 = """ 

"""

#
# Query 4. Put your SQL command between the triple quotes found below.
#
query4 = """

"""

#
# Query 5. Put your SQL command between the triple quotes found below.
#
query5 = """
           
"""

#
# Query 6. Put your SQL command between the triple quotes found below.
#
query6 = """

"""

#
# Query 7. Put your SQL command between the triple quotes found below.
#
query7 = """

"""

#
# Query 8. Put your SQL command between the triple quotes found below.
#
query8 = """

"""

#
# Query 9. Put your SQL command between the triple quotes found below.
#
query9 = """

"""

#
# Query 10. Put your SQL command between the triple quotes found below.
#
query10 = """

"""

#
# Query 11. Put your SQL command between the triple quotes found below.
#
query11 = """

"""

#
# Query 12. Put your SQL command between the triple quotes found below.
#
query12 = """

"""
