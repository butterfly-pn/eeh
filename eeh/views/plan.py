from flask import render_template, request, redirect, flash
from flask_login import current_user
from eeh.models import Plan, HarcerzPlan, Harcerz
from eeh.view_manager import login_required
from main import APP, DB

@login_required
@APP.route('/plan/<identifier>/', methods=['GET'])
def plan(identifier):
    harcerze = []
    current_plan = Plan.query.filter_by(id=identifier).first()
    if current_plan.druzyna_id == current_user['id']:
        plany = Plan.query.filter_by(druzyna_id=current_user['id']).all()
        plany_indywidualne = HarcerzPlan.query.filter_by(
            plan_id=current_user['current_plan']).all()
        for plan_indywidualny in plany_indywidualne:
            harcerz = Harcerz.query.filter_by(id=plan_indywidualny.id).first()
            harcerze.append({
                'first_name': harcerz.first_name,
                'last_name': harcerz.last_name,
                'charakterystyka': plan_indywidualny.charakterystyka,
                'cele': plan_indywidualny.cele
            })
        return render_template('plan.html', harcerze=harcerze, wizja=current_plan.wizja, cele=current_plan.cele, zz=current_plan.zz, plany=plany)
    flash("You can't do that", 'warning')
    return redirect(request.host_url)

@login_required
@APP.route('/plan/<identifier>/delete/', methods=['GET'])
def plan_delete(identifier):
    plan = Plan.query.filter_by(id=identifier).first()
    if plan.druzyna_id == current_user['id']:
        if plan.id == current_user['current_plan']:
            flash("To jest twój aktualny plan!", 'warning')
            return redirect('/plan/'+str(identifier))
        DB.session.delete(plan)
        DB.session.commit()
        flash("Usunięto "+plan.name, 'success')
    return redirect('/app/')
        

@login_required
@APP.route('/plan/new/', methods=['GET'])
def new_plan_get():
    return render_template('plan-new.html')

@login_required
@APP.route('/plan/new/', methods=['POST'])
def new_plan_post():
    new = Plan()
    new.name = request.form['name']
    new.typ = request.form['typ']
    new.druzyna_id = current_user['id']
    new.wizja = request.form['wizja']
    new.cele = request.form['cele']
    new.zz = request.form['zz']
    DB.session.add(new)
    DB.session.commit()
    return redirect('/plan/')
