GreenPlay Android Nativo v16.19

CORREÇÃO PRINCIPAL
- APK Debug agora usa uma assinatura fixa incluída no projeto.
- O package Debug continua fun.greenplay.app.debug.
- versionCode 40 / versionName 1.16.19.
- As próximas versões derivadas desta v16.19 devem preservar app/greenplay-debug.keystore e o signingConfig stableDebug.

IMPORTANTE
As versões Debug anteriores eram assinadas pela chave temporária do runner do GitHub Actions.
Por isso, a primeira instalação da v16.19 ainda exige remover a versão antiga uma única vez.
Depois que a v16.19 estiver instalada, versões futuras que preservarem esta mesma chave poderão ser instaladas por cima normalmente.

Esta chave é somente para builds de teste/debug. Para publicação em loja deve ser usada uma chave de release privada e protegida.
