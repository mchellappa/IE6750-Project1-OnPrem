Operational analytics for multi-location fitness centers, focusing on facility utilization, resource allocation, and performance metrics across all sites.

The datastore will include:

Member management
Member facility access
Class booking
Equipment/room usage system
Staff scheduling and payroll
Coach/instructor performance and certification tracking

These data will be modeled into a data warehouse platform.

These are the possible analytics with the data, Time permitting will demonstrate some of them.

Operational Analytics: 
Monthly facility utilization across swimming pool, basketball court, pickleball courts, yoga studios, and spin studios to optimize space allocation and scheduling; 
Staff-to-member ratios and optimal staffing levels by facility area and time periods.
Member Analytics: 
Group class participation patterns, instructor performance evaluation, and member engagement analysis to enhance program offerings; 
Coach effectiveness metrics including class attendance rates, member retention per instructor, and certification impact on class popularity.
Business Intelligence: 
Revenue optimization per facility area, instructor productivity metrics, and predictive analytics for capacity planning and staff resource allocation;

## Cardinalities, Business Rules & Assumptions

### Entity Cardinalities & Relationships (EERD Conceptual Model - Crow's Foot Notation)

#### Member Management Domain

**Members ──< MembershipTypes** (HAS)
```
Members ||────|| MembershipTypes
```
- Each member has exactly one current membership type
- Each membership type can be held by many members
- **Conceptual Cardinality**: Many:One (M:1)
- *Note: Historical changes handled as separate concern in implementation*

**Members ── Payments** (MAKES)
```
Members ||────o{ Payments
```
- Each member makes zero or many payments
- Each payment is made by exactly one member  
- **Conceptual Cardinality**: One:Many (1:M)

**Members ── FacilityAccess** (ACCESSES)
```
Members ||────o{ FacilityAccess
```
- Each member can access facilities multiple times
- Each access event is by exactly one member
- **Conceptual Cardinality**: One:Many (1:M)

#### Facility Management Domain

**Facilities ── FacilityAreas** (CONTAINS)
```
Facilities ||────}{ FacilityAreas
```
- Each facility must contain one or many areas (pools, courts, studios)
- Each area belongs to exactly one facility
- **Conceptual Cardinality**: One:Many (1:M)

**FacilityAreas ── Equipment** (HOUSES)
```
FacilityAreas ||────}o Equipment
```
- Each area can house zero or many pieces of equipment
- Each equipment piece is located in exactly one area
- **Conceptual Cardinality**: One:Many (1:M)

**Members ── Equipment** (USES)
```
Members }o────o{ Equipment
```
- Members can use multiple equipment pieces
- Equipment can be used by multiple members
- **Conceptual Cardinality**: Many:Many (M:N)

**Members ── Facilities** (VISITS)
```
Members }o────o{ Facilities
```
- Members can visit multiple facilities (multi-location access)
- Facilities can be visited by multiple members
- **Conceptual Cardinality**: Many:Many (M:N)

**Members ── FacilityAreas** (ACCESSES)
```
Members }o────o{ FacilityAreas
```
- Members can access multiple facility areas
- Each area can be accessed by multiple members
- **Conceptual Cardinality**: Many:Many (M:N)

#### Class Management Domain

**ClassTypes ── Classes** (DEFINES)
```
ClassTypes ||────}{ Classes
```
- Each class type defines one or many actual classes
- Each class is of exactly one class type (Yoga, Spin, etc.)
- **Conceptual Cardinality**: One:Many (1:M)

**Classes ── FacilityAreas** (HELD_IN)
```
Classes }o────|| FacilityAreas
```
- Each class is held in exactly one facility area
- Each area can host multiple classes
- **Conceptual Cardinality**: Many:One (M:1)

**Members ── Classes** (ENROLLS_IN)
```
Members }o────o{ Classes
```
- Members can enroll in multiple classes
- Each class can have multiple members enrolled
- **Conceptual Cardinality**: Many:Many (M:N)

**Instructors ── Classes** (TEACHES)
```
Instructors ||────}o Classes
```
- Each instructor can teach zero or many classes
- Each class is taught by exactly one instructor
- **Conceptual Cardinality**: One:Many (1:M)

**Instructors ── ClassTypes** (QUALIFIED_FOR)
```
Instructors }o────o{ ClassTypes
```
- Instructors can be qualified to teach multiple class types
- Each class type can be taught by multiple qualified instructors
- **Conceptual Cardinality**: Many:Many (M:N)

#### Staff Management Domain

**Staff ── Facilities** (WORKS_AT)
```
Staff }o────o{ Facilities
```
- Staff can work at multiple facilities (multi-location employees)
- Each facility employs multiple staff members
- **Conceptual Cardinality**: Many:Many (M:N)

**Staff ── Certifications** (HOLDS)
```
Staff }o────o{ Certifications
```
- Staff can hold multiple certifications (CPR, Yoga, Spin, etc.)
- Each certification can be held by multiple staff members
- **Conceptual Cardinality**: Many:Many (M:N)

**Staff ── WorkSchedule** (HAS)
```
Staff ||────}o WorkSchedule
```
- Each staff member can have zero or many scheduled work periods
- Each work schedule belongs to exactly one staff member
- **Conceptual Cardinality**: One:Many (1:M)

**Facilities ── WorkSchedule** (SCHEDULES_AT)
```
Facilities ||────}o WorkSchedule
```
- Each facility can have multiple staff work schedules
- Each work schedule is for exactly one facility
- **Conceptual Cardinality**: One:Many (1:M)

**FacilityAreas ── WorkSchedule** (ASSIGNED_TO)
```
FacilityAreas ||────}o WorkSchedule
```
- Each area can have multiple staff work assignments
- Each work schedule can be assigned to exactly one area
- **Conceptual Cardinality**: One:Many (1:M)

#### Equipment & Maintenance Domain

**Equipment ── Maintenance** (REQUIRES)
```
Equipment ||────}o Maintenance
```
- Each equipment piece requires zero or many maintenance activities
- Each maintenance activity is for exactly one equipment piece
- **Conceptual Cardinality**: One:Many (1:M)

**Staff ── Maintenance** (PERFORMS)
```
Staff }o────}o Maintenance
```
- Staff can perform multiple maintenance activities
- Each maintenance can involve multiple staff (team maintenance)
- **Conceptual Cardinality**: Many:Many (M:N)

#### Performance & Evaluation Domain

**Instructors ── PerformanceEvaluation** (RECEIVES)
```
Instructors ||────}o PerformanceEvaluation
```
- Each instructor receives zero or many performance evaluations
- Each evaluation is for exactly one instructor
- **Conceptual Cardinality**: One:Many (1:M)

**Members ── InstructorFeedback** (PROVIDES)
```
Members }o────}o InstructorFeedback
```
- Members can provide zero or many feedback entries
- Each feedback can involve multiple members (class feedback)
- **Conceptual Cardinality**: Many:Many (M:N)

**Instructors ── InstructorFeedback** (SUBJECT_OF)
```
Instructors ||────}o InstructorFeedback
```
- Each instructor can be subject of zero or many feedback entries
- Each feedback is about exactly one instructor
- **Conceptual Cardinality**: One:Many (1:M)

#### Specialization Hierarchies (ISA Relationships)

**Staff ISA Hierarchy**
```
Staff
  |
  |──── FrontDeskStaff
  |──── MaintenanceStaff  
  |──── Instructors
        |
        |──── YogaInstructor
        |──── SpinInstructor
        |──── PersonalTrainer
        |──── AquaInstructor
```

**Member ISA Hierarchy**
```
Members
  |
  |──── IndividualMember
  |──── FamilyMember
  |──── StudentMember
  |──── SeniorMember
  |──── CorporateMember
```

**FacilityArea ISA Hierarchy**
```
FacilityAreas
  |
  |──── ExerciseArea
        |──── CardioZone
        |──── WeightRoom
        |──── StretchArea
  |──── StudioSpace
        |──── YogaStudio
        |──── SpinRoom
        |──── GroupFitnessStudio
  |──── AquaticArea
        |──── SwimmingPool
        |──── HotTub
        |──── SteamRoom
  |──── CourtSpace
        |──── BasketballCourt
        |──── PickleballCourt
        |──── RacquetballCourt

### Crow's Foot Notation Legend
```
||  = One (and only one)
|o  = Zero or one
}{  = Many (one or more)
}o  = Zero or many
```

### Business Rules

#### Member Management Rules
1. **Member Status Transitions**
   - New members start with 'Active' status
   - Members can be suspended for non-payment (max 90 days)
   - Cancelled members cannot access facilities
   - Frozen memberships pause billing but maintain member benefits

2. **Membership Type Rules**
   - Family memberships allow up to 4 members per account
   - Student memberships require annual verification
   - Corporate memberships have special pricing tiers
   - Monthly fees are prorated for partial months

3. **Payment Rules**
   - Monthly fees are due on the same date each month
   - Late fees apply after 10-day grace period
   - Failed payments result in 30-day suspension after 3 attempts
   - Registration fees are one-time charges for new members

#### Facility Access Rules
1. **Access Control**
   - Members can only access facilities during operating hours
   - Suspended or cancelled members are denied access
   - Guest passes require sponsor member to be present
   - Age restrictions apply to certain areas (18+ weight room)

2. **Capacity Management**
   - Each facility area has maximum occupancy limits
   - Peak hours may have additional restrictions
   - Priority access for premium membership tiers
   - Reservations required for certain specialty areas

#### Class Management Rules
1. **Class Enrollment**
   - Members can book classes up to 7 days in advance
   - Cancellations allowed up to 2 hours before class
   - No-shows are tracked for member behavior analysis
   - Wait lists maintained for popular classes

2. **Instructor Assignment**
   - Instructors must have required certifications for class type
   - Substitute instructors require manager approval
   - Maximum teaching hours per instructor per week: 25 hours
   - Instructor performance evaluations quarterly

#### Staff Management Rules
1. **Certification Requirements**
   - All group fitness instructors require relevant certifications
   - Certifications must be renewed before expiration
   - CPR/First Aid certification mandatory for all staff
   - Personal trainers require specialized certifications

2. **Scheduling Rules**
   - Minimum 4-hour shift duration
   - Maximum 40 hours per week for part-time staff
   - Coverage required for all facility operating hours
   - Premium staffing during peak hours (6-9 AM, 5-8 PM)

### Key Assumptions

#### Operational Assumptions
1. **Facility Operations**
   - Standard operating hours: 5:00 AM - 11:00 PM (may vary by location)
   - Peak usage periods: 6:00-9:00 AM and 5:00-8:00 PM weekdays
   - Weekend patterns differ from weekday usage
   - Seasonal variations in membership and usage patterns

2. **Member Behavior**
   - Average member visits facility 2.5 times per week
   - 70% of members use cardio equipment, 45% use weight training
   - Group classes have 85% average attendance rate
   - Member retention rate: 75% annually

3. **Equipment & Maintenance**
   - Equipment has 5-7 year useful life depending on type
   - Preventive maintenance scheduled monthly
   - Equipment downtime should not exceed 5% annually
   - Replacement planning based on usage hours and age

#### Data & Technology Assumptions
1. **Data Collection**
   - Member access tracked via card readers or mobile app
   - Equipment usage tracked manually or via IoT sensors
   - Class attendance recorded digitally
   - Payment processing integrated with membership system

2. **Data Quality**
   - Member contact information updated annually
   - Staff certification expiration dates monitored proactively
   - Equipment maintenance records kept for warranty/safety compliance
   - Financial transactions recorded in real-time

3. **Reporting & Analytics**
   - Daily operational reports generated automatically
   - Monthly business intelligence dashboards for management
   - Quarterly member satisfaction surveys
   - Annual facility utilization and ROI analysis

#### Business Model Assumptions
1. **Revenue Streams**
   - 80% revenue from membership fees
   - 15% from personal training and specialty classes
   - 5% from retail and ancillary services
   - Corporate memberships provide stable revenue base

2. **Cost Structure**
   - Staff costs represent 45% of operating expenses
   - Facility maintenance and utilities: 25%
   - Equipment and technology: 15%
   - Marketing and administrative: 15%

3. **Growth Projections**
   - 10-15% annual membership growth target
   - New facility expansion every 3-5 years
   - Technology investments to improve member experience
   - Focus on premium services and specialized programs 

-- ================================================
-- INDEXES FOR PERFORMANCE
-- ================================================

-- Member access indexes (high volume table)
CREATE INDEX idx_member_access_member_id ON MemberAccess(MemberID);
CREATE INDEX idx_member_access_facility_id ON MemberAccess(FacilityID);
CREATE INDEX idx_member_access_checkin_time ON MemberAccess(CheckInTime);
CREATE INDEX idx_member_access_area_id ON MemberAccess(AreaID);

-- Class enrollment indexes
CREATE INDEX idx_class_enrollments_member_id ON ClassEnrollments(MemberID);
CREATE INDEX idx_class_enrollments_instance_id ON ClassEnrollments(InstanceID);
CREATE INDEX idx_class_enrollments_status ON ClassEnrollments(EnrollmentStatus);

-- Equipment usage indexes
CREATE INDEX idx_equipment_usage_equipment_id ON EquipmentUsage(EquipmentID);
CREATE INDEX idx_equipment_usage_member_id ON EquipmentUsage(MemberID);
CREATE INDEX idx_equipment_usage_start_time ON EquipmentUsage(StartTime);

-- Staff schedule indexes
CREATE INDEX idx_staff_schedules_staff_id ON StaffSchedules(StaffID);
CREATE INDEX idx_staff_schedules_facility_id ON StaffSchedules(FacilityID);
CREATE INDEX idx_staff_schedules_date ON StaffSchedules(ScheduleDate);

-- Performance indexes
CREATE INDEX idx_instructor_performance_instructor_id ON InstructorPerformance(InstructorID);
CREATE INDEX idx_instructor_feedback_instructor_id ON InstructorFeedback(InstructorID);
CREATE INDEX idx_instructor_feedback_member_id ON InstructorFeedback(MemberID);

-- ================================================
-- SAMPLE DATA INSERTION STATEMENTS (for testing)
-- ================================================

-- Sample Facilities
INSERT INTO Facilities VALUES 
('FAC001', 'Downtown YMCA', '123 Main St', 'Springfield', 'IL', '62701', '217-555-0100', '05:00:00', '23:00:00', TRUE),
('FAC002', 'Westside Fitness Center', '456 Oak Ave', 'Springfield', 'IL', '62702', '217-555-0200', '06:00:00', '22:00:00', TRUE);

-- Sample Facility Areas
INSERT INTO FacilityAreas VALUES 
('AREA001', 'FAC001', 'Swimming Pool', 'Swimming Pool', 50, 2000.00, TRUE),
('AREA002', 'FAC001', 'Basketball Court', 'Basketball Court', 20, 3000.00, TRUE),
('AREA003', 'FAC001', 'Yoga Studio A', 'Yoga Studio', 25, 800.00, TRUE),
('AREA004', 'FAC001', 'Spin Studio', 'Spin Studio', 30, 600.00, TRUE),
('AREA005', 'FAC002', 'Pickleball Court 1', 'Pickleball Court', 8, 400.00, TRUE);

-- Sample Membership Types
INSERT INTO MembershipTypes VALUES 
('MT001', 'Individual Monthly', 'Standard individual membership', 49.99, 25.00, NULL, 1, TRUE, CURRENT_TIMESTAMP),
('MT002', 'Family Monthly', 'Family membership up to 4 members', 89.99, 50.00, NULL, 4, TRUE, CURRENT_TIMESTAMP),
('MT003', 'Student Monthly', 'Discounted student membership', 29.99, 15.00, NULL, 1, TRUE, CURRENT_TIMESTAMP);

-- Sample Class Types
INSERT INTO ClassTypes VALUES 
('CT001', 'Beginner Yoga', 'Yoga', 'Gentle yoga for beginners', 60, 25, 'Yoga Certification', TRUE),
('CT002', 'High-Intensity Spin', 'Spin', 'High-energy cycling class', 45, 30, 'Spin Certification', TRUE),
('CT003', 'Water Aerobics', 'Aqua Fitness', 'Low-impact water exercise', 50, 20, 'Aqua Fitness Certification', TRUE);

-- Sample Certifications
INSERT INTO InstructorCertifications VALUES 
('CERT001', 'RYT-200 Yoga Teacher', 'Yoga Alliance', '200-hour registered yoga teacher', 24, TRUE),
('CERT002', 'Certified Spin Instructor', 'Mad Dogg Athletics', 'Indoor cycling instructor certification', 12, TRUE),
('CERT003', 'Aqua Fitness Instructor', 'AEA', 'Aquatic Exercise Association certification', 24, TRUE);
