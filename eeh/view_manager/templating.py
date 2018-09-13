from flask import _app_ctx_stack
from flask.templating import _render
from flask_login import current_user
from dbconnect import connection
from pymysql import escape_string

def render_template(template_name_or_list, **context):
    """Renders a template from the template folder with the given
    context.

    :param template_name_or_list: the name of the template to be
                                  rendered, or an iterable with template names
                                  the first one existing will be rendered
    :param context: the variables that should be available in the
                    context of the template.
    """
    con, conn = connection()
    sql = "select a.id_scout_team, a.name, b.id_scouting_troop, c.scout_id FROM scout_team a, scouting_troop b, scout_membership c WHERE a.id_scout_team = b.scout_team_id AND c.scouting_troop_id = b.id_scouting_troop AND b.name = \"Komenda\" AND c.scout_id = %s;"
    con.execute(sql, escape_string(str(current_user['id_user'])))
    scout_teams = con.fetchall()
    con.close()
    conn.close()
    context['scout_teams'] = scout_teams
    ctx = _app_ctx_stack.top
    ctx.app.update_template_context(context)
    return _render(ctx.app.jinja_env.get_or_select_template(template_name_or_list),
                   context, ctx.app)
