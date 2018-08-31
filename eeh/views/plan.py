from flask import render_template
from flask_login import current_user
from eeh.models import Plan, HarcerzPlan, Harcerz
from main import APP

@APP.route('/plan/', methods=['GET'])
def plan():
    harcerze = []
    current_plan = Plan.query.filter_by(id=current_user.current_plan).first()
    plany_indywidualne = HarcerzPlan.query.filter_by(plan_id=current_user.current_plan).all()
    for plan_indywidualny in plany_indywidualne:
        harcerz = Harcerz.query.filter_by(id=plan_indywidualny.id).first()
        harcerze.append({
            'first_name' : harcerz.first_name, 
            'last_name' : harcerz.last_name, 
            'charakterystyka' : plan_indywidualny.charakterystyka, 
            'cele' : plan_indywidualny.cele
            })
    return render_template('plan.html', harcerze=harcerze, wizja=current_plan.wizja, cele=current_plan.cele, zz=current_plan.zz)