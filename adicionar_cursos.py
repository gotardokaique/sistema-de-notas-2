from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicializando o Flask
app = Flask(__name__)

# Configuração para usar o banco de dados já existente
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alunos.db'  # Caminho do banco de dados existente
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo Curso
class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

# Modelo Materia
class Materia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

# Função para adicionar cursos e matérias ao banco de dados
def adiciona_curso_materia():
    # Lista de cursos
    cursos = [
    "Administração", "Medicina", "Análise e Desenvolvimento de Sistemas", "Engenharia Civil", 
    "Direito", "Arquitetura", "Psicologia", "Educação Física", "Biologia", "Ciência da Computação", 
    "Design Gráfico", "Marketing", "Gestão de Recursos Humanos", "Engenharia Elétrica", "Engenharia Mecânica", 
    "Química", "Fisioterapia", "Enfermagem", "Odontologia", "Tecnologia da Informação", 
    "Administração de Empresas", "Contabilidade", "Economia", "Letras", "Matemática", 
    "Filosofia", "Sociologia", "Pedagogia", "História", "Geografia", 
    "Teologia", "Farmácia", "Veterinária", "Turismo", "Hotelaria", 
    "Nutrição", "Gestão de Tecnologia da Informação", "Jornalismo", "Relações Internacionais", 
    "Ciências Contábeis", "Publicidade e Propaganda", "Gestão Financeira", "Processos Gerenciais", 
    "Gestão de Projetos", "Estatística", "Ciências Sociais", "Música", "Arquitetura e Urbanismo", 
    "Ciências Ambientais", "Bioquímica", "Engenharia de Produção", "Engenharia de Software", 
    "Engenharia de Alimentos", "Design de Interiores", "Design de Moda", "Cinema", "Artes Cênicas", 
    "Análise de Sistemas", "Gestão de Marketing", "Gestão de Negócios", "Gestão de Operações", 
    "Gestão de Pessoas", "Gestão Pública", "Gestão de Comércio Exterior", "Gestão da Qualidade", 
    "Gestão de Supply Chain", "Gestão de Vendas", "Gestão Hospitalar", "Gestão de Eventos", 
    "Gestão de Segurança", "Gestão de Inovação", "Gestão de Carreira", "Gestão de Comunicação", 
    "Gestão de Riscos", "Gestão de Processos", "Gestão de Serviços", "Gestão de Tecnologia", 
    "Gestão de Cadeias Produtivas", "Gestão de Logística", "Gestão de Projetos Sustentáveis", 
    "Gestão do Conhecimento", "Gestão Estratégica", "Gestão de Sustentabilidade", "Gestão de Infraestrutura", 
    "Gestão de Marketing Digital", "Gestão de Finanças", "Gestão de Meio Ambiente", 
    "Gestão de Organizações", "Gestão de Projetos Ágeis", "Gestão de TI", "Gestão de Clientes", 
    "Gestão de Compliance", "Gestão de Reputação", "Gestão de Comércio", "Gestão de Pessoas e Cultura", 
    "Gestão de Mudanças", "Gestão de Mídias Sociais", "Gestão de Equipes", "Gestão do Valor", 
    "Gestão Estratégica de Pessoas", "Gestão de Desempenho", "Gestão de Tecnologias Emergentes", 
    "Gestão de Logística Reversa", "Gestão de Infraestrutura de TI", "Gestão de Mercado", 
    "Gestão de Infraestrutura Empresarial", "Gestão de Competências", "Gestão de Marketing Estratégico"
]
    materias = [
        "Matemática", "Português", "História", "Geografia", "Física", "Química", "Biologia", 
        "Inglês", "Educação Física", "Sociologia", "Filosofia", "Artes"
    ]

    # Aqui adiciona os cursos ao banco
    for curso_nome in cursos:
        curso = Curso(nome=curso_nome)
        db.session.add(curso)
    
    # aqui as materias
    for materia_nome in materias:
        materia = Materia(nome=materia_nome)
        db.session.add(materia)
    
    db.session.commit()

if __name__ == '__main__':
      with app.app_context():
        db.create_all()
        adiciona_curso_materia() 
        print("Cursos e matérias adicionados com sucesso!")
