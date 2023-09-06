from setup import *
import requests
import datetime
import telebot
import time
import json


class CrashSinal:
    def __init__(self):
        self.bot = telebot.TeleBot(TOKEN, parse_mode='MARKDOWN')
        self.mensagens_start()
        self.date_now = str(datetime.datetime.now().strftime("%d/%m/%Y"))
        self.check_date = self.date_now
        self.apagar_mensagem = False
        self.analisar = True
        self.count = 0
        self.alvo = 0

        self.win_results = 0
        self.loss_results = 0
        self.max_hate = 0
        self.win_hate = 0

    def placar(self):
        if self.win_results + self.loss_results != 0:
            a = 100 / (self.win_results + self.loss_results) * self.win_results
        else:
            a = 0
        self.win_hate = (f'{a:,.2f}%')

        self.bot.send_message(chat_id=CHAT_ID, text=(f'''

► PLACAR GERAL = ✅{self.win_results}  |  🚫{self.loss_results} 
► Consecutivas = {self.max_hate}
► Assertividade = {self.win_hate}

    '''))
        return

    def ultimos_resultados(self):
        try:
            api_texto = json.loads(requests.get(API_CRASH).text)

            resultados = []
            for i in api_texto:
                resultados.append(float(i["crash_point"]))
            return (resultados[:6])

        except:
            print("Falha na requisição")

    def estrategia(self, resultados):
        print(resultados)
        if self.analisar == False:
            self.checar_resultado(resultados[0])
            return

        if resultados[0] < 2.0 and resultados[1]:
            print("Entrada Confirmada!")
            self.alvo = 2
            self.gales = 1
            self.sinal_entrada(resultados[0])
            return

        if resultados[0] < 2.0:
            self.alerta_entrada()
            return

        if resultados[0] >= 2.0 and resultados[1]:
            print("Entrada Confirmada!")
            self.alvo = 2
            self.gales = 1
            self.sinal_entrada(resultados[0])
            return

        if resultados[0] >= 2.0:
            self.alerta_entrada()
            return

    def apagar_alerta(self):
        if self.apagar_mensagem == True:
            print("Alerta Apagado")
            self.bot.delete_message(CHAT_ID, self.message_ids)
            self.apagar_mensagem = False

    def alerta_entrada(self):
        texto = '''⚠️ ANALISANDO ENTRADA, FIQUE ATENTO!!!'''
        self.message_ids = self.bot.send_message(CHAT_ID, texto).message_id
        self.apagar_mensagem = True
        return

    def alerta_gale(self):
        print(f"⚠️ Vamos para o {self.count}ª GALE")
        texto = f"⚠️ Vamos para o {self.count}ª GALE"
        self.message_ids = self.bot.send_message(CHAT_ID, texto).message_id
        self.apagar_mensagem = True
        return

    def sinal_entrada(self, apos):
        texto = (f'''

 *ENTRADA CONFIRMADA!*

🚀 Apostar após o {apos}x
🎯 Sair em {self.alvo}x 
🔁 Fazer até {self.gales} gales

    ''')
        self.analisar = False
        self.bot.send_message(CHAT_ID, texto)
        return

    def checar_resultado(self, resultados):
        if resultados >= self.alvo:
            print("WIN")
            texto = (f"✅✅✅ WIN ✅✅✅")
            self.win_results += 1
            self.max_hate += 1
            self.bot.send_message(CHAT_ID, texto)

        elif resultados < self.alvo:
            self.count += 1

            if self.count > self.gales:
                print("LOSS")
                texto = (f"🚫🚫🚫 LOSS 🚫🚫🚫")
                self.loss_results += 1
                self.max_hate = 0
                self.bot.send_message(CHAT_ID, texto)

            else:
                print(f"Vamos para o {self.count}ª gale!")
                self.alerta_gale()
                return

        self.count = 0
        self.analisar = True
        self.placar()
        return

    def mensagens_start(self, commands=["start", "help"]):
        if commands == "start" or "help":
            texto = f'''Esse grupo do telegram e apenas uma demostração, para exemplificar como funciona um sala de sinais do jogo Crash.
Não  é recomendado que faça entradas seguindo os sinais que são postados aqui.'''
            self.bot.send_message(CHAT_ID, texto)

    def start(self):
        checar = []
        while True:
            resultados = self.ultimos_resultados()
            if checar != resultados:
                checar = resultados
                self.apagar_alerta()
                self.estrategia(resultados)


crash = CrashSinal()
crash.start()
