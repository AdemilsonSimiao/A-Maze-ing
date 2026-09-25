------------------------------
## 📖 MANUAL DE ESTUDO — ARQUITETURA DO PROJETO A-MAZE-ING
Este manual explica como os blocos se comunicam.
## 🏛️ 1. O MAPA DO PROJETO (ESTRUTURA DE PASTAS)
O projeto é dividido em quatro partes que rodam ao redor do arquivo principal. Ele separa a lógica da matemática da tela do usuário.

* a_maze_ing.py: É o ponto de partida absoluto. Onde tudo começa.
* cli / : É a camada de entrada. Lê e valida o arquivo de configuração.
* mazegen / : É o coração do sistema. Cria o labirinto e resolve o caminho.
* display / : É a camada visual. Desenha o labirinto usando texto (ASCII).
* app / : É o gerente do sistema. Organiza os módulos e mostra o menu.

------------------------------
## 🔧 2. RESPONSABILIDADE DE CADA BLOCO E FUNÇÃO## Módulo cli / (Validação e Entrada)
Este bloco garante que o programa não comece com dados errados.

* errors.py: Cria o erro chamado ConfigError. Se algo estiver errado na configuração, o programa avisa por aqui em vez de travar o Python.
* config_parser.py: É o validador. A função "read_key_values" lê o arquivo. As funções "parse_int" e "parse_bool" convertem o texto para números e regras. A função "check_inside_maze" confere se as entradas e saídas estão no lugar certo. A função "parse_config" junta tudo isso.

## Módulo mazegen / (O Coração Matemático)
Este bloco calcula as paredes, caminhos e soluções.

* generator.py: É a fábrica do labirinto. A função "generate" cria uma grade vazia usando "_create_empty_grid". Depois, a função "_carve_tree" começa a esculpir os caminhos. Ela se conecta com o arquivo de algoritmos para saber por onde andar. No final, as funções "_remove_dead_ends" e "_add_extra_loops" limpam os becos sem saída ou criam caminhos extras.
* algorithms.py: Contém os motores matemáticos. A função "generate_edges" escolhe qual algoritmo usar através de uma lista em "_algorithms". O fluxo então vai para "dfs_edges", "prim_edges", "kruskal_edges" ou "wilson_edges".
* pattern.py: É um segredo do código. A função "plan_pattern" desenha o número "42" dentro do mapa usando coordenadas fixas.
* solver.py: É o solucionador. A função "solve" usa uma busca matemática para achar a saída do labirinto. Ela fica lendo a função "Cell.is_open" para saber onde tem parede e onde está aberto.
* encoder.py: É o exportador. A função "encode_maze" transforma o labirinto pronto em um código hexadecimal muito curto e salva no computador usando "write_file".

## Módulo display / (A Tela Visual)
Este bloco transforma a matemática em desenho.

* ascii_renderer.py: A função principal "render_maze" funciona como uma impressora. Ela monta o teto e o chão com "_horizon_line" e as paredes do meio com "_middle_line". A função "_paint" coloca as cores no terminal.

## Módulo app / (O Gerente e Orquestrador)
Este bloco sabe a ordem exata de quem chamar para o programa funcionar.

* session.py: Controla o estado atual do jogo usando "MazeState". A função "build_maze" liga o gerador e salva o resultado em "state_from_grid".
* animation.py: Cria os efeitos visuais. As funções "animate_maze" e "animate_path" criam loops que limpam a tela do terminal bem rápido e chamam o "render_maze" várias vezes, dando a impressão de que o labirinto está se desenhando sozinho.
* menu.py: Mostra as opções na tela. A função "run_menu" fica rodando sem parar. Ela lê o que você digita em "read_choice" (opções de 1 a 4) e chama as animações ou salva os arquivos.

------------------------------
## 🔄 3. O FLUXO DA INFORMAÇÃO (PASSO A PASSO)
Quando você aperta o botão para rodar, a informação caminha exatamente assim:

   1. O arquivo a_maze_ing.py inicia o programa.
   2. Ele pede para o módulo cli/ validar o arquivo de texto.
   3. Se tudo estiver certo, o arquivo principal chama o módulo app/animation.py.
   4. A animação pede para o mazegen/generator.py criar o labirinto.
   5. O gerador pergunta para o mazegen/algorithms.py qual caminho desenhar.
   6. Conforme os caminhos são calculados, o módulo display/ desenha as linhas na tela.
   7. O módulo mazegen/solver.py entra em ação e calcula a linha da resposta certa.
   8. O módulo mazegen/encoder.py salva o resultado no seu computador.
   9. O controle vai para o app/menu.py, que fica esperando você escolher a próxima opção.

------------------------------


