GreenPlay v16.187

Correção da troca TV/TV Box <-> celular:
- não abre outra Activity e não reinicia o processo ao trocar de modo;
- preserva catálogo e cache de capas que já estavam carregados;
- enquanto prepara o novo layout, mantém a tela atual visível (sem tela cinza);
- ao voltar para celular, pré-aquece as capas críticas e só então troca o layout;
- fail-safe curto para não travar a troca caso alguma imagem esteja lenta;
- mantém as correções de canais da TV/TV Box e demais ajustes da v16.186.
