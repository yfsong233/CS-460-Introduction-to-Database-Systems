#
# CS 460: Problem Set 1, SQL Programming Problems
#

#
# For each problem, use a text editor to add the appropriate SQL
# command between the triple quotes provided for that problem's variable.
#
# For example, here is how you would include a query that finds the
# names and years of all movies in the database with an R rating:
#
sample = """
    SELECT name, year
    FROM Movie
    WHERE rating = 'R';
"""

'''
Schema:
Movie(_id_, name, year, rating, runtime, genre, earning_rank)
Person(_id_, name, dob, pob)
Actor(_actor_id_, _movie_id_)
Director(_director_id_, _movie_id_)
Oscar(movie_id, person_id, type, year)
'''

#
# Problem 4. 
# find the places of birth and dates of birth 
# for Michelle Yeoh and Jamie Lee Curtis, who both won Oscars this year 
# for their performances in Everything Everywhere All at Once
# 
problem4 = """
    SELECT P.name, P.dob, P.pob
    FROM Person P, Movie M, Oscar O
    WHERE P.id = O.person_id AND M.id = O.movie_id
	    AND M.name = 'Everything Everywhere All at Once' 
	    AND (P.name = 'Michelle Yeoh' OR P.name = 'Jamie Lee Curtis');
"""


#
# Problem 5. 
# find all movies that won Best Picture in the 2010s (i.e., from 2010-2019)
# results: (name of the movie, the year in which the award was given)
# order required?
problem5 = """
    SELECT M.name, O.year
    FROM Movie M, Oscar O
    WHERE M.id = O.movie_id
	    AND O.type = 'BEST-PICTURE' 
	    AND O.year <= 2019 AND O.year >= 2010
    ORDER BY O.year DESC;
"""

#
# Problem 6. 
# determine the year(s) of any Best Director Oscars that Steven Spielberg has actually won, 
# along with the name(s) of the movie(s) for which he won. 
# result: one or more tuples of (year won, movie name).
#
problem6 = """
    SELECT O.year, M.name
    FROM Oscar O, Person P, Movie M
    WHERE P.id = O.person_id AND M.id = O.movie_id
	    AND O.type = 'BEST-DIRECTOR' 
	    AND P.name = 'Steven Spielberg';
"""

#
# Problem 7. 
# determine the number of movies in the database that are connected to at least one foreign-born actor/actress. 
# (By connected to, we mean that the database records the fact that the person acted in the movie.) 
# The result of the query should be a single number.
# Hints:
# 1. assume that all persons born in the United States have the string 'USA' at the very end of their pob field. 
# 2. be careful NOT to include people with a NULL value for pob.
# 
problem7 = """
    SELECT COUNT(DISTINCT M.id)
    FROM Person P, Movie M, Actor A
    WHERE P.id = A.actor_id AND M.id = A.movie_id
	    AND P.pob NOT LIKE '%USA';
"""

#
# Problem 8. 
# find the longest animated movie in the database, along with its runtime. 
# All animated movies have the letter N somewhere in their genre string.
# For full credit, your answer must use a subquery.
# (name, runtime) is unique?
problem8 = """
    SELECT name, runtime
    FROM Movie M
    WHERE genre like '%N%' 
        AND runtime = (
	        select MAX(runtime)
	        from Movie M
	        where genre like '%N%'
            ); 
"""

#
# Problem 9.
# find all movies that have won at least 5 of the Oscars in the database. 
# result: (movie year, movie name, number of Oscars won)
# Hint:
# 1. (a movie’s name, year) is unique
# 2. can use more than one attribute as the basis of the subgroups
#

problem9 = """
    SELECT M.year, M.name, COUNT(O.type)
    FROM Movie M, Oscar O
    WHERE M.id = O.movie_id
    GROUP BY O.movie_id, O.year
    HAVING COUNT(O.type) >= 5;
           
"""

#
# Problem 10. 
# find the names and places of birth of all directors in the database who were born in France.
#
problem10 = """
    SELECT DISTINCT P.name, P.pob
    FROM Director D, Person P
    WHERE P.id = D.director_id
	    AND P.pob LIKE '%, France';
"""

#
# Problem 11. 
# produces a table summarizing the Oscars won by each the top 25 grossing movies. 
# results: tuples of (earnings rank, movie name, award type)
# If a given movie won multiple awards, it should have one tuple for each award; 
# if it won no awards, it should have a single tuple in which the third value of the tuple is NULL. 
# Sort the tuples by earnings rank.
#
problem11 = """
    SELECT M.earnings_rank, M.name, O.type
    FROM Movie M LEFT OUTER JOIN Oscar O ON M.id = O.movie_id
    WHERE M.earnings_rank <= 25;  
"""

#
# Problem 12. 
# determine how many of the movies that have won Best Picture have runtimes 
# that are longer than the average runtime of all of the movies in the database. 
# The result of your query should be a single number.
#
problem12 = """
    SELECT COUNT(*)
    FROM Oscar O, Movie M
    WHERE M.id = O.movie_id
	    AND O.type = 'BEST-PICTURE'
	    AND M.runtime > (
	        select AVG(runtime)
	        from Movie
            );
"""

#
# Problem 13. 
# lists the winners of the “big six” Oscars (i.e., the ones in our database) from the 1993 Academy Awards. 
# result: tuples of (award type, person name, movie name). 
# In the case of the Best Picture winner, the person name should be NULL.
# Hint: take special steps to deal with the fact that 
#       Oscar tuples for Best Picture winners have a NULL value for person_id.
#
problem13 = """
    SELECT award_type, person_name, M.name as movie_name
    FROM (SELECT O.type as award_type, O.movie_id as mid, P.name as person_name
    FROM Oscar O LEFT OUTER JOIN Person P ON P.id = O.person_id
    WHERE O.year = 1993) LEFT OUTER JOIN Movie M ON mid = M.id;
"""

#
# Problem 14.
# determines how many actors or actresses have won a supporting acting award but have never won a non-supporting acting award 
# (i.e, won Best Supporting Actor but not Best Actor, or won Best Supporting Actress but not Best Actress). 
# result: a single number.
#
problem14 = """
    SELECT COUNT(DISTINCT A.actor_id)
    FROM Oscar O, Actor A
    WHERE A.actor_id = O.person_id
	AND O.type LIKE 'BEST-SUPPORTING%'
	AND A.actor_id NOT IN (
			select distinct A.actor_id
			from Oscar O, Actor A
			where A.actor_id = O.person_id
				and (O.type = 'BEST-ACTOR' or O.type = 'BEST-ACTRESS'));
"""

#
# Problem 15. 
# updates our database to include the fact that Murphy appeared in The Dark Knight.
# Hints:
# 1. This is the only question in which your answer will not be a SELECT command. You will need to figure out the correct type of SQL command to use.
# 2. You will need to begin by using one or more SELECT commands to obtain the information needed to capture the relationship between Murphy and The Dark Knight. 
#    For other problems in Part II, using preliminary queries to look up information and then using it as part of your final command isn’t allowed, 
#    but it’s necessary to do so for this problem.
# 3. The preliminary queries that you perform for this problem should NOT be included in your solution. 
#    Rather, your answer should be the single SQL command that adds the relationship between Murphy and The Dark Knight to our database.
#
problem15 = """
    INSERT INTO Actor (actor_id, movie_id)
    VALUES ('0614165', '0468569');
"""
