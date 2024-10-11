#
# CS 460: Problem Set 4: XQuery Programming Problems
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
# 1. find the names of all directors in the database who were born in Canada.
#
query1 = """
//person[@directed][contains(pob, 'Canada')]/name
"""

#
# 2. find the names of all directors in the database who were born in Canada 
# eg. <canadian_dir>Norman Jewison (Toronto, Ontario, Canada)</canadian_dir>
query2 = """
for $p in //person[@directed][contains(pob, 'Canada')]
let $name := $p/name
let $pob := $p/pob
order by $name
return 
    <canadian_dir>
        {$name/text(), " (", $pob/text(), ")"}
    </canadian_dir>

"""

#
# 3. Put your query for this problem between the triple quotes found below.
#
query3 = """
for $p in //person[@directed][contains(pob, 'Canada')]
let $pname := $p/name
let $directed := //movie[contains(@directors, $p/@id)]
let $avg_rt := if (count($directed) > 0) then avg($directed/runtime)
               else 0
order by $pname
return <canadian_dir>
    <name>{$pname/text()}</name>
    <pob>{$p/pob/text()}</pob>
    {
        for $m in $directed
        return <directed>{$m/name/text()}</directed>
    }
    <avg_runtime>{$avg_rt}</avg_runtime>
    <num_top_grossers>{count($directed[earnings_rank])}</num_top_grossers>
</canadian_dir>
"""

#
# 4. Put your query for this problem between the triple quotes found below.
#
query4 = """
for $o1 in //oscar,
    $o2 in //oscar
where $o1/@person_id = $o2/@person_id
    and $o1/year = $o2/year - 1
let $p := //person[@id = $o1/@person_id]
return 
    <back_to_back>
        <name>{$p/name/text()}</name>
        <first_win>{($o1/type/text(), " (", $o1/year/text(), ")")}</first_win>
        <second_win>{($o2/type/text(), " (", $o2/year/text(), ")")}</second_win>
    </back_to_back>

"""
