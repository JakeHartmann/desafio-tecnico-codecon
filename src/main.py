from flask import Flask, request, testing
from user import User
import json
from collections import defaultdict
from utils import *

IGNORED_ENDPOINTS = {"/evaluation"}

users_list = []
with open('usuarios.json') as file:
    for item in json.load(file):
        new_user = User(**item)
        users_list.append(new_user)

app = Flask(__name__)

def get_superusers():
    return [user for user in users_list if user.score >= 900 and user.ativo]

@app.route("/users", methods=['POST'])
def users():
    data = request.get_json()
    
    for item in data:
        new_user = User(**item)
        users_list.append(new_user)
    return jjsonify({"message": "Usuários cadastrados com sucesso"})

@app.route("/superusers")
@with_execution_time
def superusers():
    superusers_data = [user.model_dump(mode="json") for user in get_superusers()]

    response = {
        "superusers": superusers_data,
    }

    return jjsonify(response)

@app.route("/top-countries")
@with_execution_time
def get_top_countries():
    top_countries = defaultdict(int)
    for superuser in get_superusers():
        top_countries[superuser.pais] = top_countries.get(superuser.pais, 0) + 1
    top_5_countries = sorted(top_countries.items(), key=lambda pair: pair[1], reverse=True)[:5]
    
    response = {
        "countries": { top_5_countries[i][0] : top_5_countries[i][1] for i in range(len(top_5_countries)) }
    }
    
    return jjsonify(response)

@app.route("/team-insights")
@with_execution_time
def team_insights():
    team_stats = {}
    
    for user in users_list:
        team_name = user.equipe.get("nome", "Sem Nome")
        
        if team_name not in team_stats:
            team_stats[team_name] = {
                "total_members": 0,
                "leaders": 0,
                "completed_projects": 0,
                "active_members": 0
            }
            
        team_stats[team_name]["total_members"] += 1
        if user.equipe.get("lider", False):
            team_stats[team_name]["leaders"] += 1
        if user.ativo:
            team_stats[team_name]["active_members"] += 1
        
        projetos = user.equipe.get("projetos", [])

        completed_count = 0
        for projeto in projetos:
            if projeto.get("concluido"):
                completed_count += 1

        team_stats[team_name]["completed_projects"] += completed_count
    
    teams_response = []
    for team_name, stats in team_stats.items():
        total = stats["total_members"]
        active = stats["active_members"]
        if total > 0:
            active_percentage = (active / total) * 100
        else:
            active_percentage = 0.0
            
        active_percentage = round(active_percentage, 1)
        
        teams_response.append({
            "team": team_name,
            "total_members": total,
            "leaders": stats["leaders"],
            "completed_projects": stats["completed_projects"],
            "active_percentage": active_percentage
        })
    
    response = {
        "teams": teams_response
    }
    
    return jjsonify(response)

@app.route("/active-users-per-day")
@with_execution_time
def active_users_per_day():
    min_logins_str = request.args.get("min")
    if min_logins_str is not None:
        try:
            min_logins = int(min_logins_str)
        except ValueError:
            return jjsonify({"error": "Parameter 'min' must be an integer"}, 400)
    else:
        min_logins = 0
        
    logins_per_date = {}
    
    for user in users_list:
        for log in user.logs:
            date = log.get("data")
            action = log.get("acao")
        
            if action != "login":
                continue
            
            if date not in logins_per_date:
                logins_per_date[date] = 0
            
            logins_per_date[date] += 1
    
    results = []
    
    for date in sorted(logins_per_date.keys()):
        total = logins_per_date[date]
        
        if total >= min_logins:
            results.append({
                "date": date,
                "total": total
            })
    return {
        "logins": results
    }

def get_public_endpoints():
    endpoints = []
    
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and not rule.rule.startswith("/static"):
            if rule.rule not in IGNORED_ENDPOINTS:
                endpoints.append(rule.rule)
    
    return sorted(endpoints)

def test_endpoint(client: testing.FlaskClient, endpoint_path: str, method="GET"):
    start_time = time.time()
    response = client.get(endpoint_path, method=method)
    end_time = time.time()
    time_ms = round((end_time - start_time) * 1000, 2)

    try:
        response.get_json()
        valid_json = True
    except Exception:
        valid_json = False
    
    return {
        "status": response.status_code,
        "time_ms": time_ms,
        "valid_response": valid_json
    }
        
@app.route("/evaluation")
def evaluation():
    results = {}
    client: testing.FlaskClient = app.test_client()
    endpoints = get_public_endpoints()
    
    for endpoint in endpoints:
        endpoint_test_result = test_endpoint(client, endpoint)
        results[endpoint] = endpoint_test_result
    
    return jjsonify({
        "tested_endpoints": results
    })