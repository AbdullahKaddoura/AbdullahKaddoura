# Abdullah Kaddoura

<p>
  <a href="https://www.linkedin.com/in/abdullah-kaddoura-499a48222/"><img src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
  <a href="mailto:abdullahkaddoura2@gmail.com"><img src="https://img.shields.io/badge/Email-Contact-EA4335?style=flat-square&logo=gmail&logoColor=white" alt="Email" /></a>
  <img src="https://img.shields.io/badge/Dubai-UAE-1C1C1C?style=flat-square" alt="Dubai, UAE" />
</p>

---

Computer engineer and solo founder in Dubai. I architect AI systems end to end — LLM
orchestration, wearable health data pipelines, and the backends that hold them up.

---

## Featured Projects

| Demo | Repository | What It Does |
| :---: | :--- | :--- |
| <a href="https://github.com/AbdullahKaddoura/Bizzy-Frontend"><img src="assets/bizzy_demo.jpg" width="180" alt="Bizzy" /></a> | **[Bizzy](https://github.com/AbdullahKaddoura/Bizzy-Frontend)** · [backend](https://github.com/AbdullahKaddoura/Bizzy-Backend) | AI business co-pilot. Takes a founder from a raw idea to a costed roadmap by routing the conversation through five reasoning engines. |

<!-- SLOT: Evrls — add once healthBuild is scrubbed and made public -->
<!-- SLOT: new open-source utility #1 -->
<!-- SLOT: new open-source utility #2 -->

---

## How Bizzy Works

A phase-driven orchestrator keeps a single `Compass` state object per session and routes
each turn to the engine that phase calls for:

```
                    ┌──────────────┐
   user turn ──────▶│ Orchestrator │◀────── conversation history
                    └──────┬───────┘
                           │  reads / updates
                    ┌──────▼───────┐
                    │   Compass    │  session state + phase
                    └──────┬───────┘
                           │  dispatches to
   ┌──────────┬────────────┼────────────┬──────────┐
   ▼          ▼            ▼            ▼          ▼
research  feasibility  framework    solution   roadmap
                           │
                    ┌──────▼───────┐
                    │ OutputEngine │──▶ structured roadmap
                    └──────────────┘
```

**Stack:** FastAPI · OpenAI · Supabase (Postgres + auth) · React · Vite · TypeScript · Tailwind

---

## Tech Stack

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black" alt="React" />
  <img src="https://img.shields.io/badge/Vite-646CFF?style=flat-square&logo=vite&logoColor=white" alt="Vite" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white" alt="Tailwind CSS" />
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/Supabase-3FCF8E?style=flat-square&logo=supabase&logoColor=white" alt="Supabase" />
  <img src="https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white" alt="OpenAI" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker" />
</p>

---

If you are working on AI agents, wearable health data, or business automation, feel free to
[connect on LinkedIn](https://www.linkedin.com/in/abdullah-kaddoura-499a48222/) or email me at
[abdullahkaddoura2@gmail.com](mailto:abdullahkaddoura2@gmail.com).
