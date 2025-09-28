# Fitness Center Data Generation System

## Overview

This comprehensive data generation system creates realistic fake data for a multi-location fitness center chain, following business rules and operational patterns. The system generates both **Master Data Management (MDM)** tables with reference data and **Operational Data Store (ODS)** tables with high-volume transactional data.

## 🎯 Business Rules Implemented

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

## 📊 Data Volume & Scale

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

## 🚀 Quick Start

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

## 🗄️ Database Loading

### Load Data into PostgreSQL

```bash
# Load complete dataset
python database_loader.py --data-dir generated_data_complete --truncate

# Verify data integrity only
python database_loader.py --verify-only

# Load specific tables
python database_loader.py --data-dir generated_data_mdm
```

### Database Schema Requirements

Ensure your PostgreSQL database has the correct schema:

**If you are using the `psql` interactive shell, run:**

```sql
-- Run the schema creation script first
\i ../sql/FitnessCenter_ODS_Schema.sql
## 🔧 Advanced Configuration

### Custom Data Volumes

```python
from fitness_center_data_generator import FitnessCenterDataGenerator

# Initialize with custom parameters
generator = FitnessCenterDataGenerator(
    num_facilities=8,
    num_members=5000,
    num_staff=150
)

# Generate specific tables
generator.generate_facilities()
generator.generate_members()
generator.generate_staff()
```

### Custom Business Rules

```python
# Modify member demographics
def custom_member_generation(self):
    # Custom logic for specific member patterns
    pass

# Extend the generator class
class CustomGenerator(FitnessCenterDataGenerator):
    def generate_members(self):
        return self.custom_member_generation()
```

## 📈 Performance Optimization

### Large Dataset Generation

For datasets with 50,000+ members:

1. **Increase batch sizes** in database loader
2. **Use asyncpg** instead of psycopg2 for faster loading
3. **Generate in chunks** for memory efficiency
4. **Disable foreign key checks** during bulk loading

```bash
# Generate very large dataset with optimizations
python run_complete_data_generation.py \
  --facilities 50 \
  --members 100000 \
  --staff 1000 \
  --load-database
```

## 🧪 Data Quality & Testing

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

## 📊 Analytics & Reporting

### Sample Analytics Queries

```sql
-- Member retention analysis
SELECT 
    DATE_TRUNC('month', joindate) as join_month,
    COUNT(*) as new_members,
    SUM(CASE WHEN memberstatus = 'Active' THEN 1 ELSE 0 END) as retained
FROM members 
GROUP BY DATE_TRUNC('month', joindate)
ORDER BY join_month;

-- Class popularity analysis
SELECT 
    ct.classname,
    COUNT(ce.enrollmentid) as total_enrollments,
    AVG(ci.actualparticipants) as avg_attendance
FROM classtypes ct
JOIN classschedules cs ON ct.classtypeid = cs.classtypeid
JOIN classinstances ci ON cs.scheduleid = ci.scheduleid
JOIN classenrollments ce ON ci.instanceid = ce.instanceid
GROUP BY ct.classname
ORDER BY total_enrollments DESC;

-- Revenue analysis
SELECT 
    DATE_TRUNC('month', paymentdate) as payment_month,
    SUM(amount) as monthly_revenue,
    COUNT(*) as transaction_count
FROM memberpayments 
WHERE status = 'Completed'
GROUP BY DATE_TRUNC('month', paymentdate)
ORDER BY payment_month;
```

## 🔍 Troubleshooting

### Common Issues

#### Import Errors
```bash
# Install missing packages
pip install -r requirements-dataload.txt

# Check Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/src/dataload"
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

## 🏗️ Architecture

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

## 🤝 Contributing

### Adding New Tables

1. **Create generator method** in appropriate class
2. **Define business rules** and data patterns
3. **Add to loading order** in database_loader.py
4. **Update documentation** and table descriptions

### Extending Business Rules

1. **Identify pattern** to implement
2. **Add realistic weights** and probabilities  
3. **Test with small dataset** first
4. **Validate against real-world** expectations

## 📋 API Integration

After loading data, test with your FastAPI application:

```bash
# Start the FastAPI server
cd ../app
python start_server.py

# Test API endpoints with generated data
curl http://localhost:8000/members/?limit=10
curl http://localhost:8000/facilities/
curl http://localhost:8000/classes/instances?date=2024-01-15
```

## 📄 License & Usage

This data generation system is designed for:
- **Development and testing** of fitness center applications
- **Analytics and reporting** system development  
- **Performance testing** with realistic datasets
- **Educational purposes** for database and API development

Generated data is completely **synthetic** and does not represent real individuals or facilities.

---

## 🎉 Success Metrics

After successful generation, you should have:

✅ **Referentially consistent data** across all tables  
✅ **Realistic business patterns** in transactions and behavior  
✅ **Scalable volume** appropriate for your testing needs  
✅ **Time-series data** for analytics and reporting  
✅ **Geographic distribution** across multiple facilities  
✅ **Comprehensive documentation** of data patterns and relationships

**Happy Data Generating! 🚀**