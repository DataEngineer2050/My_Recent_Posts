import pandas as pd
import numpy as np

def run_recruitment_analytics (file_path):
    # Load Data
    df = pd.read_csv (file_path)

    # Date formatting
    df['stage_date'] = pd.to_datetime(df['stage_date'])

    # Define stage sequence 
    stage_order = ['Applied', 'Screened', 'Interviewed', 'Offered', 'Hired']

    # Count gap(in days) between stages
    df = df.sort_values(by=['application_id', 'stage_date'])
    df['prev_date'] = df.groupby('application_id')['stage_date'].transform(lambda x: x.shift(1))
    df['days_in_stage'] = (df['stage_date'] - df['prev_date'])

    # Take out Median(days)
    median_days = df.groupby('stage')['days_in_stage'].median().reindex(stage_order)

    # Count each category (Applied, Screened,....,Hired) in stage     
    stage_counts = (df[df['stage'].isin(stage_order)]['stage'].value_counts().reindex(stage_order))

   # Management level analytics: funnel conversion rates                
    total_applied = stage_counts ['Applied']   
    conversion_summary = pd.DataFrame ({
        'Total_Candidates': stage_counts,
        'Median_Days_From_Prev_Stage': median_days,
        'Dropped_From_Applied_Pct': ((total_applied - stage_counts)/(total_applied) * 100).round(2),
        'Step_Conversion_Pct': (stage_counts.pct_change() * 100+100).fillna(100).round(2)
    }
    ) 

    # Rejections Summary
    total_rejected = (df[df['stage'].isin(['Rejected', 'Offer Declined'])]['stage'].value_counts())

    #Result Display
    print("=== Recruitment Funnel Analytics (for CFO) ===")
    print(conversion_summary.to_string())
    print("=== Rejections / Loss Summary ===")
    print(total_rejected.to_string())

    # Save to CSV
    conversion_summary.to_csv('recruitment_funnel_metrics.csv')
    print("\n [Success] analytics saved to recruitment_funnel_metrics.csv")

# Call run_recruitment_analytics (defined at top)
if __name__ == "__main__":
    run_recruitment_analytics ('applications.csv')
