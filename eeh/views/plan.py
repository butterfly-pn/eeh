from flask import request, redirect, flash, session
from eeh.view_manager.templating import render_template
from flask_login import current_user
from eeh.view_manager import login_required, komenda_required
from main import APP
from dbconnect import connection
from pymysql import escape_string
from datetime import datetime

@login_required
@APP.route('/plan/', methods=['GET'])
def plan():
    con, conn = connection()
    con.execute("SELECT * FROM scout_team WHERE id_scout_team = %s", escape_string(str(session['id_scout_team'])))
    current_team = con.fetchone()
    con.execute("SELECT * FROM work_plan WHERE scout_team_id = %s", escape_string(str(session['id_scout_team'])))
    work_plans = con.fetchall()
    con.close()
    conn.close()
    if work_plans:
        current_work_plan = None
        for work_plan in work_plans:
            if request.args.get('work-plan'):
                current_work_plan = work_plan if int(request.args.get('work-plan')) == work_plan['id_work_plan'] else current_work_plan
            else:
                current_work_plan = work_plan if work_plan['id_work_plan'] == current_team['current_work_plan_id'] else current_work_plan
        return render_template("plan.html", work_plans=work_plans, current_work_plan=current_work_plan if current_work_plan else work_plans[-1])
    return render_template("plan-none.html")

@login_required
@APP.route('/plan/<identifier>/', methods=['GET'])
def plan_get(identifier):
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

@komenda_required
@APP.route('/plan/new/', methods=['POST'])
def new_plan_post():
    con, conn = connection()
    con.execute("INSERT INTO work_plan (name, category, scout_team_id, start_date) VALUES (%s, %s, %s, %s)", (escape_string(
        request.form['name']), escape_string(request.form['typ']), escape_string(str(session['id_scout_team'])), escape_string(str(datetime.now()))))
    conn.commit()
    work_plan_id = con.lastrowid
    con.execute("INSERT INTO characteristic (characteristic, category, parent_id, work_plan_id) VALUES (%s, %s, %s, %s)", (escape_string(request.form['wizja']), escape_string("scout_team"), escape_string(str(session['id_scout_team'])), escape_string(str(work_plan_id))))
    conn.commit()
    con.close()
    conn.close()
    return redirect('/plan/')
