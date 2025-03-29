from django.shortcuts import render
import json
from .models import Question, Company, Tag
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def import_data(request):
    print("Importing data..." , request.method , request.FILES.get('file'))
    if request.method == "POST" and request.FILES.get('file'):
        file = request.FILES['file']
        data = json.load(file.open())  # Ensure correct file handling

        for item in data:
            # Ensure keys exist before accessing them
            print(f"Importing: {item['title']}")
            company_names = item.get("companies", "")
            company_objects = [Company.objects.get_or_create(name=name.strip())[0] for name in company_names.split(",") if name.strip()]

            tag_names = item.get("related_topics", "")
            tag_objects = [Tag.objects.get_or_create(name=tag.strip())[0] for tag in tag_names.split(",") if tag.strip()]

            # Handle missing fields safely
            solution = item.get("solution", {}).get("c++", "")
            explanation = item.get("solution", {}).get("explanation", "")

            # Create the Question instance
            question = Question.objects.create(
                title=item.get("title", "Untitled"),
                difficulty=item.get("difficulty", "E")[0].upper(),  # Default to 'E' if missing
                url=item.get("url", ""),
                acceptanceRate=item.get("acceptance_rate", 0.0),  # Fixed spelling
                solution=solution,
                explanation=explanation
            )

            print()

            # Assign Many-to-Many relations
            question.companies.set(company_objects)
            question.tags.set(tag_objects)

        return HttpResponse("Data imported successfully")

    return render(request, 'form.html')
