from datetime import datetime
import cohere
from googleapiclient.discovery import build

# --- Credentials (reusing keys from previous messages) ---
COHERE_API_KEY = "N6YmtTbVW7iqKnIJgFFcIIWDSW8yK7GruKeWBn2N"
GEMINI_API_KEY = "AIzaSyDbLI6N8BcfYwN30uamRjKa2tQ1E525jOQ"

# --- Supabase client (you must configure supabase in your Django project) ---
from app.supabase_config import supabase

def generate_dual_issue_summary(issue_id, model_choice="cohere"):
    # 1. Fetch data from Supabase
    issue_info = supabase.table("familyissue").select("*").eq("id", issue_id).single().execute().data
    print(issue_info)
    issue_logs = supabase.table("familyissuelog").select("*").eq("id", issue_id).execute().data
    print(issue_logs)
    family_info = supabase.table("families").select("*").eq("family_id", issue_info["family_id"]).single().execute().data
    print(family_info)
    created_at = issue_info.get("created_at")
    created_date = datetime.fromisoformat(issue_info.get("created_at", datetime.now().isoformat())) if created_at else "Unknown"
    issue_info = supabase.table("familyissue").select("*").eq("id", issue_id).single().execute().data
    if not issue_info:
        raise ValueError(f"No issue found with ID {issue_id}")

    # user_info = supabase.table("user_details").select("*").eq("user_id", issue_id).single().execute().data
    # print(user_info)
    # response = supabase.table("family_issue").select("*").eq("id", issue_id).execute()
    # rows = response.data
    # if not rows:
    #     raise ValueError("No matching issue found with the given ID.")
    # issue_info = rows[0]

    # 2. Parse details
    created_date = datetime.fromisoformat(issue_info.get("created_at", datetime.now().isoformat())) if issue_info.get("created_at") else "Unknown"
    status_timeline = "\n".join(
        f"- {datetime.fromisoformat(log['last_update_date']).strftime('%d-%b-%Y')}: {log['status']} – {log.get('remarks', 'No remarks')}"
        for log in sorted(issue_logs, key=lambda x: x['last_update_date'])
    )

    # 3. Construct prompt
    prompt = f"""
You are a government-grade AI auditor. Generate a formal 8–10 sentence summary of the complaint timeline.
I want detailed insights into the issues raised by families regarding ration distribution and related grievances.
No short para info summary but a detailed audit report. the report should be comprehensive and cover all aspects of the issues raised.
Recommendations for improvements, escalations, and government review are essential also on what action should be taken on the authorities be mentioned along with suggestions for non repeating of the same issue too be given.
there must be atleast 8-10 sentences in the summary.
Issue Summary:
- Issue ID: {issue_id}

- Family ID: {family_info.get("id")}
- Issue Type: {issue_info.get("issue_type", "Unknown")}
- Date Filed: {created_date}
- Current Status: {issue_info.get("status", "Unknown")}
- Village: {family_info.get("village", "N/A")}
- Block: {family_info.get("block", "N/A")}
- Ration Card: {family_info.get("ration_card_number", "N/A")}

Status Timeline:
{status_timeline}

Please summarize:
1. Duration and timeliness of issue resolution.
2. Delays or poor handling of any step.
3. Suggested improvements or escalations.
4. Recommendations for audit or government review.
"""

    # 4. AI model selection
    if model_choice == "cohere":
        if len(prompt) < 250:
            prompt += " " * (250 - len(prompt))
        client = cohere.Client(COHERE_API_KEY)
        response = client.summarize(
            text=prompt,
            model="summarize-xlarge",
            length="long",
            format="paragraph",
            temperature=0.7
        )
        summary_text = response.summary

    else:  # Gemini
        service = build('generativelanguage', 'v1beta', developerKey=GEMINI_API_KEY)
        response = service.models().generateContent(
            model="models/text-bison-001",
            body={
                "prompt": {
                    "text": prompt
                },
                "temperature": 0.7,
            }
        ).execute()
        summary_text = response["candidates"][0]["output"]
        print(f"Gemini Summary: {summary_text}")

    # 5. Return summary text (can be returned, saved, or rendered in PDF)
    return summary_text

def generate_overall_issues_summary(model_choice="cohere"):
    from datetime import datetime

    all_issues = supabase.table("familyissue").select("*").execute().data
    if not all_issues:
        raise ValueError("No issues available.")

    content_blocks = []

    for issue in all_issues:
        logs = supabase.table("familyissuelog").select("*").eq("id", issue["id"]).execute().data
        family = supabase.table("families").select("*").eq("family_id", issue["family_id"]).single().execute().data

        issue_summary = f"""
- Issue: {issue.get('issue')}
- Type: {issue.get('issue_type')}
- Status: {issue.get('status')}
- Village: {family.get('village')}
- Ration Card: {family.get('ration_card_number')}
- Date: {datetime.fromisoformat(issue.get("created_at", datetime.now().isoformat()))

}
- Logs: {"; ".join(f"{l['status']} on {l['last_update_date']}" for l in logs)}
"""
        content_blocks.append(issue_summary.strip())

    full_prompt = f"""
As a government audit assistant AI, generate a professional audit summary across all the listed complaints.
I want detailed insights into the issues raised by families regarding ration distribution and related grievances.
No short para info summary but a detailed audit report. the report should be comprehensive and cover all aspects of the issues raised.
there must be atleast 8-10 sentences in the summary.
Recommendations for improvements, escalations, and government review are essential also on what action should be taken on the authorities be mentioned along with suggestions for non repeating of the same issue too be given.
Summarize recurring issues, delayed timelines, department failures, and recommend accountability measures.

Complaints:

{chr(10).join(content_blocks)}
"""

    if model_choice == "cohere":
        client = cohere.Client(COHERE_API_KEY)
        response = client.summarize(
            text=full_prompt,
            model="summarize-xlarge",
            length="long",
            format="paragraph",
            temperature=0.7
        )
        return response.summary
    elif model_choice == "gemini":
        service = build('generativelanguage', 'v1beta', developerKey=GEMINI_API_KEY)
        response = service.models().generateContent(
            model="models/text-bison-001",
            body={"prompt": {"text": full_prompt}, "temperature": 0.7}
        ).execute()
        return response["candidates"][0]["output"]
    else:
        raise ValueError("Unsupported AI model")
