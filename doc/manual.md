# Diagramas — A-Maze-ing

## Diagrama 1 — Estrutura de arquivos e pastas (só código)

```mermaid
graph TD
    %% Configuração de Estilos Globais para Compactar
    classDef folder fill:#f5f5f7,stroke:#666,stroke-width:2px,stroke-dasharray: 3 3;
    classDef file fill:#fff,stroke:#333,stroke-width:1px;
    classDef root fill:#e2e2e9,stroke:#333,stroke-width:2px,font-weight:bold;

    %% Nó Raiz Central
    ROOT["📂 a_maze_ing-1.0.0/"]
    class ROOT root;

    %% Ponto de Entrada posicionado logo abaixo da Raiz
    MAIN["📄 a_maze_ing.py<br/><i>ponto de entrada (CLI)</i>"]
    ROOT --> MAIN
    style MAIN fill:#f9d5a7,stroke:#e6a756

    %% --- COLUNA 1: CLI & DISPLAY ---
    subgraph COL_A ["Interface & Configuração"]
        direction TB
        
        CLI_DIR["📂 cli/"]
        class CLI_DIR folder;
        style CLI_DIR fill:#f9e0d5
        
        CLI_INIT["📄 __init__.py"] --- CLI_PARSER["📄 config_parser.py<br/><i>lê/valida config.txt</i>"] --- CLI_ERRORS["📄 errors.py<br/><i>ConfigError</i>"]
        CLI_DIR --> CLI_INIT
        class CLI_INIT,CLI_PARSER,CLI_ERRORS file;

        DISPLAY_DIR["📂 display/"]
        class DISPLAY_DIR folder;
        style DISPLAY_DIR fill:#e0f9d5
        
        DP_INIT["📄 __init__.py"] --- DP_ASCII["📄 ascii_renderer.py<br/><i>desenha o labirinto</i>"]
        DISPLAY_DIR --> DP_INIT
        class DP_INIT,DP_ASCII file;
    end

    %% --- COLUNA 2: CORE MAZEGEN ---
    subgraph COL_B ["Núcleo do Sistema (mazegen)"]
        direction TB
        
        MAZEGEN_DIR["📂 mazegen/"]
        class MAZEGEN_DIR folder;
        style MAZEGEN_DIR fill:#d5e8f9
        
        MG_INIT["📄 __init__.py"] --- MG_GENERATOR["📄 generator.py<br/><i>Cell + MazeGenerator</i>"] --- MG_ALGORITHMS["📄 algorithms.py<br/><i>dfs/prim/kruskal/wilson</i>"] --- MG_PATTERN["📄 pattern.py<br/><i>desenho do '42'</i>"] --- MG_SOLVER["📄 solver.py<br/><i>MazeSolver (BFS)</i>"] --- MG_ENCODER["📄 encoder.py<br/><i>serializa p/ hex</i>"] --- MG_TYPED["📄 py.typed<br/><i>PEP 561</i>"]
        
        MAZEGEN_DIR --> MG_INIT
        class MG_INIT,MG_GENERATOR,MG_ALGORITHMS,MG_PATTERN,MG_SOLVER,MG_ENCODER,MG_TYPED file;
    end

    %% --- COLUNA 3: APLICAÇÃO ---
    subgraph COL_C ["Orquestração & Menu (app)"]
        direction TB
        
        APP_DIR["📂 app/"]
        class APP_DIR folder;
        style APP_DIR fill:#f0d5f9
        
        APP_INIT["📄 __init__.py"] --- APP_SESSION["📄 session.py<br/><i>orquestra módulos</i>"] --- APP_ANIMATION["📄 animation.py<br/><i>anima o labirinto</i>"] --- APP_MENU["📄 menu.py<br/><i>menu interativo 1-4</i>"]
        
        APP_DIR --> APP_INIT
        class APP_INIT,APP_SESSION,APP_ANIMATION,APP_MENU file;
    end

    %% Conexões da Raiz para as Colunas Organizadoras
    ROOT --> CLI_DIR
    ROOT --> MAZEGEN_DIR
    ROOT --> APP_DIR

    %% Ajuste visual de layout para forçar agrupamento vertical
    COL_A ~~~ COL_B ~~~ COL_C

```

*(Sem `tests/`, `README.md`, `LICENSE.md`, `pyproject.toml`, `Makefile`, `config.txt` — só a parte de código.)*

---

## Diagrama 2 — Funções por arquivo e suas referências

### 2a. Núcleo — `mazegen/`

```mermaid
graph TD
    %% Configuração de Estilo para Legibilidade
    classDef func fill:#fff,stroke:#333,stroke-width:1px;
    classDef sub fill:#f1f5f9,stroke:#475569,stroke-width:2px,font-weight:bold;

    %% COLUNA DA ESQUERDA: Geração e Algoritmos
    subgraph COL_LEFT ["Estrutura de Geração"]
        direction TB

        subgraph GEN ["📦 mazegen/generator.py"]
            direction TB
            g_cell["Cell (dataclass)"] --- g_isopen["Cell.is_open()"] --- g_bit["Cell._direction_bit()"] --- g_init["MazeGenerator.__init__()"] --- g_empty["_create_empty_grid()"] --- g_openp["_open_passage()"] --- g_freen["_free_neighbors()"] --- g_freep["_free_positions()"] --- g_carve["_carve_tree()"] --- g_blockopen["_block_is_open()"] --- g_hasblock["_has_open_block_near()"] --- g_tryopen["_try_open()"] --- g_isdead["_is_dead_end()"] --- g_notdeadpos["_is_not_dead_end_position()"] --- g_closedn["_closed_neighbors()"] --- g_removedead["_remove_dead_ends()"] --- g_countpass["_count_passages()"] --- g_addloops["_add_extra_loops()"] --- g_steps["generate_steps()"] --- g_generate["generate()"]
        end
        style GEN fill:#d5e8f9,stroke:#4a90e2

        subgraph ALGO ["📦 mazegen/algorithms.py"]
            direction TB
            a_dfs["dfs_edges()"] --- a_prim["prim_edges()"] --- a_root["_find_root()"] --- a_kruskal["kruskal_edges()"] --- a_wilson["wilson_edges()"] --- a_names["algorithm_names()"] --- a_dict["_algorithms()"] --- a_gen["generate_edges()"]
        end
        style ALGO fill:#e2f9d5,stroke:#7ed321
    end

    %% COLUNA DA DIREITA: Utilitários, Padrões e Resolução
    subgraph COL_RIGHT ["Suporte, Padrões & Solução"]
        direction TB

        subgraph PATTERN ["📦 mazegen/pattern.py"]
            direction TB
            p_rows["pattern_rows()"] --- p_min["minimum_size()"] --- p_plan["plan_pattern()"]
        end
        style PATTERN fill:#f9e0d5,stroke:#f5a623

        subgraph SOLVER ["📦 mazegen/solver.py"]
            direction TB
            s_init["MazeSolver.__init__()"] --- s_solve["solve()"]
        end
        style SOLVER fill:#f0d5f9,stroke:#bd10e0

        subgraph ENCODER ["📦 mazegen/encoder.py"]
            direction TB
            e_cell["encode_cell()"] --- e_grid["encode_grid()"] --- e_maze["encode_maze()"] --- e_write["write_file()"]
        end
        style ENCODER fill:#f9f7d5,stroke:#d4b200
    end

    %% Aplica estilos em lote
    class g_cell,g_isopen,g_bit,g_init,g_empty,g_openp,g_freen,g_freep,g_carve,g_blockopen,g_hasblock,g_tryopen,g_isdead,g_notdeadpos,g_closedn,g_removedead,g_countpass,g_addloops,g_steps,g_generate func;
    class a_dfs,a_prim,a_root,a_kruskal,a_wilson,a_names,a_dict,a_gen func;
    class p_rows,p_min,p_plan,s_init,s_solve,e_cell,e_grid,e_maze,e_write func;

    %% Relações Cruzadas Indicativas (Colocadas no final para não distorcer o layout)
    g_carve -.->|"usa"| a_gen
    g_steps -.->|"valida"| p_plan
    s_solve -.->|"lê"| g_isopen
    e_cell -.->|"lê"| g_cell

    %% Força o alinhamento das duas colunas principais lado a lado
    COL_LEFT ~~~ COL_RIGHT

```

### 2b. Camada de aplicação — `cli/`, `display/`, `app/`, `a_maze_ing.py`

```mermaid
graph TD
    %% Configuração de Estilo para Legibilidade
    classDef func fill:#fff,stroke:#333,stroke-width:1px;
    
    %% COLUNA 1: CONFIGURAÇÃO E ERROS
    subgraph C1 ["1. Entrada & Configuração"]
        direction TB
        subgraph PARSER ["📦 cli/config_parser.py"]
            direction TB
            pc_config["MazeConfig (dataclass)"] --- pc_bool["parse_bool()"] --- pc_int["parse_int()"] --- pc_posint["parse_positive_int()"] --- pc_coord["parse_coordinates()"] --- pc_algo["parse_algorithm()"] --- pc_inside["check_inside_maze()"] --- pc_read["read_key_values()"] --- pc_req["check_required_keys()"] --- pc_parse["parse_config()"]
        end
        style PARSER fill:#f9e0d5
        
        subgraph ERRORS ["📦 cli/errors.py"]
            err["ConfigError"]
        end
        style ERRORS fill:#ffebe6
    end

    %% COLUNA 2: SESSÃO, ANIMAÇÃO E RENDERIZAÇÃO
    subgraph C2 ["2. Processamento & Telas"]
        direction TB
        subgraph SESSION ["📦 app/session.py"]
            direction TB
            sess_state["MazeState (dataclass)"] --- sess_fromgrid["state_from_grid()"] --- sess_makegen["make_generator()"] --- sess_build["build_maze()"] --- sess_save["save_maze()"]
        end
        style SESSION fill:#f0d5f9

        subgraph ANIM ["📦 app/animation.py"]
            direction TB
            an_stride["frame_stride()"] --- an_animmaze["animate_maze()"] --- an_animpath["animate_path()"]
        end
        style ANIM fill:#eef2f7

        subgraph ASCII ["📦 display/ascii_renderer.py"]
            direction TB
            r_paint["_paint()"] --- r_pathpos["_build_path_positions()"] --- r_horiz["_horizon_line()"] --- r_mid["_middle_line()"] --- r_content["_build_contents()"] --- r_render["render_maze()"]
        end
        style ASCII fill:#e0f9d5
    end

    %% COLUNA 3: ENTRADA E MENU INTERATIVO
    subgraph C3 ["3. Fluxo Principal"]
        direction TB
        subgraph MAIN ["📦 a_maze_ing.py"]
            direction TB
            main_load["load_config()"] --- main_main["main()"]
        end
        style MAIN fill:#f9d5a7

        subgraph MENU ["📦 app/menu.py"]
            direction TB
            m_choice["read_choice()"] --- m_display["display_maze()"] --- m_colors["wall_colors()"] --- m_run["run_menu()"]
        end
        style MENU fill:#fff3cd
    end

    %% Aplica classes de estilo básicas
    class pc_config,pc_bool,pc_int,pc_posint,pc_coord,pc_algo,pc_inside,pc_read,pc_req,pc_parse func;
    class err,sess_state,sess_fromgrid,sess_makegen,sess_build,sess_save func;
    class an_stride,an_animmaze,an_animpath,r_paint,r_pathpos,r_horiz,r_mid,r_content,r_render func;
    class main_load,main_main,m_choice,m_display,m_colors,m_run func;

    %% Conexões e Dependências Essenciais (Simplificadas para não estragar a verticalidade)
    main_load -.-> pc_parse
    main_load -.-> err
    pc_parse -.-> err
    
    sess_fromgrid -.->|"resolve"| SOLVER_SOLVE["mazegen.solver.MazeSolver.solve()"]
    sess_makegen -.->|"instancia"| GEN_INIT["mazegen.generator.MazeGenerator.__init__()"]
    sess_save -.->|"grava"| ENC_MAZE["mazegen.encoder.encode_maze()"]

    an_animmaze -.-> sess_makegen
    an_animmaze -.-> r_render
    an_animpath -.-> r_render

    m_run -.-> an_animmaze
    m_run -.-> sess_save
    m_run -.-> an_animpath
    main_main -.-> m_run

    %% Mantém as 3 grandes colunas alinhadas lado a lado
    C1 ~~~ C2 ~~~ C3

```