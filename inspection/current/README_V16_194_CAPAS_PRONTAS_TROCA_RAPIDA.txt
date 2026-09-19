GreenPlay v16.194

Correções desta versão:
- ao trocar TV/TV Box <-> celular, o loading prepara as primeiras capas de cada seção antes de liberar a Home;
- o carregador de imagens usa 6 workers visíveis e 3 workers de prefetch;
- cards tentam múltiplas URLs de imagem (thumbnail/portrait/image/landscape) antes de ficar vazios;
- cache em RAM/disco é consultado antes da rede para evitar espera desnecessária;
- prefetch em segundo plano passa a avançar em paralelo pelas outras seções.
