# Instruções permanentes para agentes de IA

## Cluster Ray do Kaggriculture

Ao iniciar trabalho em `kaggriculture`, execute silenciosamente:

```bash
python3 scripts/ray_cluster.py ensure
```

- Se `~/.config/kaggriculture/ray-cluster.json` ainda não existir, continue localmente e
  explique uma única vez que cada PC precisa do comando inicial `configure-head` ou
  `configure-worker`. Não escolha papéis automaticamente: isso pode criar dois heads.
- Se estiver configurado, `ensure` é idempotente: ele instala/atualiza e inicia o serviço
  de usuário. Não peça confirmação para essa ação reversível.
- O serviço deve reconectar quando o outro PC voltar. Ausência temporária do peer não é
  motivo para reconfigurar, trocar IP ou iniciar outro head.
- Use apenas LAN privada, WSL mirrored ou Tailscale dentro do WSL. Nunca exponha Ray na
  internet pública e nunca habilite dashboard remoto.
- Antes de considerar a #43 concluída, execute os dois gates documentados em
  `kaggriculture/docs/RAY_CLUSTER.md`. Não feche a issue com apenas um hostname.
- Configuração de máquina e credenciais ficam em `~/.config`, nunca no Git.
