GreenPlay v16.191

Correções focadas em desempenho do player:
- saída/redução da tela cheia mais imediata em TV Box e Android TV;
- em TV/TV Box não força mudança de orientação ao sair da tela cheia;
- no celular, restaura o player primeiro e gira para retrato depois, sem desmontar/reiniciar o stream;
- evita reinício do mesmo canal quando ele já está tocando;
- watchdog não reinicia o player durante transições de tela;
- tolerância maior a jitter/buffering antes de tentar recuperação automática;
- mantém o mesmo ExoPlayer durante abrir/fechar tela cheia para reduzir travamentos.
