import json
from core.models import Question, Company, Tag  # Adjust 'myapp' to your actual app name

# Load JSON Data
with open('data.json', 'r', encoding='utf-8') as file:
    questions_data = json.load(file)

# Loop through JSON and insert into database
for item in questions_data:
    # Create or get related companies
    company_names = item["companies"].split(",")  # Split company names from CSV string
    company_objects = [Company.objects.get_or_create(name=name.strip())[0] for name in company_names]

    # Create or get related tags
    tag_names = item["related_topics"].split(",")  # Split tags from CSV string
    tag_objects = [Tag.objects.get_or_create(name=tag.strip())[0] for tag in tag_names]

    # Create the Question instance
    question = Question.objects.create(
        title=item["title"],
        difficulty=item["difficulty"][0].upper(),  # Convert 'Easy' → 'E'
        url=item["url"],
        acceptenceRate=item["acceptance_rate"],
        solution=item["solution"]["c++"],  # Choose a default language solution
        explanation=item["solution"]["explanation"]
    )

    # Assign Many-to-Many relations
    question.companies.set(company_objects)
    question.tags.set(tag_objects)

print("✅ Data successfully inserted into the database!")
