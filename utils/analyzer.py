import re

def parse_resume(text):
    """
    Parses resume text to extract key sections.
    """
    text = text.lower()
    
    data = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": "education" in text or "university" in text or "degree" in text,
        "experience": "experience" in text or "employment" in text or "work history" in text,
        "projects": "projects" in text or "portfolio" in text or "github" in text,
        "summary": "summary" in text or "profile" in text or "objective" in text,
        "certifications": "certifications" in text or "certificates" in text,
        "text": text # Store full text for further analysis if needed
    }
    return data

def extract_name(text):
    # Improved regex for name extraction - looks for capitalized words at start
    # Note: highly unreliable on raw text without layout info, best guess
    # Trying to find 2-3 words at the beginning
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if lines:
        potential_name = lines[0]
        # Check if it looks like a name (no numbers, reasonable length)
        if len(potential_name.split()) <= 4 and all(c.isalpha() or c.isspace() for c in potential_name):
            return potential_name.title()
    return "Candidate"

def extract_email(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(email_pattern, text)
    return match.group(0) if match else None

def extract_phone(text):
    # Regex to handle various phone formats
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}'
    match = re.search(phone_pattern, text)
    return match.group(0) if match else None

def extract_skills(text):
    # Common tech skills dictionary - can be expanded
    common_skills = [
        "python", "java", "javascript", "react", "angular", "vue", "html", "css",
        "sql", "nosql", "mongodb", "postgresql", "mysql", "flask", "django",
        "node.js", "express", "aws", "azure", "docker", "kubernetes", "git",
        "c++", "c#", "ruby", "php", "swift", "kotlin", "go", "rust",
        "machine learning", "deep learning", "nlp", "pandas", "numpy", "scikit-learn",
        "tensorflow", "pytorch", "tableau", "power bi", "excel", "communication",
        "leadership", "teamwork", "agile", "scrum", "ci/cd", "rest api", "graphql",
        "typescript", "next.js", "redux", "jest", "cypress", "selenium"
    ]
    
    found_skills = []
    for skill in common_skills:
        # Check for skill existence with boundaries
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found_skills.append(skill.upper())
    
    return list(set(found_skills))

def analyze_skill_gap(found_skills, target_role):
    """
    Analyzes missing skills based on target role.
    """
    role_skills = {
        "Frontend Developer": ["HTML", "CSS", "JAVASCRIPT", "REACT", "ANGULAR", "VUE", "GIT", "TYPESCRIPT", "NEXT.JS"],
        "Backend Developer": ["PYTHON", "JAVA", "NODE.JS", "SQL", "MONGODB", "DOCKER", "API", "AWS", "REDIS", "POSTGRESQL"],
        "Full Stack Developer": ["HTML", "CSS", "JAVASCRIPT", "REACT", "NODE.JS", "PYTHON", "SQL", "GIT", "DOCKER", "AWS"],
        "Software Engineer": ["JAVA", "PYTHON", "C++", "DATA STRUCTURES", "ALGORITHMS", "GIT", "SYSTEM DESIGN", "SQL"],
        "Web Developer": ["HTML", "CSS", "JAVASCRIPT", "PHP", "WORDPRESS", "SEO", "BOOTSTRAP", "JQUERY"],
        "Mobile App Developer": ["SWIFT", "KOTLIN", "REACT NATIVE", "FLUTTER", "IOS", "ANDROID", "DART", "FIREBASE"],
        "Data Scientist": ["PYTHON", "SQL", "PANDAS", "NUMPY", "SCIKIT-LEARN", "TENSORFLOW", "TABLEAU", "POWER BI", "STATISTICS"],
        "Machine Learning Engineer": ["PYTHON", "TENSORFLOW", "PYTORCH", "SCIKIT-LEARN", "MLOPS", "DATA MODELING", "DEEP LEARNING"],
        "AI Engineer": ["PYTHON", "DEEP LEARNING", "NLP", "COMPUTER VISION", "TENSORFLOW", "PYTORCH", "KERAS", "OPENCV"],
        "DevOps Engineer": ["AWS", "DOCKER", "KUBERNETES", "CI/CD", "LINUX", "BASH", "PYTHON", "TERRAFORM", "ANSIBLE"],
        "Cloud Engineer": ["AWS", "AZURE", "GOOGLE CLOUD", "TERRAFORM", "DOCKER", "KUBERNETES", "LINUX", "NETWORKING"],
        "Site Reliability Engineer (SRE)": ["LINUX", "PYTHON", "GO", "ANSIBLE", "TERRAFORM", "MONITORING", "CI/CD", "KUBERNETES"],
        "Cybersecurity Analyst": ["NETWORK SECURITY", "LINUX", "PYTHON", "SIEM", "FIREWALLS", "WIRESHARK", "RISK ASSESSMENT"],
        "Penetration Tester": ["KALI LINUX", "METASPLOIT", "BURP SUITE", "PYTHON", "BASH", "NETWORK SECURITY", "ETHICAL HACKING"],
        "Blockchain Developer": ["SOLIDITY", "ETHEREUM", "SMART CONTRACTS", "WEB3.JS", "CRYPTOGRAPHY", "RUST", "GO"],
        "Embedded Systems Engineer": ["C", "C++", "MICROCONTROLLERS", "RTOS", "PCB DESIGN", "IOT", "FIRMWARE"],
        "Game Developer": ["C++", "C#", "UNITY", "UNREAL ENGINE", "3D MATH", "GRAPHICS PROGRAMMING", "OPENGL", "DIRECTX"],
        "Database Administrator (DBA)": ["SQL", "POSTGRESQL", "MYSQL", "ORACLE", "PERFORMANCE TUNING", "BACKUP/RECOVERY", "NOSQL"],
        "Data Engineer": ["PYTHON", "SQL", "SPARK", "HADOOP", "KAFKA", "ETL", "WAREHOUSING", "AIRFLOW", "AWS"],
        "QA / Automation Test Engineer": ["SELENIUM", "PYTHON", "JAVA", "JIRA", "CYPRESS", "TESTNG", "JUNIT", "API TESTING"],
        "Network Engineer": ["CISCO", "TCP/IP", "ROUTING", "SWITCHING", "VPN", "FIREWALLS", "WIRESHARK", "BGP", "OSPF"],
        "Systems Engineer": ["LINUX", "WINDOWS SERVER", "VIRTUALIZATION", "VMWARE", "BASH", "POWERSHELL", "ACTIVE DIRECTORY"]
    }
    
    target_skills = role_skills.get(target_role, [])
    # Case insensitive comparison
    found_skills_upper = [s.upper() for s in found_skills]
    missing = [skill for skill in target_skills if skill not in found_skills_upper]
    
    return missing

def suggest_bullet_improvements(line):
    # Very basic "weak verb" replacement suggestions
    weak_verbs = {
        "worked on": "Managed",
        "helped": "Assisted in",
        "made": "Developed",
        "did": "Executed",
        "responsible for": "Spearheaded",
        "handled": "Orchestrated",
        "utilized": "Leveraged"
    }
    
    for weak, strong in weak_verbs.items():
        if weak in line.lower():
            return f"Consider replacing '{weak}' with '{strong}' to make it impactful."
    return None
