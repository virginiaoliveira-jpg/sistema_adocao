from flask import Flask, render_template, redirect, url_for, request, flash, session, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'chave_secreta_desenvolvimento')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///larpet.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/fotos'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    
    cpf = db.Column(db.String(20))
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(200))
    data_nascimento = db.Column(db.String(20))
    tipo_residencia = db.Column(db.String(50))
    outros_animais = db.Column(db.String(10))
    motivo_adocao = db.Column(db.Text)
    
    cnpj = db.Column(db.String(20))
    razao_social = db.Column(db.String(100))
    responsavel_nome = db.Column(db.String(100))
    responsavel_cpf = db.Column(db.String(20))

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50), nullable=False)
    raca = db.Column(db.String(50))
    idade = db.Column(db.String(20))
    status = db.Column(db.String(20), default='disponível')
    localizacao = db.Column(db.String(100))
    foto = db.Column(db.String(200))
    vacinacao = db.Column(db.Text)
    
    adocoes = db.relationship('Adocao', backref='animal', lazy=True)

class Adotante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(20), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    data_nascimento = db.Column(db.String(20))
    tipo_residencia = db.Column(db.String(50))
    outros_animais = db.Column(db.String(10))
    motivo_adocao = db.Column(db.Text)
    
    adocoes = db.relationship('Adocao', backref='adotante', lazy=True)

class Adocao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
    adotante_id = db.Column(db.Integer, db.ForeignKey('adotante.id'), nullable=False)
    data_adocao = db.Column(db.DateTime, default=datetime.utcnow)
    motivo = db.Column(db.Text)
    status = db.Column(db.String(50), default='Confirmada')

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        tipo = request.form.get('tipo')
        
        if not email or not senha or not tipo:
            flash('Por favor, preencha todos os campos.', 'error')
            return redirect(url_for('login'))
        
        usuario = Usuario.query.filter_by(email=email, tipo=tipo).first()
        
        if usuario and check_password_hash(usuario.senha, senha):
            session['usuario_id'] = usuario.id
            session['tipo'] = usuario.tipo
            session['nome'] = usuario.nome
            flash(f'Bem-vindo(a), {usuario.nome}!', 'success')
            
            if usuario.tipo == "ONG":
                return redirect(url_for('animais'))
            else:
                return redirect(url_for('animais_disponiveis'))
        else:
            flash('E-mail, senha ou tipo de usuário incorretos.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('index'))

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        tipo = request.form.get('tipo')
        
        if not nome or not email or not senha or not tipo:
            flash('Por favor, preencha todos os campos obrigatórios.', 'error')
            return redirect(url_for('cadastrar'))
        
        if Usuario.query.filter_by(email=email).first():
            flash('Este e-mail já está cadastrado.', 'error')
            return redirect(url_for('cadastrar'))
        
        senha_hash = generate_password_hash(senha)
        
        novo_usuario = Usuario(
            nome=nome,
            email=email,
            senha=senha_hash,
            tipo=tipo
        )
        
        if tipo == 'Adotante':
            novo_usuario.cpf = request.form.get('cpf')
            novo_usuario.telefone = request.form.get('telefone')
            novo_usuario.endereco = request.form.get('endereco')
            novo_usuario.data_nascimento = request.form.get('data_nascimento')
            novo_usuario.tipo_residencia = request.form.get('tipo_residencia')
            novo_usuario.outros_animais = request.form.get('outros_animais')
            novo_usuario.motivo_adocao = request.form.get('motivo_adocao')
            
            adotante = Adotante(
                nome=nome,
                cpf=novo_usuario.cpf,
                telefone=novo_usuario.telefone,
                email=email,
                endereco=novo_usuario.endereco,
                data_nascimento=novo_usuario.data_nascimento,
                tipo_residencia=novo_usuario.tipo_residencia,
                outros_animais=novo_usuario.outros_animais,
                motivo_adocao=novo_usuario.motivo_adocao
            )
            db.session.add(adotante)
        
        elif tipo == 'ONG':
            novo_usuario.cnpj = request.form.get('cnpj')
            novo_usuario.razao_social = request.form.get('razao_social')
            novo_usuario.telefone = request.form.get('telefone_ong')
            novo_usuario.endereco = request.form.get('endereco_ong')
            novo_usuario.responsavel_nome = request.form.get('responsavel_nome')
            novo_usuario.responsavel_cpf = request.form.get('responsavel_cpf')
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        if tipo == 'Adotante':
            adotante.usuario_id = novo_usuario.id
            db.session.commit()
        
        flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
        return redirect(url_for('login'))
    
    return render_template('cadastrar.html')

@app.route('/animais')
def animais():
    if 'usuario_id' not in session or session.get('tipo') != 'ONG':
        flash('Acesso restrito a ONGs.', 'error')
        return redirect(url_for('login'))
    
    lista_animais = Animal.query.all()
    return render_template('animais.html', animais=lista_animais)

@app.route('/animais/adicionar', methods=['GET'])
def adicionar_animal():
    if 'usuario_id' not in session or session.get('tipo') != 'ONG':
        flash('Acesso restrito a ONGs.', 'error')
        return redirect(url_for('login'))

    return render_template('adicionar_animal.html')

@app.route('/add_animal', methods=['POST'])
def add_animal():
    if 'usuario_id' not in session or session.get('tipo') != 'ONG':
        flash('Acesso restrito a ONGs.', 'error')
        return redirect(url_for('login'))
    
    try:
        nome = request.form.get('nome')
        especie = request.form.get('especie')
        raca = request.form.get('raca')
        idade = request.form.get('idade')
        localizacao = request.form.get('localizacao')
        vacinacao = request.form.get('vacinacao')
        status = request.form.get('status', 'disponível')
        
        if not nome or not especie:
            flash('Nome e espécie são obrigatórios.', 'error')
            return redirect(url_for('animais'))
        
        foto_arquivo = request.files.get('foto')
        nome_arquivo = None
        
        if foto_arquivo and foto_arquivo.filename != '':
            nome_arquivo = secure_filename(foto_arquivo.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            nome_arquivo = f"{timestamp}_{nome_arquivo}"
            caminho = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
            foto_arquivo.save(caminho)
        
        novo_animal = Animal(
            nome=nome,
            especie=especie,
            raca=raca,
            idade=idade,
            localizacao=localizacao,
            vacinacao=vacinacao,
            status=status,
            foto=nome_arquivo
        )
        
        db.session.add(novo_animal)
        db.session.commit()
        
        flash(f'Animal {nome} cadastrado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao cadastrar animal: {str(e)}', 'error')
    
    return redirect(url_for('animais'))

@app.route('/edit_animal/<int:id>', methods=['GET', 'POST'])
def edit_animal(id):
    if 'usuario_id' not in session or session.get('tipo') != 'ONG':
        flash('Acesso restrito a ONGs.', 'error')
        return redirect(url_for('login'))
    
    animal = Animal.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            animal.nome = request.form.get('nome')
            animal.especie = request.form.get('especie')
            animal.raca = request.form.get('raca')
            animal.idade = request.form.get('idade')
            animal.localizacao = request.form.get('localizacao')
            animal.vacinacao = request.form.get('vacinacao')
            animal.status = request.form.get('status')
            
            foto_arquivo = request.files.get('foto')
            if foto_arquivo and foto_arquivo.filename != '':
                if animal.foto:
                    try:
                        caminho_antigo = os.path.join(app.config['UPLOAD_FOLDER'], animal.foto)
                        if os.path.exists(caminho_antigo):
                            os.remove(caminho_antigo)
                    except Exception as e:
                        print(f"Erro ao remover foto antiga: {e}")
                
                nome_arquivo = secure_filename(foto_arquivo.filename)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                nome_arquivo = f"{timestamp}_{nome_arquivo}"
                caminho = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
                foto_arquivo.save(caminho)
                animal.foto = nome_arquivo
            
            db.session.commit()
            flash(f'Animal {animal.nome} atualizado com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar animal: {str(e)}', 'error')
        
        return redirect(url_for('animais'))
    
    lista_animais = Animal.query.all()
    return render_template('animais.html', animais=lista_animais, animal_edit=animal)

@app.route('/delete_animal/<int:id>')
def delete_animal(id):
    if 'usuario_id' not in session or session.get('tipo') != 'ONG':
        flash('Acesso restrito a ONGs.', 'error')
        return redirect(url_for('login'))
    
    try:
        animal = Animal.query.get_or_404(id)
        
        if animal.foto:
            try:
                caminho_foto = os.path.join(app.config['UPLOAD_FOLDER'], animal.foto)
                if os.path.exists(caminho_foto):
                    os.remove(caminho_foto)
            except Exception as e:
                print(f"Erro ao remover foto: {e}")
        
        db.session.delete(animal)
        db.session.commit()
        
        flash('Animal excluído com sucesso.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir animal: {str(e)}', 'error')
    
    return redirect(url_for('animais'))

@app.route('/adotantes')
def adotantes():
    if 'usuario_id' not in session or session.get('tipo') != 'ONG':
        flash('Acesso restrito a ONGs.', 'error')
        return redirect(url_for('login'))
    
    lista_adotantes = Adotante.query.all()
    return render_template('adotantes.html', adotantes=lista_adotantes)

@app.route('/add_adotante', methods=['POST'])
def add_adotante():
    if 'usuario_id' not in session or session.get('tipo') != 'ONG':
        flash('Acesso restrito a ONGs.', 'error')
        return redirect(url_for('login'))
    
    try:
        novo_adotante = Adotante(
            nome=request.form.get('nome'),
            cpf=request.form.get('cpf'),
            telefone=request.form.get('telefone'),
            email=request.form.get('email'),
            endereco=request.form.get('endereco'),
            data_nascimento=request.form.get('data_nascimento'),
            tipo_residencia=request.form.get('tipo_residencia'),
            outros_animais=request.form.get('outros_animais'),
            motivo_adocao=request.form.get('motivo_adocao')
        )
        
        db.session.add(novo_adotante)
        db.session.commit()
        
        flash('Adotante cadastrado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao cadastrar adotante: {str(e)}', 'error')
    
    return redirect(url_for('adotantes'))

@app.route('/edit_adotante/<int:id>', methods=['GET', 'POST'])
def edit_adotante(id):
    if 'usuario_id' not in session or session.get('tipo') != 'ONG':
        flash('Acesso restrito a ONGs.', 'error')
        return redirect(url_for('login'))
    
    adotante = Adotante.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            adotante.nome = request.form.get('nome')
            adotante.cpf = request.form.get('cpf')
            adotante.telefone = request.form.get('telefone')
            adotante.email = request.form.get('email')
            adotante.endereco = request.form.get('endereco')
            adotante.data_nascimento = request.form.get('data_nascimento')
            adotante.tipo_residencia = request.form.get('tipo_residencia')
            adotante.outros_animais = request.form.get('outros_animais')
            adotante.motivo_adocao = request.form.get('motivo_adocao')
            
            db.session.commit()
            flash(f'Adotante {adotante.nome} atualizado com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar adotante: {str(e)}', 'error')
        
        return redirect(url_for('adotantes'))
    
    lista_adotantes = Adotante.query.all()
    return render_template('adotantes.html', adotantes=lista_adotantes, adotante_edit=adotante)

@app.route('/delete_adotante/<int:id>')
def delete_adotante(id):
    if 'usuario_id' not in session or session.get('tipo') != 'ONG':
        flash('Acesso restrito a ONGs.', 'error')
        return redirect(url_for('login'))
    
    try:
        adotante = Adotante.query.get_or_404(id)
        db.session.delete(adotante)
        db.session.commit()
        
        flash('Adotante excluído com sucesso.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir adotante: {str(e)}', 'error')
    
    return redirect(url_for('adotantes'))

@app.route('/animais_disponiveis')
def animais_disponiveis():
    try:
        busca = request.args.get('q', '').strip()
        
        if busca:
            from sqlalchemy import or_
            animais = Animal.query.filter(
                Animal.status == 'disponível',
                or_(
                    Animal.especie.ilike(f'%{busca}%'),
                    Animal.raca.ilike(f'%{busca}%') if Animal.raca.isnot(None) else False,
                    Animal.localizacao.ilike(f'%{busca}%') if Animal.localizacao.isnot(None) else False,
                    Animal.nome.ilike(f'%{busca}%')
                )
            ).all()
        else:
            animais = Animal.query.filter_by(status='disponível').all()
        
        return render_template('animais_disponiveis.html', animais=animais, busca=busca)
    except Exception as e:
        flash(f'Erro ao carregar animais: {str(e)}', 'error')
        return render_template('animais_disponiveis.html', animais=[], busca='')

@app.route('/adocao/<int:animal_id>', methods=['GET', 'POST'])
def adocao(animal_id):
    if 'usuario_id' not in session:
        flash('Você precisa fazer login para adotar um animal.', 'warning')
        return redirect(url_for('login'))
    
    if session.get('tipo') != 'Adotante':
        flash('Apenas adotantes podem realizar adoções.', 'error')
        return redirect(url_for('animais_disponiveis'))
    
    animal = Animal.query.get_or_404(animal_id)
    
    if animal.status != 'disponível':
        flash('Este animal não está mais disponível para adoção.', 'warning')
        return redirect(url_for('animais_disponiveis'))
    
    usuario = Usuario.query.get(session['usuario_id'])
    adotante = Adotante.query.filter_by(usuario_id=usuario.id).first()
    
    if not adotante:
        adotante = Adotante(
            usuario_id=usuario.id,
            nome=usuario.nome,
            cpf=usuario.cpf or 'Não informado',
            telefone=usuario.telefone or 'Não informado',
            email=usuario.email,
            endereco=usuario.endereco or 'Não informado',
            data_nascimento=usuario.data_nascimento,
            tipo_residencia=usuario.tipo_residencia,
            outros_animais=usuario.outros_animais,
            motivo_adocao=usuario.motivo_adocao
        )
        db.session.add(adotante)
        db.session.commit()
    
    if request.method == 'POST':
        try:
            motivo_final = request.form.get('motivo_final')
            responsabilidade = request.form.get('responsabilidade')
            
            if not responsabilidade:
                flash('Você precisa aceitar a responsabilidade para adotar.', 'error')
                return redirect(url_for('adocao', animal_id=animal_id))
            
            nova_adocao = Adocao(
                animal_id=animal.id,
                adotante_id=adotante.id,
                motivo=motivo_final,
                status='Confirmada'
            )
            
            animal.status = 'adotado'
            
            db.session.add(nova_adocao)
            db.session.commit()
            
            flash(f'Parabéns! Você adotou {animal.nome}! A ONG entrará em contato em breve.', 'success')
            return redirect(url_for('animais_disponiveis'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao processar adoção: {str(e)}', 'error')
    
    return render_template('adocao.html', animal=animal, adotante=adotante)

@app.route('/relatorios')
def relatorios():
    if 'usuario_id' not in session or session.get('tipo') != 'ONG':
        flash('Acesso restrito a ONGs.', 'error')
        return redirect(url_for('login'))
    
    animais = Animal.query.all()
    adotantes = Adotante.query.all()
    adocoes = Adocao.query.all()
    
    total_animais = len(animais)
    animais_disponiveis = len([a for a in animais if a.status == 'disponível'])
    animais_adotados = len([a for a in animais if a.status == 'adotado'])
    total_adotantes = len(adotantes)
    total_adocoes = len(adocoes)
    
    return render_template('relatorios.html',
                         animais=animais,
                         adotantes=adotantes,
                         adocoes=adocoes,
                         total_animais=total_animais,
                         animais_disponiveis=animais_disponiveis,
                         animais_adotados=animais_adotados,
                         total_adotantes=total_adotantes,
                         total_adocoes=total_adocoes)

with app.app_context():
    db.create_all()
    
    if not Usuario.query.filter_by(email='admin@larpet.com').first():
        admin = Usuario(
            nome='Admin LarPet',
            email='admin@larpet.com',
            senha=generate_password_hash('admin123'),
            tipo='ONG',
            cnpj='12.345.678/0001-99',
            razao_social='LarPet ONG',
            telefone='(11) 99999-9999',
            endereco='São Paulo - SP',
            responsavel_nome='Administrador',
            responsavel_cpf='123.456.789-10'
        )
        db.session.add(admin)
        db.session.commit()
        print('✓ Usuário admin criado: admin@larpet.com / admin123')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
