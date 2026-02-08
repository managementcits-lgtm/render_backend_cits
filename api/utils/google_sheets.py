from google.oauth2.service_account import Credentials
import gspread
import os

def save_team_to_sheet(team, participants):
    print("🔥 GOOGLE SHEETS FUNCTION CALLED")

    creds = Credentials.from_service_account_file(
        os.path.join(os.path.dirname(__file__), "../../service_acc.json"),
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )

    client = gspread.authorize(creds)

    sheet = client.open_by_url(
        "https://docs.google.com/spreadsheets/d/1ptibje4mwzhburPQCDO8JMv0Hs67N_LnSc_nWjqvUgw/edit?usp=sharing"
    ).sheet1

    for p in participants:
        sheet.append_row([
            team.team_name,
            p.role,
            p.full_name,
            p.email,
            p.phone,
            p.branch,
            p.section,
            p.year,
            team.total_participants,
            team.created_at.strftime("%Y-%m-%d %H:%M")
        ])
