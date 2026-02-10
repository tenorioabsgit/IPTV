"""
simulate_usage.py - Simula uso humano do app Pira IPTV no Roku
Envia comandos via ECP (External Control Protocol) com delays realistas.

Uso: python simulate_usage.py [--ip ROKU_IP]
"""
import urllib.request
import urllib.error
import time
import sys
import random
import xml.etree.ElementTree as ET

ROKU_IP = "192.168.5.130"
ECP_PORT = 8060

# Parse args
for i, arg in enumerate(sys.argv):
    if arg == "--ip" and i + 1 < len(sys.argv):
        ROKU_IP = sys.argv[i + 1]

BASE_URL = f"http://{ROKU_IP}:{ECP_PORT}"


def ecp_post(path):
    """Envia comando ECP (POST) ao Roku."""
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url, data=b"", method="POST")
    try:
        urllib.request.urlopen(req, timeout=5)
        return True
    except urllib.error.HTTPError as e:
        if e.code == 403:
            # ECP Limited mode - try keydown/keyup as fallback
            return False
        print(f"  [ERRO] {url}: {e}")
        return False
    except Exception as e:
        print(f"  [ERRO] {url}: {e}")
        return False


def ecp_get(path):
    """Envia query ECP (GET) ao Roku."""
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url, method="GET")
    try:
        resp = urllib.request.urlopen(req, timeout=5)
        return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  [ERRO] {url}: {e}")
        return ""


def keypress(key):
    """Envia tecla ao Roku."""
    ok = ecp_post(f"/keypress/{key}")
    if not ok:
        # Fallback: try keydown + keyup
        ecp_post(f"/keydown/{key}")
        time.sleep(0.05)
        ecp_post(f"/keyup/{key}")


def keydown(key):
    """Envia key down ao Roku."""
    ecp_post(f"/keydown/{key}")


def keyup(key):
    """Envia key up ao Roku."""
    ecp_post(f"/keyup/{key}")


def human_delay(min_s=0.8, max_s=2.5):
    """Delay aleatório simulando tempo de reação humano."""
    delay = random.uniform(min_s, max_s)
    time.sleep(delay)


def short_delay():
    """Delay curto entre ações rápidas."""
    time.sleep(random.uniform(0.3, 0.7))


def thinking_delay():
    """Delay mais longo simulando pessoa pensando/assistindo."""
    time.sleep(random.uniform(3.0, 6.0))


def watching_delay():
    """Delay longo simulando pessoa assistindo conteúdo."""
    time.sleep(random.uniform(5.0, 10.0))


def get_active_app():
    """Retorna info do app ativo."""
    xml_str = ecp_get("/query/active-app")
    if xml_str:
        try:
            root = ET.fromstring(xml_str)
            app = root.find("app")
            if app is not None:
                return app.text, app.get("id")
        except ET.ParseError:
            pass
    return "Unknown", "unknown"


def log_action(action):
    """Log com timestamp."""
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {action}")


def check_app_running():
    """Verifica se o Pira IPTV está rodando."""
    name, app_id = get_active_app()
    if app_id == "dev":
        log_action(f"App ativo: {name} (id={app_id})")
        return True
    else:
        log_action(f"App ativo: {name} (id={app_id}) - Pira IPTV nao esta aberto")
        return False


# ============================
# CENARIOS DE SIMULACAO
# ============================

def scenario_launch_app():
    """Cenario: Abrir o app a partir do Home."""
    log_action("=== CENARIO: Abrir o App ===")
    log_action("Pressionando Home...")
    keypress("Home")
    time.sleep(2)

    log_action("Lancando Pira IPTV...")
    ecp_post("/launch/dev")
    time.sleep(4)

    if check_app_running():
        log_action("App aberto com sucesso!")
        log_action("Aguardando carregamento da playlist...")
        time.sleep(5)  # Tempo para playlist carregar
    else:
        log_action("FALHA: App nao abriu. Tentando novamente...")
        ecp_post("/launch/dev")
        time.sleep(5)


def scenario_browse_categories():
    """Cenario: Navegar pelas categorias (rows) do RowList."""
    log_action("=== CENARIO: Navegar pelas Categorias ===")

    # O RowList mostra categorias como rows verticais
    # Down move entre categorias, Right/Left move entre canais na categoria

    log_action("Navegando para baixo nas categorias...")
    for i in range(4):
        human_delay(1.0, 2.0)
        keypress("Down")
        log_action(f"  Categoria {i + 2} (desceu)")
        human_delay(0.5, 1.0)

        # Navega alguns canais na categoria
        num_right = random.randint(2, 5)
        log_action(f"  Navegando {num_right} canais para a direita...")
        for j in range(num_right):
            short_delay()
            keypress("Right")

        thinking_delay()

    # Volta ao topo
    log_action("Voltando ao topo das categorias...")
    for i in range(4):
        short_delay()
        keypress("Up")

    human_delay()
    log_action("Navegacao por categorias concluida.")


def scenario_browse_channels_in_row():
    """Cenario: Navegar pelos canais dentro de uma row."""
    log_action("=== CENARIO: Navegar pelos Canais na Row ===")

    # Navega bastante para a direita
    num_channels = random.randint(6, 12)
    log_action(f"Navegando {num_channels} canais para a direita...")
    for i in range(num_channels):
        short_delay()
        keypress("Right")
        if i % 3 == 0:
            # Pausa ocasional como se estivesse lendo o nome
            human_delay(1.5, 3.0)
            log_action(f"  Canal {i + 1} - observando o hero banner...")

    thinking_delay()

    # Volta alguns
    back_count = random.randint(2, 4)
    log_action(f"Voltando {back_count} canais para a esquerda...")
    for i in range(back_count):
        short_delay()
        keypress("Left")

    human_delay()
    log_action("Navegacao por canais concluida.")


def scenario_watch_channel():
    """Cenario: Selecionar e assistir um canal."""
    log_action("=== CENARIO: Assistir um Canal ===")

    log_action("Selecionando canal (OK)...")
    keypress("Select")
    time.sleep(2)  # Tempo para o player abrir e iniciar buffering

    log_action("Aguardando stream carregar...")
    time.sleep(3)

    log_action("Assistindo canal...")
    watching_delay()

    # Mostra OSD pressionando qualquer tecla
    log_action("Mostrando OSD (pressionando Info)...")
    keypress("Info")
    human_delay(2.0, 4.0)

    log_action("Canal assistido com sucesso.")


def scenario_channel_switching():
    """Cenario: Trocar canais usando CH+/CH- (Up/Down no player)."""
    log_action("=== CENARIO: Trocar Canais (CH+/CH-) ===")

    num_switches = random.randint(3, 6)
    log_action(f"Trocando {num_switches} canais...")

    for i in range(num_switches):
        direction = random.choice(["Up", "Down"])
        action = "CH+" if direction == "Up" else "CH-"
        log_action(f"  {action} (proximo canal)...")
        keypress(direction)
        time.sleep(2)  # Tempo para buffer/iniciar stream

        # Assiste um pouco
        watch_time = random.uniform(3.0, 8.0)
        log_action(f"  Assistindo por {watch_time:.1f}s...")
        time.sleep(watch_time)

    log_action("Troca de canais concluida.")


def scenario_pause_resume():
    """Cenario: Pausar e retomar reprodução."""
    log_action("=== CENARIO: Pausar e Retomar ===")

    log_action("Pausando (Play)...")
    keypress("Play")
    human_delay(2.0, 4.0)

    log_action("Retomando (Play)...")
    keypress("Play")
    human_delay(1.0, 2.0)

    log_action("Pause/resume testado.")


def scenario_back_to_menu():
    """Cenario: Voltar do player ao menu principal."""
    log_action("=== CENARIO: Voltar ao Menu ===")

    log_action("Pressionando Back para sair do player...")
    keypress("Back")
    time.sleep(1.5)

    log_action("De volta ao menu principal.")
    human_delay()


def scenario_reopen_another_channel():
    """Cenario: Navegar para outra categoria e abrir canal diferente."""
    log_action("=== CENARIO: Abrir Outro Canal em Outra Categoria ===")

    # Move para outra categoria
    moves_down = random.randint(1, 3)
    log_action(f"Descendo {moves_down} categorias...")
    for _ in range(moves_down):
        human_delay(0.5, 1.0)
        keypress("Down")

    # Navega na categoria
    moves_right = random.randint(1, 4)
    log_action(f"Navegando {moves_right} canais para a direita...")
    for _ in range(moves_right):
        short_delay()
        keypress("Right")

    thinking_delay()

    # Seleciona
    log_action("Selecionando canal...")
    keypress("Select")
    time.sleep(3)

    log_action("Assistindo segundo canal...")
    watching_delay()


def scenario_rapid_browsing():
    """Cenario: Navegação rápida simulando busca por canal específico."""
    log_action("=== CENARIO: Navegacao Rapida (buscando canal) ===")

    log_action("Navegando rapidamente pelos canais...")
    for i in range(8):
        time.sleep(random.uniform(0.2, 0.5))
        keypress("Right")

    human_delay(0.5, 1.0)

    for i in range(3):
        time.sleep(random.uniform(0.2, 0.5))
        keypress("Left")

    # Muda de categoria rapidamente
    log_action("Mudando de categoria rapidamente...")
    for i in range(3):
        time.sleep(random.uniform(0.3, 0.6))
        keypress("Down")

    for i in range(5):
        time.sleep(random.uniform(0.2, 0.5))
        keypress("Right")

    human_delay()
    log_action("Navegacao rapida concluida.")


# ============================
# EXECUCAO PRINCIPAL
# ============================

def main():
    print("=" * 60)
    print("  PIRA IPTV - Simulacao de Uso Humano")
    print(f"  Roku: {ROKU_IP}:{ECP_PORT}")
    print("=" * 60)
    print()

    # Verifica conectividade
    log_action("Verificando conexao com o Roku...")
    name, app_id = get_active_app()
    if name == "Unknown":
        log_action("ERRO: Nao foi possivel conectar ao Roku!")
        log_action(f"Verifique se o IP {ROKU_IP} esta correto.")
        sys.exit(1)
    log_action(f"Conectado! App ativo: {name} (id={app_id})")

    # Testa se keypress funciona
    log_action("Testando permissao ECP para keypress...")
    test_ok = ecp_post("/keypress/Info")
    if not test_ok:
        print()
        print("  *** AVISO: Keypress ECP bloqueado (403 Forbidden) ***")
        print("  O Roku esta em modo ECP limitado.")
        print("  Para habilitar, va em:")
        print("    Settings > System > Advanced system settings")
        print("    > Control by mobile apps > 'Default' ou 'Permissive'")
        print()
        log_action("Continuando mesmo assim...")
        # resp = input("  Continuar mesmo assim? (s/n): ").strip().lower()
        # if resp != "s":
        #     log_action("Simulacao cancelada pelo usuario.")
        #     sys.exit(0)
        print()
    else:
        log_action("Keypress ECP funcionando!")
    print()

    # ===== FLUXO COMPLETO DE SIMULACAO =====

    # 1. Abrir o app
    scenario_launch_app()
    print()

    # 2. Navegar pelas categorias
    scenario_browse_categories()
    print()

    # 3. Navegar canais na row
    scenario_browse_channels_in_row()
    print()

    # 4. Assistir um canal
    scenario_watch_channel()
    print()

    # 5. Trocar canais com CH+/CH-
    scenario_channel_switching()
    print()

    # 6. Pausar e retomar
    scenario_pause_resume()
    print()

    # 7. Voltar ao menu
    scenario_back_to_menu()
    print()

    # 8. Abrir outro canal em outra categoria
    scenario_reopen_another_channel()
    print()

    # 9. Trocar mais canais
    scenario_channel_switching()
    print()

    # 10. Voltar ao menu
    scenario_back_to_menu()
    print()

    # 11. Navegação rápida
    scenario_rapid_browsing()
    print()

    # 12. Selecionar um último canal
    log_action("=== CENARIO: Canal Final ===")
    keypress("Select")
    time.sleep(3)
    log_action("Assistindo canal final...")
    watching_delay()

    # 13. Sair do player
    scenario_back_to_menu()
    print()

    # Resumo
    print("=" * 60)
    log_action("SIMULACAO COMPLETA!")
    print()
    print("  Cenarios executados:")
    print("    1. Abrir o app")
    print("    2. Navegar categorias (scroll vertical)")
    print("    3. Navegar canais na row (scroll horizontal)")
    print("    4. Assistir canal")
    print("    5. Trocar canais (CH+/CH-)")
    print("    6. Pausar e retomar")
    print("    7. Voltar ao menu")
    print("    8. Abrir canal em outra categoria")
    print("    9. Mais troca de canais")
    print("   10. Navegacao rapida")
    print("   11. Canal final + sair")
    print("=" * 60)


if __name__ == "__main__":
    main()
