import numpy as np

np.random.seed(42)


daily_temps = np.random.uniform(-10, 40, (5, 365))

print(f"Array Shape: {daily_temps.shape}")
print(f"Number of Dimensions: {daily_temps.ndim}")
print(f"Data Type: {daily_temps.dtype}")
print(f"Total Elements: {daily_temps.size}")
print(f"\nSample data (first 3 days for all cities):")
print(daily_temps[:, :3])

print("\n2. Creating Sales Matrix")
print("-" * 70)

monthly_sales = np.random.randint(2000, 5001, (12, 4))

print(f"Sales Matrix Shape: {monthly_sales.shape}")
print(f"Sales Data:\n{monthly_sales}")

print("\n3. Special Arrays")
print("-" * 70)

identity_5x5 = np.eye(5)
print("Identity Matrix (5x5):")
print(identity_5x5)

linear_space = np.linspace(0, 100, 50)
print(f"\nLinear Space Array (50 values from 0 to 100):")
print(f"First 5 values: {linear_space[:5]}")
print(f"Last 5 values: {linear_space[-5:]}")


print("1. Basic Slicing")
print("-" * 70)


jan_temps = daily_temps[:, 0:31]
print(f"January Temperature Data Shape: {jan_temps.shape}")

summer_temps = daily_temps[:, 152:243]
print(f"Summer Temperature Data Shape: {summer_temps.shape}")

weekend_temps = daily_temps[:, 4::7]
print(f"Weekend Temperature Data Shape: {weekend_temps.shape}")

print("\n2. Boolean Indexing")
print("-" * 70)

extreme_heat_days = np.any(daily_temps > 35, axis=0)
days_with_extreme_heat = np.where(extreme_heat_days)[0]
print(f"Number of days with temperature > 35°C: {len(days_with_extreme_heat)}")

all_cities_freezing = np.where(np.all(daily_temps < 0, axis=0))[0]
print(f"Days when all cities were below 0°C: {len(all_cities_freezing)}")

comfortable_temp_days = np.all((daily_temps >= 15) & (daily_temps <= 25), axis=0)
num_comfortable_days = np.sum(comfortable_temp_days)
print(f"Days when all cities had comfortable temps (15-25°C): {num_comfortable_days}")

original_extreme_cold = np.sum(daily_temps < -5)
daily_temps[daily_temps < -5] = -5
print(f"Data cleaning: {original_extreme_cold} values below -5°C were adjusted to -5°C")

print("\n3. Fancy Indexing")


selected_days = [0, 100, 200, 300, 364]
specific_day_temps = daily_temps[:, selected_days]
print(f"Temperatures on days {selected_days}:")
print(specific_day_temps)

quarter_splits = np.array_split(daily_temps, 4, axis=1)
quarterly_avg_temps = np.array([quarter.mean(axis=1) for quarter in quarter_splits]).T

print(f"\nQuarterly Average Temperatures (Cities x Quarters):")
print(quarterly_avg_temps)

yearly_avg_by_city = daily_temps.mean(axis=1)
city_ranking = np.argsort(yearly_avg_by_city)[::-1]
temps_sorted_by_warmth = daily_temps[city_ranking]

print(f"\nCities ranked by annual average temperature:")
for rank, city_idx in enumerate(city_ranking, 1):
    print(f"  Rank {rank}: City {city_idx + 1} with avg {yearly_avg_by_city[city_idx]:.2f}°C")


print("\n\n### PART C: MATHEMATICAL OPERATIONS & STATISTICS ###\n")

print("1. Temperature Statistical Analysis")
print("-" * 70)

city_mean_temps = np.mean(daily_temps, axis=1)
city_std_temps = np.std(daily_temps, axis=1)

print("Temperature Statistics by City:")
for city_num in range(5):
    print(f"  City {city_num + 1}: Mean = {city_mean_temps[city_num]:.2f}°C, "
          f"Std Dev = {city_std_temps[city_num]:.2f}°C")

coldest_day_indices = np.argmin(daily_temps, axis=1)
coldest_temps = daily_temps[np.arange(daily_temps.shape[0]), coldest_day_indices]

hottest_day_indices = np.argmax(daily_temps, axis=1)
hottest_temps = daily_temps[np.arange(daily_temps.shape[0]), hottest_day_indices]

print("\nExtreme Temperatures by City:")
for city_num in range(5):
    print(f"  City {city_num + 1}:")
    print(f"    Coldest: {coldest_temps[city_num]:.2f}°C on day {coldest_day_indices[city_num] + 1}")
    print(f"    Hottest: {hottest_temps[city_num]:.2f}°C on day {hottest_day_indices[city_num] + 1}")

temp_range_by_city = hottest_temps - coldest_temps
print("\nTemperature Range (Max - Min) by City:")
for city_num, temp_range in enumerate(temp_range_by_city):
    print(f"  City {city_num + 1}: {temp_range:.2f}°C")

city_correlation = np.corrcoef(daily_temps)
print("\nCorrelation Matrix Between Cities:")
print(city_correlation)

print("\n2. Sales Data Analysis")
print("-" * 70)

category_totals = monthly_sales.sum(axis=0)
print("Total Annual Sales by Product Category:")
for cat_num, total in enumerate(category_totals, 1):
    print(f"  Category {cat_num}: ${total:,}")

category_avg_monthly = monthly_sales.mean(axis=1)
print("\nAverage Sales Across All Categories by Month:")
month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
for month_idx, avg_sales in enumerate(category_avg_monthly):
    print(f"  {month_labels[month_idx]}: ${avg_sales:.2f}")

monthly_totals = monthly_sales.sum(axis=1)
top_month_idx = monthly_totals.argmax()
print(f"\nBest Performing Month: {month_labels[top_month_idx]} "
      f"(Total: ${monthly_totals[top_month_idx]:,})")

top_category_idx = category_totals.argmax()
print(f"Best Performing Product Category: Category {top_category_idx + 1} "
      f"(Total: ${category_totals[top_category_idx]:,})")

print("\n3. Advanced Computations")
print("-" * 70)

print("Computing 7-day moving averages...")
window_size = 7
moving_avg_temps = np.array([
    np.convolve(daily_temps[city], np.ones(window_size) / window_size, mode="valid")
    for city in range(daily_temps.shape[0])
])
print(f"Moving average shape: {moving_avg_temps.shape}")
print(f"Sample (City 1, first 5 days): {moving_avg_temps[0, :5]}")

z_normalized_temps = (daily_temps - daily_temps.mean(axis=1, keepdims=True)) / \
                     daily_temps.std(axis=1, keepdims=True)

print("\nZ-Score Statistics (should be ~0 mean, ~1 std):")
for city_num in range(5):
    print(f"  City {city_num + 1}: Mean = {z_normalized_temps[city_num].mean():.6f}, "
          f"Std = {z_normalized_temps[city_num].std():.6f}")

percentile_25 = np.percentile(daily_temps, 25, axis=1)
percentile_50 = np.percentile(daily_temps, 50, axis=1)
percentile_75 = np.percentile(daily_temps, 75, axis=1)

print("\nTemperature Percentiles by City:")
for city_num in range(5):
    print(f"  City {city_num + 1}:")
    print(f"    25th: {percentile_25[city_num]:.2f}°C")
    print(f"    50th: {percentile_50[city_num]:.2f}°C (Median)")
    print(f"    75th: {percentile_75[city_num]:.2f}°C")
    print(f"    IQR: {percentile_75[city_num] - percentile_25[city_num]:.2f}°C")



