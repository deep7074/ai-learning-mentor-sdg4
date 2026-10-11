def engagement_indicator(profile):
    score = 0
    reasons = []

    attendance = float(profile.get("attendance", 75))
    study_hours = float(profile.get("study_hours", 8))
    pending = int(profile.get("pending", 1))
    quiz_score = float(profile.get("quiz_score", 60))

    if attendance < 60:
        score += 2
        reasons.append("Attendance is below 60%.")
    elif attendance < 75:
        score += 1
        reasons.append("Attendance could be improved.")

    if study_hours < 4:
        score += 2
        reasons.append("Weekly study time is quite low.")
    elif study_hours < 7:
        score += 1
        reasons.append("A little more regular study time may help.")

    if pending >= 5:
        score += 2
        reasons.append("Several assignments are pending.")
    elif pending >= 2:
        score += 1
        reasons.append("There are some pending assignments.")

    if quiz_score < 40:
        score += 2
        reasons.append("Recent quiz performance suggests more revision may help.")
    elif quiz_score < 60:
        score += 1
        reasons.append("Recent quiz performance could improve with practice.")

    if score >= 4:
        return "Needs attention", reasons
    if score >= 2:
        return "Watch", reasons
    return "Stable", reasons
