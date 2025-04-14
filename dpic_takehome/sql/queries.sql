-- 1. Year-wise enrollment trends by gender
SELECT i.year, i.gender, SUM(i.enrolled) as enrollment
FROM iti_enrollments as i
GROUP BY i.year, i.gender;

-- 2. Year-wise grievences trends by type of grievances
SELECT g.year, g.cat_grivance, COUNT(g.grievance_text) as num_grievances
FROM grievances as g
GROUP BY g.year, g.cat_grivance;

-- 3. Grievances per 1000 enrolled students by district
WITH enrolment_by_year AS (SELECT i.year, i.did, i.district, SUM(i.enrolled) as enrollment
                           FROM iti_enrollments as i
                           GROUP BY i.year, i.did, i.district),
grivances_by_year AS (SELECT g.year, g.did, g.district_name, COUNT(g.grievance_text) as num_grievances
                      FROM grievances as g
                      GROUP BY g.year, g.did, g.district_name)
SELECT e.year, e.did, e.district, (g.num_grievances / e.enrollment)*1000 as grievances_pc
FROM enrolment_by_year as e
JOIN grivances_by_year as g ON e.did == g.did AND e.year == g.year
ORDER BY e.year ASC, grievances_pc DESC;

-- 4. Districts with high enrollments but low grievance submissions
WITH enrollment_dist AS (SELECT did, district, AVG(enrolled) AS avg_enrolled
                         FROM (SELECT year, did, district, SUM(enrolled) as enrolled
                         FROM iti_enrollments as i
                         GROUP BY year, did, district)
                         GROUP BY did, district),
enrollment_qtle AS (SELECT *, NTILE(4) OVER (ORDER BY avg_enrolled DESC) AS qtle
                    FROM enrollment_dist),
grievances_dist AS (SELECT g.did, g.district_name, COUNT(g.grievance_text) as num_grievances
                    FROM grievances as g
                    GROUP BY g.did, g.district_name),
grievances_qtle AS (SELECT *, NTILE(4) OVER (ORDER BY num_grievances DESC) AS qtle
                    FROM grievances_dist)
SELECT t.did, t.district, t.avg_enrolled, g.num_grievances
FROM enrollment_qtle as t, grievances_qtle as g
WHERE t.qtle <= 2 AND g.qtle <= 2 AND t.did == g.did
ORDER BY t.avg_enrolled DESC;

-- 5. Types of grievances per district
SELECT g.year, g.did, g.district_name, g.cat_grivance, COUNT(g.cat_grivance) as num_grievances
FROM grievances as g
GROUP BY g.year, g.did, g.district_name, g.cat_grivance

-- 6. Enrolment by program and district
SELECT i.year, i.district, i.program, SUM(i.enrolled) as enrollment
FROM iti_enrollments as i
GROUP BY i.year, i.district, i.program
ORDER BY i.year DESC, enrollment ASC;