"""
Data loading utilities for Brent Oil Price Change Point Analysis.
Task 1: Foundation - Data loading and validation module
"""
import pandas as pd
import numpy as np
from pathlib import Path
import requests
from typing import Tuple, Dict, Optional
import logging
import re
from io import StringIO

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BrentOilDataLoader:
    """Loader for historical Brent oil price data from challenge dataset."""

    def __init__(self, data_dir: str = "./data"):
        """
        Initialize DataLoader with data directory paths.
        
        Parameters:
        -----------
        data_dir : str
            Path to data directory (default: "./data")
        """
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        
        # Create directories if they don't exist
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
        # URL from the challenge document (Google Drive direct download link)
        self.data_url = "https://drive.google.com/uc?export=download&id=1BHxqmHCg77dYJvC0Og_d0Ty49oadN1OS"
        
        logger.info(f"DataLoader initialized. Raw data will be saved to: {self.raw_dir}")

    def download_raw_data(self, force_download: bool = False) -> Path:
        """
        Downloads the raw CSV dataset from Google Drive.
        
        Parameters:
        -----------
        force_download : bool
            If True, download even if file exists (default: False)
            
        Returns:
        --------
        Path
            Path to the downloaded CSV file
        """
        file_path = self.raw_dir / "brent_daily_prices.csv"
        
        # Check if file already exists
        if file_path.exists() and not force_download:
            logger.info(f"File already exists: {file_path}. Skipping download.")
            return file_path
        
        logger.info(f"Downloading data from {self.data_url}")
        try:
            # For Google Drive direct download
            session = requests.Session()
            
            # Get the initial response
            response = session.get(self.data_url, stream=True, timeout=30)
            response.raise_for_status()
            
            # Save content to file
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive chunks
                        f.write(chunk)
            
            file_size = file_path.stat().st_size / 1024
            logger.info(f"Successfully downloaded {file_size:.2f} KB to {file_path}")
            
            # Check if file is valid (not HTML)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                first_line = f.readline()
                if first_line.startswith('<!DOCTYPE') or first_line.startswith('<html') or 'html' in first_line.lower():
                    logger.error("Downloaded file appears to be HTML, not CSV!")
                    logger.info(f"First 200 chars: {first_line[:200]}")
                    
                    # Try alternative download method
                    logger.info("Trying alternative download method...")
                    alt_url = "https://drive.google.com/file/d/1BHxqmHCg77dYJvC0Og_d0Ty49oadN1OS/view?usp=sharing"
                    
                    # Try to extract direct download link from the view page
                    view_response = session.get(alt_url, timeout=30)
                    if view_response.status_code == 200:
                        # Look for download link in the page
                        import re
                        download_pattern = r'href="(/uc\?export=download[^"]+)"'
                        matches = re.findall(download_pattern, view_response.text)
                        if matches:
                            download_link = "https://drive.google.com" + matches[0]
                            logger.info(f"Found download link: {download_link}")
                            
                            # Download using the extracted link
                            response = session.get(download_link, stream=True, timeout=30)
                            with open(file_path, 'wb') as f:
                                for chunk in response.iter_content(chunk_size=8192):
                                    if chunk:
                                        f.write(chunk)
                            
                            logger.info(f"Re-downloaded file: {file_path.stat().st_size / 1024:.2f} KB")
            
            return file_path
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download data: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during download: {e}")
            raise

    def load_and_validate_data(self) -> pd.DataFrame:
        """
        Loads the CSV and validates its basic structure.
        
        Returns:
        --------
        pd.DataFrame
            Cleaned and validated Brent oil price dataframe
        """
        # Download data if not exists
        file_path = self.download_raw_data()
        logger.info(f"Loading data from {file_path}")
        
        # First, read the file to understand its structure
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            logger.info(f"File size: {len(content)} characters")
            
            # Try to find data lines (look for date patterns)
            date_pattern = r'\d{1,2}-[A-Za-z]{3,4}-\d{2,4}'
            lines = content.split('\n')
            
            # Find header and data lines
            data_lines = []
            header_line = None
            
            for i, line in enumerate(lines[:20]):  # Check first 20 lines
                if re.search(date_pattern, line):
                    data_lines.append(line)
                elif 'date' in line.lower() and ('price' in line.lower() or 'close' in line.lower()):
                    header_line = line
                    logger.info(f"Found header at line {i}: {line[:100]}")
            
            logger.info(f"Found {len(data_lines)} data lines with date patterns")
            
            if not data_lines:
                logger.error("No data lines found with date patterns!")
                logger.info("First 500 chars of file:")
                logger.info(content[:500])
                raise ValueError("No valid data found in file")
            
            # Try to parse the data
            if header_line:
                # We have a header, use it
                df = pd.read_csv(StringIO('\n'.join([header_line] + data_lines)), 
                                parse_dates=['Date'], 
                                dayfirst=True)
            else:
                # No header found, assume first column is Date, second is Price
                logger.info("No header found, assuming columns: Date, Price")
                
                # Clean and parse data lines
                clean_data = []
                for line in data_lines:
                    # Split by common delimiters
                    parts = re.split(r'[,;\t\s]+', line.strip())
                    if len(parts) >= 2:
                        clean_data.append(f"{parts[0]},{parts[1]}")
                
                df = pd.read_csv(StringIO('\n'.join(clean_data)), 
                                names=['Date', 'Price'],
                                parse_dates=['Date'],
                                dayfirst=True)
            
            logger.info(f"Successfully parsed {len(df)} records")
            
        except Exception as e:
            logger.error(f"Error parsing file: {e}")
            logger.info("Trying fallback parsing method...")
            
            # Fallback: Try pandas read_csv with different parameters
            try:
                df = pd.read_csv(file_path, parse_dates=['Date'], dayfirst=True)
            except:
                try:
                    df = pd.read_csv(file_path)
                    # Try to identify date column
                    for col in df.columns:
                        if pd.api.types.is_string_dtype(df[col]):
                            # Try to convert to datetime
                            df['Date'] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')
                            if df['Date'].notna().any():
                                logger.info(f"Identified date column: {col}")
                                break
                    
                    # Try to identify price column
                    for col in df.columns:
                        if pd.api.types.is_numeric_dtype(df[col]) and col != 'Date':
                            df['Price'] = df[col]
                            logger.info(f"Identified price column: {col}")
                            break
                    
                    if 'Date' not in df.columns or 'Price' not in df.columns:
                        raise ValueError("Could not identify Date and Price columns")
                        
                except Exception as e2:
                    logger.error(f"Fallback parsing also failed: {e2}")
                    raise
        
        # Validate required columns
        required_columns = ['Date', 'Price']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            error_msg = f"CSV is missing required columns: {missing_columns}. Found columns: {list(df.columns)}"
            logger.error(error_msg)
            
            # Try to rename columns
            col_mapping = {}
            for col in df.columns:
                col_lower = str(col).lower()
                if 'date' in col_lower:
                    col_mapping[col] = 'Date'
                elif 'price' in col_lower or 'close' in col_lower or 'value' in col_lower:
                    col_mapping[col] = 'Price'
            
            if col_mapping:
                df = df.rename(columns=col_mapping)
                logger.info(f"Renamed columns: {col_mapping}")
                missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"CSV is missing required columns: {missing_columns}. Found columns: {list(df.columns)}")
        
        # Sort by date and reset index
        df = df.sort_values('Date').reset_index(drop=True)
        
        # Basic data quality checks
        logger.info("=" * 50)
        logger.info("DATA VALIDATION REPORT")
        logger.info("=" * 50)
        logger.info(f"Total records loaded: {len(df):,}")
        logger.info(f"Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")
        logger.info(f"Total days covered: {(df['Date'].max() - df['Date'].min()).days:,}")
        
        # Check for missing values
        missing_count = df['Price'].isnull().sum()
        if missing_count > 0:
            logger.warning(f"Missing Price values: {missing_count} ({missing_count/len(df)*100:.2f}%)")
        else:
            logger.info("No missing Price values found.")
        
        # Check for duplicates
        duplicate_dates = df['Date'].duplicated().sum()
        if duplicate_dates > 0:
            logger.warning(f"Duplicate dates found: {duplicate_dates}")
            df = df.drop_duplicates(subset=['Date'], keep='first')
            logger.info(f"Removed duplicates. New record count: {len(df)}")
        
        # Check for price outliers/validity
        price_stats = df['Price'].describe()
        logger.info(f"Price statistics:\n{price_stats}")
        
        if (df['Price'] <= 0).any():
            logger.warning(f"Non-positive prices found: {(df['Price'] <= 0).sum()} records")
        
        logger.info("=" * 50)
        
        return df

    def save_processed_data(self, df: pd.DataFrame, filename: str) -> Path:
        """
        Save processed data to processed directory.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Dataframe to save
        filename : str
            Name of the file (without directory)
            
        Returns:
        --------
        Path
            Path to saved file
        """
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        file_path = self.processed_dir / filename
        df.to_csv(file_path, index=False)
        logger.info(f"Saved processed data to {file_path}")
        return file_path


# Example usage for testing
if __name__ == "__main__":
    print("Testing BrentOilDataLoader module...")
    
    # Initialize loader
    loader = BrentOilDataLoader(data_dir='../data')
    
    try:
        # Load and validate data
        brent_df = loader.load_and_validate_data()
        
        # Display sample
        print("\n" + "=" * 60)
        print("SAMPLE DATA (First 5 rows):")
        print("=" * 60)
        print(brent_df.head())
        
        print("\n" + "=" * 60)
        print("DATA INFO:")
        print("=" * 60)
        print(f"Shape: {brent_df.shape}")
        print(f"Columns: {list(brent_df.columns)}")
        print(f"Date dtype: {brent_df['Date'].dtype}")
        print(f"Price dtype: {brent_df['Price'].dtype}")
        
        # Save a processed version
        processed_path = loader.save_processed_data(brent_df, "brent_prices_cleaned")
        print(f"\nProcessed data saved to: {processed_path}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nTrying manual download approach...")
        print("Please download the file manually from:")
        print("https://drive.google.com/file/d/1BHxqmHCg77dYJvC0Og_d0Ty49oadN1OS/view?usp=sharing")
        print("And save it as: data/raw/brent_daily_prices.csv")