import pandas as pd
import hashlib
import os

def generate_participant_id(value):
    """Generate SHA-256 hash for a given value"""
    return hashlib.sha256(str(value).encode('utf-8')).hexdigest()

def load_and_process_csv(filename):
    """Load CSV file and create participant_id column"""
    print(f"Processing {filename}...")
    
    # Load the CSV file
    df = pd.read_csv(filename)
    
    # Check if رقم الجوال column exists
    mobile_col = 'رقم الجوال'
    name_col = None
    
    # Find the name column (look for variations)
    possible_name_cols = [' اسم الطالبة الرباعي (مثال: سارة احمد محمد الزهراني)', 
                         'الاسم الثلاثي', 'اسم الطالبة الرباعي', 'الاسم']
    
    for col in possible_name_cols:
        if col in df.columns:
            name_col = col
            break
    
    # Create participant_id based on available columns
    if mobile_col in df.columns:
        print(f"  Using mobile number column: {mobile_col}")
        df['participant_id'] = df[mobile_col].apply(generate_participant_id)
    elif name_col:
        print(f"  Using name column: {name_col}")
        df['participant_id'] = df[name_col].apply(generate_participant_id)
    else:
        print(f"  ERROR: Neither mobile number nor name column found in {filename}")
        print(f"  Available columns: {list(df.columns)}")
        return None
    
    return df

def main():
    """Main function to process all CSV files"""
    print("Phase 0, Step 1: Generate Stable Participant IDs")
    print("=" * 50)
    
    # List of CSV files to process
    csv_files = ['1h.csv', '1m.csv', '2h.csv', '2m.csv', '3h.csv', '3m.csv']
    dataframes = {}
    
    # Process each CSV file
    for filename in csv_files:
        if os.path.exists(filename):
            df = load_and_process_csv(filename)
            if df is not None:
                # Extract the base name for variable naming
                base_name = filename.replace('.csv', '')
                dataframes[f'df_{base_name}'] = df
                
                # Verify uniqueness
                total_rows = len(df)
                unique_ids = df['participant_id'].nunique()
                print(f"  {base_name}: {unique_ids} unique participant_ids out of {total_rows} rows")
                
                if unique_ids != total_rows:
                    print(f"  WARNING: Duplicate participant_ids found in {filename}")
                else:
                    print(f"  ✓ All participant_ids are unique in {filename}")
            else:
                print(f"  Failed to process {filename}")
        else:
            print(f"  ERROR: File {filename} not found")
        print()
    
    print("Step 1 complete: Stable participant_id generated for all records.")
    
    # Return the dataframes for further use
    return dataframes

if __name__ == "__main__":
    dataframes = main()