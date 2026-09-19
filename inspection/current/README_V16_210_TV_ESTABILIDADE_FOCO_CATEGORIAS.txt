GreenPlay v16.210 — correção exclusiva do modo TV / TV Box

Base: v16.209 (derivada da v16.208)
Painel: v74, sem alterações.
Modo celular: preservado; as mudanças desta versão são condicionadas ao modo TV.

Correções principais:
1. Menu superior da TV (TV, Destaque, Futebol, Filmes, Séries, Kids e Favoritos)
- foco do controle agora tem destaque visual forte: fundo verde, texto escuro e borda branca;
- os itens do menu são armados diretamente para foco, sem depender da varredura global.

2. Categoria de canais pulando para a última categoria
- corrigida a ligação de foco entre o primeiro canal e a faixa de categorias;
- antes, o mesmo primeiro canal era ligado em sequência a todas as categorias e o nextFocusUp acabava sobrescrito pela última;
- agora o UP do primeiro canal retorna para a categoria selecionada/focada, de forma determinística.

3. Travamentos ao navegar categorias/canais
- a tela TV deixa de executar varredura global de toda a árvore de views durante layouts/scroll/player;
- respostas antigas de categorias são descartadas por geração, evitando uma categoria antiga reconstruir a lista depois de outra já ter sido selecionada;
- lotes antigos de renderização também são invalidados ao trocar de categoria;
- na TV, a lista deixa de criar até 300 cards de uma vez: monta o primeiro lote e adiciona novos lotes conforme o foco se aproxima do fim;
- logos fora do primeiro lote são carregadas sob demanda;
- EPG individual não dispara em massa ao abrir a lista e é carregado somente após o foco permanecer no canal por um curto período;
- removida a reconstrução automática duplicada da lista quando já existe snapshot completo do catálogo.

4. Preservação
- nenhuma mudança de painel necessária;
- nenhuma alteração intencional no fluxo do modo celular.
