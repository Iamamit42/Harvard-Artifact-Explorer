queries = {

# ---------------- artifact_metadata ---------------- #

"1. List all artifacts from the 11th century belonging to Byzantine culture":
"""
SELECT *
FROM artifact_metadata
WHERE century='11th century'
AND culture='Byzantine';
""",

"2. Unique cultures represented":
"""
SELECT DISTINCT culture
FROM artifact_metadata
WHERE culture IS NOT NULL
ORDER BY culture;
""",

"3. List all artifacts from the Archaic Period":
"""
SELECT *
FROM artifact_metadata
WHERE period='Archaic Period';
""",

"4. Artifact titles ordered by accession year":
"""
SELECT title, accessionyear
FROM artifact_metadata
ORDER BY accessionyear DESC;
""",

"5. Number of artifacts per department":
"""
SELECT department,
COUNT(*) AS total_artifacts
FROM artifact_metadata
GROUP BY department
ORDER BY total_artifacts DESC;
""",

# ---------------- artifact_media ---------------- #

"6. Artifacts having more than one image":
"""
SELECT objectid,imagecount
FROM artifact_media
WHERE imagecount>1;
""",

"7. Average artifact rank":
"""
SELECT AVG(`rank`) AS average_rank
FROM artifact_media;
""",

"8. Colorcount greater than mediacount":
"""
SELECT objectid,colorcount,mediacount
FROM artifact_media
WHERE colorcount>mediacount;
""",

"9. Artifacts created between 1500 and 1600":
"""
SELECT objectid,datebegin,dateend
FROM artifact_media
WHERE datebegin>=1500
AND dateend<=1600;
""",

"10. Artifacts having no media":
"""
SELECT COUNT(*) AS no_media
FROM artifact_media
WHERE mediacount=0;
""",

# ---------------- artifact_colors ---------------- #

"11. Distinct hues":
"""
SELECT DISTINCT hue
FROM artifact_colors
WHERE hue IS NOT NULL
ORDER BY hue;
""",

"12. Top 5 most used colors":
"""
SELECT color,
COUNT(*) AS frequency
FROM artifact_colors
GROUP BY color
ORDER BY frequency DESC
LIMIT 5;
""",

"13. Average coverage percentage by hue":
"""
SELECT hue,
AVG(percent) AS average_percent
FROM artifact_colors
GROUP BY hue
ORDER BY average_percent DESC;
""",

"14. Colors used for a given artifact":
"""
SELECT *
FROM artifact_colors
WHERE objectid = 299843;
""",

"15. Total color entries":
"""
SELECT COUNT(*) AS total_colors
FROM artifact_colors;
""",

# ---------------- JOIN QUERIES ---------------- #

"16. Byzantine artifacts with hues":
"""
SELECT m.title,
c.hue
FROM artifact_metadata m
JOIN artifact_colors c
ON m.id=c.objectid
WHERE m.culture='Byzantine';
""",

"17. Artifact title with associated hues":
"""
SELECT m.title,
c.hue
FROM artifact_metadata m
JOIN artifact_colors c
ON m.id=c.objectid;
""",

"18. Title, culture and media rank":
"""
SELECT m.title,
m.culture,
a.`rank`
FROM artifact_metadata m
JOIN artifact_media a
ON m.id=a.objectid
WHERE m.period IS NOT NULL;
""",

"19. Top 10 ranked artifacts having Grey hue":
"""
SELECT m.title,
a.`rank`,
c.hue
FROM artifact_metadata m
JOIN artifact_media a
ON m.id=a.objectid
JOIN artifact_colors c
ON m.id=c.objectid
WHERE c.hue='Grey'
ORDER BY a.`rank`
LIMIT 10;
""",

"20. Classification with average media count":
"""
SELECT m.classification,
COUNT(*) AS total_artifacts,
AVG(a.mediacount) AS average_media
FROM artifact_metadata m
JOIN artifact_media a
ON m.id=a.objectid
GROUP BY m.classification
ORDER BY total_artifacts DESC;
""",

# ---------------- EXTRA QUERIES ---------------- #

"21. Top 10 classifications":
"""
SELECT classification,
COUNT(*) total
FROM artifact_metadata
GROUP BY classification
ORDER BY total DESC
LIMIT 10;
""",

"22. Top 10 centuries":
"""
SELECT century,
COUNT(*) total
FROM artifact_metadata
GROUP BY century
ORDER BY total DESC
LIMIT 10;
""",

"23. Average image count by department":
"""
SELECT m.department,
AVG(a.imagecount) average_images
FROM artifact_metadata m
JOIN artifact_media a
ON m.id=a.objectid
GROUP BY m.department;
""",

"24. Top 10 cultures":
"""
SELECT culture,
COUNT(*) total
FROM artifact_metadata
WHERE culture IS NOT NULL
GROUP BY culture
ORDER BY total DESC
LIMIT 10;
""",

"25. Average colors per classification":
"""
SELECT m.classification,
AVG(a.colorcount) average_colors
FROM artifact_metadata m
JOIN artifact_media a
ON m.id=a.objectid
GROUP BY m.classification;
""",

"26. Oldest artifacts":
"""
SELECT title,
datebegin
FROM artifact_metadata
JOIN artifact_media
ON artifact_metadata.id=artifact_media.objectid
ORDER BY datebegin
LIMIT 20;
""",

"27. Newest artifacts":
"""
SELECT title,
dateend
FROM artifact_metadata
JOIN artifact_media
ON artifact_metadata.id=artifact_media.objectid
ORDER BY dateend DESC
LIMIT 20;
""",

"28. Top 10 mediums":
"""
SELECT medium,
COUNT(*) total
FROM artifact_metadata
WHERE medium IS NOT NULL
GROUP BY medium
ORDER BY total DESC
LIMIT 10;
""",

"29. Average accession year by classification":
"""
SELECT classification,
AVG(accessionyear) avg_year
FROM artifact_metadata
GROUP BY classification;
""",

"30. Artifacts with highest color count":
"""
SELECT objectid,
colorcount
FROM artifact_media
ORDER BY colorcount DESC
LIMIT 20;
"""
}
