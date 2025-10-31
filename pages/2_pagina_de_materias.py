import streamlit as st
from utils import setup_logged
from menu import menu_with_redirect

st.set_page_config(page_title="Materias", page_icon="./images/Minerva_logo.jpeg", layout="wide")   # define qual nome a aba vai ter no navegador

largura_logo_home = 150

setup_logged()  # define a cor de fundo e que a pagina comeca mais pra cima pra logo ficar mais alta

menu_with_redirect()

disciplina_api = st.session_state.disc_api
nota_api = st.session_state.grade_api

@st.dialog("Modificar Nota")
def editar_nota_dialog(nota_para_editar):
    with st.form("editar_nota_form"):
        st.write("**Modificar nota**")
        
        # Inputs pré-preenchidos com os valores atuais da nota
        nova_desc = st.text_input("Descrição", value=nota_para_editar["descricao"])
        novo_valor = st.number_input("Valor", min_value=0.0, max_value=10.0, step=0.1, value=nota_para_editar["valor"])
        novo_peso = st.number_input("Peso", min_value=1, step=1, format="%d", value=nota_para_editar["peso"])
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Salvar"):
                try:
                    nota_api.update_grade(nota_para_editar["id"], nova_desc, novo_valor, novo_peso, nota_para_editar["disciplinaId"])                    
                    st.toast("Nota atualizada com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao atualizar a nota: {e}")
        
        with col2:
            if st.form_submit_button("Cancelar", type="secondary"):
                st.rerun()

@st.dialog("Modificar Disciplina")
def editar_disciplina_dialog(disciplina_para_editar):
    with st.form("editar_disciplina_form"):
        st.write("**Modificar Disciplina**")
        
        novo_nome = st.text_input("Nome da Disciplina", value=disciplina_para_editar["nome"])
        nova_descricao = st.text_area("Descrição (Opcional)", value=disciplina_para_editar.get("descricao", ""))
        nova_media = st.number_input("Média Necessária", min_value=0.0, max_value=10.0, step=0.5, value=disciplina_para_editar["mediaNecessaria"])
        novos_creditos = st.number_input("Créditos", min_value=1, step=1, format="%d", value=disciplina_para_editar["creditos"])
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Salvar"):
                try:
                    disciplina_api.update_discipline(
                        discId=disciplina_para_editar['id'], nome=novo_nome, descricao=nova_descricao, 
                        arquivada=disciplina_para_editar['arquivada'], mediaNecessaria=nova_media, creditos=novos_creditos
                    )
                    st.toast("Disciplina atualizada com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao atualizar a disciplina: {e}")
        with col2:
            if st.form_submit_button("Cancelar", type="secondary"):
                st.rerun()

def add_nota(disciplina_id: int):
    with st.expander(icon=":material/add:", label="Adicionar nota"):
        with st.form(f"form_nota_{disciplina_id}", clear_on_submit=True):
                st.write("**Adicionar nova nota**")
                cols_form = st.columns([2,1,1])
                with cols_form[0]:
                    desc_nota = st.text_input("Descrição da Nota (Ex: P1, A1)")
                with cols_form[1]:
                    valor_nota = st.number_input("Valor", min_value=0.0, max_value=10.0, step=0.1)
                with cols_form[2]:
                    peso_nota = st.number_input("Peso", min_value=0, step=1, format="%d")

                if st.form_submit_button("Adicionar Nota"):
                    if desc_nota and peso_nota > 0:
                        nota_api.create_grade(desc_nota, valor_nota, peso_nota, disciplina_id)
                        st.rerun()
                    else:
                        st.warning("Descrição e peso (maior que zero) são obrigatórios.")

def mostrar_nota(disciplina_id: int):
    with st.expander("Ver notas"):
        try:
            lista_de_notas = nota_api.list_grades_by_discipline(disciplina_id)
            if not lista_de_notas:
                st.info("Você ainda não cadastrou nenhuma nota na matéria. Adicione uma acima!")
            else:
                # Itera sobre cada dicionário de nota na lista
                for nota in lista_de_notas:
                    with st.container(border=True):
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            valor_nota = nota.get('valor')
                            valor_formatado = f"{valor_nota:.2f}" if isinstance(valor_nota, (int, float)) else "N/A"
                            st.subheader(nota.get("descricao", "Descrição não informada"))
                            st.write(f"**Valor:** {valor_formatado} | **Peso:** {nota.get('peso', 'N/A')}")                        
                        with col2:
                            if st.button("Editar", key=f"edit_nota_{nota.get('id')}", use_container_width=True):
                                nota_selecionada = {
                                    "id": nota.get("id"),
                                    "descricao": nota.get("descricao"),
                                    "valor": nota.get("valor"),
                                    "peso": nota.get("peso"),
                                    "disciplinaId": disciplina_id
                                }
                                editar_nota_dialog(nota_selecionada)
                        with col3:
                            delete_popover = st.popover("Excluir", use_container_width=True)
                            with delete_popover:
                                st.write(f"Tem certeza que deseja excluir a nota '{nota.get('descricao')}'?")
                                if st.button("Confirmar Exclusão", type="primary", key=f"confirm_delete_nota_{nota.get('id')}"):
                                    try:
                                        nota_api.delete_grade(nota.get('id'))
                                        st.toast(f"Nota '{nota.get('descricao')}' excluída!")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Erro ao excluir a nota: {e}")
        except Exception as e:
            st.error(f"Não foi possível carregar as notas. Erro: {e}")

with st.expander(icon=":material/add:",label="Criar nova materia"):
     with st.form("nova_disciplina_form", clear_on_submit=True):
        nome = st.text_input("Nome da Disciplina")
        descricao = st.text_area("Descrição (Opcional)")
        media_necessaria = st.number_input("Média Necessária para Aprovação", min_value=0.0, max_value=10.0, value=7.0, step=0.5)
        creditos = st.number_input("Créditos", min_value=0, step=1, format="%d")
        
        enviado = st.form_submit_button("Adicionar Disciplina")
        if enviado:
            if nome == "":
                st.error("Nome é um campo obrigatório")
            elif media_necessaria == 0.0:
                st.error("Média deve ser maior que 0")
            elif creditos == 0:
                st.error("Créditos deve ser maior que 0")
            else:
                disciplina_api.create_discipline(nome, descricao, False, media_necessaria, creditos)
                st.success(f"Disciplina '{nome}' criada com sucesso!")
                st.rerun()
st.markdown("---")

# Pega as disciplinas do banco de dados e as exibe
try:
    lista_de_disciplinas = disciplina_api.list_user_discipline()

    # Separa as disciplinas em ativas e arquivadas
    disciplinas_ativas = [d for d in lista_de_disciplinas if not d.get('arquivada', False)]
    disciplinas_arquivadas = [d for d in lista_de_disciplinas if d.get('arquivada', False)]

    if not disciplinas_ativas:
        st.info("Você ainda não cadastrou nenhuma matéria. Adicione uma acima!")
    else:
        # Itera sobre as disciplinas ativas
        for disciplina in disciplinas_ativas:
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
                with col1:
                    st.subheader(disciplina.get("nome", "Nome não informado"))
                    st.write(
                        f"**Créditos:** {disciplina.get('creditos', 'N/A')} | "
                        f"**Média Necessária:** {disciplina.get('mediaNecessaria', 'N/A')} | "
                        f"**Média atual:** {disciplina.get('media_atual', 'N/A')}"
                    )
                    add_nota(disciplina.get("id"))
                    mostrar_nota(disciplina.get("id"))
                with col2:
                    if st.button("Editar", key=f"edit_disc_{disciplina.get('id')}", use_container_width=True):
                        disciplina_selecionada = {
                            "id": disciplina.get('id'),
                            "nome": disciplina.get('nome'),
                            "descricao": disciplina.get('descricao'),
                            "mediaNecessaria": disciplina.get('mediaNecessaria'),
                            "creditos": disciplina.get('creditos'),
                            "arquivada": disciplina.get('arquivada', False)
                        }
                        editar_disciplina_dialog(disciplina_selecionada)
                with col3:
                    archive_popover = st.popover("Arquivar", use_container_width=True, help="Arquivar a matéria para escondê-la da lista principal.")
                    with archive_popover:
                        st.write(f"Tem certeza que deseja arquivar a matéria '{disciplina.get('nome')}'?")
                        if st.button("Confirmar", type="primary", key=f"confirm_archive_{disciplina.get('id')}"):
                            try:
                                disciplina_api.update_discipline(
                                    discId=disciplina.get('id'),
                                    nome=disciplina.get('nome'),
                                    descricao=disciplina.get('descricao'),
                                    arquivada=True,  # Mudar para arquivada
                                    mediaNecessaria=disciplina.get('mediaNecessaria'),
                                    creditos=disciplina.get('creditos')
                                )
                                st.toast(f"Matéria '{disciplina.get('nome')}' arquivada.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Erro ao arquivar a matéria: {e}")
                with col4:
                    delete_popover = st.popover("Excluir", use_container_width=True, help="Excluir a matéria permanentemente. Esta ação não pode ser desfeita.")
                    with delete_popover:
                        st.write(f"Tem certeza que deseja excluir a matéria '{disciplina.get('nome')}' permanentemente?")
                        if st.button("Confirmar Exclusão", type="primary", key=f"confirm_delete_active_disc_{disciplina.get('id')}"):
                            try:
                                disciplina_api.delete_discipline(disciplina.get('id'))
                                st.toast(f"Matéria '{disciplina.get('nome')}' excluída!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Erro ao excluir a matéria: {e}")

    # Adiciona o dropdown para matérias arquivadas
    if disciplinas_arquivadas:
        with st.expander("Matérias Arquivadas"):
            for disciplina in disciplinas_arquivadas:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([4, 1, 1])
                    with col1:
                        st.subheader(f"*(Arquivada)* {disciplina.get('nome', 'Nome não informado')}")
                    with col2:                        
                        if st.button("Desarquivar", key=f"unarchive_{disciplina.get('id')}", use_container_width=True):
                            try:
                                disciplina_api.update_discipline(
                                    discId=disciplina.get('id'),
                                    nome=disciplina.get('nome'),
                                    descricao=disciplina.get('descricao'),
                                    arquivada=False,  # Mudar para não arquivada
                                    mediaNecessaria=disciplina.get('mediaNecessaria'),
                                    creditos=disciplina.get('creditos')
                                )
                                st.toast(f"Matéria '{disciplina.get('nome')}' desarquivada.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Erro ao desarquivar a matéria: {e}")
                    with col3:
                        delete_popover = st.popover("Excluir", use_container_width=True, help="Excluir a matéria permanentemente. Esta ação não pode ser desfeita.") # nao funciona alguem me ajuda plmds erro
                        with delete_popover:
                            st.write(f"Tem certeza que deseja excluir a matéria '{disciplina.get('nome')}' permanentemente?")
                            if st.button("Confirmar Exclusão", type="primary", key=f"confirm_delete_disc_{disciplina.get('id')}"):
                                try:
                                    disciplina_api.delete_discipline(disciplina.get('id'))
                                    st.toast(f"Matéria '{disciplina.get('nome')}' excluída!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Erro ao excluir a matéria: {e}")
except Exception as e:
    st.error(f"Não foi possível carregar as disciplinas. Erro: {e}")
