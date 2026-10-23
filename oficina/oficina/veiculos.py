from flask import flash, redirect, render_template, request, url_for
from banco import obter_conexao

def listar_veiculos():
    """Lista veículos com dados do cliente proprietário."""
    conexao = obter_conexao()
    veiculos = []
    clientes = []
    
    if conexao:
        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("""
                SELECT v.id, v.cliente_id, v.placa, v.marca, v.modelo, v.ano, v.cor, v.quilometragem,
                       c.nome AS cliente_nome, c.telefone AS cliente_telefone
                FROM veiculos v
                JOIN clientes c ON v.cliente_id = c.id
                ORDER BY v.modelo ASC
            """)
            veiculos = cursor.fetchall()
            
            # Carrega clientes para o select do modal de cadastro
            cursor.execute("SELECT id, nome, cpf FROM clientes ORDER BY nome ASC")
            clientes = cursor.fetchall()
        finally:
            conexao.close()
            
    return render_template('veiculos.html', veiculos=veiculos, clientes=clientes)

def cadastrar_veiculo():
    """
    Regra do Edital: Ao cadastrar um novo veículo, o usuário DEVE
    associá-lo a um cliente previamente cadastrado.
    """
    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        placa = request.form.get('placa', '').strip().upper()
        marca = request.form.get('marca', '').strip()
        modelo = request.form.get('modelo', '').strip()
        ano = request.form.get('ano')
        cor = request.form.get('cor', '').strip()
        km = request.form.get('quilometragem', '0').strip()
        
        # Validação obrigatória da chave estrangeira
        if not cliente_id or not cliente_id.isdigit():
            flash('Regra Violada: É obrigatório associar o veículo a um cliente previamente cadastrado.', 'erro')
            return redirect(url_for('veiculos_view'))
            
        conexao = obter_conexao()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = """
                    INSERT INTO veiculos (cliente_id, placa, marca, modelo, ano, cor, quilometragem)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (cliente_id, placa, marca, modelo, int(ano), cor, int(km or 0)))
                conexao.commit()
                flash(f'Veículo {modelo} ({placa}) cadastrado e associado com sucesso!', 'sucesso')
            except Exception as e:
                flash(f'Erro ao cadastrar veículo: {str(e)}', 'erro')
            finally:
                conexao.close()
                
    return redirect(url_for('veiculos_view'))

def editar_veiculo(veiculo_id: int):
    """
    Atualiza os dados de um veículo cadastrado (Cliente proprietário, placa, modelo, etc.)
    salvando a alteração no banco de dados.
    """
    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        placa = request.form.get('placa', '').strip().upper()
        marca = request.form.get('marca', '').strip()
        modelo = request.form.get('modelo', '').strip()
        ano = request.form.get('ano')
        cor = request.form.get('cor', '').strip()
        km = request.form.get('quilometragem', '0').strip()
        
        if not cliente_id or not cliente_id.isdigit():
            flash('Erro: É obrigatório associar o veículo a um cliente.', 'erro')
            return redirect(url_for('veiculos_view'))
            
        conexao = obter_conexao()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = """
                    UPDATE veiculos 
                    SET cliente_id = %s, placa = %s, marca = %s, modelo = %s, ano = %s, cor = %s, quilometragem = %s
                    WHERE id = %s
                """
                cursor.execute(sql, (cliente_id, placa, marca, modelo, int(ano), cor, int(km or 0), veiculo_id))
                conexao.commit()
                flash('Veículo atualizado com sucesso no banco de dados!', 'sucesso')
            except Exception as e:
                flash(f'Erro ao atualizar veículo: {str(e)}', 'erro')
            finally:
                conexao.close()
                
    return redirect(url_for('veiculos_view'))

def excluir_veiculo(veiculo_id: int):
    """Exclui veículo."""
    conexao = obter_conexao()
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM veiculos WHERE id = %s", (veiculo_id,))
            conexao.commit()
            flash('Veículo excluído com sucesso.', 'sucesso')
        finally:
            conexao.close()
    return redirect(url_for('veiculos_view'))
