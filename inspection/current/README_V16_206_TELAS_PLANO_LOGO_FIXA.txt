GreenPlay v16.206

Correções:
- Perfil passa a resolver o total de telas pelo access_status e, quando necessário,
  consulta os pacotes do painel para casar o plano ativo (por ID ou nome) e puxar
  a quantidade real de telas.
- Campo Telas passa a mostrar uso x limite (ex.: 1 de 10) em vez de fixar 1 de 1.
- Quantidade resolvida fica em cache por usuário para não voltar para 1 durante
  trocas de modo/recargas.
- Logo GreenPlay embutida no APK como fallback imediato.
- Durante carregamento e troca TV <-> celular a logo aparece na hora, enquanto a
  logo remota do painel atualiza por cima quando disponível.
- Home e cabeçalhos TV/celular também usam fallback da logo para não ficar vazio.

Base: v16.205.
