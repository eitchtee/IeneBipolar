import pickle
import signal
import time
from datetime import datetime

from iene import valor_iene
from twitter import twittar

from traceback import print_exc


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


if __name__ == '__main__':
    killer = GracefulKiller()
    while not killer.kill_now:
        try:
            with open('ultimo_valor.db', 'rb') as db:
                ultimo_valor = pickle.load(db)
        except FileNotFoundError:
            print('Rodando pela primeira vez.')
            try:
                valor_atual = valor_iene()
                print(valor_atual)
            except:
                print_exc()
                time.sleep(600)
                continue
            with open('ultimo_valor.db', 'wb') as db:
                pickle.dump(valor_atual, db, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            try:
                valor_atual = valor_iene()

                diferenca = round(abs(valor_atual - ultimo_valor), 6)

                if diferenca >= 0.5:
                    valor_reais = 'R${}'.format(str(valor_atual).
                                                replace('.', ','))
                    hora = datetime.now().strftime('%H:%M')

                    if valor_atual > ultimo_valor:
                        msg = "Iene subiu :( - {} às {}".format(valor_reais,
                                                                   hora)
                        try:
                            twittar(msg)
                        except:
                            print_exc()
                            time.sleep(900)
                            continue
                        print(msg)
                    elif ultimo_valor > valor_atual:
                        msg = "Iene caiu (: - {} às {}".format(valor_reais,
                                                                  hora)
                        try:
                            twittar(msg)
                        except:
                            print_exc()
                            time.sleep(900)
                            continue
                        print(msg)
                    with open('ultimo_valor.db', 'wb') as db:
                        pickle.dump(valor_atual, db,
                                    protocol=pickle.HIGHEST_PROTOCOL)
                else:
                    print('Diferença insignificante para ser postada.')
            except:
                time.sleep(900)
                continue
            else:
                time.sleep(3900)

    print("Parando execução.")
