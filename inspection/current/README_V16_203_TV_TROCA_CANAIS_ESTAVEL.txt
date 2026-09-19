GreenPlay v16.203

Correções feitas a partir do vídeo enviado:
- evita travamento ao trocar muitos canais rapidamente no controle;
- aplica debounce curto de 180 ms e cancela trocas antigas antes de abrir o novo canal;
- impede callbacks de recuperação do canal anterior de reiniciarem o player depois de outra troca;
- reduz a quantidade de chamadas de EPG abertas de uma vez na lista (as demais carregam sob demanda ao focar);
- reforça o foco dos cards de canais para ficar visível no controle;
- mantém as correções de login/teclado/senha/Back da v16.202.

Observação: no vídeo o app não chega a sair para a tela inicial da TV; o que aparece no final é o player ficando em "Carregando canal..." depois de várias trocas. Esta versão trata exatamente esse fluxo.
