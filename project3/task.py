import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("student_performance.csv")

sns.set_theme()

# ---------------- TASK 1 ----------------

# Line Plot: Study Hours vs Current GPA
df_sorted = df.sort_values("Study_Hours_Per_Week")
plt.figure(figsize=(8,5))
plt.plot(df_sorted["Study_Hours_Per_Week"], df_sorted["Current_GPA"], color="blue")
plt.title("Study Hours vs Current GPA")
plt.xlabel("Study Hours Per Week")
plt.ylabel("Current GPA")
plt.grid()
plt.show()

# Scatter Plot: Attendance vs Final Average
plt.figure(figsize=(8,5))
majors = df["Major"].unique()
for m in majors:
    temp = df[df["Major"] == m]
    plt.scatter(temp["Attendance_Rate"], temp["Final_Average"], alpha=0.6)
plt.title("Attendance vs Final Average")
plt.xlabel("Attendance Rate")
plt.ylabel("Final Average")
plt.legend(majors)
plt.show()

# Bar Chart: Average current GPA by Major
avg_gpa = df.groupby("Major")["Current_GPA"].mean().sort_values()
plt.figure(figsize=(8,6))
plt.barh(avg_gpa.index, avg_gpa.values)
for i, v in enumerate(avg_gpa.values):
    plt.text(v, i, str(round(v,2)))
plt.title("Average Current GPA by Major")
plt.xlabel("GPA")
plt.tight_layout()
plt.show()

# Histogram of Current GPA
plt.figure(figsize=(8,5))
plt.hist(df["Current_GPA"], bins=25, edgecolor="black")
plt.axvline(df["Current_GPA"].mean(), color="red")
plt.axvline(df["Current_GPA"].median(), color="green")
plt.title("Current GPA Distribution")
plt.xlabel("Current GPA")
plt.ylabel("Count")
plt.show()

# Boxplot of 5 course scores
courses = ["Mathematics_Score","Programming_Score","Statistics_Score","English_Score","Science_Score"]
plt.figure(figsize=(10,6))
plt.boxplot(df[courses].values, labels=courses)
plt.title("Course Score Comparison")
plt.xticks(rotation=45)
plt.show()

# ---------------- Subplots ----------------
fig = plt.figure(figsize=(12,10))

plt.subplot(2,2,1)
plt.hist(df["Current_GPA"], bins=25, edgecolor="black")
plt.title("Current GPA Distribution")

plt.subplot(2,2,2)
plt.scatter(df["Study_Hours_Per_Week"], df["Current_GPA"], alpha=0.6)
plt.title("Study Hours vs GPA")

avg_scores_year = df.groupby("Year")[courses].mean().mean(axis=1)
plt.subplot(2,2,3)
plt.bar(avg_scores_year.index.astype(str), avg_scores_year.values)
plt.title("Average Course Score by Year")

plt.subplot(2,2,4)
plt.hist(df["Attendance_Rate"], bins=25, edgecolor="black")
plt.title("Attendance Rate Distribution")

plt.tight_layout()
plt.show()

# Custom Plot
plt.figure(figsize=(10,6))
plt.scatter(df["Study_Hours_Per_Week"], df["Current_GPA"], color="purple", s=30)
plt.title("Study Hours vs GPA (Custom)")
plt.xlabel("Study Hours Per Week")
plt.ylabel("Current GPA")
m = df["Study_Hours_Per_Week"].mean()
g = df["Current_GPA"].mean()
plt.annotate("Mean Hours", (m, g))
plt.grid()
plt.show()

# ---------------- TASK 2 ----------------

sns.histplot(df, x="Current_GPA", hue="Gender", kde=True)
plt.title("GPA Distribution by Gender")
plt.show()

sns.violinplot(data=df, x="Major", y="Final_Average", palette="Set2", inner="points")
plt.xticks(rotation=45)
plt.title("Final Average Across Majors")
plt.show()

sns.boxplot(data=df, x="Academic_Status", y="Study_Hours_Per_Week")
sns.swarmplot(data=df, x="Academic_Status", y="Study_Hours_Per_Week", color="black", size=3)
plt.title("Study Hours by Academic Status")
plt.show()

corr = df.corr(numeric_only=True)
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()

sns.pairplot(df[[
    "Current_GPA",
    "Study_Hours_Per_Week",
    "Attendance_Rate",
    "Sleep_Hours",
    "Previous_GPA",
    "Gender"
]], hue="Gender")
plt.show()

sns.regplot(data=df, x="Study_Hours_Per_Week", y="Current_GPA")
plt.title("Study Hours vs GPA")
plt.show()

sns.countplot(data=df, x="Major")
plt.xticks(rotation=45)
plt.title("Student Count by Major")
plt.show()

sns.barplot(data=df, x="Major", y="Current_GPA", hue="Year")
plt.xticks(rotation=45)
plt.title("GPA by Major and Year")
plt.show()

g = sns.FacetGrid(df, row="Gender", col="Has_Scholarship")
g.map_dataframe(sns.scatterplot, x="Attendance_Rate", y="Current_GPA")
plt.show()

# ---------------- TASK 3 ----------------

print("RQ1: What factors most strongly predict GPA?")
print("RQ2: How do study habits differ across performance levels?")
print("RQ3: Do scholarships or part-time work affect performance?")
print("RQ4: Are there differences between majors and years?")

plt.figure(figsize=(8,5))
sns.histplot(df["Current_GPA"], kde=True)
plt.title("Overall GPA Distribution")
plt.show()

plt.figure(figsize=(8,5))
sns.countplot(data=df, x="Gender")
plt.title("Gender Distribution")
plt.show()

plt.figure(figsize=(8,5))
sns.regplot(data=df, x="Study_Hours_Per_Week", y="Current_GPA")
plt.title("Study Hours and GPA")
plt.show()

plt.figure(figsize=(8,5))
sns.regplot(data=df, x="Attendance_Rate", y="Final_Average")
plt.title("Attendance and Final Grades")
plt.show()

plt.figure(figsize=(8,5))
sns.regplot(data=df, x="Sleep_Hours", y="Current_GPA")
plt.title("Sleep Hours and GPA")
plt.show()

plt.figure(figsize=(8,5))
sns.scatterplot(data=df, x="Previous_GPA", y="Current_GPA", hue="Major")
plt.title("Previous vs Current GPA")
plt.show()

plt.figure(figsize=(10,6))
sns.boxplot(data=df, x="Major", y="Current_GPA")
plt.xticks(rotation=45)
plt.title("GPA Differences Across Majors")
plt.show()

plt.figure(figsize=(8,5))
sns.barplot(data=df, x="Year", y="Current_GPA")
plt.title("GPA by Year Level")
plt.show()

plt.figure(figsize=(8,5))
sns.boxplot(data=df, x="Has_Scholarship", y="Current_GPA")
plt.title("Scholarship vs GPA")
plt.show()

plt.figure(figsize=(8,5))
sns.boxplot(data=df, x="Part_Time_Work_Hours", y="Current_GPA")
plt.title("Part-Time Work vs GPA")
plt.show()
