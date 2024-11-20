from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from io import BytesIO
from flask import make_response
from reportlab.lib.pagesizes import inch
import datetime
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alunos.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  

app.secret_key = 'kaiqueinventachavealeatoria'
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()


class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    sexo = db.Column(db.String(10), nullable=False)
    data_nascimento = db.Column(db.String(10), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    matricula = db.Column(db.String(10), unique=True, nullable=False)   

    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'), nullable=True)
    curso = db.relationship('Curso', backref='alunos_curso', lazy=True)

    def __repr__(self):
        return f'<Aluno {self.nome}>'      

def gerar_matricula():
    return ''.join(random.choices(string.digits, k=8))

class Curso(db.Model):
    __tablename__ = 'curso'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f'<Curso {self.nome}>'
    
class Materia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)

class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'), nullable=False)
    
    aluno = db.relationship('Aluno', backref=db.backref('notas', lazy=True))
    materia = db.relationship('Materia', backref=db.backref('notas', lazy=True))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    cursos = Curso.query.all()
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        sexo = request.form['sexo']
        data_nascimento = request.form['data_nascimento']
        cidade = request.form['cidade']
        endereco = request.form['endereco']
        matricula = gerar_matricula() 
        curso_id = request.form['curso']

        novo_aluno = Aluno(nome=nome, telefone=telefone, email=email, sexo=sexo, 
                           data_nascimento=data_nascimento, cidade=cidade, endereco=endereco, 
                           matricula=matricula, curso_id=curso_id) 

        try:
            db.session.add(novo_aluno)
            db.session.commit()
            flash('Aluno cadastrado com sucesso!', 'success')
        except Exception as e:
            flash(f'Ocorreu um erro ao cadastrar o aluno: {str(e)}', 'error')

    return render_template('cadastrar.html', cursos=cursos)

@app.route("/cadastrar_curso", methods=["GET", "POST"])
def cadastrar_curso():
    if request.method == "POST":
        nome = request.form['nome']

        curso = Curso(nome=nome)

        try:
            db.session.add(curso)
            db.session.commit()
            flash('Curso cadastrado com sucesso!', 'success')
        except Exception as e:
            flash(f'Esse curso já está cadastrado!', 'warning')
            db.session.rollback()

        return redirect(url_for('cadastrar_curso'))

    return render_template('cadastrar_curso.html')

@app.route("/alunos")
def alunos():
    alunos_cadastrados = Aluno.query.all()
    return render_template("alunos.html", alunos=alunos_cadastrados)

@app.route("/cadastrar_materia", methods=["GET", "POST"])
def cadastrar_materia():
    if request.method == "POST":
        nome = request.form['nome']

        nova_materia = Materia(nome=nome)

        try:
            db.session.add(nova_materia)
            db.session.commit()
            flash('Matéria cadastrada com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Essa matéria já esta cadastrada!', 'warning')
        
    return render_template('cadastrar_materia.html')   

@app.route('/materias')
def listar_materias():
    materias = Materia.query.all()
    return render_template('materias.html', materias=materias)

@app.route('/lancar_nota', methods=['GET', 'POST'])
def lancar_nota():
    
    if request.method == 'POST':
        aluno_id = request.form['aluno']
        materia_id = request.form['materia']
        nota = request.form['nota']
        
        try:
            nota = float(nota)
        except ValueError:
            flash('A nota deve ser um número válido! Não use vírgulas, apenas "." !', 'error')
            return redirect(url_for('lancar_nota'))

        if nota < 0.0 or nota > 10.0:
            flash('Coloque uma nota válida! A nota deve ser de 0 a 10!  ', 'warning')
            return redirect(url_for('lancar_nota'))

        nota = Nota(aluno_id=aluno_id, materia_id=materia_id, valor=nota)
        try:
            db.session.add(nota)
            db.session.commit()
            flash('Nota lançada com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro ao lançar a nota: {str(e)}', 'error')
            return redirect(url_for('lancar_nota'))

        return redirect(url_for('lancar_nota')) 
    
    alunos = Aluno.query.all()
    materias = Materia.query.all()
    return render_template('lancar_nota.html', alunos=alunos, materias=materias)

@app.route('/notas')    
def listar_notas():
    notas = Nota.query.all()
    return render_template('notas.html', notas=notas)

@app.route('/gerar_boletim', methods=['GET', 'POST'])
def gerar_boletim():

    alunos = Aluno.query.all()  
    if request.method == 'POST':
        matricula = request.form['matricula']
        aluno = Aluno.query.filter_by(matricula=matricula).first_or_404() 
        notas = Nota.query.filter_by(aluno_id=aluno.id).all()   
        return render_template('boletim.html', aluno=aluno, notas=notas)
    return render_template('selecionar_aluno.html', alunos=alunos)

@app.route("/cursos", methods=['GET', 'POST'])
def cursos():
    alunos_curso_fazer = None
    
    if request.method == 'POST':
        curso_id = request.form['curso_id']  
        curso = Curso.query.get(curso_id)  
        
        alunos_curso_fazer = Aluno.query.filter_by(curso_id=curso.id).all()
        
        if len(alunos_curso_fazer) == 0:
         alunos_curso_fazer = None
    
    cursos = Curso.query.all()
    return render_template('cursos.html', cursos=cursos, alunos_curso_fazer=alunos_curso_fazer)

def gerar_boletim_pdf(aluno, notas):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)

    styles = getSampleStyleSheet()
    title_style = styles['Title']
    subtitle_style = ParagraphStyle(name='Subtitle', parent=styles['Normal'], fontSize=12, alignment=1)
    normal_style = styles['Normal']
    
    elements = []
    elements.append(Paragraph(f"Boletim Escolar de {aluno.nome}", title_style))
    elements.append(Paragraph(f"Matrícula: {aluno.matricula}", normal_style))
    elements.append(Paragraph(f"Data de Nascimento: {aluno.data_nascimento}", normal_style))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("", subtitle_style))

    table_data = [["Matéria", "Nota"]]
    for nota in notas:
        materia_nome = nota.materia.nome if hasattr(nota.materia, 'nome') else str(nota.materia)
        table_data.append([materia_nome, str(nota.valor)])

    table = Table(table_data, colWidths=[3*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)

    footer_text = f"Emitido em {datetime.datetime.now().strftime('%d/%m/%Y')}"
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(footer_text, normal_style))

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf

@app.route('/gerar_pdf_boletim', methods=['GET', 'POST'])
def gerar_pdf_boletim():
    alunos = Aluno.query.all()  
    if request.method == 'POST':
        matricula = request.form['matricula']
        aluno = Aluno.query.filter_by(matricula=matricula).first()

        if aluno is None:
            return "Aluno não encontrado", 404

        notas = Nota.query.filter_by(aluno_id=aluno.id).all()

        pdf = gerar_boletim_pdf(aluno, notas)

        if pdf is None:
            return "Este aluno não tem notas registradas", 400 

        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=boletim.pdf'
        return response

    return render_template('selecionar_aluno_boletim.html', alunos=alunos) 

if __name__ == '__main__':
    app.run(debug=True)