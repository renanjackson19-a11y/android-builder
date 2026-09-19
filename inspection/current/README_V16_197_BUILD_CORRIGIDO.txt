GreenPlay v16.197

Correção:
- Corrigido erro de compilação em MainActivity.java na função buildModeReadyFeatured.
- Havia uma chave "}" sobrando antes das linhas que criavam Random/shuffle, o que fazia o Java interpretar aquelas instruções fora do método e gerar "<identifier> expected" na linha 92.
- Mantidas as mudanças da v16.196 para carregar os Destaques antes de abrir a Home.
