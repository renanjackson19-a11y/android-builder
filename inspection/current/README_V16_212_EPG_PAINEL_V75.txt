GreenPlay v16.212 — integração EPG otimizada com painel v75
========================================================

Base
----
- Mantém integralmente as correções da v16.211 para TV/TV Box.
- O comportamento do celular foi preservado.

EPG no modo TV/TV Box
----------------------
1. Compatibilidade direta com:
   - /api/dtlive/get_short_epg/
   - /api/dtlive/get_epg/

2. Na TV, o app consulta primeiro get_short_epg.
   - Se houver programação, usa a resposta imediatamente.
   - Se vier vazio ou falhar, tenta get_epg como fallback.
   - Evita duas requisições simultâneas por troca de canal.

3. Cache curto de EPG no aplicativo (50 segundos).
   - Evita repetir a mesma consulta ao passar pelo mesmo canal.
   - Ajuda a preservar fluidez em TVs/TV Box mais fracas.
   - O cache é separado por provedor e canal.

4. A lista de canais reutiliza o EPG em cache quando disponível.

5. A exibição existente continua:
   - programação atual no card do canal;
   - ATUAL e PRÓXIMO no overlay do player;
   - horários normalizados quando enviados pelo painel.

Painel recomendado
------------------
- GreenPlay Painel v75 EPG Automático.
- A v16.212 também mantém o fallback anterior no celular sem alterar seu fluxo.
