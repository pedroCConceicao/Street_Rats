import random
import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.dinheiro = 500
        self.estoque = {"ácido": 0, "ervas": 0, "pó branco": 0, "droga leve": 0, "droga pesada": 0}
        self.territorios = 1
        self.nivel = 1
        self.funcionarios = 0
        self.fama = 0
        self.zonas_controladas = ["Bairro Pobre"]

    def status(self):
        """ Exibe status do jogador """
        status_text = f"""
        💰 [green]Dinheiro:[/] ${self.dinheiro}
        📦 [blue]Estoque:[/] {self.estoque}
        🏠 [yellow]Territórios:[/] {self.territorios} ({", ".join(self.zonas_controladas)})
        👥 [cyan]Funcionários:[/] {self.funcionarios}
        ⭐ [red]Fama:[/] {self.fama}
        """
        console.print(Panel(status_text, title=f"👤 {self.nome}", style="bold magenta"))

class Mercado:
    precos = {"ácido": 50, "ervas": 30, "pó branco": 100}

    def mostrar_produtos(self):
        table = Table(title="🛒 Mercado de Ingredientes", style="bold yellow")
        table.add_column("Ingrediente", style="cyan", justify="center")
        table.add_column("Preço", style="green", justify="center")
        for item, preco in self.precos.items():
            table.add_row(item, f"${preco}")
        console.print(table)

    def comprar_ingredientes(self, jogador, ingrediente, quantidade):
        if ingrediente in self.precos:
            custo = self.precos[ingrediente] * quantidade
            if jogador.dinheiro >= custo:
                jogador.dinheiro -= custo
                jogador.estoque[ingrediente] += quantidade
                console.print(f"✅ Comprou {quantidade}x {ingrediente} por [green]${custo}[/]")
            else:
                console.print("[red]❌ Dinheiro insuficiente![/]")
        else:
            console.print("[red]❌ Ingrediente inválido![/]")

class Producao:
    receitas = {
        "droga leve": {"ácido": 1, "ervas": 2},
        "droga pesada": {"pó branco": 2, "ácido": 1}
    }

    def produzir(self, jogador, tipo_droga, quantidade):
        if tipo_droga in self.receitas:
            ingredientes = self.receitas[tipo_droga]
            for item, qtd in ingredientes.items():
                if jogador.estoque[item] < qtd * quantidade:
                    console.print(f"[red]❌ Ingredientes insuficientes para {quantidade}x {tipo_droga}[/]")
                    return
            for item, qtd in ingredientes.items():
                jogador.estoque[item] -= qtd * quantidade
            jogador.estoque[tipo_droga] += quantidade
            console.print(f"⚗️ Produziu {quantidade}x [green]{tipo_droga}[/] com sucesso!")
        else:
            console.print("[red]❌ Tipo de droga inválido![/]")

class Venda:
    precos_venda = {"droga leve": 150, "droga pesada": 400}

    def vender(self, jogador, zona, tipo_droga, quantidade):
        if zona not in jogador.zonas_controladas:
            console.print("[red]❌ Você não controla esta zona![/]")
            return
        if tipo_droga in jogador.estoque and jogador.estoque[tipo_droga] >= quantidade:
            modificador_lucro = Zonas.zonas[zona]["lucro"]
            lucro = self.precos_venda[tipo_droga] * quantidade * modificador_lucro
            jogador.estoque[tipo_droga] -= quantidade
            jogador.dinheiro += lucro
            jogador.fama += random.randint(1, Zonas.zonas[zona]["risco"])

            console.print(f"💰 Vendeu {quantidade}x [green]{tipo_droga}[/] em [yellow]{zona}[/] por ${lucro}")
        else:
            console.print("[red]❌ Estoque insuficiente![/]")

class Zonas:
    zonas = {
        "Bairro Pobre": {"risco": 5, "lucro": 1.0, "custo": 0},
        "Centro": {"risco": 15, "lucro": 1.5, "custo": 1000},
        "Favela": {"risco": 30, "lucro": 2.0, "custo": 2000},
        "Porto": {"risco": 50, "lucro": 3.0, "custo": 5000}
    }

    def exibir_zonas(self, jogador):
        table = Table(title="🌍 Territórios Disponíveis", style="bold cyan")
        table.add_column("Zona", style="yellow", justify="center")
        table.add_column("Risco", style="red", justify="center")
        table.add_column("Lucro", style="green", justify="center")
        table.add_column("Custo", style="blue", justify="center")

        for zona, info in self.zonas.items():
            status = "✅" if zona in jogador.zonas_controladas else f"${info['custo']}"
            table.add_row(zona, str(info["risco"]), f"{info['lucro']}x", status)

        console.print(table)

    def comprar_territorio(self, jogador, zona):
        if zona in self.zonas and zona not in jogador.zonas_controladas:
            custo = self.zonas[zona]["custo"]
            if jogador.dinheiro >= custo:
                jogador.dinheiro -= custo
                jogador.territorios += 1
                jogador.zonas_controladas.append(zona)
                console.print(f"🏠 Conquistou o território [bold cyan]{zona}[/]!")
            else:
                console.print("[red]❌ Dinheiro insuficiente![/]")
        else:
            console.print("[red]❌ Território inválido ou já possuído![/]")

def menu_territorios(jogador):
    """Submenu para ações relacionadas a territórios"""
    while True:
        console.print("\n🏴 [bold yellow]Gerenciamento de Territórios[/]")
        console.print("1️⃣ Vender Drogas  2️⃣ Atacar Gangue Rival  3️⃣ Investir em Defesa  4️⃣ Voltar")

        opcao = input("Escolha uma ação: ")

        if opcao == "1":
            console.print(f"Zonas controladas: {', '.join(jogador.zonas_controladas)}", style="cyan")
            zona = input("Escolha a zona: ").strip()
            droga = input("Droga para vender: ").strip().lower()
            qtd = int(input("Quantidade: "))
            venda.vender(jogador, zona, droga, qtd)

        elif opcao == "2":
            guerra_territorial(jogador)

        elif opcao == "3":
            console.print("[bold green]💰 Investindo em defesas no território...[/]")
            zona = input("Escolha a zona para investir: ").strip()
            custo_defesa = 500  # Custo fictício por território
            if jogador.dinheiro >= custo_defesa and zona in jogador.zonas_controladas:
                jogador.dinheiro -= custo_defesa
                console.print(f"🛡️ Defesa melhorada em [yellow]{zona}[/]!")
            else:
                console.print("[red]❌ Dinheiro insuficiente ou território inválido![/]")

        elif opcao == "4":
            return  # Volta ao menu principal

        else:
            console.print("[red]❌ Escolha inválida![/]")

class Eventos:
    def verificar_evento(self, jogador):
        chance = random.randint(1, 100)
        if chance < jogador.fama:
            console.print("[red]🚨 A polícia está investigando suas atividades![/]")
            if random.random() < 0.5:
                console.print("[red]🔒 Você foi preso! Fim de jogo.[/]")
                return False
            else:
                console.print("[yellow]💵 Subornou a polícia e escapou![/]")
                jogador.dinheiro -= 200
                jogador.fama -= 10
        return True

class NPC:
    def __init__(self, nome, personalidade):
        self.nome = nome
        self.personalidade = personalidade
        self.reputacao = random.randint(-50, 50)

    def interagir(self):
        """Submenu de interação com NPC"""
        while True:
            console.print(f"\n🤝 [bold yellow]Interagindo com {self.nome}[/]")
            console.print("[bold cyan]1️⃣ Propor Aliança  2️⃣ Negociar  3️⃣ Atacar  4️⃣ Voltar[/]")
            opcao = input("Escolha: ")

            if opcao == "1":
                console.print(f"🤝 Tentando formar aliança com {self.nome}...")
                if self.reputacao > 20:
                    console.print(f"✅ {self.nome} aceitou a aliança!")
                else:
                    console.print(f"❌ {self.nome} recusou! Reputação muito baixa.")
            elif opcao == "2":
                console.print(f"💰 Negociando com {self.nome}...")
            elif opcao == "3":
                console.print(f"⚔️ Você atacou {self.nome}!")
            elif opcao == "4":
                return  # Sai do submenu
            else:
                console.print("[red]❌ Escolha inválida![/]")

# Submenu de NPCs
def menu_npcs():
    """Submenu para escolher com qual NPC falar"""
    while True:
        console.print("\n📜 [bold yellow]Escolha um NPC para interagir:[/]")
        for i, npc in enumerate(npcs, 1):
            console.print(f"{i}️⃣ {npc.nome} ({npc.personalidade})")

        console.print("0️⃣ Voltar")
        escolha = input("Escolha um NPC: ")

        if escolha == "0":
            return  # Volta ao menu principal
        elif escolha.isdigit() and 1 <= int(escolha) <= len(npcs):
            npcs[int(escolha) - 1].interagir()
        else:
            console.print("[red]❌ Escolha inválida![/]")

class Gangue:
    def __init__(self, nome, forca, territorios):
        self.nome = nome
        self.forca = forca  # Nível de poder da gangue
        self.territorios = territorios  # Lista de zonas controladas
        self.reputacao_com_jogador = 0  # Pode ser positivo (amizade) ou negativo (rivalidade)

    def atacar(self, jogador):
        """A gangue pode tentar tomar um território do jogador"""
        if not jogador.zonas_controladas:
            return

        alvo = random.choice(jogador.zonas_controladas)
        console.print(f"\n⚠️ [bold red]A gangue {self.nome} atacou {alvo}![/]")

        if self.forca > random.randint(0, 100):  # Compara força da gangue vs. fator aleatório
            jogador.zonas_controladas.remove(alvo)
            self.territorios.append(alvo)
            console.print(f"❌ Você perdeu {alvo} para {self.nome}!")
        else:
            console.print(f"✅ Você defendeu {alvo} com sucesso!")

def guerra_territorial(jogador):
    """Sistema de disputa de territórios entre jogador e gangues"""
    while True:
        console.print("\n🏴 [bold yellow]Conflitos de Gangues[/]")
        console.print("1️⃣ Atacar uma gangue  2️⃣ Defender território  3️⃣ Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            console.print("\n👊 Escolha uma gangue para atacar:")
            for i, gangue in enumerate(gangues, 1):
                console.print(f"{i}️⃣ {gangue.nome} (Força: {gangue.forca})")

            escolha = input("Gangue alvo: ")
            if escolha.isdigit() and 1 <= int(escolha) <= len(gangues):
                gangue_alvo = gangues[int(escolha) - 1]
                if jogador.forca > gangue_alvo.forca:
                    console.print(f"✅ Você derrotou {gangue_alvo.nome} e tomou {gangue_alvo.territorios[0]}!")
                    jogador.zonas_controladas.append(gangue_alvo.territorios.pop(0))
                else:
                    console.print(f"❌ Você perdeu o ataque contra {gangue_alvo.nome}!")

        elif opcao == "2":
            gangue_atacante = random.choice(gangues)
            gangue_atacante.atacar(jogador)

        elif opcao == "3":
            return
        else:
            console.print("[red]❌ Escolha inválida![/]")


# Inicialização
console.print(Panel("💊 [bold cyan]Simulador de Tráfico[/] 💊", style="bold red"))

jogador = Jogador(input("Digite seu nome: "))
mercado = Mercado()
producao = Producao()
zonas = Zonas()
venda = Venda()
eventos = Eventos()
npcs = [NPC("Carlos 'O Cobra'", "hostil"), NPC("Tio João", "amigável")]
gangues = [
    Gangue("Os Cobras", 70, ["Favela Azul"]),
    Gangue("Mercenários", 90, ["Centro"]),
    Gangue("Facção X", 60, ["Subúrbio"])
]

def limpar_tela():
    """Limpa a tela do terminal"""
    sistema = os.name
    if sistema == "nt":  # Windows
        os.system('cls')
    else:  # macOS ou Linux
        os.system('clear')

while True:
    limpar_tela()
    jogador.status()

    console.print("\n[bold yellow]1️⃣ Comprar Ingredientes  2️⃣ Produzir Drogas  3️⃣ Comprar Territórios  4️⃣ Gerenciar Territórios  5️⃣ Falar com NPCs  6️⃣ Guerra de Gangues  7️⃣ Sair[/]")
    opcao = input("Escolha uma ação: ")

    if opcao == "1":
        mercado.mostrar_produtos()
        ing = input("Ingrediente: ").strip().lower()
        qtd = int(input("Quantidade: "))
        mercado.comprar_ingredientes(jogador, ing, qtd)

    elif opcao == "2":
        console.print("[green]Opções:[/] droga leve, droga pesada")
        tipo = input("Escolha o que produzir: ").strip().lower()
        qtd = int(input("Quantidade: "))
        producao.produzir(jogador, tipo, qtd)

    elif opcao == "3":
        zonas.exibir_zonas(jogador)
        zona = input("Zona para comprar: ").strip()
        zonas.comprar_territorio(jogador, zona)

    elif opcao == "4":
        menu_territorios(jogador)  # Substituímos pela função do submenu

    elif opcao == "5":
        menu_npcs()

    elif opcao == "6":
        guerra_territorial(jogador)

    elif opcao == "7":
        console.print("[red]🏃 Saindo do jogo...[/]")
        break


