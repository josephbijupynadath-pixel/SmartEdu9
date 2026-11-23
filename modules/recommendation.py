
def recommend_resources(subject, marks, attendance):
    """
    Recommend learning resources based on student
    academic performance and attendance.
    """

    recommendations = []

    if marks < 50:
        recommendations.append(
            "Start with basic concepts and beginner tutorials."
        )
        recommendations.append(
            "Practice simple exercises regularly."
        )

    elif marks < 70:
        recommendations.append(
            "Revise important topics and practice exercises."
        )
        recommendations.append(
            "Watch intermediate-level video tutorials."
        )

    else:
        recommendations.append(
            "Explore advanced topics in your subject."
        )
        recommendations.append(
            "Practice challenging projects and questions."
        )

    if attendance < 75:
        recommendations.append(
            "Improve class attendance and review missed lessons."
        )

    subject_resources = {
        "Database": [
            "Study SQL fundamentals.",
            "Practice database queries."
        ],
        "Python": [
            "Practice Python programming.",
            "Build small Python projects."
        ],
        "Mathematics": [
            "Practice mathematical problems.",
            "Review important formulas."
        ],
        "Computer Networks": [
            "Study networking fundamentals.",
            "Practice network configuration."
        ]
    }

    recommendations.extend(
        subject_resources.get(subject, [
            "Read subject-related textbooks.",
            "Practice additional subject exercises."
        ])
    )

    return recommendations
