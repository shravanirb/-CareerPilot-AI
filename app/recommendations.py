# Career-specific skill recommendations and roadmaps

CAREER_SKILLS = {
    "Full Stack Developer": ["HTML & CSS", "JavaScript", "React", "Node.js", "REST APIs", "SQL", "Git & GitHub"],
    "Backend Developer": ["Python / Java", "SQL", "REST APIs", "Database Management", "Backend Frameworks", "Git & GitHub"],
    "Software Engineer": ["Data Structures & Algorithms", "Programming", "Object-Oriented Programming", "SQL", "Git & GitHub", "Software Development"],
    "Machine Learning Engineer": ["Python", "Statistics", "Machine Learning", "Deep Learning", "SQL", "Git & GitHub"],
    "Data Scientist": ["Python", "Statistics", "SQL", "Machine Learning", "Data Visualization", "Pandas & NumPy"],
    "Data Analyst": ["SQL", "Excel", "Python", "Statistics", "Power BI / Tableau", "Data Visualization"],
    "Cybersecurity Analyst": ["Networking", "Linux", "Cybersecurity Fundamentals", "Python", "Security Tools", "Threat Analysis"],
    "Cloud Engineer": ["Linux", "Networking", "Cloud Fundamentals", "AWS / Azure", "Docker", "DevOps"],
    "DevOps Engineer": ["Linux", "Git", "Docker", "CI/CD", "Cloud Computing", "Kubernetes"],
    "AI Engineer": ["Python", "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "MLOps"],
    "SOC Analyst": ["Networking", "SIEM Tools", "Incident Response", "Log Analysis", "Threat Intelligence", "Linux"],
    "Penetration Tester": ["Networking", "Linux", "Web Application Security", "Scripting", "Burp Suite / Metasploit", "OWASP"],
    "Business Analyst": ["Excel", "SQL", "Data Visualization", "Business Communication", "Requirements Gathering", "JIRA"],
    "IT Support Engineer": ["Networking", "Operating Systems", "Troubleshooting", "Active Directory", "Communication", "ITIL"],
    "Automation Engineer": ["Python", "Selenium / Cypress", "CI/CD", "API Testing", "Test Frameworks", "Git"],
    "Embedded Systems Engineer": ["C / C++", "Microcontrollers", "RTOS", "Electronics", "Communication Protocols", "Debugging"]
}

CAREER_ROADMAPS = {
    "Full Stack Developer": ["HTML, CSS & JavaScript Fundamentals", "Frontend Framework (React / Vue)", "Backend with Node.js or Python", "Database Design (SQL & NoSQL)", "REST APIs & Authentication", "Build a Full-Stack Project", "Deploy & Version Control"],
    "Backend Developer": ["Python / Java Fundamentals", "SQL & Database Design", "REST APIs & HTTP", "Backend Framework (Django / Spring)", "Authentication & Security", "Build a Backend Project", "Interview Preparation"],
    "Software Engineer": ["Programming Fundamentals", "Data Structures & Algorithms", "Object-Oriented Design", "Version Control (Git)", "System Design Basics", "Build Complex Projects", "Competitive Programming & Interviews"],
    "Machine Learning Engineer": ["Python & Mathematics", "Machine Learning Algorithms", "Deep Learning (TensorFlow / PyTorch)", "Model Deployment & MLOps", "APIs & Docker", "Build End-to-End ML Projects", "Interview Preparation"],
    "Data Scientist": ["Python & Statistics", "Data Manipulation (Pandas, NumPy)", "Machine Learning Basics", "Advanced ML & Feature Engineering", "Data Storytelling & Visualization", "End-to-End Data Science Project", "Interview Preparation"],
    "Data Analyst": ["Excel Mastery", "SQL for Data Analysis", "Python (Pandas, NumPy)", "Data Visualization (Tableau / Power BI)", "Statistical Analysis", "Build Dashboard Projects", "Interview Preparation"],
    "Cybersecurity Analyst": ["Networking Fundamentals", "Linux Administration", "Security Fundamentals & Cryptography", "SIEM & Security Tools", "Threat Analysis & Incident Response", "Certifications (CompTIA Security+)", "Interview Preparation"],
    "Cloud Engineer": ["Linux & Networking", "Cloud Fundamentals", "AWS / Azure / GCP Deep Dive", "Docker & Containerization", "Infrastructure as Code (Terraform)", "Cloud Certifications", "Interview Preparation"],
    "DevOps Engineer": ["Linux Administration", "Git & Version Control", "Docker & Containerization", "CI/CD Pipelines", "Kubernetes & Orchestration", "Cloud Infrastructure & Monitoring", "Interview Preparation"],
    "AI Engineer": ["Python & Advanced Mathematics", "Machine Learning Foundations", "Deep Learning & Neural Networks", "NLP & Computer Vision", "Model Optimization & Deployment", "Build AI-Powered Applications", "Interview Preparation"],
    "SOC Analyst": ["Networking & Protocols", "Operating Systems (Windows & Linux)", "SIEM Tools (Splunk / QRadar)", "Log Analysis & Monitoring", "Incident Response Procedures", "Threat Intelligence", "Certifications & Interview Prep"],
    "Penetration Tester": ["Networking Fundamentals", "Linux & Scripting", "Web Application Security", "Penetration Testing Tools", "OWASP Top 10", "Capture The Flag Challenges", "CEH / OSCP Certifications"],
    "Business Analyst": ["Business Communication", "Excel & Data Analysis", "SQL Basics", "Requirements Gathering & Documentation", "Data Visualization", "Domain Knowledge", "Interview Preparation"],
    "IT Support Engineer": ["Operating Systems (Windows / Linux)", "Networking Basics", "Troubleshooting Methodologies", "Active Directory & Group Policy", "ITIL Framework", "Communication & Documentation", "Certifications (CompTIA A+)"],
    "Automation Engineer": ["Programming (Python / Java)", "Test Frameworks & Methodologies", "Selenium / Cypress Automation", "API Testing (Postman / REST Assured)", "CI/CD Integration", "Build Automation Framework", "Interview Preparation"],
    "Embedded Systems Engineer": ["C / C++ Programming", "Digital Electronics Basics", "Microcontrollers (ARM / AVR)", "RTOS Concepts", "Communication Protocols (I2C, SPI, UART)", "Build Embedded Projects", "Interview Preparation"]
}

CAREER_DESCRIPTIONS = {
    "Full Stack Developer": "Builds both frontend and backend of web applications, handling everything from UI design to server logic and databases.",
    "Backend Developer": "Specializes in server-side logic, databases, and APIs that power web and mobile applications behind the scenes.",
    "Software Engineer": "Designs, develops, and maintains software systems using engineering principles and best practices.",
    "Machine Learning Engineer": "Builds and deploys machine learning models into production systems, bridging data science and software engineering.",
    "Data Scientist": "Extracts insights from complex data using statistical analysis, machine learning, and data visualization.",
    "Data Analyst": "Analyzes data to help organizations make informed business decisions through reports, dashboards, and visualizations.",
    "Cybersecurity Analyst": "Protects organizations from cyber threats by monitoring systems, analyzing vulnerabilities, and responding to incidents.",
    "Cloud Engineer": "Designs, deploys, and manages cloud infrastructure and services on platforms like AWS, Azure, or GCP.",
    "DevOps Engineer": "Bridges development and operations, automating deployment pipelines, infrastructure, and monitoring.",
    "AI Engineer": "Develops artificial intelligence solutions including NLP, computer vision, and intelligent automation systems.",
    "SOC Analyst": "Monitors security operations centers, analyzes alerts, and responds to security incidents in real time.",
    "Penetration Tester": "Ethically hacks systems to find security vulnerabilities before malicious attackers can exploit them.",
    "Business Analyst": "Bridges business needs and technology solutions by analyzing requirements and processes.",
    "IT Support Engineer": "Provides technical support, troubleshoots issues, and maintains IT infrastructure for organizations.",
    "Automation Engineer": "Designs and implements automated testing frameworks and CI/CD pipelines to ensure software quality.",
    "Embedded Systems Engineer": "Develops software for embedded devices and hardware systems like IoT devices and microcontrollers."
}


def get_required_skills(career):
    return CAREER_SKILLS.get(career, ["Programming", "Problem Solving", "Communication", "Projects", "Git & GitHub"])


def get_career_roadmap(career):
    return CAREER_ROADMAPS.get(career, [
        "Understand Role Requirements", "Build Core Technical Skills",
        "Learn Essential Tools", "Work on Hands-on Projects",
        "Build Portfolio & Resume", "Interview Preparation"
    ])


def get_career_description(career):
    return CAREER_DESCRIPTIONS.get(career, "A technology career that combines technical skills with problem-solving abilities.")