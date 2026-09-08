# Kaggriculture Lab

Laboratório de estratégias para Kaggriculture: execução no interpretador oficial,
avaliação reproduzível nos dois assentos e artefatos de submissão congelados.
O critério competitivo é vitória/derrota/empate contra adversários fortes;
dinheiro e margem são diagnósticos.

Requer Python 3.12+ e Linux, macOS ou WSL. A partir do repositório:

```bash
cd kaggriculture
bash scripts/setup.sh
source .venv/bin/activate
python -m pytest -q
```

O ambiente é `kaggle-environments==1.32.7`, com versão e hash do interpretador
validados. Mudanças de ambiente exigem revalidação dos resultados.

- [Guia de execução e arquitetura](kaggriculture/README.md): partidas, ligas,
  empacotamento e preflight pelo loader real.
- [Comparação pareada e gate](kaggriculture/docs/PAIRED_EVALUATION.md): duas pernas
  em um comando, 100 blocos, ratings congelados e recomendação `SUBMIT`/`NO SUBMIT`.
- [Registro de seeds](kaggriculture/seed_registry.json): autoridade aplicada pelo
  CLI. Validação é consumida antes da execução; holdout permanece protegido.
- [Registro de adversários](kaggriculture/opponents/manifest.json): arquivos
  externos, hashes, famílias e proveniência. Licenças e atribuições acompanham
  os bundles; esses arquivos não se tornam automaticamente parte da submissão.
- [Versões imutáveis](kaggriculture/versions/): agentes e manifestos congelados.
  Use caminhos explícitos para avaliar versões recentes: o alias `champion`
  continua apontando para v000, e `challenger` para o planner em desenvolvimento.

O gate mede evidência competitiva local. A submissão ainda depende do preflight
do artefato e da política de agentes ativos. Nenhum desses comandos envia uma
submissão ao Kaggle.
