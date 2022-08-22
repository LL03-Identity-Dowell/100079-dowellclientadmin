

def username_render(request):
    current_user = request.session.get('current_user')
    username = current_user['username']
    return {
    'user_name': username,
    }

def counter_render(request):
    company_number = request.session.get('company_number')
    organisation_number = request.session.get('organisation_number')
    department_number = request.session.get('department_number')    
    project_number = request.session.get('project_number')
    return {
    "organisation_number":organisation_number, "company_number": company_number,"department_number":department_number,"project_number":project_number
    }