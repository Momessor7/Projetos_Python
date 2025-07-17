import sqlite3 #criar, manipular e conectar banco de dados, usar para arq .db
import os #permite interagir com o SO, chegar se existe, criar pastas, etc
from datetime import datetime #classe datetime da biblioteca, pegar data e h extas no cadastro

def start_database(): #função-fzr database
    """Cria o database e a table de pacientes, caso nao exista"""
    conn = sqlite3.connect('pacientes_sincope.db') #conexão com arq pacientes_sincope.db, se n existe, ela cria o arq automaticamente(conn == conexão)
    cursor = conn.cursor() #mouse dentro do database, dar comando(executar queries)

    cursor.execute('''CREATE TABLE IF NOT EXISTS pacientes (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 nome TEXT NOT NULL, 
                   idade INTEGER NOT NULL,
                   profissao TEXT,
                   diagnostico_sugerido TEXT,
                   sintomas_relatados TEXT,
                   data_registro TEXT NOT NULL
                   
                   )
                   ''') #comandos no sql
#id tipo int sendo a chave primária, e a cada novo paciente, o id aumenta sozinho
#nome tipo texto, NOT NULL diz q essa info é obrigatória
#idade do tipo int
#demais comandos de msm valor q os anteriores, sendo respectivos é claro

    conn.commit() #como um botton de "save", confirma as infos
    conn.close() #libera o arq de database, fechando a conexão(boa prática, como o scan.close em java)

def save_patients(nome, idade, profissao, diagnostico, sintomas):
    """Salvar os dados de um novo paciente no database"""
    conn = sqlite3.connect('pacientes_sincope.db')
    cursor = conn.cursor()

    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #método now pra pegar data e hora atual do SO, retornando datetime. Em seguida, o método strftime, pra formatar tempo em texto(conversão de objeto pra string de texto personalizada)
    sintomas_str = ", ".join(sintomas) #transforma uma lista de textos em um único texto, usando ","

    cursor.execute('''
    INSERT INTO pacientes (nome, idade, profissao, diagnostico_sugerido, sintomas_relatados, data_registro)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (nome, idade, profissao, diagnostico, sintomas_str, data_atual)) #passando tupla com variável na ordem exata dos ?, a bib sqlite3 substitui os ? pelos valores
#INSERT INTO = comando SQL p/ add nova linha de dados
#VALUES com ?, servem para uma segurança maior(boas práticas) em vez das variáveis
    conn.commit()
    conn.close()

DIAGNOSTIC_RULES = {
    'Síncope Vasovagal (Reflexa)': {
        'gatilho_emocional': 3, #estress, medo, ansiedade
        'dor_forte_subita': 2,
        'longo_periodo_em_pe': 3,
        'ambiente_quente_fechado': 2,
        'nausea_sudorese_palidez': 3, #sintoma pré-síncope
        'visao_turva_ou_escura': 2,
        'ocorre_apos_miccao_tossir': 2
    },
    'Síncope por Hipotensão Ortostática': {
        'ocorre_ao_levantar_se': 4, #importante
        'tontura_imediata_ao_levantar': 3,
        'uso_de_medicacao_pressao': 2, #diuréticos, anti-hipertensivos
        'desidratacao_recente': 2,
        'comum_em_idosos': 1
    },
    'Síncope Cardíaca': {
        'durante_exercicio_fisico': 4, #importante
        'palpitacoes_antes_desmaio': 3,
        'dor_no_peito_associada': 3,
        'desmaio_subito_sem_aviso': 4, #importante tbm
        'ocorreu_deitado': 3,
        'historico_familiar_morte_subita': 3,
        'doenca_cardiaca_conhecida': 2
    }
} #estrut p/ guardar regras. Chave principal = tipo de síncope, e o valor é um "dicionário" onde a chave é o sintoma e o valor é o "peso" dele

AVAILABLE_SYMPTOMS = {
    'gatilho_emocional': "Desencadeada por estresse, medo, ansiedade ou dor forte.",
    'longo_periodo_em_pe': "Ocorreu após ficar muito tempo em pé.",
    'ambiente_quente_fechado': "Ocorreu em local quente e com muita gente.",
    'nausea_sudorese_palidez': "Sentiu náuseas, suor frio ou ficou pálido(a) antes de desmaiar.",
    'visao_turva_ou_escura': "Teve a visão turva ou escura antes do episódio.",
    'ocorre_apos_miccao_tossir': "Ocorreu logo após urinar, tossir ou engolir.",
    'ocorre_ao_levantar_se': "Ocorreu logo após se levantar (de uma cadeira ou da cama).",
    'tontura_imediata_ao_levantar': "Sente tontura frequentemente ao se levantar.",
    'uso_de_medicacao_pressao': "Faz uso de medicamentos para pressão alta ou diuréticos.",
    'desidratacao_recente': "Esteve desidratado(a) ou teve vômitos/diarreia recentemente.",
    'durante_exercicio_fisico': "O desmaio ocorreu DURANTE um esforço físico.",
    'palpitacoes_antes_desmaio': "Sentiu o coração bater rápido ou de forma irregular antes do desmaio.",
    'dor_no_peito_associada': "Sentiu dor no peito antes ou durante o episódio.",
    'desmaio_subito_sem_aviso': "O desmaio foi súbito, sem nenhum sintoma de aviso.",
    'ocorreu_deitado': "O desmaio ocorreu enquanto estava deitado(a).",
    'historico_familiar_morte_subita': "Há casos de morte súbita em familiares próximos.",
    'doenca_cardiaca_conhecida': "O paciente já possui diagnóstico de alguma doença cardíaca."
} #descrição dos sintomas

def diagnosis_syncope(sintomas_selecionados): #função p/ fzr o cálculo
    """analisar sintomas e retornar o diagnóstico + provável"""
    if not sintomas_selecionados: #checa se a lista de sintomas está vazia
        return "Nenhum sintoma selecionado. Não é possível sugerir um diagnóstico.", 0 #se estiver vazia, a função para e retorna a mensagem de aviso e o peso 0
    
    scores = {
        'Síncope Vasovagal (Reflexa)': 0,
        'Síncope por Hipotensão Ortostática': 0,
        'Síncope Cardíaca': 0
        } #começar zerado para cada tipo

    #calcular peso para cada tipo
    for sintoma in sintomas_selecionados: #percorre a lista dos sintomas q o user escolheu
        for tipo, regras in DIAGNOSTIC_RULES.items(): #percorre as regras, a cada vez o tipo = vasovagal e regras = gatilho_emocional = 3(ex)
            if sintoma in regras: #checa se o sintoma existe nas regras do tipo atual
                scores[tipo] += regras[sintoma] #se o sintoma existir, add o peso correspondente

    max_score = max(scores.values()) #encontrar tipo com maior peso

    if max_score == 0: #se o peso = 0, nenhum sintoma correspondia a nenhuma regra
        return "Inconclusivo com base nos sintomas fornecidos.", 0 #função para e retorna a mensagem com diagnóstico = 0

    #encontrar o diagnostico com maior peso
    diagnostico_provavel = max(scores, key=scores.get) #max(scores) pegaria o nome do diagnóstico q vem na ordem alfabética, com o key=scores.get, diz ao max p/ n olhar os nomes e sim para os valores associados, retornando a chave q tem o maior valor
    return diagnostico_provavel, max_score

def main():
    """Função principal q exec o programa"""
    start_database()

    print("=" * 70) #imprimir o =, 70 vezes(mais bonito)
    print("         SISTEMA DE APOIO À CLASSIFICAÇÃO DE SÍNCOPE")
    print("=" * 70)
    print("AVISO IMPORTANTE:\nEste programa é uma ferramenta de apoio educacional e NÃO SUBSTITUI uma avaliação médica profissional. O diagnóstico de síncope é complexo e deve ser realizado por um médico qualificado.")

    while True: #loop infinito
        nome = input("\nNome do paciente: ") #user digitar e pressionar ENTER, texto digitado = retornado e guardado na variável
        while True: #validar idade
            try:
                idade = int(input("Idade do paciente: ")) #obriga a idade a ser um int
                break
            except ValueError: #caso falhe a conversão para int
                print("Pfv, insira um número válido para a idade.")
        profissao = input("Profissão do paciente: ")

        print("\n===== Seleção de Sintomas =====")
        print("Selecione todos os sintomas que o paciente apresentou:")

        sintomas_key = list(AVAILABLE_SYMPTOMS.keys()) #pega tds as chaves de sintomas e com o list, converte as chaves em uma lista, acessando por índices numéricos
        for i, key in enumerate(sintomas_key): #enumerate para percorrer a lista de chaves, nos dando o indice i e a key(chave do sintoma)
            print(f" {i+1:2d}. {AVAILABLE_SYMPTOMS[key]}") #imprime a lista de sintomas de forma numerada, i+1(começar em 1 e n em 0); :2d(garante q o número ocupe smp 2 dígitos(melhor visualmente)). No final usa a key pra pegar a descrição completa

        sintomas_selecionados_indices = input("\nDigite os números dos sintomas, separados por vírgula (ex: 1, 4, 11, ...): ")

        sintomas_paciente_keys = []
        try:
            indices = [int(i.strip()) - 1 for i in sintomas_selecionados_indices.split(',')] #split pega a string e a quebra em uma lista de strings(ex: "1, 5, 8" == ['1', '5', '8']). For percorre a lista, usando strip para remover espaços em branco do início ao fim, converte para int e subtrai 1 para converter o número do user de 1 p/ 0
            for i in indices: #percorre a lista q acabamos de criar
                if 0 <= i < len(sintomas_key): #verificar se o indice é válido(entre 0 e o total de sintomas)
                    sintomas_paciente_keys.append(sintomas_key[i]) #se for válido, pega a chave correspondente e add a lista final de sintomas_paciente_keys
                else:
                    print(f"AVISO: Número '{i+1}' é inválido e será ignorado.")
        except ValueError:
            print("AVISO: Entrada de sintomas inválida. Nenhum sintoma foi selecionado.")

        diagnostico, score = diagnosis_syncope(sintomas_paciente_keys) #chama a função, passa a lista de sintomas e retorna diagnostico e score

        print("\n===== Resultado da Análise =====")
        print(f"Paciente: {nome}, {idade} anos")
        print("Sintomas Relatados:")
        if sintomas_paciente_keys: #checar se a lista n está vazia, se estiver nao roda o if
            for key in sintomas_paciente_keys:
                print(f" - {AVAILABLE_SYMPTOMS[key]}") #percorre a lista para imprimi-los
        else:
            print(" - Nenhum sintoma válido selecionado.")

        print("\nSugestão de Classificação:")
        print(f" -> {diagnostico}") #f-string

        if "Cardíaca" in diagnostico: #se no diagnóstico tiver a palavra Cardíaca
            print("\n [ALERTA] A suspeita de síncope cardíaca é a mais perigosa.")
            print(" Recomenda-se avaliação cardiológica urgente(Eletrocardiograma, etc).") #imprime os alertas de urgência

        #salvar no database
        sintomas_descricoes = [AVAILABLE_SYMPTOMS[key] for key in sintomas_paciente_keys] #cria lista com as descrições completas dos sintomas, para salvar no database
        save_patients(nome, idade, profissao, diagnostico, sintomas_descricoes) #chama função de salvar, com as infos coletadas
        
        print("-" * 70)
        continuar = input("\nDeseja registrar um novo paciente? (s/n): ").lower() #lower converte a resposta para minúscula, caso digite "S"
        if continuar != 's': #se n for "s/S" acaba
            break

    print("\nSe cuida!")

if __name__ == "__main__":
    main()
