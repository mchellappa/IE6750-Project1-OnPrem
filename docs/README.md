# Fitness Center ODS Database Schema

## Overview
This document presents the Entity Relationship Diagram (ERD) for the Fitness Center Operational Data Store (ODS). The schema supports comprehensive analytics for multi-location fitness centers, including member management, facility operations, class scheduling, equipment tracking, and staff management.

## Milestone 1: Table Classification Summary

The fitness center ODS architecture consists of **Static Reference Tables** that contain stable master data used for lookups and configuration, and **Transactional Tables** that capture business events and operational data for analytics.

**Static Reference Tables (8 entities):**
• MembershipTypes - Membership plan definitions and pricing structures
• ClassTypes - Class categories and fitness program definitions  
• InstructorCertifications - Available fitness instructor certifications
• Facilities - Fitness center location and facility information
• FacilityAreas - Specific areas within facilities (pools, courts, studios, gym)
• Equipment - Equipment inventory and asset specifications
• Members - Member demographics and contact information
• Staff - Employee information and job details

**Transactional Tables (15 entities):**
• MemberAccess - Member check-in/check-out logs for facility usage tracking
• EquipmentUsage - Equipment usage sessions and duration tracking
• ClassEnrollments - Class bookings, attendance, and enrollment history
• ClassSchedules - Recurring class schedules and instructor assignments
• ClassInstances - Individual class sessions with actual attendance data
• StaffSchedules - Staff shift schedules and work assignments
• MemberPayments - Payment transactions and billing history
• MemberMemberships - Membership enrollment and renewal history
• StaffTimeTracking - Actual work hours and time tracking records
• StaffPayroll - Payroll processing and compensation records
• EquipmentMaintenance - Equipment service and maintenance history
• StaffFacilities - Staff facility assignment history
• StaffCertifications - Staff certification tracking and renewals
• InstructorPerformance - Instructor performance evaluations
• InstructorFeedback - Member feedback on instructor effectiveness

## Database Schema Entity Relationship Diagram

```mermaid
erDiagram
    %% Member Management Domain
    MEMBERS {
        varchar memberid PK
        varchar firstname
        varchar lastname
        varchar email
        varchar phone
        date dateofbirth
        char gender
        varchar address
        varchar city
        varchar state
        varchar zipcode
        varchar emergencycontact
        varchar emergencyphone
        text medicalalerts
        date joindate
        varchar memberstatus
        timestamp lastmodified
    }

    MEMBERSHIPTYPES {
        varchar membershiptypeid PK
        varchar typename
        text description
        decimal monthlyfee
        decimal registrationfee
        int duration
        int maxfamilymembers
        boolean isactive
        timestamp createddate
    }

    MEMBERMEMBERSHIPS {
        varchar membershipid PK
        varchar memberid FK
        varchar membershiptypeid FK
        date startdate
        date enddate
        varchar status
        boolean autorenew
    }

    MEMBERPAYMENTS {
        varchar paymentid PK
        varchar memberid FK
        date paymentdate
        decimal amount
        varchar paymenttype
        varchar paymentmethod
        varchar status
    }

    %% Facility Management Domain
    FACILITIES {
        varchar facilityid PK
        varchar facilityname
        varchar address
        varchar city
        varchar state
        varchar zipcode
        varchar phonenumber
        time opentime
        time closetime
        boolean isactive
    }

    FACILITYAREAS {
        varchar areaid PK
        varchar facilityid FK
        varchar areaname
        varchar areatype
        int maxcapacity
        decimal squarefootage
        boolean isactive
    }

    MEMBERACCESS {
        varchar accessid PK
        varchar memberid FK
        varchar facilityid FK
        varchar areaid FK
        timestamp checkintime
        timestamp checkouttime
        varchar accessmethod
        int duration
    }

    %% Class Management Domain
    CLASSTYPES {
        varchar classtypeid PK
        varchar classname
        varchar category
        text description
        int durationminutes
        int maxparticipants
        varchar requiredcertifications
        boolean isactive
    }

    CLASSSCHEDULES {
        varchar scheduleid PK
        varchar classtypeid FK
        varchar facilityid FK
        varchar areaid FK
        varchar instructorid FK
        int dayofweek
        time starttime
        time endtime
        int maxcapacity
        decimal price
        date effectivedate
        date expirydate
        boolean isactive
    }

    CLASSINSTANCES {
        varchar instanceid PK
        varchar scheduleid FK
        date classdate
        timestamp actualstarttime
        timestamp actualendtime
        varchar actualinstructorid FK
        int actualcapacity
        varchar status
        text cancellationreason
    }

    CLASSENROLLMENTS {
        varchar enrollmentid PK
        varchar memberid FK
        varchar instanceid FK
        timestamp enrollmentdate
        varchar enrollmentstatus
        decimal paymentamount
        timestamp checkintime
        timestamp checkouttime
    }

    %% Equipment Management Domain
    EQUIPMENT {
        varchar equipmentid PK
        varchar facilityid FK
        varchar areaid FK
        varchar equipmentname
        varchar equipmenttype
        varchar brand
        varchar model
        varchar serialnumber
        date purchasedate
        decimal purchaseprice
        date warrantyexpiry
        varchar status
    }

    EQUIPMENTUSAGE {
        varchar usageid PK
        varchar equipmentid FK
        varchar memberid FK
        timestamp starttime
        timestamp endtime
        int durationminutes
        varchar usagetype
        text notes
    }

    EQUIPMENTMAINTENANCE {
        varchar maintenanceid PK
        varchar equipmentid FK
        date maintenancedate
        varchar maintenancetype
        varchar technicianname
        text description
        decimal cost
        text partsreplaced
        date nextmaintenancedate
    }

    %% Staff Management Domain
    STAFF {
        varchar staffid PK
        varchar employeenumber
        varchar firstname
        varchar lastname
        varchar email
        varchar phone
        date hiredate
        varchar jobtitle
        varchar department
        varchar employmenttype
        decimal hourlyrate
        varchar status
        date terminationdate
    }

    STAFFFACILITIES {
        varchar assignmentid PK
        varchar staffid FK
        varchar facilityid FK
        boolean isprimary
        date startdate
        date enddate
    }

    STAFFSCHEDULES {
        varchar scheduleid PK
        varchar staffid FK
        varchar facilityid FK
        varchar areaid FK
        date scheduledate
        time starttime
        time endtime
        decimal scheduledhours
        varchar shifttype
        varchar status
    }

    STAFFTIMETRACKING {
        varchar timetrackingid PK
        varchar staffid FK
        varchar scheduleid FK
        timestamp actualstarttime
        timestamp actualendtime
        decimal actualhours
        decimal overtimehours
        int breakminutes
        text notes
    }

    STAFFPAYROLL {
        varchar payrollid PK
        varchar staffid FK
        date payperiodstart
        date payperiodend
        decimal regularhours
        decimal overtimehours
        decimal regularpay
        decimal overtimepay
        decimal bonuses
        decimal deductions
        decimal grosspay
        decimal netpay
        date paydate
    }

    %% Instructor Performance Domain
    INSTRUCTORCERTIFICATIONS {
        varchar certificationid PK
        varchar certificationname
        varchar issuingorganization
        text description
        int validitymonths
        boolean isrequired
    }

    STAFFCERTIFICATIONS {
        varchar staffcertificationid PK
        varchar staffid FK
        varchar certificationid FK
        date certificationdate
        date expirydate
        varchar certificationnumber
        varchar status
    }

    INSTRUCTORPERFORMANCE {
        varchar performanceid PK
        varchar instructorid FK
        date evaluationdate
        varchar evaluatorid FK
        int classespermonth
        decimal averageattendance
        decimal memberretentionrate
        decimal membersatisfactionscore
        decimal professionalismscore
        decimal communicationscore
        decimal overallrating
        text comments
        text goalsfornextperiod
    }

    INSTRUCTORFEEDBACK {
        varchar feedbackid PK
        varchar memberid FK
        varchar instructorid FK
        varchar classinstanceid FK
        date feedbackdate
        int teachingquality
        int communication
        int motivation
        int overallrating
        text comments
        boolean isanonymous
    }

    %% Relationships
    MEMBERS ||--o{ MEMBERMEMBERSHIPS : "has"
    MEMBERSHIPTYPES ||--o{ MEMBERMEMBERSHIPS : "defines"
    MEMBERS ||--o{ MEMBERPAYMENTS : "makes"
    MEMBERS ||--o{ MEMBERACCESS : "accesses"
    MEMBERS ||--o{ CLASSENROLLMENTS : "enrolls"
    MEMBERS ||--o{ EQUIPMENTUSAGE : "uses"
    MEMBERS ||--o{ INSTRUCTORFEEDBACK : "provides"

    FACILITIES ||--o{ FACILITYAREAS : "contains"
    FACILITIES ||--o{ MEMBERACCESS : "accessed_at"
    FACILITIES ||--o{ CLASSSCHEDULES : "hosts"
    FACILITIES ||--o{ EQUIPMENT : "houses"
    FACILITIES ||--o{ STAFFFACILITIES : "assigns"
    FACILITIES ||--o{ STAFFSCHEDULES : "schedules"

    FACILITYAREAS ||--o{ MEMBERACCESS : "accessed_in"
    FACILITYAREAS ||--o{ CLASSSCHEDULES : "scheduled_in"
    FACILITYAREAS ||--o{ EQUIPMENT : "located_in"
    FACILITYAREAS ||--o{ STAFFSCHEDULES : "assigned_to"

    CLASSTYPES ||--o{ CLASSSCHEDULES : "defines"
    CLASSSCHEDULES ||--o{ CLASSINSTANCES : "instantiates"
    CLASSINSTANCES ||--o{ CLASSENROLLMENTS : "enrolls_in"
    CLASSINSTANCES ||--o{ INSTRUCTORFEEDBACK : "receives_feedback"

    EQUIPMENT ||--o{ EQUIPMENTUSAGE : "tracked_usage"
    EQUIPMENT ||--o{ EQUIPMENTMAINTENANCE : "maintained"

    STAFF ||--o{ STAFFFACILITIES : "assigned_to"
    STAFF ||--o{ STAFFSCHEDULES : "scheduled"
    STAFF ||--o{ STAFFTIMETRACKING : "tracks_time"
    STAFF ||--o{ STAFFPAYROLL : "receives_pay"
    STAFF ||--o{ STAFFCERTIFICATIONS : "holds"
    STAFF ||--o{ CLASSSCHEDULES : "instructs"
    STAFF ||--o{ INSTRUCTORPERFORMANCE : "evaluated"
    STAFF ||--o{ INSTRUCTORFEEDBACK : "receives"

    INSTRUCTORCERTIFICATIONS ||--o{ STAFFCERTIFICATIONS : "grants"
    STAFFSCHEDULES ||--o{ STAFFTIMETRACKING : "tracks"
```

## MDM vs ODS Tables Classification

### Master Data Management (MDM) Tables

| Table Name | Category | Update Frequency | Volume | Purpose |
|------------|----------|------------------|---------|----------|
| **MEMBERSHIPTYPES** | Business Configuration | Annually or when new plans introduced | Low (5-20 records) | Define membership plans and pricing structure |
| **CLASSTYPES** | Business Configuration | Quarterly when new class types added | Low (20-50 records) | Define available class categories and requirements |
| **INSTRUCTORCERTIFICATIONS** | Business Configuration | Rarely (when industry standards change) | Low (10-30 records) | Define required and optional instructor certifications |
| **FACILITIES** | Facility & Asset Master | Rarely (when new locations open/close) | Low (1-50 records) | Define physical facility locations and operating hours |
| **FACILITYAREAS** | Facility & Asset Master | Infrequently (during renovations/expansions) | Medium (50-200 records) | Define specific areas within facilities with capacity limits |
| **EQUIPMENT** | Facility & Asset Master | Monthly (as equipment is purchased/retired) | Medium-High (500-5000 records) | Track equipment assets for maintenance and usage analysis |
| **MEMBERS** | People Master Data | Regularly (as members update personal info) | High (1,000-50,000+ records) | Core member information for all analytics and operations |
| **STAFF** | People Master Data | Monthly (hiring, role changes, terminations) | Medium (50-500 records) | Employee master data for scheduling and performance tracking |

### Operational Data Store (ODS) Tables

| Table Name | Category | Transaction Frequency | Volume Growth | Analytics Use |
|------------|----------|----------------------|---------------|---------------|
| **MEMBERACCESS** | High-Volume Operations | Continuous (thousands per day) | High (millions annually) | Peak usage patterns, facility utilization, member behavior |
| **EQUIPMENTUSAGE** | High-Volume Operations | Continuous (usage sessions) | High (hundreds of thousands annually) | Equipment utilization, maintenance planning, member preferences |
| **CLASSENROLLMENTS** | High-Volume Operations | Daily (class registrations/attendance) | Medium-High (tens of thousands annually) | Class popularity, instructor effectiveness, member engagement |
| **CLASSSCHEDULES** | Scheduled Processes | Weekly/Monthly (schedule updates) | Medium (schedule changes/new classes) | Resource allocation, instructor assignments |
| **CLASSINSTANCES** | Scheduled Processes | Daily (one per scheduled class) | Medium-High (thousands annually) | Actual vs scheduled analysis, cancellation patterns |
| **STAFFSCHEDULES** | Scheduled Processes | Weekly (shift scheduling) | Medium (weekly schedules per staff) | Labor cost analysis, coverage optimization |
| **MEMBERPAYMENTS** | Financial & HR | Monthly (recurring payments) + ad-hoc | Medium (monthly payments per member) | Revenue analysis, payment trends, delinquency tracking |
| **MEMBERMEMBERSHIPS** | Financial & HR | Monthly (enrollments/renewals/cancellations) | Medium (membership lifecycle events) | Retention analysis, membership trends |
| **STAFFTIMETRACKING** | Financial & HR | Daily (shift completion) | Medium-High (daily records per staff) | Labor cost analysis, overtime tracking |
| **STAFFPAYROLL** | Financial & HR | Bi-weekly/Monthly (payroll cycles) | Medium (payroll records per staff) | Labor cost analysis, compensation trends |
| **EQUIPMENTMAINTENANCE** | Maintenance & Operations | Weekly/Monthly (maintenance events) | Medium (maintenance events per equipment) | Predictive maintenance, cost optimization |
| **STAFFFACILITIES** | Performance & Feedback | Monthly (assignment changes) | Low-Medium (assignment history) | Staff allocation analysis |
| **STAFFCERTIFICATIONS** | Performance & Feedback | Quarterly/Annually (certification events) | Low-Medium (certifications per staff) | Certification compliance, training needs |
| **INSTRUCTORPERFORMANCE** | Performance & Feedback | Quarterly/Annually (evaluation cycles) | Low-Medium (evaluations per instructor) | Instructor effectiveness analysis |
| **INSTRUCTORFEEDBACK** | Performance & Feedback | Weekly (member feedback submission) | Medium (feedback per class/instructor) | Instructor performance, member satisfaction |

### ETL Strategy Summary

| Table Type | Loading Strategy | Update Frequency | Data Quality Focus | Storage Optimization |
|------------|------------------|------------------|-------------------|---------------------|
| **MDM Tables** | Full refresh or CDC | Daily or real-time for critical changes | High validation, business rule enforcement | Optimized for lookups, minimal indexing overhead |
| **ODS Tables** | Incremental loads based on timestamps | Real-time or micro-batch (5-15 minutes) | Focus on completeness and timeliness | Partitioned by date, optimized for analytical queries |

## Data Population Strategy for Class Project

### Python Libraries for Fake Data Generation

**Required Libraries:**
```bash
pip3 install faker pandas psycopg2-binary numpy datetime random
```

**Core Libraries Used:**
- **Faker**: Realistic fake personal data (names, addresses, emails, etc.)
- **Pandas**: Data manipulation and CSV generation
- **NumPy**: Statistical distributions and random number generation
- **Random**: Python's built-in randomization
- **DateTime**: Date and time manipulation
- **Psycopg2**: PostgreSQL database connectivity

### MDM Tables Population Approach

#### **1. Business Configuration Tables (Python Generated)**

**MembershipTypes, ClassTypes, InstructorCertifications:**
- **Generation Method**: Python scripts with predefined business rules
- **Libraries**: Built-in data structures with realistic pricing models

```python
import pandas as pd
import random
from faker import Faker

fake = Faker()

def generate_membership_types():
    """Generate realistic membership types with pricing"""
    membership_data = [
        {'MembershipTypeID': 'MT001', 'TypeName': 'Individual Monthly', 'MonthlyFee': 49.99, 'RegistrationFee': 25.00},
        {'MembershipTypeID': 'MT002', 'TypeName': 'Family Monthly', 'MonthlyFee': 89.99, 'RegistrationFee': 50.00},
        {'MembershipTypeID': 'MT003', 'TypeName': 'Student Monthly', 'MonthlyFee': 29.99, 'RegistrationFee': 15.00},
        {'MembershipTypeID': 'MT004', 'TypeName': 'Senior Monthly', 'MonthlyFee': 39.99, 'RegistrationFee': 20.00},
        {'MembershipTypeID': 'MT005', 'TypeName': 'Corporate Monthly', 'MonthlyFee': 44.99, 'RegistrationFee': 30.00},
        {'MembershipTypeID': 'MT006', 'TypeName': 'Individual Annual', 'MonthlyFee': 41.66, 'RegistrationFee': 0.00},
        {'MembershipTypeID': 'MT007', 'TypeName': 'Family Annual', 'MonthlyFee': 75.00, 'RegistrationFee': 0.00}
    ]
    return pd.DataFrame(membership_data)

def generate_class_types():
    """Generate diverse fitness class types"""
    class_types = [
        'Yoga', 'Pilates', 'Zumba', 'Spin Cycle', 'CrossFit', 'HIIT', 
        'Aqua Aerobics', 'Kickboxing', 'Boot Camp', 'Strength Training',
        'Barre', 'TRX', 'Boxing', 'Dance Fitness', 'Tai Chi'
    ]
    
    class_data = []
    for i, class_name in enumerate(class_types, 1):
        class_data.append({
            'ClassTypeID': f'CT{i:03d}',
            'TypeName': class_name,
            'Duration': random.choice([30, 45, 60, 90]),
            'MaxParticipants': random.randint(8, 25),
            'EquipmentRequired': random.choice([True, False])
        })
    
    return pd.DataFrame(class_data)

# Generate and save data
membership_df = generate_membership_types()
class_types_df = generate_class_types()

print("Sample Membership Types:")
print(membership_df.head())
```

#### **2. Facility & Asset Master Data (Python Generated)**

**Facilities, FacilityAreas, Equipment:**
- **Generation Method**: Faker for facility names, structured data for areas and equipment
- **Libraries**: Faker, Pandas, NumPy for realistic facility layouts

```python
import numpy as np
from datetime import datetime, timedelta

def generate_facilities(num_facilities=5):
    """Generate realistic fitness facilities"""
    facilities = []
    
    for i in range(1, num_facilities + 1):
        facility = {
            'FacilityID': f'FAC{i:03d}',
            'FacilityName': f"{fake.city()} Fitness Center",
            'Address': fake.street_address(),
            'City': fake.city(),
            'State': fake.state_abbr(),
            'ZipCode': fake.zipcode(),
            'PhoneNumber': fake.phone_number(),
            'OpeningHours': '5:00 AM - 11:00 PM',
            'TotalSquareFootage': random.randint(8000, 25000),
            'OpeningDate': fake.date_between(start_date='-10y', end_date='-1y')
        }
        facilities.append(facility)
    
    return pd.DataFrame(facilities)

def generate_facility_areas(facilities_df):
    """Generate areas within each facility"""
    area_types = [
        'Cardio Zone', 'Weight Training', 'Group Fitness Studio', 'Pool Area',
        'Locker Rooms', 'Reception', 'Juice Bar', 'Child Care', 'Yoga Studio',
        'Spin Room', 'Basketball Court', 'Racquetball Court'
    ]
    
    areas = []
    area_id = 1
    
    for _, facility in facilities_df.iterrows():
        # Each facility gets 6-10 random areas
        facility_areas = random.sample(area_types, random.randint(6, 10))
        
        for area_name in facility_areas:
            area = {
                'AreaID': f'AR{area_id:03d}',
                'FacilityID': facility['FacilityID'],
                'AreaName': area_name,
                'SquareFootage': random.randint(500, 3000),
                'MaxCapacity': random.randint(10, 50),
                'AccessLevel': random.choice(['General', 'Premium', 'Staff Only'])
            }
            areas.append(area)
            area_id += 1
    
    return pd.DataFrame(areas)

def generate_equipment(areas_df):
    """Generate equipment for facility areas"""
    equipment_types = {
        'Cardio Zone': ['Treadmill', 'Elliptical', 'Stationary Bike', 'Rowing Machine'],
        'Weight Training': ['Bench Press', 'Squat Rack', 'Cable Machine', 'Dumbbells', 'Leg Press'],
        'Group Fitness Studio': ['Sound System', 'Mirrors', 'Yoga Mats', 'Resistance Bands'],
        'Pool Area': ['Lane Dividers', 'Pool Vacuum', 'Water Testing Kit'],
        'Spin Room': ['Spin Bikes', 'Sound System', 'Mirrors']
    }
    
    equipment = []
    equipment_id = 1
    
    for _, area in areas_df.iterrows():
        area_name = area['AreaName']
        if area_name in equipment_types:
            # Generate 3-8 pieces of equipment per relevant area
            for _ in range(random.randint(3, 8)):
                equipment_type = random.choice(equipment_types[area_name])
                equip = {
                    'EquipmentID': f'EQ{equipment_id:04d}',
                    'AreaID': area['AreaID'],
                    'EquipmentType': equipment_type,
                    'Brand': fake.company(),
                    'Model': f"{equipment_type}-{random.randint(100, 999)}",
                    'PurchaseDate': fake.date_between(start_date='-5y', end_date='today'),
                    'WarrantyExpiry': fake.date_between(start_date='today', end_date='+2y'),
                    'Status': random.choice(['Active', 'Maintenance', 'Out of Order'], weights=[85, 10, 5])
                }
                equipment.append(equip)
                equipment_id += 1
    
    return pd.DataFrame(equipment)

# Generate facility data
facilities_df = generate_facilities(5)
areas_df = generate_facility_areas(facilities_df)
equipment_df = generate_equipment(areas_df)

print(f"Generated {len(facilities_df)} facilities, {len(areas_df)} areas, {len(equipment_df)} equipment items")
```

#### **3. People Master Data (Faker Library Integration)**

**Members, Staff:**
- **Generation Method**: Faker for realistic personal data with business logic
- **Libraries**: Faker with custom providers for fitness-specific data

```python
from datetime import datetime, timedelta
import uuid

def generate_members(num_members=1000, membership_types_df=None):
    """Generate realistic member data using Faker"""
    members = []
    
    for i in range(1, num_members + 1):
        # Generate realistic join dates (weighted toward recent years)
        join_date = fake.date_between(start_date='-3y', end_date='today')
        
        # Determine membership status based on join date and random factors
        days_since_join = (datetime.now().date() - join_date).days
        if days_since_join < 30:
            status_weights = [90, 5, 5]  # New members mostly active
        elif days_since_join < 365:
            status_weights = [80, 15, 5]  # Recent members
        else:
            status_weights = [70, 20, 10]  # Older members
        
        status = random.choices(['Active', 'Suspended', 'Cancelled'], weights=status_weights)[0]
        
        member = {
            'MemberID': f'MEM{i:06d}',
            'FirstName': fake.first_name(),
            'LastName': fake.last_name(),
            'Email': fake.email(),
            'PhoneNumber': fake.phone_number(),
            'DateOfBirth': fake.date_of_birth(minimum_age=16, maximum_age=80),
            'Gender': random.choice(['M', 'F', 'Other']),
            'Address': fake.street_address(),
            'City': fake.city(),
            'State': fake.state_abbr(),
            'ZipCode': fake.zipcode(),
            'JoinDate': join_date,
            'MemberStatus': status,
            'EmergencyContactName': fake.name(),
            'EmergencyContactPhone': fake.phone_number(),
            'MedicalConditions': random.choice([None, 'Heart Condition', 'Diabetes', 'Asthma', 'Knee Injury'], 
                                             weights=[70, 10, 10, 5, 5])
        }
        members.append(member)
    
    return pd.DataFrame(members)

def generate_staff(num_staff=50, facilities_df=None):
    """Generate realistic staff data"""
    staff_roles = [
        'Personal Trainer', 'Group Fitness Instructor', 'Front Desk', 'Manager',
        'Maintenance', 'Lifeguard', 'Nutritionist', 'Physical Therapist'
    ]
    
    staff = []
    
    for i in range(1, num_staff + 1):
        hire_date = fake.date_between(start_date='-5y', end_date='today')
        role = random.choice(staff_roles)
        
        # Salary ranges based on role
        salary_ranges = {
            'Personal Trainer': (35000, 55000),
            'Group Fitness Instructor': (25000, 40000),
            'Front Desk': (28000, 35000),
            'Manager': (55000, 85000),
            'Maintenance': (30000, 45000),
            'Lifeguard': (22000, 32000),
            'Nutritionist': (45000, 65000),
            'Physical Therapist': (60000, 80000)
        }
        
        min_sal, max_sal = salary_ranges.get(role, (30000, 50000))
        
        staff_member = {
            'StaffID': f'STF{i:04d}',
            'FirstName': fake.first_name(),
            'LastName': fake.last_name(),
            'Email': fake.email(),
            'PhoneNumber': fake.phone_number(),
            'HireDate': hire_date,
            'Role': role,
            'Salary': random.randint(min_sal, max_sal),
            'Status': random.choice(['Active', 'On Leave', 'Terminated'], weights=[85, 10, 5]),
            'FacilityID': random.choice(facilities_df['FacilityID'].tolist()) if facilities_df is not None else f'FAC{random.randint(1,5):03d}'
        }
        staff.append(staff_member)
    
    return pd.DataFrame(staff)

# Generate people data
members_df = generate_members(1000, membership_df)
staff_df = generate_staff(50, facilities_df)

print(f"Generated {len(members_df)} members and {len(staff_df)} staff members")
print("\nSample member data:")
print(members_df.head(3))
```

### ODS Tables Population Approach

#### **1. High-Volume Operational Transactions (Python Simulation)**

**MemberAccess, EquipmentUsage, ClassEnrollments:**
- **Generation Method**: Time-series simulation with realistic patterns
- **Libraries**: NumPy for statistical distributions, Pandas for time series

```python
import numpy as np
from datetime import datetime, timedelta

def generate_member_access(members_df, facilities_df, areas_df, days_back=30):
    """Generate realistic member access patterns"""
    access_records = []
    access_id = 1
    
    # Define peak hours (6-9 AM, 5-8 PM on weekdays, 9 AM-6 PM weekends)
    peak_hours_weekday = [(6, 9), (17, 20)]
    peak_hours_weekend = [(9, 18)]
    
    start_date = datetime.now() - timedelta(days=days_back)
    
    for day in range(days_back):
        current_date = start_date + timedelta(days=day)
        is_weekend = current_date.weekday() >= 5
        
        # Determine daily visit volume (higher on weekdays, peak hours)
        if is_weekend:
            daily_visits = random.randint(200, 400)
            peak_hours = peak_hours_weekend
        else:
            daily_visits = random.randint(400, 800)
            peak_hours = peak_hours_weekday
        
        # Generate visits throughout the day
        for _ in range(daily_visits):
            # Weight visit times toward peak hours
            if random.random() < 0.7:  # 70% during peak hours
                if peak_hours:
                    peak_start, peak_end = random.choice(peak_hours)
                    hour = random.randint(peak_start, peak_end)
                else:
                    hour = random.randint(6, 22)
            else:  # 30% during off-peak
                hour = random.choice([5, 6] + list(range(10, 17)) + list(range(21, 23)))
            
            minute = random.randint(0, 59)
            checkin_time = current_date.replace(hour=hour, minute=minute, second=0)
            
            # Select random member and facility
            member_id = random.choice(members_df['MemberID'].tolist())
            facility_id = random.choice(facilities_df['FacilityID'].tolist())
            area_id = random.choice(areas_df[areas_df['FacilityID'] == facility_id]['AreaID'].tolist())
            
            access_record = {
                'AccessID': f'ACC{access_id:08d}',
                'MemberID': member_id,
                'FacilityID': facility_id,
                'AreaID': area_id,
                'CheckInTime': checkin_time,
                'CheckOutTime': checkin_time + timedelta(minutes=random.randint(30, 180)),
                'AccessMethod': random.choice(['Key Card', 'Mobile App', 'Staff Override'], weights=[70, 25, 5])
            }
            access_records.append(access_record)
            access_id += 1
    
    return pd.DataFrame(access_records)

def generate_equipment_usage(access_df, equipment_df, usage_probability=0.3):
    """Generate equipment usage based on member access"""
    usage_records = []
    usage_id = 1
    
    for _, access in access_df.iterrows():
        # Get equipment in the accessed area
        area_equipment = equipment_df[equipment_df['AreaID'] == access['AreaID']]
        
        if len(area_equipment) > 0 and random.random() < usage_probability:
            # Member uses 1-3 pieces of equipment during visit
            num_equipment = random.randint(1, min(3, len(area_equipment)))
            selected_equipment = area_equipment.sample(n=num_equipment)
            
            current_time = access['CheckInTime']
            
            for _, equipment in selected_equipment.iterrows():
                usage_duration = random.randint(10, 60)  # 10-60 minutes
                
                usage_record = {
                    'UsageID': f'USG{usage_id:08d}',
                    'EquipmentID': equipment['EquipmentID'],
                    'MemberID': access['MemberID'],
                    'StartTime': current_time,
                    'EndTime': current_time + timedelta(minutes=usage_duration),
                    'UsageType': random.choice(['Workout', 'Warmup', 'Cooldown'], weights=[70, 20, 10])
                }
                usage_records.append(usage_record)
                usage_id += 1
                
                # Next equipment usage starts after this one ends
                current_time = usage_record['EndTime'] + timedelta(minutes=random.randint(2, 10))
    
    return pd.DataFrame(usage_records)

# Generate operational data
print("Generating member access data...")
access_df = generate_member_access(members_df, facilities_df, areas_df, days_back=30)

print("Generating equipment usage data...")
equipment_usage_df = generate_equipment_usage(access_df, equipment_df)

print(f"Generated {len(access_df)} access records and {len(equipment_usage_df)} equipment usage records")
```

#### **2. Scheduled Business Processes (Python Simulation)**

**ClassSchedules, ClassInstances, StaffSchedules:**
- **Generation Method**: Systematic scheduling with realistic business patterns
- **Libraries**: Pandas for date manipulation, NumPy for scheduling algorithms

```python
def generate_class_schedules(class_types_df, staff_df, facilities_df):
    """Generate recurring class schedules"""
    schedules = []
    schedule_id = 1
    
    # Get instructors (staff who can teach classes)
    instructors = staff_df[staff_df['Role'].isin(['Group Fitness Instructor', 'Personal Trainer'])]
    
    # Define time slots throughout the week
    time_slots = [
        '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
        '12:00', '17:00', '18:00', '19:00', '20:00'
    ]
    
    for _, class_type in class_types_df.iterrows():
        # Each class type gets 3-7 weekly sessions across different facilities
        num_sessions = random.randint(3, 7)
        
        for _ in range(num_sessions):
            facility_id = random.choice(facilities_df['FacilityID'].tolist())
            instructor_id = random.choice(instructors['StaffID'].tolist())
            
            schedule = {
                'ScheduleID': f'SCH{schedule_id:04d}',
                'ClassTypeID': class_type['ClassTypeID'],
                'FacilityID': facility_id,
                'InstructorID': instructor_id,
                'DayOfWeek': random.randint(1, 7),  # 1=Monday, 7=Sunday
                'StartTime': random.choice(time_slots),
                'Duration': class_type['Duration'],
                'MaxParticipants': class_type['MaxParticipants'],
                'IsActive': True
            }
            schedules.append(schedule)
            schedule_id += 1
    
    return pd.DataFrame(schedules)

def generate_class_instances(schedules_df, days_forward=30):
    """Generate specific class instances from schedules"""
    instances = []
    instance_id = 1
    
    start_date = datetime.now().date()
    
    for day in range(days_forward):
        current_date = start_date + timedelta(days=day)
        day_of_week = current_date.weekday() + 1  # Convert to 1-7 format
        
        # Find all schedules for this day of week
        daily_schedules = schedules_df[
            (schedules_df['DayOfWeek'] == day_of_week) & 
            (schedules_df['IsActive'] == True)
        ]
        
        for _, schedule in daily_schedules.iterrows():
            # Create class instance
            start_time = datetime.strptime(schedule['StartTime'], '%H:%M').time()
            class_datetime = datetime.combine(current_date, start_time)
            
            # Determine class status (most are scheduled, some might be cancelled)
            status = random.choice(['Scheduled', 'Cancelled', 'Completed'], 
                                 weights=[85, 5, 10])
            
            instance = {
                'InstanceID': f'INS{instance_id:06d}',
                'ScheduleID': schedule['ScheduleID'],
                'ClassDate': current_date,
                'StartTime': class_datetime,
                'EndTime': class_datetime + timedelta(minutes=schedule['Duration']),
                'Status': status,
                'ActualParticipants': random.randint(0, schedule['MaxParticipants']) if status != 'Cancelled' else 0
            }
            instances.append(instance)
            instance_id += 1
    
    return pd.DataFrame(instances)

def generate_member_payments(members_df, membership_types_df, months_back=6):
    """Generate member payment history"""
    payments = []
    payment_id = 1
    
    # Get active members only
    active_members = members_df[members_df['MemberStatus'] == 'Active']
    
    for _, member in active_members.iterrows():
        join_date = member['JoinDate']
        
        # Generate monthly payments from join date
        current_date = max(join_date, datetime.now().date() - timedelta(days=months_back*30))
        end_date = datetime.now().date()
        
        while current_date <= end_date:
            # Randomly assign membership type (most keep same type)
            membership_type = random.choice(membership_types_df['MembershipTypeID'].tolist())
            fee_info = membership_types_df[membership_types_df['MembershipTypeID'] == membership_type].iloc[0]
            
            # Payment success rate (95% successful)
            payment_status = random.choice(['Completed', 'Failed'], weights=[95, 5])
            
            payment = {
                'PaymentID': f'PAY{payment_id:08d}',
                'MemberID': member['MemberID'],
                'MembershipTypeID': membership_type,
                'PaymentDate': current_date,
                'Amount': fee_info['MonthlyFee'],
                'PaymentMethod': random.choice(['Credit Card', 'Bank Transfer', 'Cash'], weights=[70, 25, 5]),
                'PaymentStatus': payment_status,
                'TransactionFee': round(fee_info['MonthlyFee'] * 0.029, 2) if payment_status == 'Completed' else 0.0
            }
            payments.append(payment)
            payment_id += 1
            
            # Move to next month
            current_date = current_date + timedelta(days=30)
    
    return pd.DataFrame(payments)

# Generate scheduled process data
print("Generating class schedules...")
schedules_df = generate_class_schedules(class_types_df, staff_df, facilities_df)

print("Generating class instances...")
instances_df = generate_class_instances(schedules_df, days_forward=30)

print("Generating member payments...")
payments_df = generate_member_payments(members_df, membership_df, months_back=6)

print(f"Generated {len(schedules_df)} class schedules, {len(instances_df)} class instances, {len(payments_df)} payments")
```

### Complete Python Script Usage

The complete data generation script (`generate_fake_data.py`) includes all the above functions. To use it:

```bash
# Install required libraries
pip install faker pandas numpy psycopg2-binary

# Run the generator
python generate_fake_data.py

# This will create a 'fake_data' directory with CSV files:
# - membership_types.csv
# - class_types.csv  
# - facilities.csv
# - facility_areas.csv
# - equipment.csv
# - members.csv
# - staff.csv
# - member_access.csv
# - equipment_usage.csv
```

### Database Loading Script

```python
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

def load_csv_to_postgres(csv_directory='fake_data', 
                        connection_string='postgresql://username:password@localhost:5432/fitness_ods'):
    """Load all CSV files into PostgreSQL database"""
    
    engine = create_engine(connection_string)
    
    # Define table mapping (CSV filename to database table name)
    table_mappings = {
        'membership_types': 'MembershipTypes',
        'class_types': 'ClassTypes', 
        'facilities': 'Facilities',
        'facility_areas': 'FacilityAreas',
        'equipment': 'Equipment',
        'members': 'Members',
        'staff': 'Staff',
        'member_access': 'MemberAccess',
        'equipment_usage': 'EquipmentUsage'
    }
    
    for csv_name, table_name in table_mappings.items():
        csv_file = f"{csv_directory}/{csv_name}.csv"
        
        try:
            df = pd.read_csv(csv_file)
            df.to_sql(table_name, engine, if_exists='append', index=False)
            print(f"Loaded {len(df)} records into {table_name}")
            
        except Exception as e:
            print(f"Error loading {csv_file}: {str(e)}")

# Usage
# load_csv_to_postgres()
```

### Implementation Sequence for 3-Week Class Project

#### **Week 1: Foundation Setup (MDM Tables + Python Environment)**
**Day 1-2: Environment Setup**
```bash
# Set up Python environment
pip install faker pandas numpy psycopg2-binary sqlalchemy

# Clone/setup project repository
git clone <your-repo>
cd fitness-center-ods
```

**Day 3-4: Generate Basic MDM Data**
```python
# Run core MDM generation
generator = FitnessDataGenerator()
generator.generate_membership_types()
generator.generate_class_types() 
generator.generate_facilities(5)
generator.generate_facility_areas()
generator.generate_equipment()
```

**Day 5-7: People Master Data**
```python
# Generate realistic member and staff data
generator.generate_members(1000)  # 1000 members for testing
generator.generate_staff(50)      # 50 staff across 5 facilities

# Save MDM data to CSV
generator.save_to_csv('week1_mdm_data')
```

#### **Week 2: Operational Data Simulation (High-Volume ODS)**
**Day 8-10: Access Patterns**
```python
# Generate 30 days of member access data
generator.generate_member_access(days_back=30)

# Create equipment usage based on access patterns  
generator.generate_equipment_usage(usage_probability=0.3)
```

**Day 11-12: Class Management**
```python
# Set up class schedules
schedules_df = generate_class_schedules(class_types_df, staff_df, facilities_df)

# Generate 30 days of class instances
instances_df = generate_class_instances(schedules_df, days_forward=30)
```

**Day 13-14: Data Quality & Validation**
```python
# Validate data integrity
validate_referential_integrity()
check_business_rules()
generate_data_quality_report()
```

#### **Week 3: Complete Integration & Analytics**
**Day 15-17: Financial & Feedback Data**
```python
# Generate payment history
payments_df = generate_member_payments(members_df, membership_df, months_back=6)

# Create instructor feedback and performance data
feedback_df = generate_instructor_feedback()
performance_df = generate_staff_performance()
```

**Day 18-19: Database Loading**
```python
# Load all data into PostgreSQL
load_csv_to_postgres(
    csv_directory='fake_data',
    connection_string='postgresql://user:pass@localhost:5432/fitness_ods'
)

# Create indexes for performance
create_performance_indexes()
```

**Day 20-21: Analytics Validation**
```sql
-- Test analytical queries
SELECT * FROM peak_usage_analysis;
SELECT * FROM equipment_utilization_report;  
SELECT * FROM member_retention_metrics;
```

### Data Quality and Validation Framework

#### **Automated Data Quality Checks**
```python
def validate_data_quality(data_dict):
    """Comprehensive data quality validation"""
    
    quality_report = {}
    
    # 1. Completeness checks
    for table_name, df in data_dict.items():
        missing_data = df.isnull().sum()
        quality_report[f"{table_name}_completeness"] = {
            'total_records': len(df),
            'missing_values': missing_data.to_dict(),
            'completeness_score': ((df.size - df.isnull().sum().sum()) / df.size) * 100
        }
    
    # 2. Referential integrity
    integrity_checks = {
        'member_access_refs': validate_foreign_keys(
            data_dict['member_access'], 
            [('MemberID', data_dict['members']), 
             ('FacilityID', data_dict['facilities'])]
        ),
        'equipment_area_refs': validate_foreign_keys(
            data_dict['equipment'],
            [('AreaID', data_dict['facility_areas'])]
        )
    }
    
    # 3. Business rule validation
    business_rules = {
        'member_ages': validate_age_constraints(data_dict['members']),
        'payment_amounts': validate_payment_amounts(data_dict['member_payments']),
        'access_times': validate_access_patterns(data_dict['member_access'])
    }
    
    return {
        'quality_metrics': quality_report,
        'integrity_checks': integrity_checks, 
        'business_rules': business_rules
    }

def generate_data_profile_report(data_dict):
    """Generate comprehensive data profiling report"""
    
    profile_report = {}
    
    for table_name, df in data_dict.items():
        profile_report[table_name] = {
            'record_count': len(df),
            'column_count': len(df.columns),
            'memory_usage': df.memory_usage(deep=True).sum(),
            'date_range': get_date_ranges(df),
            'numeric_stats': df.describe() if len(df.select_dtypes(include=[np.number]).columns) > 0 else None,
            'categorical_stats': get_categorical_stats(df)
        }
    
    return profile_report
```

#### **Performance Monitoring**
```python
def monitor_data_generation_performance():
    """Monitor and optimize data generation performance"""
    
    import time
    import psutil
    
    performance_metrics = {}
    
    start_time = time.time()
    start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
    
    # Generate data with timing
    generator = FitnessDataGenerator()
    
    # Time each major operation
    operations = [
        ('mdm_tables', lambda: generator.generate_all_mdm()),
        ('member_access', lambda: generator.generate_member_access(30)),
        ('equipment_usage', lambda: generator.generate_equipment_usage()),
        ('payments', lambda: generator.generate_member_payments())
    ]
    
    for op_name, op_func in operations:
        op_start = time.time()
        op_func()
        op_end = time.time()
        
        performance_metrics[op_name] = {
            'duration_seconds': op_end - op_start,
            'memory_usage_mb': psutil.Process().memory_info().rss / 1024 / 1024
        }
    
    total_time = time.time() - start_time
    peak_memory = psutil.Process().memory_info().rss / 1024 / 1024
    
    return {
        'total_generation_time': total_time,
        'peak_memory_usage_mb': peak_memory,
        'operation_breakdown': performance_metrics
    }
```

This comprehensive Python-based approach provides you with realistic fake data that maintains referential integrity, follows business patterns, and scales appropriately for your class project. The modular design allows you to generate data incrementally and validate quality at each step.

