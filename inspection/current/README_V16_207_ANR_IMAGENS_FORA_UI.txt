GreenPlay v16.207 — correção de "não está respondendo" (ANR)

Correção principal:
- remove leitura/decodificação de imagens do cache em disco da thread principal;
- BitmapFactory.decode e acesso ao cache de arquivos agora rodam somente nos pools de imagem;
- a thread da interface consulta apenas o cache em RAM e continua respondendo ao toque/controle;
- mantém todas as correções da v16.206 (TV/TV Box, login, player, telas do plano, logo fallback etc.).

Motivo encontrado:
A função Img.loadBest() fazia disk() para vários candidatos de capa na thread de UI.
Em Homes com muitos cards isso podia bloquear o Android por vários segundos e causar ANR.
