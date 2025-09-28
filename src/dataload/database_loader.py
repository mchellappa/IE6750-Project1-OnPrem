#!/usr/bin/env python3
"""
Fitness Center Database Loader

This module loads the generated fake data into the PostgreSQL database,
following proper insert order based on foreign key dependencies.

Author: Fitness Center Analytics Team
Date: September 2025
Version: 1.0
"""

import os
import sys
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import logging
from datetime import datetime
from decimal import Decimal
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FitnessCenterDatabaseLoader:
    """Loads generated data into PostgreSQL database following dependency order"""
    
    def __init__(self, database_url=None):
        """
        Initialize database loader
        
        Args:
            database_url: PostgreSQL connection string
        """
        self.database_url = database_url or os.getenv(
            'DATABASE_URL', 
            'postgresql://postgres:Brenau27@localhost:5432/postgres'
        )
        self.connection = None
        self.cursor = None
        
        # Define table loading order (respects foreign key dependencies)
        self.load_order = [
            # Master Data Management (MDM) - No dependencies
            'membershiptypes',
            'classtypes', 
            'instructorcertifications',
            'facilities',
            
            # Facility & Asset Master - Depends on facilities
            'facilityareas',
            'equipment',
            
            # People Master Data - No dependencies  
            'members',
            'staff',
            
            # Operational Configuration - Depends on facilities, areas, staff, classtypes
            'classschedules',
            
            # Financial Transaction Data - Depends on members, membershiptypes
            'membermemberships',
            'memberpayments',
            
            # Operational Transaction Data - Depends on schedules
            'classinstances',
            'classenrollments',
            
            # Additional ODS tables (if generated)
            'memberaccess',
            'equipmentusage',
            'equipmentmaintenance',
            'staffschedules',
            'stafftimetracking',
            'staffpayroll',
            'stafffacilities',
            'staffcertifications',
            'instructorfeedback',
            'instructorperformance'
        ]
    
    def connect(self):
        """Establish database connection"""
        try:
            logger.info(f"Connecting to database...")
            self.connection = psycopg2.connect(self.database_url)
            self.cursor = self.connection.cursor()
            logger.info("Database connection established successfully")
            return True
            
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("Database connection closed")
    
    def truncate_all_tables(self):
        """Truncate all tables in reverse dependency order"""
        logger.info("Truncating all tables...")
        
        try:
            # Disable foreign key checks temporarily
            self.cursor.execute("SET session_replication_role = replica;")
            
            # Truncate in reverse order
            for table_name in reversed(self.load_order):
                try:
                    self.cursor.execute(f"TRUNCATE TABLE {table_name} CASCADE;")
                    logger.info(f"Truncated table: {table_name}")
                except Exception as e:
                    logger.warning(f"Could not truncate {table_name}: {e}")
            
            # Re-enable foreign key checks
            self.cursor.execute("SET session_replication_role = DEFAULT;")
            self.connection.commit()
            
            logger.info("All tables truncated successfully")
            
        except Exception as e:
            logger.error(f"Error truncating tables: {e}")
            self.connection.rollback()
            raise
    
    def load_csv_data(self, data_dir="generated_data"):
        """Load data from CSV files in dependency order"""
        logger.info(f"Loading data from {data_dir}...")
        
        total_records = 0
        
        for table_name in self.load_order:
            csv_file = os.path.join(data_dir, f"{table_name}.csv")
            
            if not os.path.exists(csv_file):
                logger.warning(f"CSV file not found: {csv_file}")
                continue
            
            try:
                # Read CSV
                df = pd.read_csv(csv_file)
                
                if len(df) == 0:
                    logger.warning(f"No data in {csv_file}")
                    continue
                
                # Load into database
                records_loaded = self.load_table_data(table_name, df)
                total_records += records_loaded
                
                logger.info(f"Loaded {records_loaded:,} records into {table_name}")
                
            except Exception as e:
                logger.error(f"Error loading {table_name}: {e}")
                raise
        
        logger.info(f"Total records loaded: {total_records:,}")
        return total_records
    
    def load_table_data(self, table_name, df):
        """Load DataFrame into specific table"""
        if len(df) == 0:
            return 0
        
        try:
            # Prepare column names and placeholders
            columns = list(df.columns)
            placeholders = ', '.join(['%s'] * len(columns))
            
            # Convert DataFrame to list of tuples
            data_tuples = []
            for _, row in df.iterrows():
                # Convert values to appropriate types
                row_data = []
                for value in row:
                    if pd.isna(value):
                        row_data.append(None)
                    elif isinstance(value, (pd.Timestamp, datetime)):
                        row_data.append(value.isoformat() if hasattr(value, 'isoformat') else str(value))
                    else:
                        row_data.append(value)
                data_tuples.append(tuple(row_data))
            
            # Build INSERT query
            insert_query = f"""
                INSERT INTO {table_name} ({', '.join(columns)})
                VALUES %s
                ON CONFLICT DO NOTHING
            """
            
            # Execute batch insert
            execute_values(
                self.cursor, 
                insert_query, 
                data_tuples,
                template=None,
                page_size=1000
            )
            
            self.connection.commit()
            return len(data_tuples)
            
        except Exception as e:
            logger.error(f"Error inserting data into {table_name}: {e}")
            self.connection.rollback()
            raise
    
    def verify_data_integrity(self):
        """Verify loaded data integrity and relationships"""
        logger.info("Verifying data integrity...")
        
        integrity_checks = {
            'facilities': "SELECT COUNT(*) FROM facilities WHERE isactive = true",
            'members': "SELECT COUNT(*) FROM members WHERE memberstatus = 'Active'",
            'staff': "SELECT COUNT(*) FROM staff WHERE status = 'Active'",
            'member_membership_integrity': """
                SELECT COUNT(*) FROM membermemberships mm 
                JOIN members m ON mm.memberid = m.memberid 
                JOIN membershiptypes mt ON mm.membershiptypeid = mt.membershiptypeid
            """,
            'class_enrollment_integrity': """
                SELECT COUNT(*) FROM classenrollments ce
                JOIN classinstances ci ON ce.instanceid = ci.instanceid
                JOIN classschedules cs ON ci.scheduleid = cs.scheduleid
                JOIN members m ON ce.memberid = m.memberid
            """,
            'payment_integrity': """
                SELECT COUNT(*) FROM memberpayments mp
                JOIN membermemberships mm ON mp.membershipid = mm.membershipid
                JOIN members m ON mp.memberid = m.memberid
            """
        }
        
        results = {}
        
        for check_name, query in integrity_checks.items():
            try:
                self.cursor.execute(query)
                count = self.cursor.fetchone()[0]
                results[check_name] = count
                logger.info(f"{check_name}: {count:,} records")
                
            except Exception as e:
                logger.error(f"Integrity check failed for {check_name}: {e}")
                results[check_name] = "ERROR"
        
        return results
    
    def generate_summary_report(self):
        """Generate data loading summary report"""
        logger.info("Generating summary report...")
        
        try:
            # Get record counts for all tables
            table_counts = {}
            
            for table_name in self.load_order:
                try:
                    self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = self.cursor.fetchone()[0]
                    table_counts[table_name] = count
                except Exception as e:
                    logger.warning(f"Could not get count for {table_name}: {e}")
                    table_counts[table_name] = 0
            
            # Generate report
            report = {
                'load_date': datetime.now().isoformat(),
                'database_url': self.database_url.replace(self.database_url.split('@')[0].split('//')[1], '***'),
                'table_counts': table_counts,
                'total_records': sum(table_counts.values()),
                'integrity_checks': self.verify_data_integrity()
            }
            
            # Save report to file
            report_file = f"data_load_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            logger.info(f"Summary report saved to {report_file}")
            
            # Print summary to console
            print("\n" + "="*50)
            print("DATA LOADING SUMMARY")
            print("="*50)
            print(f"Load Date: {report['load_date']}")
            print(f"Total Records: {report['total_records']:,}")
            print("\nTable Record Counts:")
            print("-"*30)
            
            for table, count in table_counts.items():
                if count > 0:
                    print(f"{table:25}: {count:>8,}")
            
            print("-"*30)
            print(f"{'TOTAL':25}: {report['total_records']:>8,}")
            print("="*50)
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating summary report: {e}")
            return None


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Load fitness center data into PostgreSQL')
    parser.add_argument('--data-dir', default='generated_data', 
                       help='Directory containing CSV files')
    parser.add_argument('--database-url', 
                       help='PostgreSQL connection string')
    parser.add_argument('--truncate', action='store_true',
                       help='Truncate tables before loading')
    parser.add_argument('--verify-only', action='store_true',
                       help='Only verify data integrity, do not load')
    
    args = parser.parse_args()
    
    # Initialize loader
    loader = FitnessCenterDatabaseLoader(args.database_url)
    
    try:
        # Connect to database
        if not loader.connect():
            sys.exit(1)
        
        if args.verify_only:
            # Only run verification
            loader.verify_data_integrity()
            loader.generate_summary_report()
        else:
            # Truncate if requested
            if args.truncate:
                confirmation = input("Are you sure you want to truncate all tables? (yes/no): ")
                if confirmation.lower() == 'yes':
                    loader.truncate_all_tables()
                else:
                    logger.info("Truncation cancelled")
                    sys.exit(0)
            
            # Load data
            loader.load_csv_data(args.data_dir)
            
            # Generate report
            loader.generate_summary_report()
        
    except KeyboardInterrupt:
        logger.info("Loading cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Loading failed: {e}")
        sys.exit(1)
    finally:
        loader.disconnect()


if __name__ == "__main__":
    main()