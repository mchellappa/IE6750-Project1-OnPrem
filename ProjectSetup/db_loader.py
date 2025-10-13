#!/usr/bin/env python3
"""
PostgreSQL Database Loader for             print(f"SUCCESS: Connected         except psycopg2.Error as e:
            print(f"ERROR: Error clearing tables: {e}")
            self.connection.rollback()
            raiseostgreSQL database: {self.connection_params['database']}")
            return True
        except psycopg2.Error as e:
            print(f"ERROR: Error connecting to database: {e}")
            return Falsess Center Data Warehouse
Loads CSV files directly into PostgreSQL ODS database using COPY command
Much faster and more efficient than individual INSERT statements
"""

import os
import sys
import pandas as pd
import psycopg2
from pathlib import Path
import json
from datetime import datetime
import argparse

class FitnessCenterDBLoader:
    def __init__(self, host='localhost', port=5432, database='fitness_center_ods', 
                 user='postgres', password=None):
        self.connection_params = {
            'host': host,
            'port': port,
            'database': database,
            'user': user,
            'password': password
        }
        self.connection = None
        self.cursor = None
        
        # Define table loading order (respects foreign key dependencies)
        self.table_order = [
            'facilities',
            'facility_areas', 
            'members',
            'staff',
            'class_types',
            'equipment',
            'class_enrollments',
            'equipment_usage'
        ]
        
        # CSV to table mapping
        self.csv_table_mapping = {
            'facilities.csv': 'ods.facilities',
            'facility_areas.csv': 'ods.facility_areas',
            'members.csv': 'ods.members', 
            'staff.csv': 'ods.staff',
            'class_types.csv': 'ods.class_types',
            'equipment.csv': 'ods.equipment',
            'class_enrollments.csv': 'ods.class_enrollments',
            'equipment_usage.csv': 'ods.equipment_usage'
        }

    def connect(self):
        """Establish database connection"""
        try:
            self.connection = psycopg2.connect(**self.connection_params)
            self.cursor = self.connection.cursor()
            print(f"✅ Connected to PostgreSQL database: {self.connection_params['database']}")
            return True
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("INFO: Database connection closed")

    def clear_tables(self):
        """Clear all ODS tables in reverse dependency order"""
        reverse_order = list(reversed(self.table_order))
        
        try:
            print("\nINFO: Clearing existing data...")
            
            # Disable foreign key checks temporarily
            self.cursor.execute("SET session_replication_role = replica;")
            
            for table_name in reverse_order:
                full_table_name = f"ods.{table_name}"
                self.cursor.execute(f"TRUNCATE TABLE {full_table_name} CASCADE;")
                print(f"   Cleared {full_table_name}")
            
            # Re-enable foreign key checks
            self.cursor.execute("SET session_replication_role = DEFAULT;")
            
            self.connection.commit()
            print("SUCCESS: All tables cleared successfully")
            
        except psycopg2.Error as e:
            print(f"Error clearing tables: {e}")
            self.connection.rollback()
            raise

    def validate_csv_files(self, data_dir):
        """Validate that all required CSV files exist"""
        missing_files = []
        
        for csv_file in self.csv_table_mapping.keys():
            csv_path = Path(data_dir) / csv_file
            if not csv_path.exists():
                missing_files.append(csv_file)
        
        if missing_files:
            print(f"ERROR: Missing CSV files: {missing_files}")
            return False
            
        print("SUCCESS: All required CSV files found")
        return True

    def get_table_info(self, table_name):
        """Get column information for a table"""
        try:
            self.cursor.execute(f"""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_schema = 'ods' AND table_name = '{table_name}'
                ORDER BY ordinal_position
            """)
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"ERROR: Error getting table info for {table_name}: {e}")
            return []

    def load_csv_to_table(self, csv_path, table_name):
        """Load CSV file directly into PostgreSQL table using COPY command"""
        try:
            # Read CSV to get column names
            df = pd.read_csv(csv_path)
            
            print(f"INFO: Loading {csv_path.name} -> {table_name} ({len(df)} records)")
            
            # Create a temporary CSV for PostgreSQL COPY (handles data types properly)
            temp_csv = csv_path.parent / f"temp_{csv_path.name}"
            
            # Clean data for PostgreSQL
            df_clean = df.copy()
            
            # Handle NaN values
            df_clean = df_clean.fillna('')
            
            # Convert datetime columns to proper format if they exist
            datetime_columns = ['last_modified', 'join_date', 'hire_date', 'purchase_date', 
                              'warranty_expiry', 'date_of_birth', 'enrollment_date', 'class_date',
                              'usage_date']
            
            for col in datetime_columns:
                if col in df_clean.columns:
                    df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
            
            # Save cleaned CSV
            df_clean.to_csv(temp_csv, index=False, na_rep='\\N')
            
            # Use COPY command for fast bulk insert
            with open(temp_csv, 'r') as f:
                self.cursor.copy_expert(
                    f"COPY {table_name} FROM STDIN WITH CSV HEADER NULL '\\N'",
                    f
                )
            
            self.connection.commit()
            
            # Clean up temporary file
            temp_csv.unlink()
            
            # Verify record count
            self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = self.cursor.fetchone()[0]
            print(f"   SUCCESS: Loaded {count} records successfully")
            
            return count
            
        except Exception as e:
            print(f"   ERROR: Error loading {csv_path.name}: {e}")
            self.connection.rollback()
            raise

    def load_all_data(self, data_dir):
        """Load all CSV files in correct dependency order"""
        data_path = Path(data_dir)
        
        if not self.validate_csv_files(data_path):
            return False
        
        total_records = 0
        loading_summary = []
        
        print(f"\nINFO: Loading data from: {data_path}")
        print("=" * 60)
        
        for table_name in self.table_order:
            csv_file = f"{table_name}.csv"
            csv_path = data_path / csv_file
            full_table_name = self.csv_table_mapping[csv_file]
            
            try:
                record_count = self.load_csv_to_table(csv_path, full_table_name)
                total_records += record_count
                loading_summary.append({
                    'table': full_table_name,
                    'records': record_count,
                    'status': 'SUCCESS'
                })
                
            except Exception as e:
                loading_summary.append({
                    'table': full_table_name,
                    'records': 0,
                    'status': f'FAILED: {e}'
                })
                print(f"ERROR: Failed to load {table_name}: {e}")
                return False
        
        print("=" * 60)
        print(f"SUCCESS: Data loading completed! Total records loaded: {total_records:,}")
        
        # Print summary
        print("\nINFO: Loading Summary:")
        for item in loading_summary:
            status_icon = "SUCCESS" if item['status'] == 'SUCCESS' else "ERROR"
            print(f"   {status_icon}: {item['table']:<30} {item['records']:>8,} records")
        
        return True

    def validate_data_integrity(self):
        """Validate foreign key relationships and data quality"""
        print("\nINFO: Validating data integrity...")
        
        validation_queries = [
            {
                'name': 'Facility Areas → Facilities',
                'query': """
                    SELECT COUNT(*) FROM ods.facility_areas fa 
                    LEFT JOIN ods.facilities f ON fa.facility_id = f.facility_id 
                    WHERE f.facility_id IS NULL
                """,
                'expected': 0
            },
            {
                'name': 'Equipment → Facilities',
                'query': """
                    SELECT COUNT(*) FROM ods.equipment e 
                    LEFT JOIN ods.facilities f ON e.facility_id = f.facility_id 
                    WHERE f.facility_id IS NULL
                """,
                'expected': 0
            },
            {
                'name': 'Class Enrollments → Members',
                'query': """
                    SELECT COUNT(*) FROM ods.class_enrollments ce 
                    LEFT JOIN ods.members m ON ce.member_id = m.member_id 
                    WHERE m.member_id IS NULL
                """,
                'expected': 0
            },
            {
                'name': 'Equipment Usage → Members',
                'query': """
                    SELECT COUNT(*) FROM ods.equipment_usage eu 
                    LEFT JOIN ods.members m ON eu.member_id = m.member_id 
                    WHERE m.member_id IS NULL
                """,
                'expected': 0
            },
            {
                'name': 'Members with Valid Birth Dates',
                'query': """
                    SELECT COUNT(*) FROM ods.members 
                    WHERE date_of_birth IS NULL OR date_of_birth > CURRENT_DATE
                """,
                'expected': 0
            }
        ]
        
        all_passed = True
        
        for validation in validation_queries:
            try:
                self.cursor.execute(validation['query'])
                result = self.cursor.fetchone()[0]
                
                if result == validation['expected']:
                    print(f"   SUCCESS: {validation['name']}: PASSED")
                else:
                    print(f"   ERROR: {validation['name']}: FAILED ({result} violations)")
                    all_passed = False
                    
            except psycopg2.Error as e:
                print(f"   ERROR: {validation['name']}: ERROR - {e}")
                all_passed = False
        
        return all_passed

    def generate_summary_report(self):
        """Generate data summary report"""
        print("\nINFO: Data Summary Report:")
        print("=" * 50)
        
        summary_queries = [
            ("Total Facilities", "SELECT COUNT(*) FROM ods.facilities"),
            ("Total Members", "SELECT COUNT(*) FROM ods.members"),
            ("Total Staff", "SELECT COUNT(*) FROM ods.staff"),
            ("Total Equipment", "SELECT COUNT(*) FROM ods.equipment"),
            ("Total Class Enrollments", "SELECT COUNT(*) FROM ods.class_enrollments"),
            ("Total Equipment Usage", "SELECT COUNT(*) FROM ods.equipment_usage"),
            ("Date Range (Enrollments)", """
                SELECT MIN(class_date)::text || ' to ' || MAX(class_date)::text 
                FROM ods.class_enrollments
            """),
            ("Date Range (Equipment Usage)", """
                SELECT MIN(usage_date)::text || ' to ' || MAX(usage_date)::text 
                FROM ods.equipment_usage
            """)
        ]
        
        for description, query in summary_queries:
            try:
                self.cursor.execute(query)
                result = self.cursor.fetchone()[0]
                print(f"{description:<25}: {result}")
            except psycopg2.Error as e:
                print(f"{description:<25}: ERROR - {e}")


def main():
    parser = argparse.ArgumentParser(description='Load fitness center CSV data into PostgreSQL')
    parser.add_argument('--data-dir', default='ods_sample_data', 
                       help='Directory containing CSV files (default: ods_sample_data)')
    parser.add_argument('--host', default='localhost', 
                       help='PostgreSQL host (default: localhost)')
    parser.add_argument('--port', type=int, default=5432,
                       help='PostgreSQL port (default: 5432)')
    parser.add_argument('--database', default='fitness_center_ods',
                       help='Database name (default: fitness_center_ods)')
    parser.add_argument('--user', default='postgres',
                       help='Database user (default: postgres)')
    parser.add_argument('--password',
                       help='Database password (will prompt if not provided)')
    parser.add_argument('--clear', action='store_true',
                       help='Clear existing data before loading')
    parser.add_argument('--validate-only', action='store_true',
                       help='Only run data validation, do not load')
    
    args = parser.parse_args()
    
    # Prompt for password if not provided
    if not args.password:
        import getpass
        args.password = getpass.getpass("PostgreSQL password: ")
    
    # Initialize loader
    loader = FitnessCenterDBLoader(
        host=args.host,
        port=args.port,
        database=args.database,
        user=args.user,
        password=args.password
    )
    
    # Connect to database
    if not loader.connect():
        sys.exit(1)
    
    try:
        if args.validate_only:
            # Just validate existing data
            loader.validate_data_integrity()
            loader.generate_summary_report()
        else:
            # Clear data if requested
            if args.clear:
                loader.clear_tables()
            
            # Load data
            if loader.load_all_data(args.data_dir):
                # Validate loaded data
                if loader.validate_data_integrity():
                    print("\nSUCCESS: All data validation checks passed!")
                else:
                    print("\nWARNING: Some data validation checks failed. Please review.")
                
                # Generate summary report
                loader.generate_summary_report()
            else:
                print("\nERROR: Data loading failed!")
                sys.exit(1)
                
    finally:
        loader.disconnect()


if __name__ == "__main__":
    main()