# Landscape Survey: Sandboxing and Isolation for Agentic AI Systems

Date: 2026-03-10

## Executive Summary

The agentic AI ecosystem has converged on a clear consensus: **shared-kernel container isolation (standard Docker/runc) is insufficient for executing untrusted AI-generated code**. The industry is rapidly moving toward microVMs (Firecracker, Kata Containers), user-space kernels (gVisor), and purpose-built sandbox platforms. This document catalogs how every major agentic framework and product handles execution environments, with concrete technical details and references.

---

## 1. Isolation Technologies: A Taxonomy

### 1.1 Standard Docker Containers (Linux namespaces + cgroups)

- **Security model**: Process-level isolation sharing the host kernel
- **Startup**: Milliseconds
- **Key limitation**: Kernel vulnerability or misconfiguration allows container escape and host access
- **Verdict**: Suitable only for trusted, vetted code in single-tenant environments
- **Used by**: AutoGPT (with known escape vulnerabilities), CrewAI (fallback), SWE-bench (evaluation standard)

### 1.2 gVisor (User-Space Kernel)

- **Security model**: Intercepts syscalls in user space via the Sentry process before they reach the host kernel. Reduces kernel attack surface from hundreds of syscalls to a minimal vetted subset
- **Startup**: Milliseconds
- **Overhead**: 10-30% on I/O-heavy workloads; minimal on compute-heavy tasks
- **Used by**: Anthropic (Claude web), Kubernetes Agent Sandbox (default runtime), Google GKE
- **Reference**: [Northflank guide](https://northflank.com/blog/how-to-sandbox-ai-agents)

### 1.3 Firecracker MicroVMs

- **Security model**: Hardware-level isolation with dedicated Linux kernels per workload inside KVM
- **Startup**: ~125ms boot time; <5 MiB memory overhead per VM
- **Scaling**: Up to 150 VMs/second/host
- **Used by**: E2B, AWS Lambda (origin), Fly.io Sprites, Docker Sandboxes (macOS/Windows via platform hypervisors)
- **Reference**: [E2B architecture](https://e2b.dev/docs), [Fly.io Sprites](https://fly.io/blog/code-and-let-live/)

### 1.4 Kata Containers

- **Security model**: Hardware-level isolation orchestrating multiple VMMs (Firecracker, Cloud Hypervisor, QEMU) through standard container APIs
- **Startup**: ~200ms
- **Used by**: Kubernetes Agent Sandbox (alternative runtime), enterprise Kubernetes deployments
- **Reference**: [Kata + Agent Sandbox integration](https://katacontainers.io/blog/kata-containers-agent-sandbox-integration/)

### 1.5 OS-Level Lightweight Sandboxing

- **bubblewrap** (bwrap): Linux namespace-based process restriction. No containers, no VMs. Kernel-level enforcement with fast startup and minimal overhead.
  - **Used by**: Anthropic Claude Code (Linux)
- **macOS Seatbelt** (sandbox-exec): macOS kernel sandbox profiles restricting process capabilities
  - **Used by**: Anthropic Claude Code (macOS)
- **nsjail**: Google-developed process isolation using Linux namespaces + seccomp-bpf filters
  - **Used by**: Google internal systems, available for custom deployments
- **Reference**: [Anthropic engineering blog](https://www.anthropic.com/engineering/claude-code-sandboxing)

### 1.6 WebAssembly (WASM)

- **Security model**: Sandboxed by construction; inherits browser sandbox security properties
- **Implementation**: Pyodide (CPython compiled to WASM) for Python execution
- **Limitations**: Limited to Python standard library + select packages; no native system access
- **Used by**: LangChain Sandbox (now deprecated), HuggingFace smolagents WasmExecutor, Mozilla wasm-agents
- **Reference**: [NVIDIA WASM sandboxing blog](https://developer.nvidia.com/blog/sandboxing-agentic-ai-workflows-with-webassembly/)

### 1.7 Apple Containers (macOS Tahoe, September 2025+)

- **Security model**: Lightweight VMs per container, no shared daemon, sub-second startup
- **Used by**: Emerging alternative for Claude Code on macOS
- **Reference**: [Infralovers blog](https://www.infralovers.com/blog/2026-02-15-sandboxing-claude-code-macos/)

---

## 2. Major Agentic Systems and Their Approaches

### 2.1 Claude Code (Anthropic)

**Isolation approach**: OS-level primitives (bubblewrap on Linux, Seatbelt on macOS)

**Two isolation boundaries**:
1. **Filesystem isolation**: Read/write restricted to current working directory. Blocks access to SSH keys, config files, etc. Enforced at OS level so it applies to all spawned subprocesses.
2. **Network isolation**: Proxy-based architecture using a Unix domain socket. Proxy validates allowed domains; users confirm new domain requests. Administrators can customize proxy rules.

**Key result**: Sandboxing reduces permission prompts by 84%, enabling more autonomous operation.

**Docker integration**: Claude Code can also run inside Docker Sandboxes (see Section 2.10), but its native sandboxing is OS-level, not container-based.

**Critical rule**: Never mount the host Docker socket into a Claude Code container -- this allows sandbox escape.

**References**:
- [Anthropic engineering blog](https://www.anthropic.com/engineering/claude-code-sandboxing)
- [Claude Code sandboxing docs](https://code.claude.com/docs/en/sandboxing)

### 2.2 OpenAI Codex (Cloud + CLI)

**Isolation approach**: Container-based cloud sandbox with network restrictions

**Architecture**:
- Each task creates a fresh container from a `codex-universal` base image (or custom Dockerfile)
- Repository checked out at selected branch/commit SHA
- Setup scripts run with internet access enabled; internet disabled during agent execution
- Secrets available only during setup phase, removed before agent phase
- HTTP/HTTPS network proxy for security and abuse prevention
- Container state cached up to 12 hours; cache invalidates on config changes

**Key design choice**: Internet access disabled during task execution -- agent can only interact with code explicitly provided via GitHub repos and pre-installed dependencies.

**Docker-in-Docker**: Supported but documented as a community discussion topic with friction.

**References**:
- [Codex cloud environments](https://developers.openai.com/codex/cloud/environments/)
- [Codex Docker sandbox docs](https://docs.docker.com/ai/sandboxes/agents/codex/)
- [codex-universal Dockerfile](https://github.com/openai/codex-universal)

### 2.3 Devin (Cognition Labs)

**Isolation approach**: Isolated VMs in cloud, VPC deployment model

**Architecture**:
- Each Devin instance runs in an isolated virtual machine with a Linux shell, code editor, Chromium browser, and the Devin agent
- Multiple parallel instances can be spun up simultaneously
- Enterprise: Virtual Private Cloud (VPC) deployment separates Devin Backend from Customer VPC
- Customer data resides fully within their VPC; communication encrypted in transit
- Dev Box (Linux shell + editor + browser + agent) runs inside customer-controlled environment

**References**:
- [Cognition introducing Devin](https://cognition.ai/blog/introducing-devin)
- [Devin 2.0 technical design](https://medium.com/@takafumi.endo/agent-native-development-a-deep-dive-into-devin-2-0s-technical-design-3451587d23c0)

### 2.4 OpenHands (formerly OpenDevin)

**Isolation approach**: Docker containers with REST API, evolving toward modular SDK

**V0 Architecture**:
- Per-task Docker container sandbox spun up for each session
- REST API server running inside container listens for action execution requests
- Three internal components: Bash shell, Jupyter IPython server, Chromium browser (Playwright)
- Configurable workspace directory mounted into sandbox
- Containers torn down post-session for filesystem integrity

**V1 Architecture (SDK redesign)**:
- Refactored into modular SDK with opt-in sandboxing
- V0 assumption that all tool calls must run in Docker caused friction: two independent processes with divergent states, resource exhaustion in multi-tenant deployments
- V1 provides reusable agent, tool, and workspace packages with clear boundaries

**ICLR 2025 paper**: Published describing the platform architecture.

**References**:
- [OpenHands ICLR 2025 paper](https://openreview.net/pdf/95990590797cff8b93c33af989ecf4ac58bde9bb.pdf)
- [OpenHands SDK paper (arXiv)](https://arxiv.org/html/2511.03690v1)
- [Custom sandbox guide](https://docs.openhands.dev/openhands/usage/advanced/custom-sandbox-guide)

### 2.5 SWE-agent / SWE-bench

**Isolation approach**: Per-task Docker containers (evaluation standard)

**Architecture**:
- Each of 500 SWE-bench tasks runs in an isolated Docker container
- Container captures exact repo state immediately before the PR was merged
- Public Docker image registry with optimized layer caching (67 GiB for 2290 images, 10x reduction)
- SWE-bench Verified (500 tasks) runs in 62 minutes on a single 32-core VM

**SWE-ReX**: Separate sandboxed code execution framework powering SWE-agent, supporting local and cloud execution with massive parallelism.

**SWE-World**: Research exploring Docker-free evaluation environments (arxiv 2602.03419).

**References**:
- [SWE-bench Docker setup](https://www.swebench.com/SWE-bench/guides/docker_setup/)
- [SWE-ReX GitHub](https://github.com/SWE-agent/SWE-ReX)
- [Epoch AI: SWE-bench in one hour](https://epoch.ai/blog/swebench-docker)

### 2.6 AutoGPT

**Isolation approach**: Docker Compose for deployment; Docker containers for Python code sandbox

**Architecture**:
- Docker Compose creates isolated containers for backend services
- Custom Python code execution uses a temporary dedicated Docker container
- Non-Docker version: shell commands execute without any sandboxing (critical vulnerability)

**Known vulnerabilities**:
- Path traversal attacks can overwrite files outside workspace directory (CVE documented)
- Container escape demonstrated by security researchers
- sandbox-exec escape in non-Docker mode (GitHub Advisory GHSA-5h38-mgp9-rj5f)

**References**:
- [Positive Security: Hacking Auto-GPT container escape](https://positive.security/blog/auto-gpt-rce)
- [AutoGPT security advisory](https://github.com/Significant-Gravitas/AutoGPT/security/advisories/GHSA-5h38-mgp9-rj5f)

### 2.7 LangChain / LangGraph

**Isolation approach**: Multiple options, evolving toward cloud sandboxes

**Three approaches offered**:
1. **Pyodide/WASM sandbox** (langchain-sandbox): Python in WebAssembly via Deno. Now deprecated; not recommended for production.
2. **Docker containers**: Agent-in-sandbox or agent-on-host-with-sandbox-API patterns
3. **Cloud sandboxes**: E2B integration for Deep Agents; recommended for production

**Two architecture patterns**:
- **Agent inside sandbox**: Docker/VM image with agent framework pre-installed; connect from outside
- **Agent on host**: Code execution delegated to sandbox via API; API keys stay outside sandbox

**References**:
- [LangChain sandboxes docs](https://docs.langchain.com/oss/python/deepagents/sandboxes)
- [LangChain sandbox blog](https://blog.langchain.com/execute-code-with-sandboxes-for-deepagents/)
- [langchain-sandbox GitHub](https://github.com/langchain-ai/langchain-sandbox)

### 2.8 CrewAI

**Isolation approach**: Docker for CodeInterpreterTool; fallback to restricted Python

**Architecture**:
- CodeInterpreterTool uses Docker for secure code execution
- If Docker unavailable, falls back to restricted Python sandbox
- Known issue: `allow_code_execution=True` inside Docker fails; workaround requires `unsafe_mode=True`

**Integration with external sandboxes**: SandboxAI, Container Use (Dagger), Amazon Bedrock AgentCore

**References**:
- [CrewAI CodeInterpreterTool docs](https://docs.crewai.com/en/tools/ai-ml/codeinterpretertool)
- [CrewAI Docker issue #3028](https://github.com/crewAIInc/crewAI/issues/3028)

### 2.9 Cursor / Windsurf

**Isolation approach**: Minimal sandboxing; significant security gaps

**Key findings**:
- Neither tool has robust sandboxing mechanisms
- Agents can access files beyond intended scope, including confidential/sensitive information
- Cursor's "YOLO mode" executes commands without user confirmation
- Environment variables and API keys can be inadvertently exposed
- Cursor: Privacy Mode prevents code retention on servers; SOC 2 only
- Windsurf: ZDR, SOC 2, HIPAA, FedRAMP/DOD, ITAR, RBAC, SCIM compliance; zero-data retention defaults

**Recommended mitigations**: Stricter sandboxing for file access, strengthened exclusion mechanisms (e.g., Cursor's planned "cursor ban" file)

**References**:
- [Geeky Gadgets security analysis](https://www.geeky-gadgets.com/cursor-windsurf-security-risks/)
- [Apiiro security analysis](https://apiiro.com/blog/securing-code-with-cursor-and-windsurf/)

### 2.10 Docker Sandboxes (Docker Inc., 2025-2026)

**Isolation approach**: MicroVM-based sandboxes with private Docker daemons

**Architecture**:
- Each sandbox runs a complete Docker daemon inside a dedicated microVM
- Hypervisor: macOS virtualization.framework, Windows Hyper-V
- File synchronization (not volume mounting) preserves absolute paths bidirectionally
- HTTP/HTTPS filtering proxy at `host.docker.internal:3128` for network control
- Credential injection: proxy intercepts API requests to major providers (OpenAI, Anthropic, Google, GitHub) and injects auth headers transparently -- credentials never enter the VM
- Sandboxes cannot communicate with each other or access host localhost
- Each sandbox has isolated Docker daemon state, image cache, installed packages

**Supported agents**: Claude Code, Codex CLI, Copilot CLI, Gemini CLI, Kiro

**Lifecycle**: `docker sandbox create` / `docker sandbox run` / `docker sandbox rm`

**Key differentiator**: Only sandboxing solution that allows agents to build and run Docker containers (Docker-in-Docker) while remaining isolated from the host.

**References**:
- [Docker Sandboxes architecture docs](https://docs.docker.com/ai/sandboxes/architecture/)
- [Docker blog: new approach for coding agent safety](https://www.docker.com/blog/docker-sandboxes-a-new-approach-for-coding-agent-safety/)
- [Docker blog: run Claude Code safely](https://www.docker.com/blog/docker-sandboxes-run-claude-code-and-other-coding-agents-unsupervised-but-safely/)

### 2.11 Container Use (Dagger)

**Isolation approach**: Container + Git worktree per agent for parallel coding

**Architecture**:
- Each agent gets its own containerized sandbox + Git worktree
- Git worktrees share repository metadata but maintain independent file states
- Each container has isolated resources and network access
- MCP-compatible: works with Claude Code, Cursor, etc.
- Focus on parallel, conflict-free multi-agent workflows

**Status**: Early development (as of 2025)

**References**:
- [Dagger blog](https://dagger.io/blog/agent-container-use)
- [Container Use GitHub](https://github.com/dagger/container-use)
- [InfoQ coverage](https://www.infoq.com/news/2025/08/container-use/)

---

## 3. Sandbox-as-a-Service Platforms

### 3.1 E2B

- **Isolation**: Firecracker microVMs
- **Startup**: ~200ms
- **Pricing**: $0.000028/CPU/s (hosted) with $100 one-time credits
- **Features**: Open-source runtime, Python/JS SDKs, filesystem API, desktop environment (E2B Desktop), Docker MCP Catalog (200+ tools)
- **Adoption**: 88% of Fortune 100 signed up; $21M Series A (Insight Partners)
- **Reference**: [e2b.dev](https://e2b.dev/), [GitHub](https://github.com/e2b-dev/E2B)

### 3.2 Modal Sandboxes

- **Isolation**: Container-based with serverless fabric
- **Startup**: Sub-second cold starts
- **Scaling**: 20,000+ concurrent units
- **Pricing**: $0.0000131/CPU/s with $30/month credits
- **Features**: Python/JS/Go SDKs, built-in tunneling, granular egress policies
- **Reference**: [Modal sandbox comparison](https://modal.com/blog/top-code-agent-sandbox-products)

### 3.3 Fly.io Sprites

- **Isolation**: Firecracker microVMs (KVM hardware-isolated)
- **Startup**: Sub-second; Machines API spins up in hundreds of milliseconds
- **Features**: Persistent VMs that auto-idle when inactive, 100GB storage, global edge regions
- **Pricing**: $0.000000529/CPU/s (cheapest per-CPU)
- **Reference**: [Fly.io Sprites announcement](https://www.sdxcentral.com/news/flyio-debuts-sprites-persistent-vms-that-let-ai-agents-keep-their-state/), [Fly.io AI](https://fly.io/ai)

### 3.4 Daytona

- **Isolation**: Docker/OCI containers with native state management
- **Startup**: 90ms (fastest claimed)
- **Pricing**: $0.000028/CPU/s
- **Features**: Built-in Git/LSP support, live stdout/stderr streaming, warm pool scaling, state pause/resume/archive
- **Pivot**: From dev environments to AI agent infrastructure (early 2025); $24M Series A (Feb 2026)
- **Reference**: [daytona.io](https://www.daytona.io/), [GitHub](https://github.com/daytonaio/daytona)

### 3.5 Together Code Sandbox

- **Isolation**: Full VM snapshots
- **Startup**: 500ms warm resume; 2.7s cold start
- **Features**: Hot-swappable VM sizes (2-64 vCPU), Git-versioned storage, live preview hosts
- **Pricing**: $0.0000248/CPU/s

### 3.6 Kubernetes Agent Sandbox (Google/Community)

- **Isolation**: gVisor (default) or Kata Containers
- **Architecture**: Kubernetes CRD + Operator providing declarative API for stateful, isolated pods
- **Features**: Stable identity, persistent storage, kernel + network isolation
- **Status**: Kubernetes SIG Apps subproject; launched at KubeCon NA 2025
- **Reference**: [Agent Sandbox docs](https://agent-sandbox.sigs.k8s.io/), [GitHub](https://github.com/kubernetes-sigs/agent-sandbox)

---

## 4. Common Patterns and Design Decisions

### 4.1 Container-per-Task vs. Persistent Containers

| Pattern | Used By | Pros | Cons |
|---|---|---|---|
| **Ephemeral (per-task)** | OpenAI Codex, SWE-bench, OpenHands V0 | Clean state, no secret accumulation, reproducible | Cold start overhead, dependency reinstallation |
| **Persistent (long-lived)** | Devin, Fly.io Sprites, Daytona | State preservation, faster iteration, no rebuild | Secret accumulation risk, drift, resource management |
| **Cached with invalidation** | OpenAI Codex (12hr cache) | Balance of speed and freshness | Cache staleness, invalidation complexity |

### 4.2 Agent-in-Sandbox vs. Agent-on-Host

| Pattern | Used By | Pros | Cons |
|---|---|---|---|
| **Agent inside sandbox** | Devin, Docker Sandboxes, Codex Cloud | Maximum isolation; agent cannot access host at all | Higher resource usage; credential management complexity |
| **Agent on host, execution in sandbox** | LangChain, CrewAI, Claude Code (native) | API keys stay outside sandbox; lighter weight | Host agent surface still exposed; network boundary needed |

### 4.3 Network Isolation Strategies

- **Full disconnection during execution**: OpenAI Codex (internet disabled during agent phase)
- **Proxy-based filtering**: Docker Sandboxes (HTTP/HTTPS proxy with allow/deny lists), Claude Code (Unix domain socket proxy)
- **Egress policies**: Modal (per-sandbox egress), Kubernetes Agent Sandbox (network isolation)
- **No network isolation**: Cursor, Windsurf (significant gap)

### 4.4 Credential Management Patterns

- **Proxy injection**: Docker Sandboxes inject credentials via proxy -- never stored in VM
- **Setup-only secrets**: OpenAI Codex provides secrets during setup, removes before agent phase
- **Credential brokers**: NVIDIA recommends short-lived tokens via brokers rather than long-lived env vars
- **Host-side only**: LangChain agent-on-host pattern keeps API keys outside sandbox

### 4.5 File System Strategies

- **Volume mounting**: OpenHands (workspace directory mounted), traditional Docker
- **File synchronization**: Docker Sandboxes (bidirectional copy, not mount -- preserves absolute paths)
- **Git worktrees**: Container Use / Dagger (independent file states sharing repo metadata)
- **OS-level restriction**: Claude Code (bubblewrap/seatbelt restrict to CWD)

---

## 5. Why Containerization/Isolation Matters for Agents

### 5.1 Security Threats

- **Indirect prompt injection**: Adversaries embed malicious instructions in repos, PRs, git histories, `.cursorrules`, MCP responses (OWASP Top 10 AI Agent threat)
- **Tool interaction manipulation**: Agent tools manipulated in unintended ways
- **Container/sandbox escape**: Demonstrated against AutoGPT; kernel vulnerabilities enable escape from standard containers
- **Configuration file poisoning**: Writes to `.cursorrules`, `CLAUDE.md`, MCP configs establish durable attacker control

### 5.2 What Isolation Solves

1. **Blast radius limitation**: Compromised agent cannot access host system, other projects, or credentials
2. **Reproducibility**: Consistent environments across runs (SWE-bench depends on this)
3. **Resource limits**: CPU, memory, disk quotas prevent runaway agents
4. **Cleanup/reset**: Ephemeral containers guarantee clean state; no secret accumulation
5. **Parallel execution**: Multiple agents work on different tasks without interference (Container Use, Devin)
6. **Auditability**: Isolated environments enable logging and forensics

### 5.3 NVIDIA's Defense-in-Depth Recommendations

1. Network egress restrictions with tightly scoped allowlists
2. Workspace isolation blocking writes outside workspace
3. Configuration file protection (block all writes; no user approval override)
4. Virtualized kernel isolation (VMs, unikernels, Kata containers)
5. Secret injection with credential brokers and short-lived tokens
6. Ephemeral sandboxes or periodic recreation (weekly for VM-based)
7. Fresh user confirmation for each dangerous action (never cache approvals)

**Reference**: [NVIDIA security guidance](https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk/)

---

## 6. Summary Comparison Table

| System | Isolation Tech | Container/VM | Network Policy | Credential Model | Open Source |
|---|---|---|---|---|---|
| **Claude Code** | bubblewrap/seatbelt | OS-level | Proxy (Unix socket) | Host-side | Partially |
| **OpenAI Codex** | Container (cloud) | Per-task container | Internet off during execution | Setup-only secrets | No |
| **Devin** | VM (cloud) | Per-instance VM | VPC-level | Customer VPC | No |
| **OpenHands** | Docker container | Per-session | Container networking | Mounted env vars | Yes (ICLR 2025) |
| **SWE-bench** | Docker container | Per-task | Standard Docker | N/A (evaluation) | Yes |
| **AutoGPT** | Docker container | Per-execution | Standard Docker | Env vars (vulnerable) | Yes |
| **LangChain** | WASM/Docker/Cloud | Configurable | Depends on backend | Agent-on-host pattern | Yes |
| **CrewAI** | Docker (fallback: restricted Python) | Per-execution | Standard Docker | Env vars | Yes |
| **Cursor/Windsurf** | Minimal | None | None | Direct access | No |
| **Docker Sandboxes** | MicroVM | Per-sandbox VM | HTTP proxy with allow/deny | Proxy injection | No |
| **E2B** | Firecracker microVM | Per-sandbox | Configurable | SDK-based | Partially |
| **Modal** | Container (serverless) | Per-sandbox | Egress policies | SDK-based | No |
| **Fly.io Sprites** | Firecracker microVM | Persistent VM | KVM isolation | Machine-level | No |
| **Daytona** | Docker/OCI container | Per-sandbox | Configurable | API-based | Yes |
| **K8s Agent Sandbox** | gVisor/Kata | Per-pod | K8s network policies | K8s secrets | Yes |
| **Container Use (Dagger)** | Docker + Git worktree | Per-agent | Container networking | MCP-based | Yes |

---

## 7. Industry Trajectory and Open Questions

### Current consensus (early 2026):
- Standard Docker containers alone are not sufficient for untrusted AI-generated code
- The industry is stratifying: **gVisor** for multi-tenant SaaS, **Firecracker microVMs** for production agent execution, **bubblewrap/seatbelt** for local developer tools
- Docker Sandboxes (microVM-based) are becoming the de facto local development standard, with support for all major coding agents
- Kubernetes Agent Sandbox is emerging as the enterprise orchestration layer

### Open questions:
1. **Performance vs. security tradeoff**: How much overhead is acceptable? gVisor's 10-30% I/O overhead vs. Firecracker's ~125ms boot time vs. bubblewrap's near-zero overhead
2. **State management**: Ephemeral vs. persistent sandboxes -- agents increasingly need state across tasks (Fly.io Sprites, Daytona)
3. **Multi-agent coordination**: How do isolated agents share context? Container Use / Dagger exploring Git worktree approach
4. **Configuration file attacks**: NVIDIA recommends blocking all writes to agent config files -- but this limits agent autonomy
5. **WASM viability**: Lightweight and secure by construction, but limited ecosystem support (LangChain deprecated their WASM approach)

---

## Sources

### Docker and Containerization
- [Docker Sandboxes Architecture](https://docs.docker.com/ai/sandboxes/architecture/)
- [Docker: New Approach for Coding Agent Safety](https://www.docker.com/blog/docker-sandboxes-a-new-approach-for-coding-agent-safety/)
- [Docker: Run Claude Code Safely](https://www.docker.com/blog/docker-sandboxes-run-claude-code-and-other-coding-agents-unsupervised-but-safely/)
- [Docker + E2B Partnership](https://www.docker.com/blog/docker-e2b-building-the-future-of-trusted-ai/)

### Anthropic / Claude Code
- [Anthropic Engineering: Claude Code Sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing)
- [Claude Code Sandboxing Docs](https://code.claude.com/docs/en/sandboxing)
- [Infralovers: Sandboxing Claude Code on macOS](https://www.infralovers.com/blog/2026-02-15-sandboxing-claude-code-macos/)

### OpenAI Codex
- [Codex Cloud Environments](https://developers.openai.com/codex/cloud/environments/)
- [Codex Security](https://developers.openai.com/codex/security/)
- [Codex Docker Sandbox](https://docs.docker.com/ai/sandboxes/agents/codex/)

### Devin / Cognition Labs
- [Introducing Devin](https://cognition.ai/blog/introducing-devin)
- [Devin 2.0 Technical Design](https://medium.com/@takafumi.endo/agent-native-development-a-deep-dive-into-devin-2-0s-technical-design-3451587d23c0)

### OpenHands
- [OpenHands ICLR 2025 Paper](https://openreview.net/pdf/95990590797cff8b93c33af989ecf4ac58bde9bb.pdf)
- [OpenHands SDK Paper](https://arxiv.org/html/2511.03690v1)
- [OpenHands Custom Sandbox Guide](https://docs.openhands.dev/openhands/usage/advanced/custom-sandbox-guide)

### SWE-agent / SWE-bench
- [SWE-bench Docker Setup](https://www.swebench.com/SWE-bench/guides/docker_setup/)
- [SWE-ReX GitHub](https://github.com/SWE-agent/SWE-ReX)
- [Epoch AI: SWE-bench in One Hour](https://epoch.ai/blog/swebench-docker)
- [SWE-World: Docker-Free Environments](https://arxiv.org/html/2602.03419v1)

### AutoGPT
- [Positive Security: Container Escape](https://positive.security/blog/auto-gpt-rce)
- [AutoGPT Security Advisory](https://github.com/Significant-Gravitas/AutoGPT/security/advisories/GHSA-5h38-mgp9-rj5f)

### LangChain / LangGraph
- [LangChain Sandboxes Docs](https://docs.langchain.com/oss/python/deepagents/sandboxes)
- [LangChain Sandbox Blog](https://blog.langchain.com/execute-code-with-sandboxes-for-deepagents/)
- [langchain-sandbox GitHub](https://github.com/langchain-ai/langchain-sandbox)

### CrewAI
- [CrewAI CodeInterpreterTool](https://docs.crewai.com/en/tools/ai-ml/codeinterpretertool)

### Cursor / Windsurf
- [Geeky Gadgets Security Analysis](https://www.geeky-gadgets.com/cursor-windsurf-security-risks/)
- [Apiiro Security Analysis](https://apiiro.com/blog/securing-code-with-cursor-and-windsurf/)

### Sandbox Platforms
- [E2B](https://e2b.dev/)
- [Modal Sandbox Comparison](https://modal.com/blog/top-code-agent-sandbox-products)
- [Fly.io Sprites](https://www.sdxcentral.com/news/flyio-debuts-sprites-persistent-vms-that-let-ai-agents-keep-their-state/)
- [Daytona](https://www.daytona.io/)
- [Kubernetes Agent Sandbox](https://agent-sandbox.sigs.k8s.io/)
- [Container Use / Dagger](https://github.com/dagger/container-use)

### Security Guidance
- [NVIDIA: Practical Security Guidance for Agentic Workflows](https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk/)
- [Northflank: How to Sandbox AI Agents](https://northflank.com/blog/how-to-sandbox-ai-agents)
- [Northflank: Best Code Execution Sandbox](https://northflank.com/blog/best-code-execution-sandbox-for-ai-agents)

### WebAssembly
- [NVIDIA: Sandboxing with WebAssembly](https://developer.nvidia.com/blog/sandboxing-agentic-ai-workflows-with-webassembly/)
- [Mozilla wasm-agents](https://github.com/mozilla-ai/wasm-agents-blueprint)

### Kubernetes / Enterprise
- [Google: Agentic AI on Kubernetes](https://cloud.google.com/blog/products/containers-kubernetes/agentic-ai-on-kubernetes-and-gke)
- [Google OSS Blog: Agent Execution Standard](https://opensource.googleblog.com/2025/11/unleashing-autonomous-ai-agents-why-kubernetes-needs-a-new-standard-for-agent-execution.html)
- [Kata + Agent Sandbox Integration](https://katacontainers.io/blog/kata-containers-agent-sandbox-integration/)
- [InfoQ: Agent Sandbox on Kubernetes](https://www.infoq.com/news/2025/12/agent-sandbox-kubernetes/)

### Comparison / Overview
- [AI Sandbox Comparison 2026: E2B vs Lifo vs Daytona](https://lifo.sh/blog/ai-sandbox-comparison-2026)
- [Koyeb: Top Sandbox Platforms 2026](https://www.koyeb.com/blog/top-sandbox-code-execution-platforms-for-ai-code-execution-2026)
- [Better Stack: 11 Best Sandbox Runners 2026](https://betterstack.com/community/comparisons/best-sandbox-runners/)
- [awesome-sandbox GitHub](https://github.com/restyler/awesome-sandbox)
