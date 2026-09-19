GreenPlay v16.209 — correções exclusivas do modo TV / TV Box

Escopo:
- nenhuma alteração intencional no fluxo visual/comportamento do modo celular;
- correções aplicadas somente quando o app está em Android TV/TV Box (tvMode).

Correções:
1. Foco das categorias no controle
- categoria focada agora recebe destaque forte (fundo verde, texto escuro e borda branca);
- trilho horizontal centraliza/acompanha a categoria focada;
- categoria selecionada permanece identificável mesmo quando o foco sai dela.

2. Foco dos canais
- preserva o listener próprio de foco dos cards de canais;
- impede a rotina global de foco da TV de sobrescrever o destaque dos cards.

3. Travamentos / lentidão do modo TV
- a varredura global da árvore de views foi limitada e agrupada;
- deixa de percorrer toda a tela a cada alteração de layout/frame do player/listas;
- pausa a varredura durante fullscreen e transições da TV.

4. Voltar / tela verde na TV
- em Android TV/TV Box, o player não é mais removido e recolocado na árvore da tela ao entrar/sair do fullscreen;
- mantém a mesma superfície do player durante a transição para evitar Surface/decoder perdido ou quadro verde em determinadas TVs;
- ao sair do fullscreen/cinema restaura painel de canais, barra superior, fundo e foco;
- Back/Escape/B do controle passam pelo mesmo fluxo de retorno do app.

Base: v16.208
Painel: compatível com v74; nenhuma alteração de painel necessária para estas correções.
