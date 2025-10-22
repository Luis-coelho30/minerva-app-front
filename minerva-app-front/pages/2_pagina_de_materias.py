import streamlit as st
from utils import setup_logged
from menu import menu_with_redirect

st.set_page_config(page_title="Materias", page_icon="./images/Minerva_logo.jpeg", layout="wide")   # define qual nome a aba vai ter no navegador

largura_logo_home = 150

setup_logged()  # define a cor de fundo e que a pagina comeca mais pra cima pra logo ficar mais alta

menu_with_redirect()

def add_nota():
    with st.form(f"form_nota_", clear_on_submit=True):
            st.write("**Adicionar nova nota**")
            cols_form = st.columns([2,1,1])
            with cols_form[0]:
                desc_nota = st.text_input("Descrição da Nota (Ex: P1, T1)")
            with cols_form[1]:
                valor_nota = st.number_input("Valor", min_value=0.0, max_value=10.0, step=0.1)
            with cols_form[2]:
                peso_nota = st.number_input("Peso", min_value=0.0, step=0.5)
            
            if st.form_submit_button("Adicionar Nota"):
                if desc_nota and peso_nota > 0:
                    #db.add_nota(user_id, disciplina['id'], desc_nota, valor_nota, peso_nota)
                    st.rerun()
                else:
                    st.warning("Descrição e peso (maior que zero) são obrigatórios.")


with st.expander(icon=":material/add:",label="Criar nova materia"):
     with st.form("nova_disciplina_form", clear_on_submit=True):
        nome = st.text_input("Nome da Disciplina")
        descricao = st.text_area("Descrição (Opcional)")
        media_necessaria = st.number_input("Média Necessária para Aprovação", min_value=0.0, max_value=10.0, value=7.0, step=0.5)
        faltas = st.number_input("Faltas até agora", min_value=0, step=1)
        creditos = st.number_input("Créditos", min_value=0, step=1, format="%d")
        
        enviado = st.form_submit_button("Adicionar Disciplina")
        # envia os dados pro banco de dados
st.markdown("---")

# pegar as disciplinas do BD e mostrar

# exemplo
for n in range(10):
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader("Disciplina de Exemplo ")
            st.write(f"**Créditos:** N/A | **Média Necessária:** N/A")

        #with st.expander("Gerenciar Notas"):
            #notas = db.get_notas_by_disciplina(disciplina['id'], user_id)
            # if notas:
            #     # Cabeçalho da lista de notas
            #     header_cols = st.columns([4, 2, 2, 1])
            #     header_cols[0].write("**Descrição**")
            #     header_cols[1].write("**Valor**")
            #     header_cols[2].write("**Peso**")
                
            #     st.markdown("---")

            #     for nota in notas:
            #         row_cols = st.columns([4, 2, 2, 1])
            #         row_cols[0].write(nota['descricao'])
            #         row_cols[1].write(nota['valor'])
            #         row_cols[2].write(nota['peso'])
            #         # Botão para deletar a nota
            #         if row_cols[3].button("🗑️", key=f"del_nota_{nota['id']}", help="Deletar nota"):
            #             #db.delete_nota(nota['id'], user_id)
            #             st.rerun()
            # else:
            #     st.info("Nenhuma nota cadastrada para esta disciplina.")
        with st.expander(icon=":material/add:",label="Adicionar nova nota", expanded=False):
            with st.form(f"form_nota_{n}", clear_on_submit=True):
                    st.write("**Adicionar nova nota**")
                    cols_form = st.columns([2,1,1])
                    with cols_form[0]:
                        desc_nota = st.text_input("Descrição da Nota (Ex: P1, T1)")
                    with cols_form[1]:
                        valor_nota = st.number_input("Valor", min_value=0.0, max_value=10.0, step=0.1)
                    with cols_form[2]:
                        peso_nota = st.number_input("Peso", min_value=0.0, step=0.5)
                    
                    if st.form_submit_button("Adicionar Nota"):
                        if desc_nota and peso_nota > 0:
                            #db.add_nota(user_id, disciplina['id'], desc_nota, valor_nota, peso_nota)
                            st.rerun()
                        else:
                            st.warning("Descrição e peso (maior que zero) são obrigatórios.")
        

        
    

    