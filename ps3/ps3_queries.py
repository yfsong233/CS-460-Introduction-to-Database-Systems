#
# CS 460: Problem Set 3: XQuery Programming Problems
#

#
# For each query, use a text editor to add the appropriate XQuery
# command between the triple quotes provided for that query's variable.
#
# For example, here is how you would include a query that finds
# the names of all movies in the database from 1990.
#
sample = """
    for $m in //movie
    where $m/year = 1990
    return $m/name
"""

#
# 1. Put your query for this problem between the triple quotes found below.
#    Follow the same format as the model query shown above.
#
query1 = """
//person[contains(dob, "11-26")]/name
"""

#
# 2. Put your query for this problem between the triple quotes found below.
#
query2 = """
for $o in //oscar,
    $m in //movie
where $o/@movie_id = $m/@id and $o/type = 'BEST-PICTURE' and $o/year <= 2019 and $o/year >= 2010
order by $o/year
return <best_picture><year>{$o/year/text()}</year><name>{$m/name/text()}</name></best_picture>
"""

#
# 3. Put your query for this problem between the triple quotes found below.
#
query3 = """
for $o in //oscar, $m in //movie
where $o/@movie_id = $m/@id and $o/year = 1993 
return <oscar_93>
            <type> {$o/type/text()} </type>
            <movie> {$m/name/text()} </movie>
        {
            for $p in //person
            where $o/@person_id = $p/@id
            return <person> {$p/name/text()} </person>
        }
        </oscar_93>
"""

#
# 4. Put your query for this problem between the triple quotes found below.
#
query4 = """
for $y in distinct-values(//movie/year[. >= 2010])
let $m := //movie[year = $y]
order by $y
return <year_summary>
       <year>{$y}</year>
       <num_movies>{count($m)}</num_movies>
       <avg_runtime>{avg($m/runtime)}</avg_runtime>
        {
            for $id in distinct-values(//oscar[year = $y + 1]/@movie_id)
            return <oscar_winner>{//movie[@id = $id]/name/text()}</oscar_winner>
        }
        </year_summary>
"""

#
# 5. Put your query for this problem between the triple quotes found below.
#
query5 = """
for $m in //movie
let $w := //oscar[@movie_id = $m/@id], $oscar_y := $m/year + 1
where count($w) >= 4
order by $oscar_y
return
  <many_oscars>
    <movie>{$m/name/text()}</movie>
    <year>{$oscar_y}</year>
    {
      for $o in $w
      return <type>{$o/type/text()}</type>
    }
  </many_oscars>


"""
