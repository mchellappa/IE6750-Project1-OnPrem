# Fitness Center ODS Generated Dataset Documentation

**Generation Date:** 2025-09-27 23:18:44

**Parameters:**
- Facilities: 5
- Members: 2,000
- Staff: 100

## Table Structure and Record Counts

### Master Data Management (MDM) Tables

| Table Name | Record Count | Description |
|------------|-------------:|-------------|
| membershiptypes | 10 | Membership plan definitions and pricing |
| classtypes | 55 | Group fitness class types and requirements |
| instructorcertifications | 15 | Required instructor certifications |
| facilities | 5 | Fitness center locations and details |
| facilityareas | 57 | Areas within each facility (gym, studios, etc.) |
| equipment | 1,205 | Fitness equipment inventory and status |
| members | 2,000 | Member profiles and contact information |
| staff | 100 | Staff employment records and details |

### Operational Data Store (ODS) Tables

| Table Name | Record Count | Description |
|------------|-------------:|-------------|
| membermemberships | 2,606 | Member enrollment in membership plans |
| memberpayments | 2,981 | Payment transactions and billing history |
| classschedules | 83 | Weekly class schedule templates |
| classinstances | 373 | Individual class occurrences |
| classenrollments | 3,787 | Member enrollment in specific classes |

**Total Records Generated:** 13,277

## Business Rules Implemented

### Member Demographics and Behavior
- Age-based membership preferences (students, families, seniors)
- Realistic churn and retention patterns
- Geographic distribution across facility locations
- Medical alerts based on age demographics

### Facility Operations
- Multi-location fitness center chain simulation
- Equipment allocation by area type and capacity
- Realistic operating hours and facility scheduling
- Equipment lifecycle and maintenance patterns

### Class Operations
- Time-based attendance patterns (peak vs. off-peak)
- Seasonal enrollment variations
- Member preferences and enrollment behavior
- No-show and waitlist management

### Financial Patterns
- Realistic payment methods and success rates
- Membership type pricing and duration logic
- Registration fees and auto-renewal patterns
- Payment failure and retry scenarios

## Data Quality and Relationships

- All foreign key relationships properly maintained
- Referential integrity enforced across all tables
- Realistic data distributions and patterns
- Time-series data with proper temporal ordering

## Usage Instructions

### CSV Files Location
- Complete dataset: `generated_data_complete/`
- MDM only: `generated_data_mdm/`

### Database Loading
```bash
# Load all data into PostgreSQL
python database_loader.py --data-dir generated_data_complete --truncate
```

### API Testing
```bash
# Start FastAPI server
python start_server.py

# Test API endpoints
curl http://localhost:8000/members/
curl http://localhost:8000/facilities/
```
