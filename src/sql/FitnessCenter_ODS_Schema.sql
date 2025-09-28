-- Fitness Center Operational Data Store (ODS) Schema
-- Core tables for multi-location fitness center analytics

-- ================================================
-- DROP EXISTING TABLES (for refresh)
-- ================================================
-- Drop tables in reverse dependency order to avoid foreign key conflicts
DROP TABLE IF EXISTS InstructorFeedback CASCADE;
DROP TABLE IF EXISTS InstructorPerformance CASCADE;
DROP TABLE IF EXISTS StaffCertifications CASCADE;
DROP TABLE IF EXISTS InstructorCertifications CASCADE;
DROP TABLE IF EXISTS StaffPayroll CASCADE;
DROP TABLE IF EXISTS StaffTimeTracking CASCADE;
DROP TABLE IF EXISTS StaffSchedules CASCADE;
DROP TABLE IF EXISTS StaffFacilities CASCADE;
DROP TABLE IF EXISTS Staff CASCADE;
DROP TABLE IF EXISTS EquipmentMaintenance CASCADE;
DROP TABLE IF EXISTS EquipmentUsage CASCADE;
DROP TABLE IF EXISTS Equipment CASCADE;
DROP TABLE IF EXISTS ClassEnrollments CASCADE;
DROP TABLE IF EXISTS ClassInstances CASCADE;
DROP TABLE IF EXISTS ClassSchedules CASCADE;
DROP TABLE IF EXISTS ClassTypes CASCADE;
DROP TABLE IF EXISTS MemberAccess CASCADE;
DROP TABLE IF EXISTS FacilityAreas CASCADE;
DROP TABLE IF EXISTS Facilities CASCADE;
DROP TABLE IF EXISTS MemberPayments CASCADE;
DROP TABLE IF EXISTS MemberMemberships CASCADE;
DROP TABLE IF EXISTS MembershipTypes CASCADE;
DROP TABLE IF EXISTS Members CASCADE;

-- ================================================
-- 1. MEMBER MANAGEMENT SYSTEM TABLES
-- ================================================

-- Core member information
CREATE TABLE Members (
    MemberID VARCHAR(20) PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    Phone VARCHAR(20),
    DateOfBirth DATE,
    Gender CHAR(1) CHECK (Gender IN ('M', 'F', 'O')),
    Address VARCHAR(200),
    City VARCHAR(50),
    State VARCHAR(20),
    ZipCode VARCHAR(10),
    EmergencyContact VARCHAR(100),
    EmergencyPhone VARCHAR(20),
    MedicalAlerts TEXT,
    JoinDate DATE NOT NULL,
    MemberStatus VARCHAR(20) DEFAULT 'Active' CHECK (MemberStatus IN ('Active', 'Suspended', 'Cancelled', 'Frozen')),
    LastModified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Membership types and pricing
CREATE TABLE MembershipTypes (
    MembershipTypeID VARCHAR(20) PRIMARY KEY,
    TypeName VARCHAR(50) NOT NULL,
    Description TEXT,
    MonthlyFee DECIMAL(10,2) NOT NULL,
    RegistrationFee DECIMAL(10,2) DEFAULT 0,
    Duration INT, -- months
    MaxFamilyMembers INT DEFAULT 1,
    IsActive BOOLEAN DEFAULT TRUE,
    CreatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Member membership history
CREATE TABLE MemberMemberships (
    MembershipID VARCHAR(20) PRIMARY KEY,
    MemberID VARCHAR(20) NOT NULL,
    MembershipTypeID VARCHAR(20) NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE,
    Status VARCHAR(20) DEFAULT 'Active' CHECK (Status IN ('Active', 'Expired', 'Cancelled')),
    AutoRenew BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID),
    FOREIGN KEY (MembershipTypeID) REFERENCES MembershipTypes(MembershipTypeID)
);

-- Payment history
CREATE TABLE MemberPayments (
    PaymentID VARCHAR(20) PRIMARY KEY,
    MemberID VARCHAR(20) NOT NULL,
    PaymentDate DATE NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    PaymentType VARCHAR(50) CHECK (PaymentType IN ('Monthly Fee', 'Registration', 'Late Fee', 'Personal Training', 'Other', 'Monthly Membership', 'Membership + Registration')),
    PaymentMethod VARCHAR(20) CHECK (PaymentMethod IN ('Credit Card', 'Debit Card', 'Bank Transfer', 'Cash', 'Check')),
    Status VARCHAR(20) DEFAULT 'Completed' CHECK (Status IN ('Completed', 'Pending', 'Failed', 'Refunded')),
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);

-- ================================================
-- 2. FACILITY ACCESS SYSTEM TABLES
-- ================================================

-- Facility locations
CREATE TABLE Facilities (
    FacilityID VARCHAR(20) PRIMARY KEY,
    FacilityName VARCHAR(100) NOT NULL,
    Address VARCHAR(200),
    City VARCHAR(50),
    State VARCHAR(20),
    ZipCode VARCHAR(10),
    PhoneNumber VARCHAR(20),
    OpenTime TIME,
    CloseTime TIME,
    IsActive BOOLEAN DEFAULT TRUE
);

-- Facility areas/rooms
CREATE TABLE FacilityAreas (
    FacilityID VARCHAR(20) NOT NULL,
    AreaID VARCHAR(20) NOT NULL,
    AreaName VARCHAR(50) NOT NULL,
    AreaType VARCHAR(30) CHECK (AreaType IN (
        'Swimming Pool', 'Basketball Court', 'Pickleball Court', 'Yoga Studio', 'Spin Studio', 
        'Gym Floor', 'Locker Room', 'Reception', 'Cardio', 'Strength', 'Studio', 
        'Pool', 'Court', 'Refreshment', 'Childcare', 'Private Training'
    )),
    MaxCapacity INT,
    SquareFootage DECIMAL(10,2),
    IsActive BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (FacilityID, AreaID),
    FOREIGN KEY (FacilityID) REFERENCES Facilities(FacilityID)
);

-- Member check-in/check-out logs
CREATE TABLE MemberAccess (
    AccessID VARCHAR(20) PRIMARY KEY,
    MemberID VARCHAR(20) NOT NULL,
    FacilityID VARCHAR(20) NOT NULL,
    AreaID VARCHAR(20),
    CheckInTime TIMESTAMP NOT NULL,
    CheckOutTime TIMESTAMP,
    AccessMethod VARCHAR(20) CHECK (AccessMethod IN ('Key Card', 'Mobile App', 'Front Desk', 'Biometric', 'Card Scan')),
    Duration INT, -- calculated in minutes
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID),
    FOREIGN KEY (FacilityID) REFERENCES Facilities(FacilityID),
    FOREIGN KEY (FacilityID, AreaID) REFERENCES FacilityAreas(FacilityID, AreaID)
);

-- ================================================
-- 3. CLASS BOOKING SYSTEM TABLES
-- ================================================

-- Class types and categories
CREATE TABLE ClassTypes (
    ClassTypeID VARCHAR(20) PRIMARY KEY,
    ClassName VARCHAR(50) NOT NULL,
    Category VARCHAR(30) CHECK (Category IN (
        'Yoga', 'Pilates', 'Zumba', 'Spin', 'CrossFit', 'HIIT',
        'Aqua Fitness', 'Kickboxing', 'Boot Camp', 'Strength Training',
        'Barre', 'TRX', 'Boxing', 'Dance', 'Tai Chi', 'Meditation',
        'Cardio', 'Martial Arts', 'Youth', 'Senior'
    )),
    Description TEXT,
    DurationMinutes INT NOT NULL,
    MaxParticipants INT,
    RequiredCertifications VARCHAR(200),
    IsActive BOOLEAN DEFAULT TRUE
);

-- Class schedules
CREATE TABLE ClassSchedules (
    ScheduleID VARCHAR(20) PRIMARY KEY,
    ClassTypeID VARCHAR(20) NOT NULL,
    FacilityID VARCHAR(20) NOT NULL,
    AreaID VARCHAR(20) NOT NULL,
    InstructorID VARCHAR(20), -- Links to Staff table
    DayOfWeek INT CHECK (DayOfWeek BETWEEN 1 AND 7), -- 1=Monday, 7=Sunday
    StartTime TIME NOT NULL,
    EndTime TIME NOT NULL,
    MaxCapacity INT,
    Price DECIMAL(8,2) DEFAULT 0,
    EffectiveDate DATE NOT NULL,
    ExpiryDate DATE,
    IsActive BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (ClassTypeID) REFERENCES ClassTypes(ClassTypeID),
    FOREIGN KEY (FacilityID) REFERENCES Facilities(FacilityID),
    FOREIGN KEY (FacilityID, AreaID) REFERENCES FacilityAreas(FacilityID, AreaID)
);

-- Individual class instances
CREATE TABLE ClassInstances (
    InstanceID VARCHAR(20) PRIMARY KEY,
    ScheduleID VARCHAR(20) NOT NULL,
    ClassDate DATE NOT NULL,
    ActualStartTime TIMESTAMP,
    ActualEndTime TIMESTAMP,
    ActualInstructorID VARCHAR(20),
    ActualCapacity INT,
    Status VARCHAR(20) DEFAULT 'Scheduled' CHECK (Status IN ('Scheduled', 'Completed', 'Cancelled', 'Rescheduled')),
    CancellationReason TEXT,
    FOREIGN KEY (ScheduleID) REFERENCES ClassSchedules(ScheduleID)
);

-- Class enrollments
CREATE TABLE ClassEnrollments (
    EnrollmentID VARCHAR(20) PRIMARY KEY,
    MemberID VARCHAR(20) NOT NULL,
    InstanceID VARCHAR(20) NOT NULL,
    EnrollmentDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    EnrollmentStatus VARCHAR(20) DEFAULT 'Enrolled' CHECK (EnrollmentStatus IN ('Enrolled', 'Attended', 'No Show', 'Cancelled', 'Waitlisted')),
    PaymentAmount DECIMAL(8,2) DEFAULT 0,
    CheckInTime TIMESTAMP,
    CheckOutTime TIMESTAMP,
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID),
    FOREIGN KEY (InstanceID) REFERENCES ClassInstances(InstanceID)
);

-- ================================================
-- 4. EQUIPMENT/ROOM USAGE SYSTEM TABLES
-- ================================================

-- Equipment inventory
CREATE TABLE Equipment (
    EquipmentID VARCHAR(20) PRIMARY KEY,
    FacilityID VARCHAR(20) NOT NULL,
    AreaID VARCHAR(20) NOT NULL,
    EquipmentName VARCHAR(100) NOT NULL,
    EquipmentType VARCHAR(50) CHECK (EquipmentType IN ('Cardio', 'Strength', 'Free Weights', 'Pool Equipment', 'Court Equipment', 'Studio Equipment')),
    Brand VARCHAR(50),
    Model VARCHAR(50),
    SerialNumber VARCHAR(50),
    PurchaseDate DATE,
    PurchasePrice DECIMAL(10,2),
    WarrantyExpiry DATE,
    Status VARCHAR(20) DEFAULT 'Active' CHECK (Status IN ('Active', 'Maintenance', 'Out of Service', 'Retired')),
    FOREIGN KEY (FacilityID) REFERENCES Facilities(FacilityID),
    FOREIGN KEY (FacilityID, AreaID) REFERENCES FacilityAreas(FacilityID, AreaID)
);

-- Equipment usage tracking
CREATE TABLE EquipmentUsage (
    UsageID VARCHAR(20) PRIMARY KEY,
    EquipmentID VARCHAR(20) NOT NULL,
    MemberID VARCHAR(20),
    StartTime TIMESTAMP NOT NULL,
    EndTime TIMESTAMP,
    DurationMinutes INT,
    UsageType VARCHAR(20) CHECK (UsageType IN ('Member Use', 'Maintenance', 'Cleaning', 'Class Use')),
    Notes TEXT,
    FOREIGN KEY (EquipmentID) REFERENCES Equipment(EquipmentID),
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);

-- Equipment maintenance records
CREATE TABLE EquipmentMaintenance (
    MaintenanceID VARCHAR(20) PRIMARY KEY,
    EquipmentID VARCHAR(20) NOT NULL,
    MaintenanceDate DATE NOT NULL,
    MaintenanceType VARCHAR(30) CHECK (MaintenanceType IN ('Preventive', 'Corrective', 'Emergency', 'Inspection')),
    TechnicianName VARCHAR(100),
    Description TEXT,
    Cost DECIMAL(10,2),
    PartsReplaced TEXT,
    NextMaintenanceDate DATE,
    FOREIGN KEY (EquipmentID) REFERENCES Equipment(EquipmentID)
);

-- ================================================
-- 5. STAFF SCHEDULING AND PAYROLL TABLES
-- ================================================

-- Staff/Employee information
CREATE TABLE Staff (
    StaffID VARCHAR(20) PRIMARY KEY,
    EmployeeNumber VARCHAR(20) UNIQUE,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(100),
    Phone VARCHAR(20),
    HireDate DATE NOT NULL,
    JobTitle VARCHAR(50),
    Department VARCHAR(30) CHECK (Department IN ('Front Desk', 'Fitness', 'Aquatics', 'Maintenance', 'Management', 'Childcare', 'Operations', 'Sales', 'Wellness')),
    EmploymentType VARCHAR(20) CHECK (EmploymentType IN ('Full-time', 'Part-time', 'Contract', 'Intern')),
    HourlyRate DECIMAL(8,2),
    Status VARCHAR(20) DEFAULT 'Active' CHECK (Status IN ('Active', 'Inactive', 'Terminated', 'On Leave')),
    TerminationDate DATE
);

-- Staff assignments to facilities
CREATE TABLE StaffFacilities (
    AssignmentID VARCHAR(20) PRIMARY KEY,
    StaffID VARCHAR(20) NOT NULL,
    FacilityID VARCHAR(20) NOT NULL,
    IsPrimary BOOLEAN DEFAULT FALSE,
    StartDate DATE NOT NULL,
    EndDate DATE,
    FOREIGN KEY (StaffID) REFERENCES Staff(StaffID),
    FOREIGN KEY (FacilityID) REFERENCES Facilities(FacilityID)
);

-- Staff schedules
CREATE TABLE StaffSchedules (
    ScheduleID VARCHAR(20) PRIMARY KEY,
    StaffID VARCHAR(20) NOT NULL,
    FacilityID VARCHAR(20) NOT NULL,
    AreaID VARCHAR(20),
    ScheduleDate DATE NOT NULL,
    StartTime TIME NOT NULL,
    EndTime TIME NOT NULL,
    ScheduledHours DECIMAL(4,2),
    ShiftType VARCHAR(20) CHECK (ShiftType IN ('Regular', 'Overtime', 'Holiday', 'Training')),
    Status VARCHAR(20) DEFAULT 'Scheduled' CHECK (Status IN ('Scheduled', 'Completed', 'No Show', 'Cancelled')),
    FOREIGN KEY (StaffID) REFERENCES Staff(StaffID),
    FOREIGN KEY (FacilityID) REFERENCES Facilities(FacilityID),
    FOREIGN KEY (FacilityID, AreaID) REFERENCES FacilityAreas(FacilityID, AreaID)
);

-- Staff actual work hours (time tracking)
CREATE TABLE StaffTimeTracking (
    TimeTrackingID VARCHAR(20) PRIMARY KEY,
    StaffID VARCHAR(20) NOT NULL,
    ScheduleID VARCHAR(20),
    ActualStartTime TIMESTAMP,
    ActualEndTime TIMESTAMP,
    ActualHours DECIMAL(4,2),
    OvertimeHours DECIMAL(4,2) DEFAULT 0,
    BreakMinutes INT DEFAULT 0,
    Notes TEXT,
    FOREIGN KEY (StaffID) REFERENCES Staff(StaffID),
    FOREIGN KEY (ScheduleID) REFERENCES StaffSchedules(ScheduleID)
);

-- Payroll records
CREATE TABLE StaffPayroll (
    PayrollID VARCHAR(20) PRIMARY KEY,
    StaffID VARCHAR(20) NOT NULL,
    PayPeriodStart DATE NOT NULL,
    PayPeriodEnd DATE NOT NULL,
    RegularHours DECIMAL(6,2),
    OvertimeHours DECIMAL(6,2),
    RegularPay DECIMAL(10,2),
    OvertimePay DECIMAL(10,2),
    Bonuses DECIMAL(10,2) DEFAULT 0,
    Deductions DECIMAL(10,2) DEFAULT 0,
    GrossPay DECIMAL(10,2),
    NetPay DECIMAL(10,2),
    PayDate DATE,
    FOREIGN KEY (StaffID) REFERENCES Staff(StaffID)
);

-- ================================================
-- 6. COACH/INSTRUCTOR PERFORMANCE AND CERTIFICATION TABLES
-- ================================================

-- Instructor certifications
CREATE TABLE InstructorCertifications (
    CertificationID VARCHAR(20) PRIMARY KEY,
    CertificationName VARCHAR(100) NOT NULL,
    IssuingOrganization VARCHAR(100),
    Description TEXT,
    ValidityMonths INT, -- How long certification is valid
    IsRequired BOOLEAN DEFAULT FALSE
);

-- Staff certifications (links staff to their certifications)
CREATE TABLE StaffCertifications (
    StaffCertificationID VARCHAR(20) PRIMARY KEY,
    StaffID VARCHAR(20) NOT NULL,
    CertificationID VARCHAR(20) NOT NULL,
    CertificationDate DATE NOT NULL,
    ExpiryDate DATE,
    CertificationNumber VARCHAR(50),
    Status VARCHAR(20) DEFAULT 'Active' CHECK (Status IN ('Active', 'Expired', 'Suspended', 'Revoked')),
    FOREIGN KEY (StaffID) REFERENCES Staff(StaffID),
    FOREIGN KEY (CertificationID) REFERENCES InstructorCertifications(CertificationID)
);

-- Instructor performance metrics
CREATE TABLE InstructorPerformance (
    PerformanceID VARCHAR(20) PRIMARY KEY,
    InstructorID VARCHAR(20) NOT NULL,
    EvaluationDate DATE NOT NULL,
    EvaluatorID VARCHAR(20), -- Staff member who did evaluation
    ClassesPerMonth INT,
    AverageAttendance DECIMAL(5,2),
    MemberRetentionRate DECIMAL(5,2),
    MemberSatisfactionScore DECIMAL(3,2), -- 1-5 scale
    ProfessionalismScore DECIMAL(3,2),
    CommunicationScore DECIMAL(3,2),
    OverallRating DECIMAL(3,2),
    Comments TEXT,
    GoalsForNextPeriod TEXT,
    FOREIGN KEY (InstructorID) REFERENCES Staff(StaffID),
    FOREIGN KEY (EvaluatorID) REFERENCES Staff(StaffID)
);

-- Member feedback on instructors
CREATE TABLE InstructorFeedback (
    FeedbackID VARCHAR(20) PRIMARY KEY,
    MemberID VARCHAR(20) NOT NULL,
    InstructorID VARCHAR(20) NOT NULL,
    ClassInstanceID VARCHAR(20),
    FeedbackDate DATE NOT NULL,
    TeachingQuality INT CHECK (TeachingQuality BETWEEN 1 AND 5),
    Communication INT CHECK (Communication BETWEEN 1 AND 5),
    Motivation INT CHECK (Motivation BETWEEN 1 AND 5),
    OverallRating INT CHECK (OverallRating BETWEEN 1 AND 5),
    Comments TEXT,
    IsAnonymous BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID),
    FOREIGN KEY (InstructorID) REFERENCES Staff(StaffID),
    FOREIGN KEY (ClassInstanceID) REFERENCES ClassInstances(InstanceID)
);

