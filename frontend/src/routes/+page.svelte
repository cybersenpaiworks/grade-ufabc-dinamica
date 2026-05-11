<script lang="ts">
  import dadosMock from "$lib/turmas.json";

  // --- 1. DEFINIÇÃO DE TIPOS (TYPESCRIPT) ---
  interface Horario {
    dia: string;
    inicio: string;
    fim: string;
    frequencia: string;
  }

  interface Turma {
    CURSO: string;
    "CÓDIGO DE TURMA": string;
    TURMA: string;
    CAMPUS: string;
    TURNO: string;
    "VAGAS TOTAIS": string;
    "VAGAS REMANESCENT ES": string;
    HORARIOS_TEORIA?: Horario[];
    HORARIOS_PRATICA?: Horario[];
    [key: string]: any;
  }

  type TurmaGrade = Turma & { tipo: "T" | "P" };

  // --- 2. ESTADO INICIAL E DADOS ---
  let turmas: Turma[] = dadosMock.dados as Turma[];

  // Estados dos filtros
  let termoBusca: string = "";
  let cursoSelecionado: string = '';
  let campusSelecionado: string = "";
  let turnoSelecionado: string = "";
  let apenasComVagas: boolean = false;
  let diaSelecionado: string = '';
  let horarioSelecionado: string = '';

  // Estado global da grade
  let turmasSelecionadas: Turma[] = [];

  // Constantes de visualização
  const diasSemana: string[] = [
    "segunda",
    "terça",
    "quarta",
    "quinta",
    "sexta",
    "sábado",
  ];
  const blocosHorario = [
    { inicio: "08:00", fim: "10:00" },
    { inicio: "10:00", fim: "12:00" },
    { inicio: "14:00", fim: "16:00" },
    { inicio: "16:00", fim: "18:00" },
    { inicio: "19:00", fim: "21:00" },
    { inicio: "21:00", fim: "23:00" },
  ];

  // --- 3. LÓGICA DE NEGÓCIO ---
  function toggleTurma(turma: Turma): void {
    const jaSelecionada = turmasSelecionadas.some(
      (t) => t["CÓDIGO DE TURMA"] === turma["CÓDIGO DE TURMA"],
    );

    if (jaSelecionada) {
      turmasSelecionadas = turmasSelecionadas.filter(
        (t) => t["CÓDIGO DE TURMA"] !== turma["CÓDIGO DE TURMA"],
      );
    } else {
      turmasSelecionadas = [...turmasSelecionadas, turma];
    }
  }

  // --- 4. MOTOR REATIVO ---
  // Extração de opções únicas para os dropdowns
  $: cursosDisponiveis = [...new Set(turmas.map(t => t.CURSO).filter(Boolean))].sort();
  $: campiDisponiveis = [
    ...new Set(turmas.map((t) => t.CAMPUS).filter(Boolean)),
  ].sort();
  $: turnosDisponiveis = [
    ...new Set(turmas.map((t) => t.TURNO).filter(Boolean)),
  ].sort();

  // Filtro de tabela multidimensional
  $: turmasFiltradas = turmas.filter((turma) => {
    const matchBusca =
      termoBusca === "" ||
      turma.TURMA.toLowerCase().includes(termoBusca.toLowerCase()) ||
      turma.CURSO.toLowerCase().includes(termoBusca.toLowerCase());
    const matchCurso = cursoSelecionado === '' || turma.CURSO === cursoSelecionado;
    const matchCampus =
      campusSelecionado === "" || turma.CAMPUS === campusSelecionado;
    const matchTurno =
      turnoSelecionado === "" || turma.TURNO === turnoSelecionado;

    const vagasLivres = parseInt(turma["VAGAS REMANESCENT ES"] || "0");
    const matchVagas = apenasComVagas ? vagasLivres > 0 : true;

    const horariosTurma = [...(turma.HORARIOS_TEORIA || []), ...(turma.HORARIOS_PRATICA || [])];
    
    const matchDia = diaSelecionado === '' || horariosTurma.some(h => h.dia === diaSelecionado);
    const matchHorario = horarioSelecionado === '' || horariosTurma.some(h => h.inicio === horarioSelecionado);

    return matchBusca && matchCurso && matchCampus && matchTurno && matchVagas && matchDia && matchHorario;
  });

  // Identificador de aula para a Grade Visual
  $: obterTurmaNoHorario = (dia: string, inicio: string): TurmaGrade | null => {
    for (const turma of turmasSelecionadas) {
      const teoria = turma.HORARIOS_TEORIA || [];
      if (teoria.some((h) => h.dia === dia && h.inicio === inicio))
        return { ...turma, tipo: "T" };

      const pratica = turma.HORARIOS_PRATICA || [];
      if (pratica.some((h) => h.dia === dia && h.inicio === inicio))
        return { ...turma, tipo: "P" };
    }
    return null;
  };

  // Verifica se uma turma candidata tem choque de horário com as já selecionadas
  $: temConflito = (turma: Turma): boolean => {
    // Se a turma já está na grade, ignoramos o aviso de "conflito" para não ficar vermelho
    if (
      turmasSelecionadas.some(
        (t) => t["CÓDIGO DE TURMA"] === turma["CÓDIGO DE TURMA"],
      )
    )
      return false;

    const horariosNovaTurma = [
      ...(turma.HORARIOS_TEORIA || []),
      ...(turma.HORARIOS_PRATICA || []),
    ];

    for (const hNovo of horariosNovaTurma) {
      for (const tSelecionada of turmasSelecionadas) {
        const horariosSelecionada = [
          ...(tSelecionada.HORARIOS_TEORIA || []),
          ...(tSelecionada.HORARIOS_PRATICA || []),
        ];

        const bateuHorario = horariosSelecionada.some((hSel) => {
          // Se for no mesmo dia e mesmo horário de início
          if (hSel.dia === hNovo.dia && hSel.inicio === hNovo.inicio) {
            // Verifica se são quinzenais complementares
            const f1 = (hNovo.frequencia || "").toLowerCase();
            const f2 = (hSel.frequencia || "").toLowerCase();

            if (
              (f1.includes("quinzenal i") && f2.includes("quinzenal ii")) ||
              (f1.includes("quinzenal ii") && f2.includes("quinzenal i"))
            ) {
              return false; // Encaixe perfeito, não é conflito
            }

            return true; // Bateu horário e não são complementares = CONFLITO!
          }
          return false;
        });

        if (bateuHorario) return true;
      }
    }
    return false;
  };
</script>

<main class="container">
  <h1>Explorador de Turmas UFABC</h1>

  <div class="filtros-container">
    <div class="filtro-item busca-texto">
      <label for="busca">Buscar Disciplina</label>
      <input 
        id="busca"
        type="text" 
        bind:value={termoBusca} 
        placeholder="Ex: Biologia Molecular..."
      />
    </div>

    <div class="filtro-item">
      <label for="curso">Curso</label>
      <select id="curso" bind:value={cursoSelecionado}>
        <option value="">Todos</option>
        {#each cursosDisponiveis as curso}
          <option value={curso}>{curso}</option>
        {/each}
      </select>
    </div>

    <div class="filtro-item">
      <label for="campus">Campus</label>
      <select id="campus" bind:value={campusSelecionado}>
        <option value="">Todos</option>
        {#each campiDisponiveis as campus}
          <option value={campus}>{campus}</option>
        {/each}
      </select>
    </div>

    <div class="filtro-item">
      <label for="turno">Turno</label>
      <select id="turno" bind:value={turnoSelecionado}>
        <option value="">Todos</option>
        {#each turnosDisponiveis as turno}
          <option value={turno}>{turno}</option>
        {/each}
      </select>
    </div>

    <div class="filtro-item">
      <label for="dia">Dia da Semana</label>
      <select id="dia" bind:value={diaSelecionado}>
        <option value="">Todos</option>
        {#each diasSemana as dia}
          <option value={dia} class="capitalize">{dia}</option>
        {/each}
      </select>
    </div>

    <div class="filtro-item">
      <label for="horario">Horário</label>
      <select id="horario" bind:value={horarioSelecionado}>
        <option value="">Todos</option>
        {#each blocosHorario as bloco}
          <option value={bloco.inicio}>{bloco.inicio} às {bloco.fim}</option>
        {/each}
      </select>
    </div>

    <div class="filtro-item toggle-vagas">
      <label class="checkbox-label">
        <input type="checkbox" bind:checked={apenasComVagas} />
        Mostrar apenas turmas com vagas livres
      </label>
    </div>
  </div>

  <div class="resumo-resultados">
    <p>
      Mostrando <strong>{turmasFiltradas.length}</strong> de {turmas.length} turmas
      encontradas.
    </p>
  </div>

  <div class="tabela-container">
    <table>
      <thead>
        <tr>
          <th>Ação</th>
          <th>Curso</th>
          <th>Disciplina</th>
          <th>Campus</th>
          <th>Turno</th>
          <th>Vagas Totais</th>
          <th>Vagas Livres</th>
        </tr>
      </thead>
      <tbody>
        {#each turmasFiltradas as turma (turma["CÓDIGO DE TURMA"])}
          <tr
            class="
            {turmasSelecionadas.some(
              (t) => t['CÓDIGO DE TURMA'] === turma['CÓDIGO DE TURMA'],
            )
              ? 'linha-selecionada'
              : ''} 
            {temConflito(turma) ? 'linha-conflito' : ''}
          "
          >
            <td>
              <button
                class="btn-acao {turmasSelecionadas.some(
                  (t) => t['CÓDIGO DE TURMA'] === turma['CÓDIGO DE TURMA'],
                )
                  ? 'btn-remover'
                  : 'btn-adicionar'}"
                on:click={() => toggleTurma(turma)}
              >
                {turmasSelecionadas.some(
                  (t) => t["CÓDIGO DE TURMA"] === turma["CÓDIGO DE TURMA"],
                )
                  ? "Remover"
                  : "Adicionar"}
              </button>
            </td>
            <td class="text-sm">{turma.CURSO}</td>
            <td>
              <strong>{turma.TURMA.split("-")[0]}</strong>
              {#if temConflito(turma)}
                <br /><span class="aviso-conflito">⚠️ Choque de Horário</span>
              {/if}
            </td>
            <td><span class="badge">{turma.CAMPUS}</span></td>
            <td>{turma.TURNO}</td>
            <td>{turma["VAGAS TOTAIS"]}</td>
            <td>
              <span
                class="vagas-badge {parseInt(turma['VAGAS REMANESCENT ES']) > 0
                  ? 'vagas-ok'
                  : 'vagas-zero'}"
              >
                {turma["VAGAS REMANESCENT ES"]}
              </span>
            </td>
          </tr>
        {/each}

        {#if turmasFiltradas.length === 0}
          <tr>
            <td colspan="7" class="estado-vazio"
              >Nenhuma turma encontrada com estes filtros.</td
            >
          </tr>
        {/if}
      </tbody>
    </table>
  </div>

  {#if turmasSelecionadas.length > 0}
    <div class="grade-container">
      <h2>Sua Grade Montada ({turmasSelecionadas.length} disciplinas)</h2>

      <div class="grade-tabela">
        <table>
          <thead>
            <tr>
              <th class="horario-col-header">Horário</th>
              {#each diasSemana as dia}
                <th class="capitalize">{dia}</th>
              {/each}
            </tr>
          </thead>
          <tbody>
            {#each blocosHorario as bloco}
              <tr>
                <td class="horario-col">{bloco.inicio} - {bloco.fim}</td>

                {#each diasSemana as dia}
                  {@const aula = obterTurmaNoHorario(dia, bloco.inicio)}

                  <td class="celula-grade {aula ? 'tem-aula' : ''}">
                    {#if aula}
                      <div class="aula-card">
                        <span class="aula-nome" title={aula.TURMA}
                          >{aula.TURMA.split("-")[0]}</span
                        >
                        <div class="aula-meta">
                          <span
                            class="badge {aula.tipo === 'T'
                              ? 'badge-teoria'
                              : 'badge-pratica'}"
                          >
                            {aula.tipo === "T" ? "Teoria" : "Prática"}
                          </span>
                          <span class="badge">{aula.CAMPUS}</span>
                        </div>
                      </div>
                    {/if}
                  </td>
                {/each}
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </div>
  {/if}
</main>

<style>
  /* Base */
  .container {
    padding: 2rem;
    font-family: system-ui, sans-serif;
    max-width: 1400px;
    margin: 0 auto;
  }
  h1 {
    color: #212529;
    margin-bottom: 1.5rem;
  }

  /* Filtros */
  .filtros-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 8px;
    border: 1px solid #e9ecef;
  }
  .filtro-item {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  .toggle-vagas {
    grid-column: 1 / -1;
    padding-top: 0.5rem;
    border-top: 1px dashed #dee2e6;
  }
  .checkbox-label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
    font-size: 0.95rem;
    color: #0056b3;
    font-weight: 600;
  }
  .checkbox-label input {
    width: 1.2rem;
    height: 1.2rem;
    cursor: pointer;
  }
  label {
    font-size: 0.875rem;
    font-weight: 600;
    color: #495057;
  }
  input[type="text"],
  select {
    padding: 0.75rem;
    border: 1px solid #ced4da;
    border-radius: 4px;
    font-size: 1rem;
    background-color: white;
  }
  .resumo-resultados {
    margin-bottom: 1rem;
    color: #6c757d;
    font-size: 0.9rem;
  }

  /* Tabela de Dados */
  .tabela-container {
    overflow-x: auto;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    max-height: 500px;
    overflow-y: auto;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
  }
  th,
  td {
    border-bottom: 1px solid #dee2e6;
    padding: 0.75rem 1rem;
  }
  th {
    background-color: #f8f9fa;
    font-weight: 600;
    color: #495057;
    position: sticky;
    top: 0;
    z-index: 10;
    box-shadow: 0 2px 2px -1px rgba(0, 0, 0, 0.1);
  }
  tr:hover {
    background-color: #f8f9fa;
  }
  .text-sm {
    font-size: 0.85rem;
    color: #495057;
  }

  /* Badges e Botões */
  .badge {
    background-color: #e9ecef;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: bold;
    color: #495057;
  }
  .vagas-badge {
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-weight: bold;
  }
  .vagas-ok {
    background-color: #d4edda;
    color: #155724;
  }
  .vagas-zero {
    background-color: #f8d7da;
    color: #721c24;
  }
  .estado-vazio {
    text-align: center;
    padding: 3rem;
    color: #6c757d;
  }

  .btn-acao {
    padding: 0.4rem 0.75rem;
    border: none;
    border-radius: 4px;
    font-weight: 600;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.2s;
    width: 85px;
  }
  .btn-adicionar {
    background-color: #0d6efd;
    color: white;
  }
  .btn-adicionar:hover {
    background-color: #0b5ed7;
  }
  .btn-remover {
    background-color: #dc3545;
    color: white;
  }
  .btn-remover:hover {
    background-color: #bb2d3b;
  }

  /* Grade Horária */
  .grade-container {
    margin-top: 3rem;
    border-top: 2px dashed #dee2e6;
    padding-top: 2rem;
  }
  .grade-container h2 {
    margin-bottom: 1.5rem;
    color: #212529;
  }
  .grade-tabela {
    overflow-x: auto;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    background: white;
  }
  .grade-tabela table {
    min-width: 900px;
    table-layout: fixed;
  }
  .grade-tabela th {
    background-color: #343a40;
    color: white;
    text-align: center;
    border: 1px solid #454d55;
    position: static;
    box-shadow: none;
  }
  .grade-tabela td {
    border: 1px solid #dee2e6;
    padding: 0.5rem;
    vertical-align: top;
    height: 110px;
  }
  .horario-col-header {
    width: 120px;
  }
  .horario-col {
    background-color: #f8f9fa;
    font-weight: bold;
    text-align: center;
    vertical-align: middle !important;
    color: #495057;
  }
  .capitalize {
    text-transform: capitalize;
  }

  .tem-aula {
    background-color: #f0f7ff;
    box-shadow: inset 0 0 0 2px #cce3ff;
  }
  .aula-card {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    height: 100%;
    justify-content: space-between;
  }
  .aula-nome {
    font-size: 0.8rem;
    font-weight: 700;
    line-height: 1.3;
    color: #052c65;
    display: -webkit-box;
    line-clamp: 3;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  .aula-meta {
    display: flex;
    gap: 0.25rem;
    flex-wrap: wrap;
  }
  .badge-teoria {
    background-color: #fd7e14;
    color: white;
  }
  .badge-pratica {
    background-color: #20c997;
    color: white;
  }

  /* Estilos Dinâmicos da Tabela */
  tr.linha-selecionada {
    background-color: #f0f7ff !important;
    border-left: 4px solid #0d6efd;
  }

  tr.linha-conflito {
    background-color: #fff5f5 !important;
    opacity: 0.75; /* Deixa a linha mais opaca para indicar que não é ideal */
  }

  tr.linha-conflito td {
    color: #842029;
  }

  .aviso-conflito {
    font-size: 0.7rem;
    color: #dc3545;
    font-weight: bold;
  }

  @media (max-width: 768px) {
    .filtros-container {
      grid-template-columns: 1fr;
    }
  }
</style>
