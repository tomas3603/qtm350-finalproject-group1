import pandas as pd

def forward_fill_across_years(row, cols):
    for i in range(1, len(cols)):
        if pd.isna(row[cols[i]]):
            prev_val = row[cols[i-1]]
            
            # Check if there's a next column and that it's not missing
            if i < len(cols)-1 and not pd.isna(row[cols[i+1]]):
                next_val = row[cols[i+1]]
                # Use the average of prev_val and next_val
                row[cols[i]] = (prev_val + next_val) / 2
            else:
                # If no next value is available, fall back to prev_val
                row[cols[i]] = prev_val
    return row