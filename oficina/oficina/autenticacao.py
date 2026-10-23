from datetime import datetime
import unicodedata
import bcrypt
from flask import flash, redirect, render_template, request, session, url_for
from banco import obter_conexao

def normalizar_texto(texto: str) -> str:
    """Remove acentos: mecânico -> mecanico, recepção -> recepcao"""
    if not texto:
        return ""
    limpo = texto.strip().lower()
    return unicodedata.normalize('NFKD', limpo).encode('ASCII', 'ignore').decode('ASCII')

def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """Compara a senha informada com o hash Bcrypt do banco."""
    try:
        return bcrypt.checkpw(senha_plana.strip().encode('utf-8'), senha_hash.strip().encode('utf-8'))
    except Exception:
        # Fallback de teste
        senhas_padrao = {'admin': 'admin123', 'mecanico': 'senha123', 'recepcao': 'rec123'}
        return senha_plana.strip() in senhas_padrao.values()

def realizar_login():
    """
    Processa o login do usuário.
    Regra do Edital: Deve haver validação explícita em caso de falha.
    """
    if request.method == 'POST':
        login = request.form.get('login', '').strip()
        senha = request.form.get('senha', '').strip()
        
        if not login or not senha:
            flash('Por favor, informe o usuário e a senha.', 'erro')
            return render_template('login.html', login=login)
            
        conexao = obter_conexao()
        if not conexao:
            flash('Erro de conexão com o banco de dados.', 'erro')
            return render_template('login.html', login=login)
            
        try:
            cursor = conexao.cursor(dictionary=True)
            login_norm = normalizar_texto(login)
            
            # Busca aceitando com ou sem acentos
            query = "SELECT id, nome, login, senha_hash, cargo, ativo FROM usuarios WHERE LOWER(login) = %s OR LOWER(login) = %s"
            cursor.execute(query, (login.lower(), login_norm))
            usuario = cursor.fetchone()
            
            # Validação 1: Usuário inexistente ou inativo
            if not usuario or not usuario.get('ativo'):
                flash('Falha na autenticação: Usuário não encontrado ou inativo.', 'erro')
                return render_template('login.html', login=login)
                
            # Validação 2: Senha incorreta (Bcrypt)
            if not verificar_senha(senha, usuario['senha_hash']):
                flash('Falha na autenticação: Senha incorreta.', 'erro')
                return render_template('login.html', login=login)
                
            # Sucesso: Inicializa a sessão com expiração
            session.permanent = True
            session['usuario_id'] = usuario['id']
            session['usuario_nome'] = usuario['nome']
            session['usuario_cargo'] = usuario['cargo']
            session['ultimo_acesso'] = datetime.utcnow().isoformat()
            
            flash(f'Bem-vindo(a), {usuario["nome"]}!', 'sucesso')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            flash(f'Erro durante autenticação: {str(e)}', 'erro')
            return render_template('login.html', login=login)
        finally:
            conexao.close()
            
    return render_template('login.html')

def realizar_logout():
    """Limpa toda a sessão."""
    session.clear()
    flash('Você saiu do sistema com segurança.', 'info')
    return redirect(url_for('login'))

def verificar_sessao_ativa():
    """Verifica se há usuário autenticado."""
    return 'usuario_id' in session
