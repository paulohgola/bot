# BOT TELEGRAM: EXPENSES BOT    

Este bot ajuda você a registrar e acompanhar suas despesas diretamente pelo Telegram, facilitando o controle financeiro pessoal ou em grupo.

## Pré-requisitos

- [Python](https://python.org/) versão 3.13.7 ou superior
- Uma conta no Telegram
- Token de bot do Telegram (obtenha com o [BotFather](https://core.telegram.org/bots#botfather))

## Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/paulohgola/bot.git
cd bot
pip install -r requirements.txt
```

## Configuração

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```
TELEGRAM_TOKEN=seu_token_aqui
```

Substitua `seu_token_aqui` pelo token fornecido pelo BotFather.


No Telegram, procure pelo seu bot e envie comandos como:

- `/start` — Inicia a conversa com o bot
- `/adicionardespesa` — Adiciona uma despesa
- `/listardespesas` — Lista as despesas registradas
- `/grafico` — Cria um gráfico das despesas
- `/deletardespesa` — deleta a despesa selecionada
- `/comandos` — Mostra os comandos atuais

## Contribuição

Sinta-se à vontade para abrir issues ou enviar pull requests. Sugestões e melhorias são bem-vindas!
