# FITNESS CENTER DATA WAREHOUSE IMPLEMENTATION ROADMAP
## PostgreSQL ODS + Data Warehouse + Talend ETL

### **PostgreSQL Environment Setup**

#### **Step 1: Database Infrastructure**
```sql
-- Create separate databases for clean separation
CREATE DATABASE fitness_center_ods;
CREATE DATABASE fitness_center_dw;

-- Create dedicated users with appropriate permissions
CREATE USER ods_user WITH PASSWORD 'ods_secure_pwd';
CREATE USER dw_user WITH PASSWORD 'dw_secure_pwd';
CREATE USER etl_user WITH PASSWORD 'etl_secure_pwd';

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE fitness_center_ods TO ods_user;
GRANT ALL PRIVILEGES ON DATABASE fitness_center_dw TO dw_user;
GRANT CONNECT ON DATABASE fitness_center_ods TO etl_user;
GRANT CONNECT ON DATABASE fitness_center_dw TO etl_user;
```

#### **Step 2: ODS Schema Creation**
```sql
-- Connect to fitness_center_ods database
\c fitness_center_ods;

-- Create ODS schema matching your source system structure
CREATE SCHEMA ods;

-- ODS Tables (simplified for class project)
CREATE TABLE ods.members (
    member_id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth DATE,
    gender CHAR(1),
    phone VARCHAR(20),
    email VARCHAR(255),
    address VARCHAR(500),
    city VARCHAR(100),
    state VARCHAR(50),
    country VARCHAR(100),
    membership_type VARCHAR(50),
    join_date DATE,
    member_status VARCHAR(20),
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ods.facilities (
    facility_id VARCHAR(50) PRIMARY KEY,
    facility_name VARCHAR(200),
    address VARCHAR(500),
    city VARCHAR(100),
    state VARCHAR(50),
    country VARCHAR(100),
    region VARCHAR(50),
    phone VARCHAR(20),
    operating_hours VARCHAR(100),
    capacity INTEGER,
    facility_type VARCHAR(50),
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ods.facility_areas (
    area_id VARCHAR(50) PRIMARY KEY,
    facility_id VARCHAR(50) REFERENCES ods.facilities(facility_id),
    area_name VARCHAR(100),
    area_type VARCHAR(50),
    max_capacity INTEGER,
    square_footage DECIMAL(10,2),
    equipment_count INTEGER,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ods.staff (
    staff_id VARCHAR(50) PRIMARY KEY,
    employee_number VARCHAR(50),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    job_title VARCHAR(100),
    department VARCHAR(100),
    hire_date DATE,
    specialization VARCHAR(100),
    hourly_rate DECIMAL(10,2),
    employment_status VARCHAR(20),
    facility_id VARCHAR(50) REFERENCES ods.facilities(facility_id),
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ods.class_types (
    class_type_id VARCHAR(50) PRIMARY KEY,
    class_name VARCHAR(200),
    class_category VARCHAR(50),
    difficulty_level VARCHAR(20),
    duration_minutes INTEGER,
    max_participants INTEGER,
    required_certifications VARCHAR(500),
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ods.equipment (
    equipment_id VARCHAR(50) PRIMARY KEY,
    equipment_name VARCHAR(200),
    equipment_category VARCHAR(50),
    equipment_type VARCHAR(50),
    brand VARCHAR(100),
    model VARCHAR(100),
    serial_number VARCHAR(100),
    purchase_date DATE,
    warranty_expiry DATE,
    status VARCHAR(20),
    facility_id VARCHAR(50) REFERENCES ods.facilities(facility_id),
    area_id VARCHAR(50) REFERENCES ods.facility_areas(area_id),
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- FACT SOURCE TABLES
CREATE TABLE ods.class_enrollments (
    enrollment_id VARCHAR(50) PRIMARY KEY,
    member_id VARCHAR(50) REFERENCES ods.members(member_id),
    class_type_id VARCHAR(50) REFERENCES ods.class_types(class_type_id),
    instructor_id VARCHAR(50) REFERENCES ods.staff(staff_id),
    facility_id VARCHAR(50) REFERENCES ods.facilities(facility_id),
    area_id VARCHAR(50) REFERENCES ods.facility_areas(area_id),
    enrollment_date DATE,
    class_date DATE,
    scheduled_start_time TIME,
    actual_start_time TIME,
    scheduled_end_time TIME,
    actual_end_time TIME,
    enrollment_status VARCHAR(20),
    checkin_time TIME,
    checkout_time TIME,
    attendance_status VARCHAR(20),
    payment_amount DECIMAL(10,2),
    instructor_rating INTEGER,
    member_satisfaction_score INTEGER,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ods.equipment_usage (
    usage_id VARCHAR(50) PRIMARY KEY,
    member_id VARCHAR(50) REFERENCES ods.members(member_id),
    equipment_id VARCHAR(50) REFERENCES ods.equipment(equipment_id),
    usage_date DATE,
    start_time TIME,
    end_time TIME,
    duration_minutes INTEGER,
    usage_type VARCHAR(50),
    intensity_level INTEGER,
    member_satisfaction_score INTEGER,
    facility_id VARCHAR(50) REFERENCES ods.facilities(facility_id),
    area_id VARCHAR(50) REFERENCES ods.facility_areas(area_id),
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add indexes for ETL performance
CREATE INDEX idx_members_last_modified ON ods.members(last_modified);
CREATE INDEX idx_equipment_usage_date ON ods.equipment_usage(usage_date);
CREATE INDEX idx_class_enrollments_date ON ods.class_enrollments(enrollment_date);
```

#### **Step 3: Dimension Tables**
```sql
-- Connect to fitness_center_dw database
\c fitness_center_dw;

CREATE SCHEMA dw;

-- Shared Dimensions
CREATE TABLE dw.dim_geography (
    geography_key SERIAL PRIMARY KEY,
    city VARCHAR(100),
    state VARCHAR(50),
    country VARCHAR(100),
    region VARCHAR(50)
);

CREATE TABLE dw.dim_member (
    member_key SERIAL PRIMARY KEY,
    member_id VARCHAR(50),
    age_group VARCHAR(20),
    gender CHAR(1),
    geography_key INTEGER REFERENCES dw.dim_geography(geography_key),
    membership_type VARCHAR(50),
    join_date DATE,
    member_status VARCHAR(20),
    effective_date DATE,
    expiry_date DATE,
    is_current BOOLEAN DEFAULT TRUE
);

CREATE TABLE dw.dim_facility (
    facility_key SERIAL PRIMARY KEY,
    facility_id VARCHAR(50),
    facility_name VARCHAR(200),
    geography_key INTEGER REFERENCES dw.dim_geography(geography_key)
);

CREATE TABLE dw.dim_facility_area (
    area_key SERIAL PRIMARY KEY,
    area_id VARCHAR(50),
    facility_key INTEGER REFERENCES dw.dim_facility(facility_key),
    area_name VARCHAR(100),
    area_type VARCHAR(50)
);

CREATE TABLE dw.dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE,
    day_of_week VARCHAR(20),
    day_of_week_num INTEGER,
    week_of_year INTEGER,
    month_name VARCHAR(20),
    month_num INTEGER,
    year INTEGER,
    is_weekend BOOLEAN
);

CREATE TABLE dw.dim_time (
    time_key SERIAL PRIMARY KEY,
    time_30min TIME,
    hour_24 INTEGER,
    hour_12 INTEGER,
    am_pm VARCHAR(2),
    time_block VARCHAR(20),
    interval_of_day INTEGER
);

CREATE TABLE dw.dim_staff (
    staff_key SERIAL PRIMARY KEY,
    staff_id VARCHAR(50),
    instructor_name VARCHAR(200),
    job_title VARCHAR(100),
    specialization VARCHAR(100),
    hire_date DATE,
    effective_date DATE,
    expiry_date DATE,
    is_current BOOLEAN DEFAULT TRUE
);

-- Specialized Dimensions
CREATE TABLE dw.dim_class_type (
    class_type_key SERIAL PRIMARY KEY,
    class_type_id VARCHAR(50),
    class_name VARCHAR(200),
    class_category VARCHAR(50),
    duration_minutes INTEGER,
    max_participants INTEGER
);

CREATE TABLE dw.dim_equipment (
    equipment_key SERIAL PRIMARY KEY,
    equipment_id VARCHAR(50),
    equipment_name VARCHAR(200),
    equipment_category VARCHAR(50),
    equipment_type VARCHAR(50),
    facility_key INTEGER REFERENCES dw.dim_facility(facility_key),
    area_key INTEGER REFERENCES dw.dim_facility_area(area_key)
);
```

#### **Step 4: Fact Tables**
```sql
-- Fact Tables
CREATE TABLE dw.fact_class_enrollment (
    enrollment_key SERIAL PRIMARY KEY,
    member_key INTEGER REFERENCES dw.dim_member(member_key),
    class_type_key INTEGER REFERENCES dw.dim_class_type(class_type_key),
    staff_key INTEGER REFERENCES dw.dim_staff(staff_key),
    facility_key INTEGER REFERENCES dw.dim_facility(facility_key),
    area_key INTEGER REFERENCES dw.dim_facility_area(area_key),
    enrollment_date_key INTEGER REFERENCES dw.dim_date(date_key),
    class_date_key INTEGER REFERENCES dw.dim_date(date_key),
    start_time_key INTEGER REFERENCES dw.dim_time(time_key),
    
    -- Measures
    enrollment_count INTEGER DEFAULT 1,
    attendance_count INTEGER DEFAULT 0,
    no_show_count INTEGER DEFAULT 0,
    cancellation_count INTEGER DEFAULT 0,
    payment_amount DECIMAL(10,2),
    attendance_duration_minutes INTEGER,
    instructor_rating INTEGER,
    member_satisfaction_score INTEGER,
    late_arrival_minutes INTEGER DEFAULT 0,
    early_departure_minutes INTEGER DEFAULT 0
);

CREATE TABLE dw.fact_equipment_usage (
    usage_key SERIAL PRIMARY KEY,
    member_key INTEGER REFERENCES dw.dim_member(member_key),
    equipment_key INTEGER REFERENCES dw.dim_equipment(equipment_key),
    facility_key INTEGER REFERENCES dw.dim_facility(facility_key),
    area_key INTEGER REFERENCES dw.dim_facility_area(area_key),
    usage_date_key INTEGER REFERENCES dw.dim_date(date_key),
    start_time_key INTEGER REFERENCES dw.dim_time(time_key),
    
    -- Measures
    usage_session_count INTEGER DEFAULT 1,
    usage_duration_minutes INTEGER,
    peak_hour_flag INTEGER DEFAULT 0,
    weekend_usage_flag INTEGER DEFAULT 0,
    intensity_level INTEGER,
    member_satisfaction_score INTEGER
);

-- Performance indexes
CREATE INDEX idx_fact_class_enrollment_date ON dw.fact_class_enrollment(class_date_key);
CREATE INDEX idx_fact_equipment_usage_date ON dw.fact_equipment_usage(usage_date_key);
CREATE INDEX idx_fact_equipment_usage_equipment ON dw.fact_equipment_usage(equipment_key);
CREATE INDEX idx_fact_class_enrollment_member ON dw.fact_class_enrollment(member_key);
```
#### **Step 5: Static Date and Time Dimensions**

```sql
-- Populate DIM_DATE (5-year range)
INSERT INTO dw.dim_date (date_key, full_date, day_of_week, day_of_week_num, 
                        week_of_year, month_name, month_num, year, is_weekend)
SELECT 
    TO_CHAR(date_series, 'YYYYMMDD')::INTEGER as date_key,
    date_series as full_date,
    TO_CHAR(date_series, 'Day') as day_of_week,
    EXTRACT(DOW FROM date_series) as day_of_week_num,
    EXTRACT(WEEK FROM date_series) as week_of_year,
    TO_CHAR(date_series, 'Month') as month_name,
    EXTRACT(MONTH FROM date_series) as month_num,
    EXTRACT(YEAR FROM date_series) as year,
    CASE WHEN EXTRACT(DOW FROM date_series) IN (0,6) THEN TRUE ELSE FALSE END as is_weekend
FROM generate_series('2020-01-01'::date, '2030-12-31'::date, '1 day') as date_series;

-- Populate DIM_TIME (30-minute intervals)
INSERT INTO dw.dim_time (time_30min, hour_24, hour_12, am_pm, time_block, interval_of_day)
SELECT 
    time_series as time_30min,
    EXTRACT(HOUR FROM time_series) as hour_24,
    CASE 
        WHEN EXTRACT(HOUR FROM time_series) = 0 THEN 12
        WHEN EXTRACT(HOUR FROM time_series) > 12 THEN EXTRACT(HOUR FROM time_series) - 12
        ELSE EXTRACT(HOUR FROM time_series)
    END as hour_12,
    CASE WHEN EXTRACT(HOUR FROM time_series) < 12 THEN 'AM' ELSE 'PM' END as am_pm,
    CASE 
        WHEN EXTRACT(HOUR FROM time_series) BETWEEN 6 AND 11 THEN 'Morning'
        WHEN EXTRACT(HOUR FROM time_series) BETWEEN 12 AND 17 THEN 'Afternoon'
        WHEN EXTRACT(HOUR FROM time_series) BETWEEN 18 AND 22 THEN 'Evening'
        ELSE 'Off-Hours'
    END as time_block,
    ((EXTRACT(HOUR FROM time_series) * 2) + 
     CASE WHEN EXTRACT(MINUTE FROM time_series) >= 30 THEN 1 ELSE 0 END + 1) as interval_of_day
FROM generate_series('00:00:00'::time, '23:30:00'::time, '30 minutes') as time_series;
```

##### **PostgreSQL Data Import**
```sql
-- Import data using generated SQL scripts
\c fitness_center_ods;

-- Import in dependency order
\i ods_sample_data/sql_scripts/insert_facilities.sql
\i ods_sample_data/sql_scripts/insert_facility_areas.sql  
\i ods_sample_data/sql_scripts/insert_members.sql
\i ods_sample_data/sql_scripts/insert_staff.sql
\i ods_sample_data/sql_scripts/insert_class_types.sql
\i ods_sample_data/sql_scripts/insert_equipment.sql
\i ods_sample_data/sql_scripts/insert_class_enrollments.sql
\i ods_sample_data/sql_scripts/insert_equipment_usage.sql

-- Verify data import
SELECT 'facilities' as table_name, COUNT(*) as record_count FROM ods.facilities
UNION ALL
SELECT 'members', COUNT(*) FROM ods.members  
UNION ALL
SELECT 'equipment', COUNT(*) FROM ods.equipment
UNION ALL 
SELECT 'class_enrollments', COUNT(*) FROM ods.class_enrollments
UNION ALL
SELECT 'equipment_usage', COUNT(*) FROM ods.equipment_usage;
```

##### **Data Validation Queries**
```sql
-- Validate demographic distributions
SELECT 
    CASE 
        WHEN EXTRACT(YEAR FROM AGE(date_of_birth)) BETWEEN 18 AND 25 THEN '18-25'
        WHEN EXTRACT(YEAR FROM AGE(date_of_birth)) BETWEEN 26 AND 35 THEN '26-35'
        WHEN EXTRACT(YEAR FROM AGE(date_of_birth)) BETWEEN 36 AND 50 THEN '36-50'
        WHEN EXTRACT(YEAR FROM AGE(date_of_birth)) BETWEEN 51 AND 65 THEN '51-65'
        ELSE '65+'
    END as age_group,
    gender,
    COUNT(*) as member_count
FROM ods.members 
GROUP BY age_group, gender
ORDER BY age_group, gender;

-- Validate equipment category distribution  
SELECT equipment_category, COUNT(*) as equipment_count
FROM ods.equipment 
GROUP BY equipment_category;

-- Validate class attendance patterns
SELECT 
    attendance_status,
    COUNT(*) as enrollment_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM ods.class_enrollments
GROUP BY attendance_status;
```