# Fitness Center Data Generation System

## Overview

This comprehensive data generation system creates realistic fake data for a multi-location fitness center chain, following business rules and operational patterns. The system generates both **Master Data Management (MDM)** tables with reference data and **Operational Data Store (ODS)** tables with high-volume transactional data.

## Business Rules Implemented

### Member Demographics & Behavior
- **Age-based preferences**: Students prefer basic plans, families choose family plans, seniors select senior discounts
- **Realistic churn patterns**: New members have higher retention, seasonal variations in enrollment
- **Geographic distribution**: Members prefer facilities near their location
- **Visit frequency patterns**: Most members visit 2-4 times per week, with peak hours modeling

### Facility Operations
- **Multi-location chain**: 1-50 facilities across different cities
- **Equipment allocation**: Realistic equipment distribution by area type (cardio, strength, studios)
- **Operating hours**: Standard business hours with some 24/7 locations
- **Capacity management**: Area capacities based on square footage and activity type

### Class Operations & Scheduling
- **Time-based attendance**: Peak hours (6-9 AM, 5-8 PM weekdays), lower weekend attendance
- **Seasonal patterns**: Higher enrollment in spring, lower in winter holidays
- **Instructor requirements**: Classes matched to certified instructors
- **Waitlist management**: Popular classes generate waitlists and no-shows

### Financial Patterns
- **Realistic payment methods**: Credit cards (60%), debit cards (25%), other methods (15%)
- **Payment success rates**: 95% successful transactions with realistic failure patterns
- **Membership pricing**: Registration fees, monthly/annual plans, auto-renewal logic
- **Corporate discounts**: Special pricing for corporate memberships

## Data Volume & Scale

| Table Category | Volume Range | Update Frequency |
|---------------|--------------|------------------|
| **MDM Tables** | 10-1,000 records | Rarely (quarterly/annually) |
| **People Master** | 1,000-50,000+ records | Monthly updates |
| **Asset Master** | 500-5,000 records | Monthly updates |
| **ODS Transaction** | 10,000-1M+ records | Real-time/daily |

### Specific Table Volumes

| Table Name | Record Count | Description |
|------------|-------------:|-------------|
| `membershiptypes` | 10 | Membership plans and pricing |
| `classtypes` | 40 | Group fitness class definitions |
| `facilities` | 1-50 | Fitness center locations |
| `members` | 1,000-50,000+ | Member profiles |
| `staff` | 50-500 | Employee records |
| `equipment` | 500-5,000 | Fitness equipment inventory |
| `membermemberships` | 2,000-100,000+ | Membership enrollments |
| `memberpayments` | 5,000-200,000+ | Payment transactions |
| `classenrollments` | 20,000-500,000+ | Class registrations |
| `memberaccess` | 100,000-1M+ | Facility access logs |

## Quick Start

### Prerequisites

```bash
# Install required packages
pip install -r requirements-dataload.txt

# Or install individually:
pip install pandas numpy faker psycopg2-binary python-decouple
```

### Generate Demo Dataset

```bash
# Generate small demo dataset (2 facilities, 500 members, 25 staff)
python run_complete_data_generation.py --demo

# Generate medium dataset (5 facilities, 2K members, 100 staff)
python run_complete_data_generation.py --facilities 5 --members 2000 --staff 100

# Generate large dataset (10 facilities, 10K members, 250 staff)
python run_complete_data_generation.py --full-scale
```

### Generate and Load to Database

```bash
# Generate data and load to PostgreSQL
python run_complete_data_generation.py --demo --load-database \
  --database-url "postgresql://username:password@localhost:5432/fitnessdb"

# Generate only CSV files (no database loading)
python run_complete_data_generation.py --demo --generate-only
```

## 📁 Generated Files Structure

```
generated_data_complete/          # Complete dataset (MDM + ODS)
├── membershiptypes.csv          # Membership plans
├── classtypes.csv               # Class definitions
├── facilities.csv               # Facility locations
├── members.csv                  # Member profiles
├── staff.csv                    # Staff records
├── equipment.csv                # Equipment inventory
├── membermemberships.csv        # Membership enrollments
├── memberpayments.csv           # Payment history
├── classschedules.csv           # Class schedules
├── classinstances.csv           # Individual class sessions
├── classenrollments.csv         # Class registrations
└── memberaccess.csv             # Facility access logs

generated_data_mdm/               # MDM tables only
└── [MDM CSV files]

logs/                            # Generation logs
└── data_generation_YYYYMMDD_HHMMSS.log
```

## Database Loading

### Load Data into PostgreSQL

```bash
# Load complete dataset
python database_loader.py --data-dir generated_data_complete --truncate

# Verify data integrity only
python database_loader.py --verify-only

# Load specific tables
python database_loader.py --data-dir generated_data_mdm
```



### Validation Checks

The system includes automatic validation:

- **Referential integrity**: All foreign keys properly maintained
- **Business rule compliance**: Data follows realistic patterns
- **Data distribution**: Proper statistical distributions
- **Temporal consistency**: Time-series data in correct order

### Manual Verification

```bash
# Check data integrity after loading
python -c "
from database_loader import FitnessCenterDatabaseLoader
loader = FitnessCenterDatabaseLoader()
loader.connect()
loader.verify_data_integrity()
"
```


## Troubleshooting

### Common Issues

#### Import Errors
```bash
# Install missing packages
pip install -r requirements-dataload.txt

# Check Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src/dataload"
```

#### Database Connection Issues
```bash
# Test connection
python -c "
import psycopg2
conn = psycopg2.connect('postgresql://user:pass@localhost/db')
print('Connection successful')
"
```

#### Memory Issues with Large Datasets
```python
# Process in smaller batches
generator = FitnessCenterDataGenerator(
    num_facilities=10,
    num_members=10000,  # Reduce if memory issues
    num_staff=200
)
```

### Log Analysis

Check generation logs for detailed information:

```bash
# View latest log file
tail -f logs/data_generation_*.log

# Search for errors
grep -i error logs/data_generation_*.log
```

## Architecture

### Component Overview

```
run_complete_data_generation.py     # Main orchestrator
├── fitness_center_data_generator.py    # MDM table generation
├── fitness_center_ods_generator.py     # ODS table generation
├── additional_data_generator.py         # Supplementary tables
└── database_loader.py                   # PostgreSQL loading

Supporting Files:
├── requirements-dataload.txt            # Python dependencies
└── README.md                           # This documentation
```

### Data Flow

1. **MDM Generation**: Reference data (facilities, membership types, staff)
2. **ODS Generation**: Transactional data (payments, enrollments, access logs)
3. **Relationship Building**: Ensures foreign key integrity
4. **CSV Export**: Saves data to files
5. **Database Loading**: Bulk loads into PostgreSQL
6. **Validation**: Verifies data integrity



