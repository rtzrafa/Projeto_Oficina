import re
import bcrypt
from flask import flash, redirect, render_template, request, url_for
from banco import obter_conexao

def validar_cpf_digitos(cpf_str: str) -> bool:
    """
    Regra do Edital: No CPF, valide apenas o número de dígitos,
    não é necessário validar se o CPF é real.
    """
    apenas_numeros = re.sub(r'\D', '', cpf_str)
    return len(apenas_numeros) == 11

def criptografar_cpf(cpf_str: str) -> str:
    """
    Regra do Edital: O CPF dos clientes deve ser armazenado de forma
    criptografada no banco de dados (LGPD).
    """
    apenas_numeros = re.sub(r'\D', '', cpf_str)
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(apenas_numeros.encode('utf-8'), salt).decode('utf-8')

def listar_clientes():
    """
    Regra do Edital: Busca para inserir termo e, após confirmação,
    exibir listagem atualizada correspondente.
    """
    termo = request.args.get('busca', '').strip()
    conexao = obter_conexao()
    clientes = []
    
    if conexao:
        try:
            cursor = conexao.cursor(dictionary=True)
            if termo:
                param = f"%{termo}%"
                query = """
                    SELECT id, nome, cpf, cpf_hash, telefone, email, endereco, data_cadastro
                    FROM clientes
                    WHERE nome LIKE %s OR cpf LIKE %s OR email LIKE %s OR telefone LIKE %s
                    ORDER BY nome ASC
                """
                cursor.execute(query, (param, param, param, param))
            else:
                cursor.execute("SELECT id, nome, cpf, cpf_hash, telefone, email, endereco, data_cadastro FROM clientes ORDER BY nome ASC")
            clientes = cursor.fetchall()
        finally:
            conexao.close()
            
    return render_template('clientes.html', clientes=clientes, termo_busca=termo)

def cadastrar_cliente():
    """Cadastra cliente validando 11 dígitos e aplicando Bcrypt no CPF."""
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        cpf_bruto = request.form.get('cpf', '').strip()
        telefone = request.form.get('telefone', '').strip()
        email = request.form.get('email', '').strip()
        endereco = request.form.get('endereco', '').strip()
        
        # Validação obrigatória de 11 dígitos
        if not validar_cpf_digitos(cpf_bruto):
            flash('Erro no CPF: O CPF deve conter exatamente 11 dígitos numéricos.', 'erro')
            return redirect(url_for('clientes_view'))
            
        numeros = re.sub(r'\D', '', cpf_bruto)
        cpf_formatado = f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"
        cpf_hash = criptografar_cpf(numeros)
        
        conexao = obter_conexao()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = """
                    INSERT INTO clientes (nome, cpf, cpf_hash, telefone, email, endereco, data_cadastro)
                    VALUES (%s, %s, %s, %s, %s, %s, CURRENT_DATE)
                """
                cursor.execute(sql, (nome, cpf_formatado, cpf_hash, telefone, email, endereco))
                conexao.commit()
                flash('Cliente cadastrado com sucesso! CPF armazenado com hash Bcrypt.', 'sucesso')
            except Exception as e:
                flash(f'Erro ao cadastrar: {str(e)}', 'erro')
            finally:
                conexao.close()
                
    return redirect(url_for('clientes_view'))

def editar_cliente(cliente_id: int):
    """
    Regra do Edital: Permitir editar os dados de um cliente já cadastrado,
    salvando a alteração no banco de dados.
    """
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        telefone = request.form.get('telefone', '').strip()
        email = request.form.get('email', '').strip()
        endereco = request.form.get('endereco', '').strip()
        
        conexao = obter_conexao()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = "UPDATE clientes SET nome = %s, telefone = %s, email = %s, endereco = %s WHERE id = %s"
                cursor.execute(sql, (nome, telefone, email, endereco, cliente_id))
                conexao.commit()
                flash('Dados do cliente atualizados com sucesso!', 'sucesso')
            except Exception as e:
                flash(f'Erro ao atualizar: {str(e)}', 'erro')
            finally:
                conexao.close()
                
    return redirect(url_for('clientes_view'))

def excluir_cliente(cliente_id: int):
    """Exclui cliente."""
    conexao = obter_conexao()
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM clientes WHERE id = %s", (cliente_id,))
            conexao.commit()
            flash('Cliente removido com sucesso.', 'sucesso')
        finally:
            conexao.close()
    return redirect(url_for('clientes_view'))
