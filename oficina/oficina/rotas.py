from datetime import datetime
from flask import redirect, render_template, request, session, url_for
import autenticacao
import clientes
import veiculos
import agendamento
from banco import obter_conexao

def registrar_rotas(app):
    
    # Interceptor de segurança: Expiração e autenticação obrigatória
    @app.before_request
    def checar_seguranca():
        rotas_livres = ['login', 'static']
        if request.endpoint in rotas_livres or request.endpoint is None:
            return
            
        if not autenticacao.verificar_sessao_ativa():
            session.clear()
            return redirect(url_for('login'))
            
        session['ultimo_acesso'] = datetime.utcnow().isoformat()

    # Context processor: Injeta o nome do usuário logado em todos os templates HTML
    @app.context_processor
    def injetar_dados():
        return {
            'usuario_logado': session.get('usuario_nome'),
            'usuario_cargo': session.get('usuario_cargo')
        }

    # Rotas de Autenticação
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return autenticacao.realizar_login()

    @app.route('/logout')
    def logout():
        return autenticacao.realizar_logout()

    # Dashboard Principal
    @app.route('/dashboard')
    def dashboard():
        con = obter_conexao()
        tot_c = 0; tot_v = 0; tot_a = 0; proximos = []
        if con:
            cur = con.cursor(dictionary=True)
            cur.execute("SELECT COUNT(*) AS total FROM clientes"); tot_c = cur.fetchone()['total']
            cur.execute("SELECT COUNT(*) AS total FROM veiculos"); tot_v = cur.fetchone()['total']
            cur.execute("SELECT COUNT(*) AS total FROM agendamentos"); tot_a = cur.fetchone()['total']
            cur.execute("""
                SELECT a.id, a.data_agendamento, a.descricao_servico, a.status,
                       c.nome AS cliente_nome, v.placa, v.modelo
                FROM agendamentos a
                JOIN clientes c ON a.cliente_id = c.id
                JOIN veiculos v ON a.veiculo_id = v.id
                ORDER BY a.data_agendamento ASC LIMIT 5
            """)
            proximos = cur.fetchall()
            con.close()
        return render_template('dashboard.html', total_clientes=tot_c, total_veiculos=tot_v, total_agendamentos=tot_a, proximos_servicos=proximos)

    # Clientes
    @app.route('/clientes')
    def clientes_view(): return clientes.listar_clientes()

    @app.route('/clientes/novo', methods=['POST'])
    def clientes_novo(): return clientes.cadastrar_cliente()

    @app.route('/clientes/editar/<int:id>', methods=['POST'])
    def clientes_editar(id): return clientes.editar_cliente(id)

    @app.route('/clientes/excluir/<int:id>')
    def clientes_excluir(id): return clientes.excluir_cliente(id)

    # Veículos
    @app.route('/veiculos')
    def veiculos_view(): return veiculos.listar_veiculos()

    @app.route('/veiculos/novo', methods=['POST'])
    def veiculos_novo(): return veiculos.cadastrar_veiculo()

    @app.route('/veiculos/editar/<int:id>', methods=['POST'])
    def veiculos_editar(id): return veiculos.editar_veiculo(id)

    @app.route('/veiculos/excluir/<int:id>')
    def veiculos_excluir(id): return veiculos.excluir_veiculo(id)

    # Agendamentos
    @app.route('/agendamentos')
    def agendamentos_view(): return agendamento.listar_agendamentos()

    @app.route('/agendamentos/novo', methods=['POST'])
    def agendamentos_novo(): return agendamento.cadastrar_agendamento()

    @app.route('/agendamentos/atualizar-data/<int:id>', methods=['POST'])
    def agendamentos_atualizar_data(id): return agendamento.atualizar_data_agendamento(id)

    @app.route('/agendamentos/excluir/<int:id>')
    def agendamentos_excluir(id): return agendamento.excluir_agendamento(id)
