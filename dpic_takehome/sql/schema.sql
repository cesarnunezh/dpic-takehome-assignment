-- Table: districts
DROP TABLE IF EXISTS districts;
CREATE TABLE districts(
    did char(4),
    name varchar(30),
    primary key (did)
    );

-- Table: itis
DROP TABLE IF EXISTS itis;
CREATE TABLE itis(
    iid char(4),
    name varchar(30),
    primary key (iid)
    );

-- Table: grievances
DROP TABLE IF EXISTS grievances;
CREATE TABLE grievances(
    district_name varchar(30),
    submission_date date,
    grievance_text text,
    submitted_by varchar(30),
    year int,
    resolved float,
    did char(4),
    cat_grivance text,
    primary key (district_name, submission_date, grievance_text, submitted_by),
    foreign key (did) references districts
    );

-- Table: iti_enrollment
DROP TABLE IF EXISTS iti_enrollments;
CREATE TABLE iti_enrollments(
    year int,
    district varchar(30),
    institute_name text,
    program text,
    gender varchar(6),
    enrolled float,
    did char(4),
    iid char(4),
    primary key (year, district, institute_name, program, gender),
    foreign key (did) references districts,
    foreign key (iid) references itis
    );