from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'deniroData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Deniro Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM deniro')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, deni=result)


@app.route('/view/<int:city_id>', methods=['GET'])
def record_view(city_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM deniro WHERE id=%s', city_id)
    result = cursor.fetchone()
    return render_template('view.html', title='View Form', city=result)


@app.route('/edit/<int:city_id>', methods=['GET'])
def form_edit_get(city_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM deniro WHERE id=%s', city_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', city=result[0])


@app.route('/edit/<int:city_id>', methods=['POST'])
def form_update_post(city_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldYear'), request.form.get('fldRating'), request.form.get('fldTitle'),
                 city_id)
    sql_update_query = """UPDATE deniro t SET t.fldYear = %s, t.fldRating = %s, t.fldTitle = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/deniro/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New City Form')


@app.route('/deniro/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldYear'), request.form.get('fldRating'), request.form.get('fldTitle'))
    sql_insert_query = """INSERT INTO deniro (fldYear,fldRating,fldTitle) VALUES (%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:city_id>', methods=['POST'])
def form_delete_post(city_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM deniro WHERE id = %s """
    cursor.execute(sql_delete_query, city_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/deniro', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM deniro')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/deniro/<int:deni_id>', methods=['GET'])
def api_retrieve(deni_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM deniro WHERE id=%s', deni_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/deniro/', methods=['POST'])
def api_add() -> str:
    content = request.json
    cursor = mysql.get_db().cursor()
    inputData = (content['fldYear'], content['fldRating'], content['fldTitle'])
    sql_insert_query = """INSERT INTO deniro (fldYear,fldRating,fldTitle) VALUES (%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/deniro/<int:deni_id>', methods=['PUT'])
def api_edit(deni_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['fldYear'], content['fldRating'], content['fldTitle'],deni_id)
    sql_update_query = """UPDATE deniro t SET t.fldYear = %s, t.fldRating = %s, t.fldTitle = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/deniro/<int:deni_id>', methods=['DELETE'])
def api_delete(deni_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM deniro WHERE Id = %s """
    cursor.execute(sql_delete_query, deni_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
