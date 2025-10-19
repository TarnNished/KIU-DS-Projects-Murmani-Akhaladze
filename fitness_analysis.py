import numpy as np

np.random.seed(42)

print("=" * 80)
print("TASK 3: APPLIED DATA ANALYSIS - FITNESS TRACKING")
print("=" * 80)

print("\n### PART A: DATA GENERATION & PREPARATION ###\n")
print("-" * 80)

num_users = 100
num_days = 90
num_metrics = 4

print("Generating fitness tracking data...")
print(f"Dimensions: {num_users} users × {num_days} days × {num_metrics} metrics")

fitness_data = np.zeros((num_users, num_days, num_metrics))

fitness_data[:, :, 0] = np.random.normal(loc=8500, scale=2500, size=(num_users, num_days))
fitness_data[:, :, 0] = np.clip(fitness_data[:, :, 0], 2000, 15000)

fitness_data[:, :, 1] = np.random.normal(loc=2500, scale=400, size=(num_users, num_days))
fitness_data[:, :, 1] = np.clip(fitness_data[:, :, 1], 1500, 3500)

fitness_data[:, :, 2] = np.random.normal(loc=100, scale=30, size=(num_users, num_days))
fitness_data[:, :, 2] = np.clip(fitness_data[:, :, 2], 20, 180)

fitness_data[:, :, 3] = np.random.normal(loc=85, scale=12, size=(num_users, num_days))
fitness_data[:, :, 3] = np.clip(fitness_data[:, :, 3], 60, 120)

print(f"Data shape: {fitness_data.shape}")
print(f"Sample data (User 1, Day 1): {fitness_data[0, 0, :]}")

print("\nGenerating user metadata...")
user_metadata = np.zeros((num_users, 3))
user_metadata[:, 0] = np.arange(1, num_users + 1)
user_metadata[:, 1] = np.random.randint(18, 71, size=num_users)
user_metadata[:, 2] = np.random.randint(0, 2, size=num_users)

print(f"Metadata shape: {user_metadata.shape}")
print(f"Sample metadata (first 5 users):")
print("User ID | Age | Gender")
for i in range(5):
    gender_label = "Male" if user_metadata[i, 2] == 1 else "Female"
    print(f"  {int(user_metadata[i, 0]):3d}   | {int(user_metadata[i, 1]):2d}  | {gender_label}")

print("\nIntroducing data quality issues...")

total_elements = fitness_data.size
nan_count = int(total_elements * 0.05)
nan_indices = np.random.choice(total_elements, nan_count, replace=False)
flat_data = fitness_data.flatten()
flat_data[nan_indices] = np.nan
fitness_data = flat_data.reshape(fitness_data.shape)

print(f"Inserted {nan_count} NaN values ({(nan_count/total_elements)*100:.1f}% of data)")

outlier_count = int(total_elements * 0.02)
outlier_indices = np.random.choice(total_elements, outlier_count, replace=False)

flat_data = fitness_data.flatten()
for idx in outlier_indices:
    metric_type = idx % num_metrics
    if metric_type == 0:
        flat_data[idx] = np.random.choice([500, 50000])
    elif metric_type == 1:
        flat_data[idx] = np.random.choice([500, 8000])
    elif metric_type == 2:
        flat_data[idx] = np.random.choice([5, 400])
    else:
        flat_data[idx] = np.random.choice([30, 180])

fitness_data = flat_data.reshape(fitness_data.shape)
print(f"Inserted {outlier_count} outlier values ({(outlier_count/total_elements)*100:.1f}% of data)")

print(f"\nData preparation complete!")
print(f"Total data quality issues: {nan_count + outlier_count} ({((nan_count + outlier_count)/total_elements)*100:.1f}%)")

print("\n\n### PART B: DATA CLEANING & VALIDATION ###\n")
print("-" * 80)

def handle_missing(data):
    data_copy = data.copy()

    for metric in range(data_copy.shape[2]):
        metric_data = data_copy[:, :, metric]
        metric_mean = np.nanmean(metric_data)
        metric_data[np.isnan(metric_data)] = metric_mean
        data_copy[:, :, metric] = metric_data

    return data_copy

def remove_outliers(data, metric_index):
    data_copy = data.copy()
    metric_data = data_copy[:, :, metric_index].flatten()

    q1 = np.percentile(metric_data[~np.isnan(metric_data)], 25)
    q3 = np.percentile(metric_data[~np.isnan(metric_data)], 75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outlier_mask = (metric_data < lower_bound) | (metric_data > upper_bound)
    outlier_count = np.sum(outlier_mask & ~np.isnan(metric_data))

    median_value = np.nanmedian(metric_data)
    metric_data[outlier_mask] = median_value

    data_copy[:, :, metric_index] = metric_data.reshape(data_copy.shape[0], data_copy.shape[1])

    return data_copy, outlier_count, lower_bound, upper_bound

print("Starting data cleaning pipeline...\n")

fitness_data_original = fitness_data.copy()

initial_nan_count = np.sum(np.isnan(fitness_data))
print(f"Initial NaN count: {initial_nan_count}")

metric_names = ['Daily Steps', 'Calories', 'Active Minutes', 'Avg Heart Rate']

for metric_idx in range(num_metrics):
    fitness_data, outliers_removed, lower, upper = remove_outliers(fitness_data, metric_idx)
    print(f"\n{metric_names[metric_idx]}:")
    print(f"  Outliers removed: {outliers_removed}")
    print(f"  Valid range: [{lower:.2f}, {upper:.2f}]")

print("\n" + "-" * 80)
print("Handling missing values...")
fitness_data = handle_missing(fitness_data)

final_nan_count = np.sum(np.isnan(fitness_data))
print(f"\nFinal NaN count: {final_nan_count}")

if final_nan_count == 0:
    print("✓ Data cleaning successful! No NaN values remain.")
else:
    print(f"⚠ Warning: {final_nan_count} NaN values still present.")

print(f"\nCleaned data statistics:")
for metric_idx, name in enumerate(metric_names):
    metric_data = fitness_data[:, :, metric_idx]
    print(f"{name}: Mean={metric_data.mean():.2f}, Std={metric_data.std():.2f}, "
          f"Min={metric_data.min():.2f}, Max={metric_data.max():.2f}")

print("\n\n### PART C: COMPREHENSIVE ANALYSIS ###\n")
print("=" * 80)

print("\n1. USER BEHAVIOR PATTERNS")
print("-" * 80)

user_avg_metrics = fitness_data.mean(axis=1)

print("Average metrics per user (showing first 5 users):")
print("User | Steps   | Calories | Active Min | Heart Rate")
for i in range(5):
    print(f"  {int(user_metadata[i, 0]):2d} | {user_avg_metrics[i, 0]:7.1f} | "
          f"{user_avg_metrics[i, 1]:8.1f} | {user_avg_metrics[i, 2]:10.1f} | "
          f"{user_avg_metrics[i, 3]:10.1f}")

print("\nIdentifying top 10 most active users...")

z_scores = np.zeros_like(user_avg_metrics)
for metric in range(num_metrics):
    mean = user_avg_metrics[:, metric].mean()
    std = user_avg_metrics[:, metric].std()
    z_scores[:, metric] = (user_avg_metrics[:, metric] - mean) / std

combined_z_score = z_scores.sum(axis=1)
top_10_indices = np.argsort(combined_z_score)[-10:][::-1]

print("\nTop 10 Most Active Users:")
print("Rank | User ID | Combined Z-Score | Steps   | Calories")
for rank, idx in enumerate(top_10_indices, 1):
    user_id = int(user_metadata[idx, 0])
    print(f" {rank:2d}  |   {user_id:3d}   | {combined_z_score[idx]:15.2f} | "
          f"{user_avg_metrics[idx, 0]:7.1f} | {user_avg_metrics[idx, 1]:8.1f}")

print("\nFinding most consistent users...")
user_std_steps = fitness_data[:, :, 0].std(axis=1)
most_consistent_indices = np.argsort(user_std_steps)[:10]

print("\nTop 10 Most Consistent Users (by steps):")
print("Rank | User ID | Std Dev | Avg Steps")
for rank, idx in enumerate(most_consistent_indices, 1):
    user_id = int(user_metadata[idx, 0])
    print(f" {rank:2d}  |   {user_id:3d}   | {user_std_steps[idx]:7.2f} | {user_avg_metrics[idx, 0]:9.1f}")

print("\nClassifying users by activity level...")
steps_25th = np.percentile(user_avg_metrics[:, 0], 25)
steps_75th = np.percentile(user_avg_metrics[:, 0], 75)

low_activity = np.sum(user_avg_metrics[:, 0] < steps_25th)
medium_activity = np.sum((user_avg_metrics[:, 0] >= steps_25th) &
                         (user_avg_metrics[:, 0] <= steps_75th))
high_activity = np.sum(user_avg_metrics[:, 0] > steps_75th)

print(f"\nActivity Level Distribution:")
print(f"  Low Activity (< {steps_25th:.0f} steps): {low_activity} users ({low_activity}%)")
print(f"  Medium Activity ({steps_25th:.0f}-{steps_75th:.0f} steps): {medium_activity} users ({medium_activity}%)")
print(f"  High Activity (> {steps_75th:.0f} steps): {high_activity} users ({high_activity}%)")

print("\n\n2. TEMPORAL TRENDS")
print("-" * 80)

print("Computing 7-day rolling averages...")

population_daily_avg = fitness_data.mean(axis=0)

rolling_avg_7day = np.zeros((num_days - 6, num_metrics))
for metric in range(num_metrics):
    rolling_avg_7day[:, metric] = np.convolve(population_daily_avg[:, metric],
                                               np.ones(7)/7, mode='valid')

print(f"7-day rolling average shape: {rolling_avg_7day.shape}")
print(f"First 5 days (Steps): {rolling_avg_7day[:5, 0]}")

print("\nAnalyzing weekly patterns...")
day_of_week_avg = np.zeros((7, num_metrics))

for day_idx in range(7):
    days_in_category = population_daily_avg[day_idx::7, :]
    day_of_week_avg[day_idx, :] = days_in_category.mean(axis=0)

day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
print("\nAverage Activity by Day of Week:")
print("Day    | Steps   | Calories | Active Min | Heart Rate")
for day_idx, day_name in enumerate(day_names):
    print(f"{day_name}    | {day_of_week_avg[day_idx, 0]:7.1f} | "
          f"{day_of_week_avg[day_idx, 1]:8.1f} | {day_of_week_avg[day_idx, 2]:10.1f} | "
          f"{day_of_week_avg[day_idx, 3]:10.1f}")

print("\nAnalyzing activity trends over time...")

first_30_days = population_daily_avg[:30, :].mean(axis=0)
last_30_days = population_daily_avg[-30:, :].mean(axis=0)

print("\nFirst 30 Days vs Last 30 Days:")
for metric_idx, name in enumerate(metric_names):
    change = last_30_days[metric_idx] - first_30_days[metric_idx]
    pct_change = (change / first_30_days[metric_idx]) * 100
    trend = "↑" if change > 0 else "↓"
    print(f"{name}: {first_30_days[metric_idx]:.1f} → {last_30_days[metric_idx]:.1f} "
          f"({trend} {abs(pct_change):.1f}%)")

print("\nMonth-over-Month Growth Rates:")
month1_avg = population_daily_avg[:30, :].mean(axis=0)
month2_avg = population_daily_avg[30:60, :].mean(axis=0)
month3_avg = population_daily_avg[60:90, :].mean(axis=0)

growth_m1_m2 = ((month2_avg - month1_avg) / month1_avg) * 100
growth_m2_m3 = ((month3_avg - month2_avg) / month2_avg) * 100

print("\nMonth 1 → Month 2:")
for metric_idx, name in enumerate(metric_names):
    print(f"  {name}: {growth_m1_m2[metric_idx]:+.2f}%")

print("\nMonth 2 → Month 3:")
for metric_idx, name in enumerate(metric_names):
    print(f"  {name}: {growth_m2_m3[metric_idx]:+.2f}%")

print("\n\n3. CORRELATIONS & INSIGHTS")
print("-" * 80)

print("Computing correlation matrix...")
metrics_flat = fitness_data.reshape(-1, num_metrics)
correlation_matrix = np.corrcoef(metrics_flat.T)

print("\nCorrelation Matrix (Metrics):")
print("           Steps  Calories  Active  Heart Rate")
for idx, name in enumerate(metric_names):
    print(f"{name:12s} ", end="")
    for corr_val in correlation_matrix[idx, :]:
        print(f"{corr_val:7.3f}  ", end="")
    print()

print("\nAnalyzing age vs activity relationship...")
age_groups = [(18, 30), (31, 45), (46, 60), (61, 70)]
age_activity = np.zeros((len(age_groups), num_metrics))

for idx, (min_age, max_age) in enumerate(age_groups):
    age_mask = (user_metadata[:, 1] >= min_age) & (user_metadata[:, 1] <= max_age)
    if np.sum(age_mask) > 0:
        age_activity[idx, :] = user_avg_metrics[age_mask, :].mean(axis=0)

print("\nAverage Activity by Age Group:")
print("Age Group  | Steps   | Calories | Active Min")
for idx, (min_age, max_age) in enumerate(age_groups):
    print(f"{min_age}-{max_age}      | {age_activity[idx, 0]:7.1f} | "
          f"{age_activity[idx, 1]:8.1f} | {age_activity[idx, 2]:10.1f}")

print("\nGender-based activity comparison...")
female_mask = user_metadata[:, 2] == 0
male_mask = user_metadata[:, 2] == 1

female_avg = user_avg_metrics[female_mask, :].mean(axis=0)
male_avg = user_avg_metrics[male_mask, :].mean(axis=0)

print("\nAverage Activity by Gender:")
print("Gender | Steps   | Calories | Active Min | Heart Rate")
print(f"Female | {female_avg[0]:7.1f} | {female_avg[1]:8.1f} | "
      f"{female_avg[2]:10.1f} | {female_avg[3]:10.1f}")
print(f"Male   | {male_avg[0]:7.1f} | {male_avg[1]:8.1f} | "
      f"{male_avg[2]:10.1f} | {male_avg[3]:10.1f}")

print("\nCalculating Health Score...")
steps_normalized = (user_avg_metrics[:, 0] - user_avg_metrics[:, 0].min()) / \
                   (user_avg_metrics[:, 0].max() - user_avg_metrics[:, 0].min()) * 100
calories_normalized = (user_avg_metrics[:, 1] - user_avg_metrics[:, 1].min()) / \
                      (user_avg_metrics[:, 1].max() - user_avg_metrics[:, 1].min()) * 100
active_normalized = (user_avg_metrics[:, 2] - user_avg_metrics[:, 2].min()) / \
                    (user_avg_metrics[:, 2].max() - user_avg_metrics[:, 2].min()) * 100

health_score = (steps_normalized * 0.4 + calories_normalized * 0.3 + active_normalized * 0.3)

top_5_health = np.argsort(health_score)[-5:][::-1]
print("\nTop 5 Users by Health Score:")
print("Rank | User ID | Health Score")
for rank, idx in enumerate(top_5_health, 1):
    user_id = int(user_metadata[idx, 0])
    print(f" {rank}   |   {user_id:3d}   | {health_score[idx]:12.2f}")

print("\n\n4. GOAL ACHIEVEMENT")
print("-" * 80)

GOAL_STEPS = 8000
GOAL_CALORIES = 2000
GOAL_ACTIVE_MIN = 60

print(f"Daily Goals: {GOAL_STEPS} steps, {GOAL_CALORIES} calories, {GOAL_ACTIVE_MIN} active minutes")

steps_goal_met = (fitness_data[:, :, 0] >= GOAL_STEPS).sum(axis=1) / num_days * 100
calories_goal_met = (fitness_data[:, :, 1] >= GOAL_CALORIES).sum(axis=1) / num_days * 100
active_goal_met = (fitness_data[:, :, 2] >= GOAL_ACTIVE_MIN).sum(axis=1) / num_days * 100

all_goals_met = ((fitness_data[:, :, 0] >= GOAL_STEPS) &
                 (fitness_data[:, :, 1] >= GOAL_CALORIES) &
                 (fitness_data[:, :, 2] >= GOAL_ACTIVE_MIN)).sum(axis=1) / num_days * 100

print("\nGoal Achievement Summary:")
print(f"Average Steps Goal Achievement: {steps_goal_met.mean():.1f}%")
print(f"Average Calories Goal Achievement: {calories_goal_met.mean():.1f}%")
print(f"Average Active Minutes Goal Achievement: {active_goal_met.mean():.1f}%")
print(f"Average All Goals Met: {all_goals_met.mean():.1f}%")

consistent_achievers = np.where(all_goals_met > 80)[0]
print(f"\nUsers who meet ALL goals >80% of the time: {len(consistent_achievers)} users")

if len(consistent_achievers) > 0:
    print("\nTop Consistent Goal Achievers:")
    print("User ID | Achievement Rate | Avg Steps | Avg Calories | Avg Active Min")
    for idx in consistent_achievers[:10]:
        user_id = int(user_metadata[idx, 0])
        print(f"  {user_id:3d}   | {all_goals_met[idx]:15.1f}% | "
              f"{user_avg_metrics[idx, 0]:9.1f} | {user_avg_metrics[idx, 1]:12.1f} | "
              f"{user_avg_metrics[idx, 2]:14.1f}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
