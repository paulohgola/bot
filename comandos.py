from db import adicionar_despesa, listar_despesas, deletar_despesa
from datetime import datetime
import telebot.types  # Adicione esta linha

def registrar_comandos(bot, user_data, despesas, gerar_grafico):
    @bot.message_handler(commands=['help', 'start'])
    def send_welcome(message):
        bot.reply_to(message, """\
Olá!! Me chamo Expenses Bot, o seu bot de gastos favorito!
Aqui está uma lista de todos os meus comandos que você pode utilizar!
/adicionardespesa - Adiciona uma nova despesa
/grafico - Mostra um gráfico das despesas
/comandos - Lista todos os comandos
/help - Mostra esta mensagem de ajuda
/listardespesas - Lista todas as despesas
/deletardespesa - Deleta uma despesa
/salvarplanilha - Salva as despesas em uma planilha
""")

    @bot.message_handler(commands=['adicionardespesa'])
    def adicionar_despesa_cmd(message):  # Renomeado para evitar conflito
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton('Alimentação', callback_data='cat_alimentacao'),
            telebot.types.InlineKeyboardButton('Transporte', callback_data='cat_transporte'),
            telebot.types.InlineKeyboardButton('Lazer', callback_data='cat_lazer'),
            telebot.types.InlineKeyboardButton('Outros', callback_data='cat_outros')
        )
        bot.send_message(message.chat.id, "Escolha a categoria da despesa:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('cat_'))
    def categoria_escolhida(call):
        categoria = call.data.replace('cat_', '')
        user_data[call.from_user.id] = {'categoria': categoria}
        bot.send_message(call.message.chat.id, "Digite o nome da despesa: ")
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, receber_nome_despesa)

    def receber_nome_despesa(message):
        user_data[message.from_user.id]['nome'] = message.text
        bot.send_message(message.chat.id, "Agora digite o valor da despesa: ")
        bot.register_next_step_handler(message, receber_valor_despesa)

    def receber_valor_despesa(message):
        try:
            valor = float(message.text.replace(',', '.'))
            dados = user_data[message.from_user.id]
            dados['valor'] = valor
            dados['user_id'] = message.from_user.id
            dados['data'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Salva no banco de dados
            adicionar_despesa(
                dados['user_id'],
                dados['categoria'],
                dados['nome'],
                dados['valor'],
                dados['data']
            )
            despesas.append(dados.copy())  # Opcional: manter na lista em memória
            bot.send_message(message.chat.id, f"Despesa adicionada:\nCategoria: {dados['categoria']}\nNome: {dados['nome']}\nValor: R$ {dados['valor']:.2f}")
            user_data.pop(message.from_user.id)
        except ValueError:
            bot.send_message(message.chat.id, "Por favor, digite um número válido")
            bot.register_next_step_handler(message, receber_valor_despesa)

    @bot.message_handler(commands=['grafico'])
    def enviar_grafico(message):
        despesas_usuario = listar_despesas(message.from_user.id)
        if not despesas_usuario:
            bot.send_message(message.chat.id, "Não existe nenhuma despesa")
            return
        # Monta lista de dicionários para o gerar_grafico
        despesas_dict = [
            {'categoria': cat, 'nome': desc, 'valor': val, 'data': data}
            for cat, desc, val, data in despesas_usuario
        ]
        caminho_arquivo = gerar_grafico(despesas_dict)
        with open(caminho_arquivo, 'rb') as f:
            bot.send_photo(message.chat.id, f)

    @bot.message_handler(commands=['comandos'])
    def comandos(message):
        bot.send_message(message.chat.id, 
        """         
Aqui está todos os comandos atuais meus!!!

/adicionardespesa - Adiciona uma nova despesa
/grafico - Mostra um gráfico das despesas
/help - Mostra esta mensagem de ajuda
/comandos - Lista todos os comandos
/listardespesas - Lista todas as despesas
/deletardespesa - Deleta uma despesa
/salvarplanilha - Salva as despesas em uma planilha""")
        
    @bot.message_handler(commands=['listardespesas'])
    def listar_despesas_cmd(message):
        despesas_usuario = listar_despesas(message.from_user.id)
        if not despesas_usuario:
            bot.send_message(message.chat.id, "Você não possui despesas cadastradas.")
            return
        resposta = "Suas despesas:\n"
        for despesa in despesas_usuario:
            # Se despesa tem 5 campos: id, categoria, descricao, valor, data
            _, cat, desc, val, data = despesa
            resposta += f"- [{cat}] {desc}: R$ {val:.2f} em {data}\n"
        bot.send_message(message.chat.id, resposta)
    
    @bot.message_handler(commands=['deletardespesa'])
    def deletar_despesa_cmd(message):
        despesas_usuario = listar_despesas(message.from_user.id)
        if not despesas_usuario:
            bot.send_message(message, "Você não possui despesas cadastradas")
            return
        resposta = "Qual despesa deseja deletar?\n"
        for idx, (id, cat, desc, val, data) in enumerate(despesas_usuario, 1):
            resposta += f"{idx}. [{cat}] {desc}: R${val:.2f} em {data}\n"
        bot.send_message(message.chat.id, resposta)
        bot.register_next_step_handler(message, processar_delecao, despesas_usuario)
    
    def processar_delecao(message, despesas_usuario):
        try:
            idx = int(message.text) - 1
            if idx < 0 or idx >= len(despesas_usuario):
                raise ValueError
            id_despesa = despesas_usuario[idx][0] # O id está na primeira posição da tupla
            deletar_despesa(id_despesa)
            bot.send_message(message.chat.id, "Despesa deletada com sucesso!")
        except Exception:
            bot.send_message(message.chat.id, "Opção inválida, tente novamente!")