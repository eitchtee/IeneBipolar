import os
import pickle
import random
import signal
import time
from datetime import datetime
from traceback import print_exc

from iene import valor_iene
from twitter import twittar


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


if __name__ == '__main__':
    work_dir = os.path.dirname(os.path.realpath(__file__))
    db_path = os.path.normpath('{}/ultimo_valor.db'.format(work_dir))

    killer = GracefulKiller()
    while not killer.kill_now:
        try:
            with open(db_path, 'rb') as db:
                ultimo_valor = pickle.load(db)
        except:
            print('Rodando pela primeira vez.')
            try:
                valor_atual = valor_iene()
            except:
                print_exc()
                time.sleep(600)
                continue
            with open(db_path, 'wb') as db:
                pickle.dump(valor_atual, db, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            try:
                valor_atual = valor_iene()

                diferenca = abs(valor_atual - ultimo_valor)

                if diferenca >= 0.0001:
                    valor_reais = 'R${}'.format(str(valor_atual).
                                                replace('.', ','))
                    hora = datetime.now().strftime('%H:%M')

                    if valor_atual > ultimo_valor:
                        msg = f"🔴 Iene subiu :( - {valor_reais} às {hora}"
                        try:
                            twittar(msg)
                        except:
                            print_exc()
                            time.sleep(900)
                            continue
                        print(msg)
                    elif ultimo_valor > valor_atual:
                        msg = f"🟢 Iene caiu (: - {valor_reais} às {hora}"
                        try:
                            twittar(msg)
                        except:
                            print_exc()
                            time.sleep(900)
                            continue
                        print(msg)
                    with open(db_path, 'wb') as db:
                        pickle.dump(valor_atual, db,
                                    protocol=pickle.HIGHEST_PROTOCOL)
                else:
                    print(f'Diferença insignificante para ser postada. '
                          f'Último valor: {ultimo_valor} | '
                          f'Valor atual: {valor_atual} | '
                          f'Diferença: {diferenca:.8f}')
            except:
                time.sleep(900)
                continue
            else:
                time.sleep(random.randint(500, 7200))

    print("Parando execução.")
