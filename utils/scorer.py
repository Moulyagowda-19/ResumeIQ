def calculate_ats_score(data):
    """
    Calculates ATS score based on extracted data and returns score + breakdown.
    """
    score = 0
    feedback = []
    breakdown = {
        "Contact Info": 0,
        "Skills": 0,
        "Experience": 0,
        "Projects": 0,
        "Education": 0,
        "Formatting": 0,
        "Keywords": 0
    }
    
    # 1. Contact Info (5 points)
    if data.get('email') and data.get('phone'):
        score += 5
        breakdown["Contact Info"] = 5
    elif data.get('email') or data.get('phone'):
        score += 3
        breakdown["Contact Info"] = 3
        feedback.append("Include both email and phone number.")
    else:
        feedback.append("Contact information is missing (Email/Phone).")

    # 2. Skills Presence (20 points)
    skills_count = len(data.get('skills', []))
    if skills_count >= 10:
        score += 20
        breakdown["Skills"] = 20
    elif skills_count >= 5:
        score += 10
        breakdown["Skills"] = 10
        feedback.append("Add more technical skills to pass ATS filters.")
    else:
        score += 5
        breakdown["Skills"] = 5
        feedback.append("Resume has very few detected skills.")

    # 3. Experience Section (15 points)
    if data.get('experience'):
        score += 15
        breakdown["Experience"] = 15
    else:
        feedback.append("Experience section not detected or unclear.")

    # 4. Projects Section (15 points)
    if data.get('projects'):
        score += 15
        breakdown["Projects"] = 15
    else:
        feedback.append("Projects section missing. Critical for tech roles.")

    # 5. Education Section (10 points - implicit mostly, but checking presence)
    if data.get('education'):
        score += 10
        breakdown["Education"] = 10
    else:
        feedback.append("Education section missing.")

    # 6. Formatting & Readability (10 points - heuristic)
    text_len = len(data.get('text', ''))
    if 500 < text_len < 5000:
        score += 10
        breakdown["Formatting"] = 10
    else:
        score += 5
        breakdown["Formatting"] = 5
        feedback.append("Resume might be too short or too long.")

    # 7. Keyword Match / Role relevance (25 points)
    if skills_count > 0:
        score += 25
        breakdown["Keywords"] = 25
    
    return min(100, score), breakdown, feedback
