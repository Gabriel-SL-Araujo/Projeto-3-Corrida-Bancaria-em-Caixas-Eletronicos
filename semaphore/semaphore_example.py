import threading
import time
import random
from queue import Queue


class Conta:
    def __init__(self, nome_conta, saldo_inicial):
        self.nome_conta = nome_conta
        self.saldo = saldo_inicial
        self.historico_transacoes = []

        self.mutex_saldo = threading.Lock() # Protege a seção crítica
        self.semaforo_notificacao = threading.Semaphore(0) # Alerta a Thread de Notificações de que há evento para processar
        self.fila_notificacoes = Queue()

    def transferencia(self, usuario, conta_destino, valor):
        primeira, segunda = sorted(
            [self, conta_destino],
            key=lambda conta: conta.nome_conta
        )

        with primeira.mutex_saldo: # Garantia da Exclusão Mútua

            with segunda.mutex_saldo:

                if self.saldo >= valor:
                    time.sleep(random.uniform(0.1, 0.5))

                    conta_destino.saldo += valor
                    self.saldo -= valor

                    taxa = self.__taxa()

                    self.saldo -= taxa

                    self.historico_transacoes.append(-valor)
                    self.historico_transacoes.append(-taxa)
                    conta_destino.historico_transacoes.append(valor)

                    print(f"[{usuario} - {self.nome_conta}] Transferência APROVADA no valor de R$ {valor:.2f} para {conta_destino.nome_conta}. Saldo atual: {self.saldo:.2f}")
                    print(f"[{usuario} - {self.nome_conta}] Taxa de transferência cobrada no valor de R$ {self.__taxa():.2f}")
                else:
                    print(f"[{usuario} - {self.nome_conta}] Transferência de R$ {valor:.2f} NEGADA! Saldo insuficiente ({self.saldo:.2f}).")


    def saque(self, usuario, valor):
        with self.mutex_saldo: # Protege a alteração do saldo
            if self.saldo >= valor:
                time.sleep(random.uniform(0.1, 0.5))

                self.saldo -= valor
                self.historico_transacoes.append(-valor)

                print(f"[{usuario} - {self.nome_conta}] Saque APROVADO no valor de R$ {valor:.2f}. Saldo atual: R$ {self.saldo:.2f}")
            else:
                print(f"[{usuario} - {self.nome_conta}] Saque NEGADO no valor de R$ {valor:.2f}. Saldo insuficiente (R$ {self.saldo:.2f})")

            self.fila_notificacoes.put((usuario, valor))
            self.semaforo_notificacao.release()


    def deposito(self, usuario, valor):
        with self.mutex_saldo: # Garatia da Exclusão Mútua
            time.sleep(random.uniform(0.1, 0.5))

            self.saldo += valor
            self.historico_transacoes.append(valor)

            print(f"[{usuario} - {self.nome_conta}] Depósito no valor de R$ {valor:.2f}. Saldo atual: R$ {self.saldo:.2f}")


    def __taxa(self): # Coba uma taxa aleatória pela transferência realizada
        taxa = self.saldo * random.uniform(0.001, 0.003)

        return taxa


def notificao(conta, id_notificacao):
    print(f"Serviço SMS #[{id_notificacao}] - Iniciando e aguardando saques na {conta.nome_conta}...\n")

    while True:
        # Esse trecho de código permanece bloqueado até que uma operação aconteça
        conta.semaforo_notificacao.acquire()

        if conta.fila_notificacoes.empty():
            break

        usuario, valor = conta.fila_notificacoes.get()
        print(f"\n--- [SMS PARA {conta.nome_conta}] ---")
        print(f"Um saque de R$ {valor:.2f} foi efetuado por {usuario}.")
        print(f"----------------------------------------\n")

def simulacao(conta, usuario, conta_destino):
    for _ in range(3):
        operacao = random.randint(0, 2)

        valor = random.uniform(10.0, 200.0)

        if operacao == 0:
            conta.deposito(usuario, valor)
        elif operacao == 1:
            conta.saque(usuario, valor)
        else:
            conta.transferencia(usuario, conta_destino, valor)

        time.sleep(random.uniform(0.1, 0.5))


if __name__ == "__main__":
    conta_a = Conta("Conta A", 1000.0)
    conta_b = Conta("Conta B", 600.0)

    threads_list = []

    print("Iniciando simulação bancária...")
    print()

    notificador_a = threading.Thread(target=notificao, args=(conta_a, "A"))
    notificador_b = threading.Thread(target=notificao, args=(conta_b, "B"))

    notificador_a.daemon = True # .daemon indica que estas threads são processos secundários/auxiliares
    notificador_b.daemon = True # e que a thread main não deve esperar elas terminarem
    notificador_a.start()
    notificador_b.start()

    for i in range(2):
        thread = threading.Thread(target=simulacao, args=(conta_a, f"Usuário {i+1}", conta_b))
        threads_list.append(thread)
        thread.start()

    for i in range(2):
        thread = threading.Thread(target=simulacao, args=(conta_b, f"Usuário {i+1}", conta_a))
        threads_list.append(thread)
        thread.start()

    for thread in threads_list:
        thread.join()

    saldo_inicial_a = 1000.0
    saldo_atual_a = conta_a.saldo
    soma_historico_a = sum(conta_a.historico_transacoes)
    saldo_esperado_a = saldo_inicial_a + soma_historico_a

    print(f"\n--- [Saldo final na Conta A] ---")
    print(f"-- Saldo esperado: R$ {saldo_esperado_a:.2f}")
    print(f"-- Saldo atual: R$ {saldo_atual_a:.2f}")
    print(f"-- Soma do Histórico: R$ {soma_historico_a:.2f}")
    print(f"--------------------------------\n")

    saldo_inicial_b = 600.0
    saldo_atual_b = conta_b.saldo
    soma_historico_b = sum(conta_b.historico_transacoes)
    saldo_esperado_b = saldo_inicial_b + soma_historico_b

    print(f"\n--- [Saldo final na Conta B] ---")
    print(f"-- Saldo esperado: R$ {saldo_esperado_b:.2f}")
    print(f"-- Saldo atual: R$ {saldo_atual_b:.2f}")
    print(f"-- Soma do Histórico: R$ {soma_historico_b:.2f}")
    print(f"--------------------------------\n")

    print()
    print("Fim da simulação.")