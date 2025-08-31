from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from agents import Agent, Runner
from setupconfg import config
from pretty_print import print_pretty_json

# class ActionItem(BaseModel):
#     task: str
#     assignee: str
#     due_date: Optional[str] = None
#     priority: str = "medium"

# class Decision(BaseModel):
#     topic: str
#     decision: str
#     rationale: Optional[str] = None

# class MeetingMinutes(BaseModel):
#     meeting_title: str
#     date: str
#     attendees: List[str]
#     agenda_items: List[str]
#     key_decisions: List[Decision]
#     action_items: List[ActionItem]
#     next_meeting_date: Optional[str] = None
#     meeting_duration_minutes: int

# # Meeting minutes extractor
# agent = Agent(
#     name="MeetingSecretary",
#     instructions="""Extract structured meeting minutes from meeting transcripts.
#     Identify all key decisions, action items, and important details.""",
#     output_type=MeetingMinutes
# )

# meeting_transcript = """
# Marketing Strategy Meeting - January 15, 2024
# Attendees: Sarah (Marketing Manager), John (Product Manager), Lisa (Designer), Mike (Developer)
# Duration: 90 minutes

# Agenda:
# 1. Q1 Campaign Review
# 2. New Product Launch Strategy  
# 3. Budget Allocation
# 4. Social Media Strategy

# Key Decisions:
# - Approved $50K budget for Q1 digital campaigns based on strong ROI data
# - Decided to launch new product in March instead of February for better market timing
# - Will focus social media efforts on Instagram and TikTok for younger demographics

# Action Items:
# - Sarah to create campaign timeline by January 20th (high priority)
# - John to finalize product features by January 25th
# - Lisa to design landing page mockups by January 22nd
# - Mike to review technical requirements by January 30th

# Next meeting: January 29, 2024
# """

# result = Runner.run_sync(agent,meeting_transcript,run_config=config)

# print("=== Meeting Minutes ===")
# print_pretty_json(result.final_output)

from typing import List, Optional

class Education(BaseModel):
    degree: str
    institution: str
    graduation_year: int
    gpa: Optional[float] = None

class Experience(BaseModel):
    position: str
    company: str
    start_year: int
    end_year: Optional[int] = None  # None if current job
    responsibilities: List[str]

class Resume(BaseModel):
    full_name: str
    email: str
    phone: str
    summary: str
    education: List[Education]
    experience: List[Experience]
    skills: List[str]
    languages: List[str]

# Create resume parser
resume_parser = Agent(
    name="ResumeParser",
    instructions="Extract structured information from resume text.",
    output_type=Resume
)

# Test with sample resume
sample_resume = """
John Smith
Email: john.smith@email.com, Phone: (555) 123-4567

Professional Summary:
Experienced software developer with 5 years in web development and team leadership.

Education:
- Bachelor of Computer Science, MIT, 2018, GPA: 3.8
- Master of Software Engineering, Stanford, 2020

Experience:
- Senior Developer at Google (2020-present): Led team of 5 developers, implemented microservices architecture
- Junior Developer at Startup Inc (2018-2020): Built React applications, maintained CI/CD pipelines

Skills: Python, JavaScript, React, Docker, Kubernetes
Languages: English (native), Spanish (conversational), French (basic)
"""

result = Runner.run_sync(resume_parser,  sample_resume, run_config=config)

print("=== Parsed Resume ===")
print(f"Name: {result.final_output.full_name}")
print(f"Email: {result.final_output.email}")
print(f"Phone: {result.final_output.phone}")
print(f"Summary: {result.final_output.summary}")

print("\nEducation:")
for edu in result.final_output.education:
    gpa_str = f", GPA: {edu.gpa}" if edu.gpa else ""
    print(f"  • {edu.degree} from {edu.institution} ({edu.graduation_year}){gpa_str}")

print("\nExperience:")
for exp in result.final_output.experience:
    end_year = exp.end_year if exp.end_year else "present"
    print(f"  • {exp.position} at {exp.company} ({exp.start_year}-{end_year})")
    for resp in exp.responsibilities:
        print(f"    - {resp}")

print(f"\nSkills: {', '.join(result.final_output.skills)}")
print(f"Languages: {', '.join(result.final_output.languages)}")

print_pretty_json(result.final_output)