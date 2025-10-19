students = {
    "S001": {"name": "Giorgi Beridze", "scores": [88, 92, 79, 95], "attendance": 28},
    "S002": {"name": "Davit Kvaratskhelia", "scores": [75, 81, 74, 80], "attendance": 26},
    "S003": {"name": "Nino Gelashvili", "scores": [90, 85, 88, 91], "attendance": 30},
    "S004": {"name": "Tamar Lomidze", "scores": [67, 70, 65, 72], "attendance": 22},
    "S005": {"name": "Levan Chavchavadze", "scores": [95, 93, 97, 92], "attendance": 29},
    "S006": {"name": "Mariam Jorjadze", "scores": [80, 78, 83, 77], "attendance": 27},
    "S007": {"name": "Aleksandre Kipiani", "scores": [60, 68, 70, 65], "attendance": 19},
    "S008": {"name": "Salome Mchedlidze", "scores": [85, 87, 82, 89], "attendance": 30},
    "S009": {"name": "Nikoloz Tsereteli", "scores": [73, 76, 70, 75], "attendance": 25},
    "S010": {"name": "Murmani Akhaladze", "scores": [100, 99, 98, 97], "attendance": 29},
}

def calculate_average(scores: list) -> float:
    return round(sum(scores) / len(scores), 2)

def assign_grade(average: float) -> str:
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"

def check_eligibility(student_dict: dict, total_classes: int = 30) -> tuple:

    avg = calculate_average(student_dict["scores"])
    att = student_dict["attendance"]
    attendance_percentage = (att / total_classes) * 100

    if avg < 60:
        reason = f"not enough avg LOL ({avg})"
        return (False, reason)

    elif attendance_percentage < 75:
        reason = f"Insufficient attendance ({att}/{total_classes})"
        return (False, reason)

    else:
        return (True, "Passed")

def find_top_performers(students: dict, n: int = 5) -> list:
    student_avg = []
    for student_id, student_info in students.items():
        avg_score = calculate_average(student_info["scores"])
        student_avg.append((student_id, avg_score))

    student_avg.sort(key=lambda x: x[1], reverse=True)

    top_students = student_avg[0:n]
    return top_students

def generate_report(students: dict) -> dict:
    total_students = len(students)
    averages = [calculate_average(s["scores"]) for s in students.values()]
    attendance = [s["attendance"] for s in students.values()]
    passed = [check_eligibility(s)[0] for s in students.values()]

    return {
        "total_students": total_students,
        "passed_count": sum(passed),
        "failed_count": total_students - sum(passed),
        "class_average": round(sum(averages) / total_students, 2),
        "highest_score": max(averages),
        "lowest_score": min(averages),
        "average_attendance_rate": round(sum(attendance) / (total_students * 30) * 100, 2)
    }

if __name__ == "__main__":

    # 1. Find and display top 5 performers
    print("\n=== TOP 5 PERFORMERS ===")
    top_5 = find_top_performers(students, 5)
    for rank, (student_id, avg_score) in enumerate(top_5, 1):
        student_name = students[student_id]["name"]
        grade = assign_grade(avg_score)
        print(f"{rank}. {student_id} - {student_name}: {avg_score} ({grade})")

    # 2. Students who failed
    print("\n=== STUDENTS WHO FAILED ===")
    failed_students = []
    for student_id, student_info in students.items():
        passed, reason = check_eligibility(student_info)
        if not passed:
            failed_students.append((student_id, reason))

    if failed_students:
        for student_id, reason in failed_students:
            student_name = students[student_id]["name"]
            print(f"{student_id} - {reason}")
    else:
        print("No students failed!")

    # 3. Generate and display class summary report
    print("\n=== CLASS SUMMARY REPORT ===")
    print("-" * 50)
    report = generate_report(students)
    total = report["total_students"]
    passed = report["passed_count"]
    failed = report["failed_count"]
    print(f"Total Students: {total}")
    print(f"Passed: {passed} ({(passed/total)*100:.1f}%)")
    print(f"Failed: {failed} ({(failed/total)*100:.1f}%)")
    print(f"Class Average: {report['class_average']}")
    print(f"Highest Score: {report['highest_score']}")
    print(f"Lowest Score: {report['lowest_score']}")
    print(f"Average Attendance Rate: {report['average_attendance_rate']}%")

    # 4. Grade Distribution
    print("\n=== GRADE DISTRIBUTION ===")
    grades = [assign_grade(calculate_average(s["scores"])) for s in students.values()]
    dist = {g: grades.count(g) for g in sorted(set(grades))}
    for g, count in dist.items():
        print(f"{g}: {count} student{'s' if count > 1 else ''}")

    print("\n" + "=" * 50)
    print("END OF REPORT")
    print("=" * 50)