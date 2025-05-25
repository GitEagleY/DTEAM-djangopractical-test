import json
from openai import OpenAI
from django.conf import settings
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from .models import ModelCV


def translate_text(cv_id: int, target_language: str) -> dict:
    try:
        cv_instance = ModelCV.objects.get(pk=cv_id)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"CV with ID {cv_id} does not exist.")

    cv_data = model_to_dict(cv_instance)
    serialized_cv = json.dumps(cv_data)

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Translate the following CV content into {target_language}."},
            {"role": "user", "content": serialized_cv}
        ]
    )

    try:
        translated_content = response.choices[0].message.content
        return json.loads(translated_content)
    except (IndexError, AttributeError, json.JSONDecodeError) as e:
        raise ValueError("Failed to parse translation response") from e
