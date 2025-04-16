import pandas as pd
import numpy as np
from model_utils import generate_sample_data

# Generate sample data using the function
df = generate_sample_data()

# Save to CSV with descriptive name
output_file = 'sample_learner_data.csv'
df.to_csv(output_file, index=False)

# Print first few rows to verify
print(f"\nSample data saved to {output_file}")
print("\nFirst few rows:")
print(df.head())
print(f"\nTotal records generated: {len(df)}")