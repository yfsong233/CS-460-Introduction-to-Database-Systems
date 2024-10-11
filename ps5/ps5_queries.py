#
# CS 460: Problem Set 5: MongoDB Query Problems
#

#
# For each query, use a text editor to add the appropriate XQuery
# command between the triple quotes provided for that query's variable.
#
# For example, here is how you would include a query that finds
# the names of all movies in the database from 1990.
#
sample = """
    db.movies.find( { year: 1990 }, 
                    { name: 1, _id: 0 } )
"""

#
# 1. Write a query to find the names and places of birth of all people in the database that were born in the state of Florida. 
# To ensure that you do not include people born in cities or towns named Florida (like Florida, Massachusetts!), 
# you should ensure that the string “Florida, USA” is at the very end of the person’s place of birth.
#
query1 = """
    db.people.find({pob: /Florida, USA$/},
                   {_id: 0, name: 1, pob: 1})
"""

#
# 2. Find the names and earnings ranks of all top-grossing movies released in 2023. 
#  Our database only includes an earnings_rank field in a movie document when that movie is a top grosser.
#
query2 = """
    db.movies.find({year: 2023, earnings_rank: {$exists: true}},
                   {_id: 0, name: 1, earnings_rank: 1})
"""

#
# 3. Julianne Moore is a BU alum (CFA ‘83). 
# Write a query that finds the name, year, and rating of all movies in the database in which she has acted.
# You will need to use dot notation for the field that appears in the selection document, 
# and therefore you will need to surround that field name with quotes.
#
query3 = """
    db.movies.find({"actors.name": "Julianne Moore"},
                   {_id: 0, name: 1, year: 1, rating: 1})
"""

#
# 4. Write a query to find the names of the movies that won the Oscar for BEST-PICTURE from 2020 to the present. 
# The result documents should include the name of the movie and the year in which the award was given.
#
query4 = """
    db.oscars.find({year: {$gte: 2020}, type: "BEST-PICTURE"},
                   {_id: 0, "movie.name": 1, year: 1})
"""

#
# 5. Write a query to find the number of directors in the database who were born in either November or December. 
# Use pattern matching and one of the logical operators ($and, $or, or $not). 
# You may assume that all dates of birth are stored using the format 'yyyy-mm-dd'. 
# You should use the single-purpose aggregation method called count that we covered covered in lecture, not an aggregation pipeline.
#
query5 = """
    db.people.count({$or: [{dob: /-11-/}, {dob: /-12-/}], hasDirected: {$exists: true}})
"""

#
# 6.Write a query to find the name and runtime of the shortest movie in the database. 
# If two or more movies are tied for the shortest runtime, 
# your query may produce the name and runtime of any one of them.
#
query6 = """
    db.movies.aggregate(
        {$sort: {runtime: 1}},
        {$limit: 1},
        {$project: {_id: 0, name: 1, runtime: 1}}
    )
"""

#
# 7. write a MongoDB query to find all movies that have won at least four of the Oscars in the database. Three fields:
# num_awards: the number of Oscars won by the movie
# types: an array containing the types of Oscars won by the movie
# movie: the name of the movie.
#
query7 = """
    db.oscars.aggregate(
        {$group: {_id: "$movie.id",
                   types: {$push: "$type"},
                   movie: {$first: "$movie.name"},
                   count: {$sum: 1}}},
        {$match: {count: {$gte: 4}}},
        {$project: {_id: 0,
                    num_awards: "$count",
                    types: "$types",
                    movie: "$movie"}}
    )
"""

#
# 8. Write a query to create, for each year from 2010 and 2020, a summary document that includes the following fields:
# 1. num_movies: the total number of movies from that year
# 2. avg_runtime: the average runtime of movies from that year
# 3. best_rank: the earnings rank of the movie from that year that has earned the most money. 
# The lower the earnings rank, the more money the movie has made.
# 4. year
# Sort the results documents by year, from 2010 to 2020.
# a null earnings_rank for certain year is possible and expected.
#
query8 = """
    db.movies.aggregate(
        {$match: {year: {$gte: 2010, $lte: 2020}}},
        {$group: {_id: "$year",
                  count: {$sum: 1},
                  avg_runtime: {$avg: "$runtime"},
                  best_rank: {$min: "$earnings_rank"}}},
        {$sort: {_id: 1}},
        {$project: {_id: 0,
                    num_movies: "$count",
                    avg_runtime: "$avg_runtime",
                    best_rank: "$best_rank",
                    year: "$_id"}}
    )
"""

#
# 9. Write a query to find all people who have acted in 3 or more of the animated movies in the database. 2 fields:
# num_animated: the number of animated movies in which the person acted
# actor: the name of the person
# Sorted by the number of movies, from largest to smallest, 
# and then by alphabetical order of actor's name for actors with same number of movies queried.
# Assumptions: all people in the database have unique names.
# all animated movies have an N somewhere in the sequence of letters that make up the value of their genre field.
#
query9 = """
    db.movies.aggregate(
        {$match: {genre: /N/}},
        {$unwind: "$actors"},
        {$group: {_id: "$actors.id",
                  count: {$sum: 1},
                  actor: {$first: "$actors.name"}}},
        {$match: {count: {$gte: 3}}},
        {$project: {_id: 0,
                    num_animated: "$count",
                    actor: "$actor"}},
        {$sort: {num_animated: -1, actor: 1}}
    )
"""

#
# 10. Find the top 5 countries in terms of the number of people in the database who were born there.
# num_born: the number of people in the database who were born in the country
# country: the name of the country.
#
query10 = """
    db.people.aggregate(
        {$match: {pob: {$exists: true}}},
        {$project: {country: {$arrayElemAt: [{$split: ["$pob", ", "]}, -1]}}},
        {$group: {_id: "$country",
                  num_born: {$sum: 1}}},
        {$sort: {num_born: -1}},
        {$limit: 5},
        {$project: {_id: 0,
                    num_born: "$num_born",
                    country: "$_id"}}
    )
"""
