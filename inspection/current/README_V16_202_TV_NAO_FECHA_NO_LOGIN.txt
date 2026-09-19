GreenPlay v16.202

Correção baseada no vídeo enviado:
- o aplicativo saía da tela de login e voltava ao launcher da TV ao receber Voltar/Escape/B do controle;
- na tela de login, Voltar agora NÃO fecha o aplicativo diretamente;
- é exibida confirmação "Sair do aplicativo?" antes de encerrar;
- KEYCODE_BACK, KEYCODE_ESCAPE e BUTTON_B são tratados no modo TV;
- mantém teclado adaptado, foco visual e botão mostrar/ocultar senha da v16.201.

Observação: o vídeo mostra uma saída limpa para o launcher, sem mensagem de erro do Android. Este patch evita a saída acidental pelo controle. Se houver encerramento sem qualquer tecla de Voltar/Home, será necessário logcat do aparelho para identificar crash nativo/específico do firmware.
