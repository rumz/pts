
CREATE OR REPLACE FUNCTION weekdays(date,date) 
RETURNS BIGINT 
LANGUAGE SQL AS 
$_$ 
  SELECT count(*) FROM 
    (SELECT extract('dow' FROM $1+x) AS dow 
     FROM generate_series(0,$2-$1) x) AS foo 
  WHERE dow BETWEEN 1 AND 5; 
$_$; 

CREATE OR REPLACE FUNCTION weekdays(text,text) 
RETURNS BIGINT LANGUAGE SQL AS 
$_$ 
  SELECT weekdays($1::date,$2::date); 
$_$; 
