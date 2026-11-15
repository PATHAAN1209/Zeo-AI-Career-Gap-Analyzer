import json
import re

def slugify(text: str) -> str:
    s = text.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')

ROLES_BY_CATEGORY = {
    "Software Development & Engineering": [
        ("Frontend Web Developer", "Builds responsive, interactive user interfaces with modern web technologies.", [
            ("HTML5 & Semantic Markup", "critical", ["html", "html5", "semantic web"]),
            ("CSS3, Flexbox & Grid", "critical", ["css", "css3", "flexbox", "css grid", "tailwind", "responsive design"]),
            ("JavaScript (ES6+)", "critical", ["javascript", "js", "ecmascript", "es6"]),
            ("React.js Framework", "critical", ["react", "react.js", "reactjs", "next.js"]),
            ("State Management", "high", ["redux", "zustand", "context api", "recoil", "vuex"]),
            ("REST & GraphQL APIs", "high", ["rest api", "graphql", "axios", "fetch api"]),
            ("Git & Version Control", "high", ["git", "github", "gitlab", "version control"]),
            ("Web Performance & SEO", "medium", ["lighthouse", "web vitals", "performance optimization", "lazy loading"])
        ], ["TypeScript", "Next.js", "Jest & React Testing Library", "CI/CD"]),

        ("Backend Developer", "Develops robust server-side systems, databases, and microservice architectures.", [
            ("Server-side Language (Python/Node/Go/Java)", "critical", ["python", "node.js", "golang", "java", "c#", "backend"]),
            ("RESTful API & GraphQL Design", "critical", ["rest api", "fastapi", "express", "django", "spring boot", "graphql"]),
            ("SQL & Relational Databases", "critical", ["sql", "postgresql", "mysql", "database design", "relational database"]),
            ("NoSQL & Caching (Redis/MongoDB)", "high", ["redis", "mongodb", "caching", "nosql"]),
            ("Authentication & Security", "high", ["jwt", "oauth", "auth0", "cors", "rbac", "encryption"]),
            ("Docker & Containerization", "high", ["docker", "containerization", "docker-compose"]),
            ("Git & Automated Testing", "high", ["git", "pytest", "unit tests", "integration tests"])
        ], ["Kubernetes", "Microservices", "Kafka", "Cloud Computing"]),

        ("Full-Stack Developer", "Engineers complete web solutions spanning frontend, backend, databases, and cloud.", [
            ("Frontend Engineering (React/Vue)", "critical", ["react", "vue", "javascript", "typescript", "frontend"]),
            ("Backend Frameworks (Node/Python)", "critical", ["node.js", "express", "fastapi", "django", "backend"]),
            ("Database Architecture (SQL & NoSQL)", "critical", ["postgresql", "mongodb", "sql", "prisma", "orm"]),
            ("RESTful & GraphQL APIs", "critical", ["rest api", "api integration", "graphql", "endpoints"]),
            ("Cloud Deployment & DevOps", "high", ["docker", "aws", "vercel", "ci/cd", "deployment"]),
            ("Authentication & Security", "high", ["oauth", "jwt", "session management", "security"])
        ], ["Microservices", "System Architecture", "Performance Tuning"]),

        ("Mobile App Developer (iOS/Swift)", "Develops native high-performance applications for Apple iOS ecosystem.", [
            ("Swift Programming", "critical", ["swift", "swiftui", "uikit", "ios development"]),
            ("SwiftUI & UIKit Architecture", "critical", ["swiftui", "uikit", "autolayout", "viewcontroller"]),
            ("iOS Design Patterns & Architecture (MVVM)", "high", ["mvvm", "mvc", "combine", "clean architecture"]),
            ("Core Data & Local Storage", "high", ["core data", "realm", "sqlite", "userdefaults"]),
            ("App Store Deployment & TestFlight", "high", ["app store", "testflight", "xcode", "certificates"]),
            ("REST APIs & Network Handling", "high", ["urlsession", "alamofire", "codable", "rest api"])
        ], ["Combine Framework", "Objective-C", "Metal", "ARKit"]),

        ("Mobile App Developer (Android/Kotlin)", "Builds native modern Android applications using Kotlin and Jetpack.", [
            ("Kotlin Programming", "critical", ["kotlin", "android studio", "android development"]),
            ("Jetpack Compose & UI Architecture", "critical", ["jetpack compose", "xml layouts", "material design"]),
            ("Android Architecture Components (MVVM)", "high", ["mvvm", "viewmodel", "livedata", "coroutines", "flow"]),
            ("Room Database & SQLite", "high", ["room", "sqlite", "datastore", "local storage"]),
            ("REST API & Retrofit", "high", ["retrofit", "okhttp", "rest api", "json parsing"]),
            ("Google Play Console & Deployment", "high", ["google play", "apk", "aab", "play console"])
        ], ["Ktor", "Hilt/Dagger DI", "WorkManager", "NDK"]),

        ("Cross-Platform App Developer (Flutter/React Native)", "Builds universal mobile apps for iOS and Android from a single codebase.", [
            ("Flutter/Dart or React Native", "critical", ["flutter", "dart", "react native", "expo"]),
            ("Cross-Platform UI & Animations", "critical", ["widgets", "native components", "styling", "animations"]),
            ("State Management (Riverpod/Bloc/Redux)", "high", ["riverpod", "bloc", "provider", "redux"]),
            ("Native Device API Integration", "high", ["camera", "gps", "push notifications", "bluetooth"]),
            ("App Store & Play Store Deployment", "high", ["deployment", "testflight", "play store", "build pipelines"])
        ], ["Native Bridges", "CodePush", "Offline Sync"]),

        ("Game Developer (Unity/Unreal Engine)", "Creates immersive 2D/3D games and simulation engines.", [
            ("C# or C++ for Games", "critical", ["c#", "c++", "scripting", "game programming"]),
            ("Unity or Unreal Engine", "critical", ["unity", "unreal engine", "game engine", "blueprints"]),
            ("3D Math, Physics & Collision Systems", "high", ["linear algebra", "physics engine", "raycasting", "quaternions"]),
            ("Game State & Gameplay Mechanics", "high", ["gameplay", "ai logic", "state machines", "inventory"]),
            ("Shaders, Lighting & Optimization", "high", ["shaders", "hlsl", "particle systems", "profiling"])
        ], ["Multiplayer Networking", "VR/AR Gaming", "Blender Pipeline"]),

        ("Embedded Systems Programmer", "Programs microcontrollers, firmware, and resource-constrained hardware devices.", [
            ("Embedded C & C++", "critical", ["embedded c", "c++", "low level programming", "microcontroller"]),
            ("Hardware Protocols (I2C, SPI, UART, CAN)", "critical", ["i2c", "spi", "uart", "can bus", "gpio"]),
            ("RTOS & Bare-Metal Programming", "high", ["freertos", "rtos", "interrupts", "timers", "bare metal"]),
            ("Microcontrollers (ARM, STM32, ESP32, AVR)", "high", ["stm32", "esp32", "arduino", "arm cortex"]),
            ("Oscilloscopes & Hardware Debugging", "high", ["oscilloscope", "logic analyzer", "jtag", "schematics"])
        ], ["PCB Design", "IoT Protocols (MQTT)", "Device Drivers"]),

        ("API Integration Specialist", "Architects, connects, and automates high-volume third-party API ecosystems.", [
            ("REST, GraphQL & Webhook Standards", "critical", ["rest api", "graphql", "webhooks", "api integration"]),
            ("API Authentication (OAuth 2.0, API Keys, mTLS)", "critical", ["oauth", "oauth2", "api keys", "jwt", "mtls"]),
            ("Postman & API Documentation", "high", ["postman", "openapi", "swagger", "api testing"]),
            ("Middleware & ETL Automation", "high", ["middleware", "zapier", "make", "n8n", "node.js", "python"]),
            ("Rate Limiting, Retries & Error Handling", "high", ["rate limiting", "backoff", "circuit breaker", "logging"])
        ], ["Kafka", "API Gateway", "Kong", "MuleSoft"]),

        ("WordPress / CMS Developer", "Develops custom themes, plugins, and scalable headless CMS architectures.", [
            ("PHP & WordPress Core", "critical", ["php", "wordpress", "theme development", "plugin development"]),
            ("HTML5, CSS3, Modern JavaScript", "critical", ["html", "css", "javascript", "jquery", "gutenberg"]),
            ("MySQL & Database Queries (WPDB)", "high", ["mysql", "wpdb", "database optimization"]),
            ("WooCommerce & E-Commerce Integration", "high", ["woocommerce", "payment gateways", "checkout customization"]),
            ("CMS Security & Speed Optimization", "high", ["caching", "cdn", "security hardening", "seo"])
        ], ["Headless WordPress", "GraphQL", "ACF Pro"]),

        ("Shopify / E-Commerce Developer", "Builds custom storefronts, Liquid themes, and Shopify app extensions.", [
            ("Liquid Template Language", "critical", ["liquid", "shopify liquid", "theme development"]),
            ("Shopify Storefront & Admin APIs", "critical", ["shopify api", "graphql", "storefront api"]),
            ("HTML5, CSS3 & JavaScript for Commerce", "high", ["css", "javascript", "ajax cart", "tailwind"]),
            ("Payment Gateways & App Integrations", "high", ["checkout extensibility", "klarna", "stripe", "apps"]),
            ("Store Speed & Conversion Optimization", "high", ["page speed", "cro", "core web vitals"])
        ], ["Hydrogen & Oxygen", "Shopify Apps (Node/Remix)"]),

        ("Webflow / No-Code Developer", "Designs and builds modern responsive visual websites and interactions.", [
            ("Webflow Visual CMS & Designer", "critical", ["webflow", "cms", "visual development"]),
            ("CSS Layouts, Flexbox & Grid Mastery", "critical", ["css", "flexbox", "grid", "responsive layout"]),
            ("Client-First Style System & BEM", "high", ["client-first", "relume", "bem", "design systems"]),
            ("Custom Code (HTML/CSS/JS) Injection", "high", ["javascript", "custom code", "api webhooks"]),
            ("Webflow Interactions & GSAP Animations", "high", ["interactions", "animations", "gsap", "scroll animations"])
        ], ["Wized", "Xano", "Finsweet Attributes"]),

        ("DevOps Engineer", "Automates software delivery pipelines, cloud infrastructure, and deployment security.", [
            ("CI/CD Automation (GitHub Actions/GitLab)", "critical", ["ci/cd", "github actions", "gitlab ci", "jenkins"]),
            ("Docker & Containerization", "critical", ["docker", "containers", "dockerfile"]),
            ("Infrastructure as Code (Terraform)", "critical", ["terraform", "iac", "cloudformation"]),
            ("Linux Systems Administration & Bash", "high", ["linux", "bash", "shell scripting", "networking"]),
            ("Cloud Platforms (AWS/GCP/Azure)", "high", ["aws", "gcp", "azure", "cloud computing"]),
            ("Monitoring & Observability (Prometheus/Grafana)", "high", ["prometheus", "grafana", "datadog", "elk"])
        ], ["Kubernetes", "Ansible", "ArgoCD", "Helm"]),

        ("Site Reliability Engineer (SRE)", "Ensures high availability, fault tolerance, and automated incident response.", [
            ("SLO, SLA & Error Budget Management", "critical", ["slo", "sla", "error budget", "reliability"]),
            ("Incident Management & Post-Mortems", "critical", ["incident response", "post-mortem", "on-call", "root cause"]),
            ("Distributed Systems Architecture", "high", ["microservices", "distributed systems", "high availability"]),
            ("Automated Monitoring & Telemetry", "high", ["datadog", "prometheus", "opentelemetry", "pagerduty"]),
            ("Scripting & Automation (Go/Python)", "high", ["python", "go", "bash", "automation"])
        ], ["Chaos Engineering", "Kubernetes", "Load Testing"]),

        ("Cloud Solutions Architect (AWS/Azure/GCP)", "Designs secure, scalable, cost-effective enterprise cloud architectures.", [
            ("Enterprise Cloud Services (AWS/Azure/GCP)", "critical", ["aws", "azure", "gcp", "cloud architecture"]),
            ("High Availability & Disaster Recovery Design", "critical", ["disaster recovery", "load balancing", "multi-region"]),
            ("Cloud Security & IAM Governance", "high", ["iam", "vpc", "security groups", "compliance"]),
            ("Cost Optimization & FinOps", "high", ["finops", "cost optimization", "reserved instances"]),
            ("Serverless & Microservices Patterns", "high", ["serverless", "lambda", "ecs", "api gateway"])
        ], ["Terraform", "Well-Architected Framework", "Kubernetes"]),

        ("Blockchain / Smart Contract Developer", "Engineers decentralized apps (dApps), smart contracts, and cryptographic protocols.", [
            ("Solidity or Rust (Solana)", "critical", ["solidity", "rust", "smart contracts", "evm"]),
            ("Web3 Libraries (Ethers.js / Web3.js)", "critical", ["ethers.js", "web3.js", "wagmi", "viem"]),
            ("Smart Contract Security & Auditing", "high", ["reentrancy", "formal verification", "slither", "security audit"]),
            ("Development Tools (Hardhat / Foundry)", "high", ["hardhat", "foundry", "truffle"]),
            ("Token Standards (ERC-20, ERC-721)", "high", ["erc-20", "erc-721", "erc-1155", "nft"])
        ], ["DeFi Protocols", "Zero Knowledge Proofs", "Layer 2 Solutions"]),

        ("QA Automation Engineer", "Builds automated test suites and end-to-end testing frameworks.", [
            ("Test Automation Frameworks (Playwright/Cypress/Selenium)", "critical", ["playwright", "cypress", "selenium", "test automation"]),
            ("Programming (JavaScript/TypeScript or Python)", "critical", ["javascript", "typescript", "python", "automation scripting"]),
            ("API Testing (Postman / REST-assured)", "high", ["api testing", "postman", "rest-assured", "supertest"]),
            ("CI/CD Pipeline Test Integration", "high", ["ci/cd", "github actions", "test reporting"]),
            ("Test Planning, Edge Cases & Bug Reporting", "high", ["test cases", "jira", "bug tracking", "test strategies"])
        ], ["Performance Testing (JMeter)", "Appium Mobile", "Contract Testing"]),

        ("Manual Software Tester", "Conducts meticulous manual functional, exploratory, and regression testing.", [
            ("Functional & Regression Testing", "critical", ["functional testing", "regression testing", "sanity testing"]),
            ("Test Case Design & Documentation", "critical", ["test cases", "test scenarios", "test documentation"]),
            ("Defect Tracking & Bug Life Cycle (Jira)", "high", ["jira", "bug reporting", "defect tracking"]),
            ("Cross-Browser & Cross-Device Testing", "high", ["cross-browser", "mobile testing", "browserstack"]),
            ("API Testing Basics (Postman)", "high", ["postman", "api verification", "http status codes"])
        ], ["Exploratory Testing", "Usability Testing", "SQL for Testers"]),

        ("Database Administrator (DBA)", "Manages database performance, integrity, replication, backups, and security.", [
            ("Relational DB Engines (PostgreSQL / MySQL / Oracle)", "critical", ["postgresql", "mysql", "oracle", "sql server"]),
            ("Query Optimization & Indexing Tuning", "critical", ["indexing", "explain plan", "query optimization", "performance tuning"]),
            ("Backup, Recovery & High Availability", "high", ["backup", "point-in-time recovery", "replication", "failover"]),
            ("Database Security & Access Permissions", "high", ["security", "roles", "privileges", "encryption"]),
            ("Capacity Planning & Monitoring", "high", ["storage planning", "monitoring", "connection pooling"])
        ], ["Sharding", "NoSQL Operations", "Cloud Managed DBs (RDS)"]),

        ("Firmware Developer", "Writes low-level code that operates directly on electronic hardware and processors.", [
            ("C and Assembly Language", "critical", ["c", "assembly", "low level programming"]),
            ("Microprocessor Architectures (ARM, RISC-V)", "critical", ["arm", "risc-v", "registers", "bootloaders"]),
            ("Board Support Packages & Drivers", "high", ["bsp", "device drivers", "hal"]),
            ("Hardware Debugging (JTAG / SWD / Oscilloscope)", "high", ["jtag", "swd", "in-circuit emulation"]),
            ("Memory Management & Power Optimization", "high", ["dma", "low power modes", "memory constraints"])
        ], ["RTOS", "Bluetooth Low Energy", "Automotive standards"]),

        ("AR/VR Developer", "Creates immersive spatial computing experiences for headsets and mobile devices.", [
            ("Unity or Unreal Engine for XR", "critical", ["unity", "unreal engine", "xr", "vr", "ar"]),
            ("C# or C++ Programming", "critical", ["c#", "c++", "object oriented"]),
            ("OpenXR & XR Interaction Toolkit", "high", ["openxr", "quest sdk", "apple visionos", "interaction"]),
            ("Spatial Audio & 3D Physics", "high", ["spatial audio", "3d math", "physics simulation"]),
            ("Performance Profiling for Frame Rates", "high", ["gpu profiling", "draw calls", "occlusion culling"])
        ], ["Apple Vision Pro", "WebXR", "3D Shader Writing"]),

        ("Desktop Application Developer", "Builds standalone desktop software for Windows, macOS, and Linux.", [
            ("Frameworks (Electron / Tauri / Qt / .NET)", "critical", ["electron", "tauri", "qt", ".net", "wpf"]),
            ("C++, C#, or TypeScript/JavaScript", "critical", ["c++", "c#", "typescript", "native desktop"]),
            ("Local File System & IPC Architecture", "high", ["ipc", "file system", "native api", "threading"]),
            ("Packaging & Installers (MSI, DMG, Flatpak)", "high", ["installers", "code signing", "auto update"]),
            ("Native OS Performance Tuning", "high", ["memory management", "gpu acceleration", "profiling"])
        ], ["Cross-Platform Compiling", "Rust / Tauri", "Accessibility"]),

        ("Web Scraper / Data Extraction Specialist", "Builds resilient crawlers and automated data extraction pipelines.", [
            ("Python Scraping (Scrapy, Beautiful Soup)", "critical", ["python", "scrapy", "beautifulsoup", "data extraction"]),
            ("Headless Browsers (Playwright / Puppeteer)", "critical", ["playwright", "puppeteer", "selenium"]),
            ("Anti-Bot & CAPTCHA Bypass Architecture", "high", ["proxy rotation", "user-agents", "rate limiting"]),
            ("Data Cleaning & Pipeline Formatting", "high", ["pandas", "json", "csv", "data validation"]),
            ("SQL/NoSQL Storage of Raw Payloads", "high", ["mongodb", "postgresql", "s3 storage"])
        ], ["Distributed Crawling", "Tor / Proxy Pools", "API reverse engineering"]),

        ("Low-Code Platform Developer (Bubble/PowerApps)", "Delivers production applications quickly using visual low-code ecosystems.", [
            ("Bubble.io or Microsoft Power Apps", "critical", ["bubble", "bubble.io", "power apps", "low-code"]),
            ("Database Schema Design & Relationships", "critical", ["database design", "relational data", "data tables"]),
            ("API Connectors & Webhooks", "high", ["api connector", "rest api", "webhooks"]),
            ("Workflow Logic & Conditional States", "high", ["workflows", "conditions", "logic branching"]),
            ("User Security & Role-Based Access", "high", ["privacy rules", "roles", "security"])
        ], ["Custom Plugins", "Power Automate", "Payment integrations"]),

        ("Open-Source Maintainer / Contributor", "Champions open-source software libraries, community triage, and codebase governance.", [
            ("Git, GitHub Workflows & Forking", "critical", ["git", "github", "pull requests", "forking", "code review"]),
            ("Code Quality & Testing Standards", "critical", ["unit tests", "linting", "clean code", "formatting"]),
            ("Documentation & Issue Triage", "high", ["markdown", "technical writing", "issue triage", "changelogs"]),
            ("Open Source Licensing & Governance", "high", ["mit license", "apache", "contributor guidelines"]),
            ("CI Automation & Release Packaging", "high", ["github actions", "semantic release", "npm/pypi publishing"])
        ], ["Community Management", "Security Advisories", "Benchmarking"]),

        ("Browser Extension Developer", "Builds powerful browser plugins that enhance user workflows across Chrome and Firefox.", [
            ("Manifest V3 Architecture", "critical", ["manifest v3", "chrome extensions", "service workers"]),
            ("JavaScript / TypeScript & DOM Manipulation", "critical", ["javascript", "typescript", "dom manipulation", "content scripts"]),
            ("Background Service Workers & Messaging", "high", ["service worker", "runtime messaging", "storage api"]),
            ("Cross-Browser Compatibility (Firefox / Safari)", "high", ["cross-browser", "webextensions", "firefox"]),
            ("Chrome Web Store Submission & Security", "high", ["web store", "permissions", "content security policy"])
        ], ["React in Extensions", "OAuth Integration", "WebAssembly"]),

        ("Accessibility (a11y) Web Specialist", "Audits and architects websites for compliance with WCAG, screen readers, and disability standards.", [
            ("WCAG 2.1 / 2.2 Guidelines", "critical", ["wcag", "accessibility", "a11y", "section 508"]),
            ("ARIA Roles & Semantic HTML", "critical", ["aria", "semantic html", "aria-live", "screen readers"]),
            ("Screen Reader Testing (NVDA, JAWS, VoiceOver)", "high", ["nvda", "jaws", "voiceover", "assistive technology"]),
            ("Keyboard Navigation & Focus Management", "high", ["keyboard navigation", "focus trapping", "tabindex"]),
            ("Automated Auditing (Axe-core, Lighthouse)", "high", ["axe", "lighthouse", "accessibility audit"])
        ], ["Color Contrast Analysis", "VPAT Authoring", "Inclusive Design"]),

        ("Performance Optimization Engineer", "Accelerates load times, algorithmic execution, and asset delivery pipelines.", [
            ("Chrome DevTools & CPU/Memory Profiling", "critical", ["devtools", "profiling", "memory leaks", "flamegraphs"]),
            ("Core Web Vitals Optimization (LCP, INP, CLS)", "critical", ["core web vitals", "lcp", "inp", "cls", "lighthouse"]),
            ("Bundle Splitting & Tree Shaking", "high", ["webpack", "vite", "tree shaking", "code splitting"]),
            ("Caching Strategies & CDN Architecture", "high", ["caching", "service workers", "cdn", "http/3"]),
            ("Image & Media Optimization Formats", "high", ["webp", "avif", "lazy loading", "compression"])
        ], ["Web Workers", "WebAssembly", "Database Query Optimization"]),

        ("Legacy Code Migration Specialist", "Refactors, updates, and modernizes deprecated codebases and monolithic frameworks.", [
            ("Code Analysis & Monolith Architecture", "critical", ["code analysis", "refactoring", "monolith", "legacy code"]),
            ("Incremental Migration Strategies (Strangler Fig)", "critical", ["strangler fig", "incremental migration", "backward compatibility"]),
            ("Automated Regression Testing & Coverage", "high", ["regression testing", "integration testing", "test coverage"]),
            ("API Decoupling & Microservices", "high", ["api gateway", "microservices", "event-driven"]),
            ("Language Upgrades (Python 2 to 3, JS to TS)", "high", ["typescript migration", "framework upgrades", "ci/cd"])
        ], ["Containerization", "Database Schema Evolution", "Documentation"]),

        ("Technical Support Engineer", "Diagnoses complex software issues, reads stack traces, and resolves technical customer tickets.", [
            ("Technical Troubleshooting & Root Cause Analysis", "critical", ["troubleshooting", "root cause", "debugging", "incident resolution"]),
            ("API & Log Analysis (Splunk, Datadog, Postman)", "critical", ["log analysis", "postman", "http status codes", "splunk"]),
            ("SQL Queries for Data Verification", "high", ["sql", "queries", "data validation"]),
            ("Ticketing Systems & Customer Communication (Zendesk)", "high", ["zendesk", "jira", "customer support", "ticket escalation"]),
            ("Knowledge Base & Technical Documentation", "high", ["technical writing", "kb articles", "sop"])
        ], ["Basic Scripting (Python/Bash)", "SLA Management", "Cloud Console Basics"])
    ],

    "Artificial Intelligence & Data": [
        ("Prompt Engineer", "Crafts, evaluates, and optimizes generative AI prompts, system instructions, and few-shot patterns.", [
            ("System Instructions & Prompt Architecture", "critical", ["prompt engineering", "few-shot", "cot", "chain of thought"]),
            ("LLM Evaluation & Benchmarking", "critical", ["evals", "ragas", "prompt evaluation", "benchmarking"]),
            ("RAG (Retrieval-Augmented Generation)", "high", ["rag", "vector search", "embeddings", "retrieval"]),
            ("Context Window Optimization & Tokenomics", "high", ["token limit", "cost optimization", "chunking"]),
            ("Guardrails & Anti-Jailbreak Hardening", "high", ["guardrails", "moderation", "jailbreak defense", "prompt injection"])
        ], ["LangChain", "LlamaIndex", "Semantic Router", "DSPy"]),

        ("AI Workflow Automation Specialist", "Designs end-to-end autonomous agent loops, tool-calling pipelines, and business workflows.", [
            ("Autonomous Agents & Tool Calling", "critical", ["ai agents", "tool calling", "function calling", "crewai", "autogen"]),
            ("Automation Platforms (Make / n8n / LangGraph)", "critical", ["n8n", "make.com", "langgraph", "zapier"]),
            ("API Integration & Webhooks", "high", ["rest api", "webhooks", "json parsing"]),
            ("Data Transformation & Logic Branching", "high", ["python", "javascript", "data pipeline"]),
            ("Error Handling & Execution Monitoring", "high", ["monitoring", "retry policies", "logging"])
        ], ["Vector Databases", "Local LLMs (Ollama)", "Enterprise Security"]),

        ("Machine Learning Operations (MLOps) Technician", "Deploys, monitors, tracks, and maintains production machine learning models.", [
            ("Model Tracking (MLflow / W&B)", "critical", ["mlflow", "wandb", "experiment tracking", "model registry"]),
            ("Model Serving & Containerization (Docker, FastAPI)", "critical", ["docker", "fastapi", "triton", "model serving"]),
            ("CI/CD for ML (CML, GitHub Actions)", "high", ["cml", "github actions", "ml pipelines"]),
            ("Data & Model Drift Detection (Evidently AI)", "high", ["drift detection", "evidently", "data drift", "monitoring"]),
            ("Cloud ML Infrastructure (AWS SageMaker / Vertex AI)", "high", ["sagemaker", "vertex ai", "cloud ml"])
        ], ["Kubeflow", "Feature Stores (Feast)", "ONNX Optimization"]),

        ("Data Analyst", "Extracts business insights from tabular data using SQL, statistical metrics, and visualization tools.", [
            ("SQL Querying & Aggregations", "critical", ["sql", "joins", "cte", "window functions", "aggregations"]),
            ("Excel Advanced Analysis (Pivot, Formulas)", "critical", ["excel", "pivot tables", "vlookup", "xlookup", "power query"]),
            ("BI Dashboards (Power BI or Tableau)", "high", ["power bi", "tableau", "dashboards", "data reporting"]),
            ("Data Cleaning & Python/R Basics", "high", ["pandas", "python", "data cleaning", "exploratory data analysis"]),
            ("Business Storytelling & KPIs", "high", ["kpis", "data presentation", "stakeholder communication"])
        ], ["Statistics", "A/B Testing", "Google Analytics 4"]),

        ("Business Intelligence (BI) Developer (PowerBI/Tableau)", "Architects scalable semantic data models, enterprise reporting, and executive dashboards.", [
            ("Power BI (DAX / Power Query) or Tableau", "critical", ["power bi", "tableau", "dax", "power query", "calculated fields"]),
            ("Data Modeling (Star & Snowflake Schema)", "critical", ["data modeling", "star schema", "dimensional modeling"]),
            ("Advanced SQL for BI", "high", ["sql", "stored procedures", "views", "performance tuning"]),
            ("Automated Refresh & Gateway Management", "high", ["data gateways", "scheduled refresh", "workspace management"]),
            ("Data Storytelling & UX for Dashboards", "high", ["dashboard design", "ui/ux", "user adoption"])
        ], ["SSAS", "Fabric", "Alteryx"]),

        ("Data Engineer (ETL Pipelines)", "Constructs robust, high-volume data warehouses, streaming pipelines, and ETL jobs.", [
            ("Python & SQL for Data Engineering", "critical", ["python", "sql", "data pipelines", "etl"]),
            ("Orchestration (Apache Airflow / Prefect)", "critical", ["airflow", "prefect", "dag", "orchestration"]),
            ("Cloud Data Warehouses (Snowflake/BigQuery/Redshift)", "high", ["snowflake", "bigquery", "redshift", "data warehouse"]),
            ("Distributed Data Processing (Spark / PySpark)", "high", ["spark", "pyspark", "distributed computing"]),
            ("Data Transformation Frameworks (dbt)", "high", ["dbt", "data modeling", "lineage"])
        ], ["Kafka", "Delta Lake", "Iceberg", "Docker"]),

        ("AI Model Trainer / RLHF Specialist", "Guides model alignment, human feedback reinforcement learning, and fine-tuning datasets.", [
            ("RLHF & DPO Principles", "critical", ["rlhf", "dpo", "reinforcement learning", "model alignment"]),
            ("Dataset Curation & Quality Filtering", "critical", ["data curation", "filtering", "synthetic data", "data quality"]),
            ("Evaluation Metrics & Reward Modeling", "high", ["reward models", "evals", "benchmarking", "perplexity"]),
            ("Fine-Tuning Frameworks (LoRA, PEFT)", "high", ["lora", "peft", "hugging face", "fine-tuning"]),
            ("Python & NLP Libraries", "high", ["python", "transformers", "pytorch"])
        ], ["DeepSpeed", "Axolotl", "Safety Filtering"]),

        ("Data Annotator / Labeler", "Labels, annotates, and verifies structured training datasets for computer vision and NLP models.", [
            ("Data Annotation Tools (LabelImg, CVAT, Prodigy)", "critical", ["cvat", "labelimg", "prodigy", "annotation tools"]),
            ("Bounding Boxes, Segmentation & Polygons", "critical", ["bounding boxes", "segmentation", "polygons", "keypoints"]),
            ("Quality Assurance & Inter-Annotator Agreement", "high", ["quality control", "accuracy", "consensus"]),
            ("Taxonomy & Guideline Adherence", "high", ["annotation guidelines", "classification", "metadata"]),
            ("Basic Excel / CSV Data Verification", "high", ["csv", "spreadsheets", "data validation"])
        ], ["Python Basics", "Active Learning Tools"]),

        ("Computer Vision Technician", "Develops and deploys image classification, object detection, and visual recognition pipelines.", [
            ("OpenCV & Image Processing", "critical", ["opencv", "image processing", "filtering", "computer vision"]),
            ("Deep Learning for Vision (YOLO, CNNs)", "critical", ["yolo", "cnn", "pytorch", "tensorflow", "object detection"]),
            ("Data Augmentation & Preprocessing", "high", ["albumentations", "data augmentation", "normalization"]),
            ("Edge Deployment (TensorRT, OpenCV OAK)", "high", ["tensorrt", "edge ai", "model quantization"]),
            ("Evaluation Metrics (mAP, IoU, F1)", "high", ["map", "iou", "precision-recall", "model validation"])
        ], ["3D Point Clouds", "Segmentation (SAM)", "Video Stream Processing"]),

        ("Natural Language Processing (NLP) Specialist", "Processes textual unstructured data, text embeddings, sentiment analysis, and tokenization.", [
            ("Transformers & Hugging Face Ecosystem", "critical", ["transformers", "hugging face", "bert", "gpt", "nlp"]),
            ("Text Preprocessing & Tokenization", "critical", ["tokenization", "spacy", "nltk", "regex", "lemmatization"]),
            ("Vector Embeddings & Semantic Search", "high", ["embeddings", "vector search", "cosine similarity", "chromadb"]),
            ("Text Classification & Named Entity Recognition (NER)", "high", ["ner", "sentiment analysis", "classification"]),
            ("Python & PyTorch", "high", ["python", "pytorch", "deep learning"])
        ], ["LLM Fine-Tuning", "Topic Modeling", "Multilingual Models"]),

        ("Synthetic Data Generator", "Creates realistic artificial data for training, privacy preservation, and simulation testing.", [
            ("Generative Techniques (GANs, Diffusion, LLMs)", "critical", ["synthetic data", "gans", "diffusion models", "generative ai"]),
            ("Statistical Validation & Distribution Matching", "critical", ["ks-test", "distribution matching", "statistical fidelity"]),
            ("Data Anonymization & Differential Privacy", "high", ["differential privacy", "anonymization", "k-anonymity"]),
            ("Python & Tabular Synthesis (SDV Library)", "high", ["sdv", "faker", "python", "pandas"]),
            ("Synthetic Edge-Case Simulation", "high", ["edge cases", "simulation", "stress testing"])
        ], ["Unity Perception", "Physics Simulation Engines"]),

        ("AI Ethics & Bias Auditor", "Assesses algorithmic fairness, demographic bias, compliance, and transparent explainability.", [
            ("Fairness Metrics & Disparate Impact Analysis", "critical", ["fairness metrics", "disparate impact", "bias detection", "equity"]),
            ("Model Explainability (SHAP, LIME)", "critical", ["shap", "lime", "explainability", "feature importance"]),
            ("AI Regulations & Governance (EU AI Act, NIST)", "high", ["eu ai act", "nist ai rmf", "governance", "compliance"]),
            ("Adversarial Testing & Red Teaming", "high", ["red teaming", "adversarial testing", "safety auditing"]),
            ("Python Data Analysis", "high", ["python", "pandas", "statistical testing"])
        ], ["Auditing Frameworks", "Policy Drafting", "Ethics Committees"]),

        ("Predictive Analytics Specialist", "Builds forecast models, regression engines, and time-series projections.", [
            ("Regression & Classification Models", "critical", ["regression", "logistic regression", "random forest", "xgboost"]),
            ("Time-Series Analysis (ARIMA, Prophet)", "critical", ["time series", "arima", "prophet", "forecasting"]),
            ("Feature Engineering & Selection", "high", ["feature engineering", "pca", "correlation analysis"]),
            ("Model Validation & Overfitting Prevention", "high", ["cross validation", "rmse", "mae", "roc-auc"]),
            ("Python / R Scientific Computing", "high", ["python", "pandas", "scipy", "r language"])
        ], ["Survival Analysis", "Monte Carlo Simulations", "Bayesian Statistics"]),

        ("SQL Database Specialist", "Specializes in query tuning, relational architecture, window functions, and procedures.", [
            ("Advanced SQL (CTEs, Window Functions)", "critical", ["sql", "window functions", "cte", "subqueries", "joins"]),
            ("Index Optimization & Execution Plans", "critical", ["indexes", "explain plan", "query tuning", "performance"]),
            ("Stored Procedures, Triggers & Views", "high", ["stored procedures", "triggers", "views", "pl/sql", "t-sql"]),
            ("Data Normalization & Schema Design", "high", ["normalization", "schema design", "foreign keys"]),
            ("Database Engines (PostgreSQL / MySQL / MS SQL)", "high", ["postgresql", "mysql", "sql server"])
        ], ["Partitioning", "Connection Pooling", "ETL Integration"]),

        ("Web Analytics Specialist (GA4)", "Configures tracking tags, conversion funnels, event taxonomies, and user journeys.", [
            ("Google Analytics 4 (GA4)", "critical", ["ga4", "google analytics", "event tracking", "conversions"]),
            ("Google Tag Manager (GTM)", "critical", ["google tag manager", "gtm", "tags", "triggers", "datalayer"]),
            ("Funnel Analysis & User Pathing", "high", ["funnels", "retention", "drop-off", "conversion rate"]),
            ("Data Studio / Looker Studio Dashboards", "high", ["looker studio", "data studio", "reporting"]),
            ("UTM Governance & Campaign Attribution", "high", ["utm tracking", "attribution modeling", "campaign analysis"])
        ], ["BigQuery with GA4", "Server-Side Tagging", "Cookie Consent"]),

        ("Geospatial / GIS Analyst", "Processes spatial layers, satellite imagery, coordinate projections, and cartographic maps.", [
            ("GIS Software (QGIS, ArcGIS)", "critical", ["qgis", "arcgis", "spatial analysis", "cartography"]),
            ("Geospatial Data Formats (GeoJSON, Shapefile, Raster)", "critical", ["geojson", "shapefile", "raster", "vector layers"]),
            ("Spatial SQL (PostGIS)", "high", ["postgis", "spatial queries", "st_intersects"]),
            ("Python Geospatial (GeoPandas, Shapely, Folium)", "high", ["geopandas", "shapely", "folium", "python"]),
            ("Coordinate Reference Systems (CRS) & Projections", "high", ["crs", "epsg", "map projections"])
        ], ["Remote Sensing", "LiDAR Data Processing", "Google Earth Engine"]),

        ("Quantitative Trading Bot Developer", "Builds automated execution algorithms, backtesting engines, and financial models.", [
            ("Algorithmic Trading & Backtesting (Backtrader/VectorBT)", "critical", ["backtesting", "algo trading", "backtrader", "vectorbt"]),
            ("Financial Math, Indicators & Statistics", "critical", ["sharpe ratio", "drawdown", "moving averages", "rsi", "macd"]),
            ("Broker & Exchange APIs (CCXT, Interactive Brokers)", "high", ["ccxt", "binance api", "interactive brokers", "rest api", "websockets"]),
            ("Python & High-Performance Data Processing", "high", ["python", "numpy", "pandas", "numba"]),
            ("Risk Management & Position Sizing", "high", ["risk management", "stop loss", "position sizing", "portfolio optimization"])
        ], ["C++ for Low Latency", "Machine Learning for Alpha", "Execution Algorithms"]),

        ("AI Chatbot / Voice Agent Builder", "Builds conversational voice agents, IVR systems, and conversational chatbots.", [
            ("Conversational Design & Intent Classification", "critical", ["conversational design", "intents", "dialogue management"]),
            ("Speech-to-Text & Text-to-Speech (Whisper, ElevenLabs)", "critical", ["whisper", "elevenlabs", "tts", "stt", "voice agents"]),
            ("Twilio / WebRTC & Telephony Integration", "high", ["twilio", "webrtc", "telephony", "sip"]),
            ("LLM Agent Tooling & Function Calling", "high", ["function calling", "tools", "live api", "webhooks"]),
            ("State Management & Session Context", "high", ["redis", "session management", "conversation memory"])
        ], ["Voice VAD Optimization", "Real-time Streaming", "Rasa Framework"]),

        ("Data Visualization Designer", "Crafts interactive graphics, data narratives, and human-centered chart interfaces.", [
            ("Visualization Theory & Visual Hierarchy", "critical", ["data visualization", "visual hierarchy", "color theory", "chart selection"]),
            ("D3.js or Observable Plot", "critical", ["d3.js", "d3", "svg", "observable", "javascript charts"]),
            ("Design Tools (Figma, Adobe Illustrator)", "high", ["figma", "illustrator", "infographics"]),
            ("Data Wrangling (Python or JavaScript)", "high", ["pandas", "json", "data transformation"]),
            ("Interactive Storytelling & Tooltips", "high", ["interactivity", "transitions", "tooltips", "accessibility"])
        ], ["WebGL / Three.js for Data", "Tableau Advanced", "Animation"]),

        ("Data Privacy & Governance Analyst", "Enforces regulatory compliance, data cataloging, access audits, and PII protection.", [
            ("Data Privacy Frameworks (GDPR, CCPA, HIPAA)", "critical", ["gdpr", "ccpa", "hipaa", "privacy law", "compliance"]),
            ("PII Auditing & Data Masking", "critical", ["pii", "data masking", "anonymization", "tokenization"]),
            ("Data Catalogs & Lineage (Collibra / Alation)", "high", ["data catalog", "data lineage", "collibra", "metadata"]),
            ("Access Control & Retention Policies", "high", ["rbac", "retention policies", "data lifecycle"]),
            ("Risk Assessment & DPIA Reports", "high", ["dpia", "privacy impact assessment", "audit reports"])
        ], ["ISO 27001", "Privacy by Design", "Security Clearance"]),

        ("Marketing Mix Modeling Analyst", "Attributes revenue across multi-channel advertising spend using econometric models.", [
            ("Econometric Modeling & Media Mix Modeling", "critical", ["marketing mix modeling", "mmm", "econometrics", "attribution"]),
            ("Adstock & Diminishing Returns Transformations", "critical", ["adstock", "diminishing returns", "saturation curves"]),
            ("Python / R Modeling (Robyn or LightweightMMM)", "high", ["robyn", "lightweightmmm", "pymc", "python", "r"]),
            ("Cross-Channel Media Data Integration", "high", ["ad spend", "impressions", "cross-channel data"]),
            ("ROI & Budget Optimization Forecasting", "high", ["roi", "budget allocation", "scenario planning"])
        ], ["Bayesian Statistics", "Causal Inference", "Geo-Lift Experiments"]),

        ("Sports Performance Data Analyst", "Analyzes tracking data, player metrics, biometric sensors, and game strategy.", [
            ("Sports Analytics Metrics & KPIs", "critical", ["sports analytics", "expected goals", "player tracking", "efficiency"]),
            ("Python / R for Sports Data", "critical", ["python", "r", "pandas", "data manipulation"]),
            ("Spatial Tracking & Heatmaps", "high", ["heatmaps", "spatial tracking", "gps tracking"]),
            ("Data Visualization & Match Reports", "high", ["data visualization", "tableau", "match analysis"]),
            ("Statistical Significance & Injury Risk Analysis", "high", ["statistical modeling", "injury prevention", "workload"])
        ], ["Computer Vision for Video", "Machine Learning in Sports", "Sensor Telemetry"]),

        ("Healthcare Data Analyst", "Processes electronic health records (EHR), clinical datasets, and epidemiological metrics.", [
            ("Healthcare Standards (HL7, FHIR, ICD-10)", "critical", ["hl7", "fhir", "icd-10", "cpt codes", "ehr"]),
            ("HIPAA Compliance & Clinical Privacy", "critical", ["hipaa", "phi", "patient privacy", "clinical data"]),
            ("SQL Querying on Clinical Warehouses", "high", ["sql", "claims data", "clinical databases"]),
            ("Biostatistics & Epidemiological Methods", "high", ["biostatistics", "survival analysis", "cohort analysis"]),
            ("Healthcare Dashboards & Quality Metrics (HEDIS)", "high", ["hedis", "clinical quality", "power bi", "tableau"])
        ], ["Python / R Biostatistics", "Epic / Cerner Systems", "Machine Learning for Diagnostics"]),

        ("Financial Data Modeler", "Constructs discounted cash flow, credit scoring, stress test, and equity models.", [
            ("Financial Modeling & DCF Valuation", "critical", ["financial modeling", "dcf", "valuation", "three-statement model"]),
            ("Advanced Excel & Financial Functions", "critical", ["excel", "financial functions", "scenario analysis", "macros"]),
            ("Credit Risk & Probability of Default Models", "high", ["credit risk", "probability of default", "scorecards"]),
            ("Python for Finance (QuantLib / NumPy)", "high", ["python", "numpy", "pandas", "financial analysis"]),
            ("Financial Statement Analysis (Balance Sheet, P&L)", "high", ["balance sheet", "income statement", "cash flow"])
        ], ["Monte Carlo Simulation", "Bloomberg Terminal", "CFA Knowledge"]),

        ("CRM Data Hygiene Specialist", "Cleans, deduplicates, enriches, and validates customer relationship data.", [
            ("CRM Databases (Salesforce / HubSpot)", "critical", ["salesforce", "hubspot", "crm", "contact records"]),
            ("Data Deduplication & Merge Strategies", "critical", ["deduplication", "data merging", "record cleanup"]),
            ("Data Enrichment & Validation Tools", "high", ["clearbit", "zoominfo", "data enrichment", "validation rules"]),
            ("Excel / OpenRefine Advanced Data Cleaning", "high", ["openrefine", "excel", "regex", "data transformation"]),
            ("Field Mapping & Import/Export Operations", "high", ["data loader", "import export", "field mapping"])
        ], ["SQL Basics", "Zapier Automation", "GDPR Data Removal Requests"])
    ],

    "Cybersecurity & IT Infrastructure": [
        ("Penetration Tester (Ethical Hacker)", "Simulates cyberattacks to expose vulnerabilities in networks, web apps, and endpoints.", [
            ("Network & Web App Penetration Testing", "critical", ["penetration testing", "ethical hacking", "owasp top 10", "vulnerability scanning"]),
            ("Tools (Burp Suite, Metasploit, Nmap)", "critical", ["burp suite", "metasploit", "nmap", "wireshark"]),
            ("Exploit Development & Scripting (Python/Bash)", "high", ["python", "bash", "exploit development", "payloads"]),
            ("Privilege Escalation & Lateral Movement", "high", ["privilege escalation", "active directory", "lateral movement"]),
            ("Technical Reporting & Remediation Advice", "high", ["pen test report", "vulnerability documentation", "cvss"])
        ], ["OSCP Certification", "Reverse Engineering", "Wireless Cracking"]),

        ("SOC (Security Operations Center) Analyst", "Monitors SIEM feeds, detects unauthorized intrusions, and investigates security alerts.", [
            ("SIEM Platforms (Splunk, Microsoft Sentinel)", "critical", ["siem", "splunk", "sentinel", "qradar", "log monitoring"]),
            ("Alert Triage & Incident Escalation", "critical", ["alert triage", "incident investigation", "false positives"]),
            ("Network Protocol Analysis (TCP/IP, DNS, HTTP)", "high", ["tcp/ip", "packet analysis", "wireshark", "dns"]),
            ("Endpoint Detection and Response (EDR)", "high", ["edr", "crowdstrike", "defender", "carbon black"]),
            ("MITRE ATT&CK Framework Mapping", "high", ["mitre att&ck", "threat tactics", "indicators of compromise"])
        ], ["SOAR Automation", "Threat Hunting", "YARA Rules"]),

        ("Incident Response Specialist", "Leads emergency response, containment, and forensic recovery following a security breach.", [
            ("Incident Containment & Eradication", "critical", ["incident response", "containment", "eradication", "forensic triage"]),
            ("Digital Forensics Artifact Analysis", "critical", ["memory forensics", "disk analysis", "event logs", "volatility"]),
            ("Chain of Custody & Legal Evidence Handling", "high", ["chain of custody", "evidence collection", "forensic image"]),
            ("Playbook Execution & Crisis Management", "high", ["incident playbooks", "crisis management", "post-incident review"]),
            ("Malware Remediation & System Recovery", "high", ["malware removal", "backup restoration", "hardening"])
        ], ["Reverse Engineering", "Threat Intelligence Integration", "Tabletop Exercises"]),

        ("Vulnerability Assessment Analyst", "Discovers, prioritizes, and oversees remediation of enterprise security weaknesses.", [
            ("Vulnerability Scanners (Nessus, Qualys, Rapid7)", "critical", ["nessus", "qualys", "rapid7", "vulnerability scanning"]),
            ("CVSS Scoring & Risk Prioritization", "critical", ["cvss", "vulnerability management", "risk scoring"]),
            ("Patch Management & Coordination", "high", ["patching", "remediation", "patch management"]),
            ("Asset Discovery & Inventory Mapping", "high", ["asset management", "port scanning", "shadow it"]),
            ("Compliance Standards (PCI-DSS, CIS Benchmarks)", "high", ["cis benchmarks", "pci-dss", "security baselines"])
        ], ["Scripting (Python)", "Zero-Day Research", "Jira Integration"]),

        ("Cloud Security Specialist", "Protects cloud infrastructure, Kubernetes clusters, and multi-tenant architectures.", [
            ("Cloud Security Posture Management (CSPM)", "critical", ["cspm", "cloud security", "aws security", "azure security"]),
            ("IAM Least Privilege Architecture", "critical", ["iam", "least privilege", "role-based access", "kms"]),
            ("Container & Kubernetes Security", "high", ["kubernetes security", "docker security", "trivy", "falco"]),
            ("Cloud Network Security (VPC, Security Groups, WAF)", "high", ["waf", "vpc", "security groups", "cloud firewall"]),
            ("Compliance & Audit in Cloud", "high", ["cloud compliance", "guardduty", "cloudtrail", "soc2"])
        ], ["Infrastructure as Code Security (Checkov)", "Zero Trust", "DevSecOps"]),

        ("Network Administrator", "Configures routers, switches, firewalls, and maintains campus network backbones.", [
            ("Cisco / Juniper Routing & Switching", "critical", ["cisco", "ccna", "routing", "switching", "vlan", "bgp", "ospf"]),
            ("TCP/IP, Subnetting & IP Addressing", "critical", ["tcp/ip", "subnetting", "ipv4", "ipv6", "dhcp", "dns"]),
            ("Firewall & VPN Configuration", "high", ["firewall", "vpn", "ipsec", "palo alto", "fortinet"]),
            ("Network Monitoring Tools (SNMP, PRTG, Wireshark)", "high", ["wireshark", "snmp", "prtg", "network monitoring"]),
            ("Cable Management & Hardware Rack Installations", "high", ["patch panels", "fiber optics", "cat6", "rack layout"])
        ], ["SD-WAN", "Wireless Controllers", "Network Automation (Ansible)"]),

        ("Systems Administrator (Linux/Windows)", "Deploys, updates, and manages physical and virtual server infrastructure.", [
            ("Linux OS (RHEL/Ubuntu) or Windows Server", "critical", ["linux", "ubuntu", "centos", "rhel", "windows server", "active directory"]),
            ("User Management, Permissions & Group Policy (GPO)", "critical", ["active directory", "gpo", "permissions", "user management", "ssh"]),
            ("Scripting for Automation (Bash / PowerShell)", "high", ["powershell", "bash", "shell scripting", "automation"]),
            ("Virtualization (VMware ESXi, Hyper-V, Proxmox)", "high", ["vmware", "hyper-v", "proxmox", "virtualization"]),
            ("System Backup, Patching & Disaster Recovery", "high", ["veeam", "system updates", "patch management", "backups"])
        ], ["Ansible", "Storage (SAN/NAS)", "Clustering"]),

        ("IT Help Desk Technician", "Provides tier 1 and tier 2 hardware, software, and remote desktop support.", [
            ("Operating System Troubleshooting (Windows/Mac)", "critical", ["windows 10/11", "macos", "troubleshooting", "os diagnostics"]),
            ("Hardware Setup & Peripheral Diagnostics", "critical", ["hardware repairs", "printers", "monitors", "peripherals", "docking stations"]),
            ("Ticketing Systems (ServiceNow, Jira, Zendesk)", "high", ["servicenow", "jira service management", "zendesk", "sla"]),
            ("Remote Support Tools (AnyDesk, TeamViewer)", "high", ["remote desktop", "teamviewer", "anydesk"]),
            ("Account Provisioning & Password Resets (AD, O365)", "high", ["active directory", "office 365", "google workspace", "mfa"])
        ], ["Network Basics", "Asset Tagging", "CompTIA A+"]),

        ("Identity & Access Management (IAM) Specialist", "Designs single sign-on, multi-factor authentication, and privileged access.", [
            ("SSO Protocols (SAML 2.0, OIDC, OAuth)", "critical", ["saml", "oidc", "oauth2", "single sign-on", "sso"]),
            ("Identity Providers (Okta, Microsoft Entra ID)", "critical", ["okta", "entra id", "azure ad", "ping identity"]),
            ("Privileged Access Management (PAM - CyberArk)", "high", ["pam", "cyberark", "privileged access", "session recording"]),
            ("Role-Based Access Control (RBAC) Governance", "high", ["rbac", "abac", "access certification", "lifecycle management"]),
            ("Multi-Factor Authentication (MFA) Enforcement", "high", ["mfa", "fido2", "authenticator", "conditional access"])
        ], ["SailPoint", "Directory Synchronization", "Zero Trust Architecture"]),

        ("Digital Forensics Investigator", "Extracts, decrypts, and analyzes court-admissible digital evidence from compromised devices.", [
            ("Forensic Imaging & Write-Blockers", "critical", ["forensic imaging", "write blocker", "e01", "raw image", "ftk imager"]),
            ("Forensics Toolkits (Autopsy, EnCase, Volatility)", "critical", ["autopsy", "encase", "volatility", "x-ways"]),
            ("File System Analysis (NTFS, EXT4, APFS)", "high", ["ntfs", "mft", "file carving", "deleted files"]),
            ("Memory & Registry Forensics", "high", ["ram forensics", "windows registry", "prefetch", "shimcache"]),
            ("Expert Witness Reporting & Legal Testimony", "high", ["forensic report", "expert testimony", "evidence custody"])
        ], ["Mobile Forensics (Cellebrite)", "Malware Triage", "Email Forensics"]),

        ("Threat Intelligence Analyst", "Tracks APT groups, uncovers attack campaigns, and disseminates actionable threat indicators.", [
            ("Threat Feeds & STIX/TAXII Standards", "critical", ["threat intelligence", "stix", "taxii", "ioc", "feeds"]),
            ("Adversary Profiling (APTs, TTPs, MITRE)", "critical", ["apt groups", "ttps", "mitre att&ck", "threat actors"]),
            ("OSINT & Dark Web Monitoring", "high", ["osint", "dark web", "shodan", "maltego", "threat hunting"]),
            ("Intelligence Report Authoring", "high", ["threat briefing", "bulletins", "risk analysis"]),
            ("YARA Rules & IoC Extraction", "high", ["yara", "hashes", "ip reputation", "domain analysis"])
        ], ["MISP Platform", "Reverse Engineering Basics", "Geopolitical Analysis"]),

        ("Application Security (AppSec) Engineer", "Embeds security into software development lifecycles (SAST, DAST, code review).", [
            ("Secure Code Review & OWASP Top 10", "critical", ["secure coding", "owasp top 10", "code review", "vulnerabilities"]),
            ("SAST & DAST Tools (SonarQube, Snyk, Zap)", "critical", ["sast", "dast", "sonarqube", "snyk", "owasp zap"]),
            ("Software Bill of Materials (SBOM) & Dependencies", "high", ["sbom", "dependency check", "cve", "supply chain security"]),
            ("Security Champions & DevSecOps Pipelines", "high", ["devsecops", "ci/cd security", "threat modeling"]),
            ("Threat Modeling (STRIDE Framework)", "high", ["threat modeling", "stride", "data flow diagrams"])
        ], ["API Security", "Penetration Testing", "Security Policy"]),

        ("Malware Analyst", "Dissects malicious executables, ransomware, and trojans in controlled sandbox labs.", [
            ("Static Analysis (Ghidra, IDA Pro, Strings)", "critical", ["static analysis", "ghidra", "ida pro", "disassembly", "pe analysis"]),
            ("Dynamic Analysis & Sandboxing (Cuckoo, Any.Run)", "critical", ["dynamic analysis", "cuckoo sandbox", "process monitor", "regshot"]),
            ("x86/x64 Assembly Language", "high", ["assembly", "x86", "x64", "registers", "opcodes"]),
            ("De-obfuscation & Anti-Analysis Bypass", "high", ["deobfuscation", "unpacking", "anti-debugging", "anti-vm"]),
            ("YARA Rule Creation & Signature Writing", "high", ["yara", "signatures", "indicators of compromise"])
        ], ["Kernel Debugging", "Ransomware Decryption", "Memory Injection Techniques"]),

        ("Hardware Repair & Diagnostics Technician", "Troubleshoots circuit boards, replaces microsoldered components, and repairs hardware.", [
            ("Component-Level Electronics Diagnostics", "critical", ["schematics", "multimeter", "short circuit", "voltage rails"]),
            ("Microsoldering & SMT Rework", "critical", ["microsoldering", "soldering iron", "hot air rework", "flux", "bga"]),
            ("Laptop & Motherboard Disassembly", "high", ["laptop repair", "motherboard", "screen replacement", "connectors"]),
            ("Firmware Flashing & BIOS Recovery", "high", ["bios programmer", "ch341a", "firmware flashing"]),
            ("ESD Safety & Clean Lab Procedures", "high", ["esd protection", "thermal paste", "diagnostic cards"])
        ], ["Oscilloscope Diagnostics", "Power Supply Repair", "Cleanroom Techniques"]),

        ("VoIP & Telecom Technician", "Installs, configures, and maintains PBX systems, SIP trunks, and enterprise telephony.", [
            ("SIP Protocol & VoIP Architecture", "critical", ["sip", "voip", "rtp", "codecs", "pbx"]),
            ("IP PBX Platforms (Asterisk, 3CX, Cisco CUCM)", "critical", ["asterisk", "3cx", "cisco cucm", "freepbx"]),
            ("QoS & Voice Network Prioritization", "high", ["qos", "jitter", "packet loss", "vlan"]),
            ("Telecom Hardware (SIP Phones, FXS/FXO Gateways)", "high", ["polycom", "yealink", "gateways", "punchdown blocks"]),
            ("Call Routing & Dial Plan Configuration", "high", ["dial plans", "ivr", "call queues", "trunking"])
        ], ["PSTN Interconnects", "Session Border Controllers", "Telecom Cabling"]),

        ("Server Rack & Data Center Technician", "Installs server chassis, cable trays, UPS batteries, and cooling systems in data centers.", [
            ("Server Chassis Installation (1U to 4U)", "critical", ["server rack", "rail kits", "rack and stack", "chassis"]),
            ("Structured Fiber & Copper Cabling", "critical", ["fiber optic", "cat6a", "cable management", "patch panels", "fluke tester"]),
            ("Power Distribution (PDU, UPS, Redundant Feeds)", "high", ["pdu", "ups", "three-phase power", "generators"]),
            ("HVAC & Hot/Cold Aisle Containment", "high", ["hot aisle", "cold aisle", "airflow management", "cooling units"]),
            ("Hardware RMA, Drive Swaps & BIOS Setup", "high", ["drive replacement", "raid controllers", "ipmi", "idrac", "ilo"])
        ], ["Data Center Infrastructure Management (DCIM)", "Environmental Monitoring"]),

        ("Compliance & GRC Analyst (ISO/SOC2)", "Audits internal controls, manages corporate risk registers, and guides audits.", [
            ("Security Frameworks (ISO 27001, SOC 2, NIST)", "critical", ["iso 27001", "soc 2", "nist csf", "compliance"]),
            ("Internal Audit & Control Testing", "critical", ["internal audit", "control testing", "gap analysis", "evidence gathering"]),
            ("Third-Party Vendor Risk Assessment", "high", ["vendor risk", "questionnaires", "third-party risk management"]),
            ("Risk Registers & Risk Assessment Methodology", "high", ["risk register", "risk assessment", "mitigation plans"]),
            ("Policy Drafting & Security Governance", "high", ["policy drafting", "acceptable use policy", "governance"])
        ], ["GRC Platforms (Vanta, Drata)", "HIPAA / FedRAMP", "Board Reporting"]),

        ("Smart Home / IoT Security Installer", "Configures secure smart home hubs, cameras, sensors, and isolated IoT networks.", [
            ("Smart Protocols (Zigbee, Z-Wave, Matter, Thread)", "critical", ["zigbee", "z-wave", "matter", "thread", "smart home"]),
            ("IoT Network Segmentation & VLANs", "critical", ["vlan", "network isolation", "firewall rules", "guest network"]),
            ("IP Camera & NVR System Installation", "high", ["nvr", "ip cameras", "poe", "onvif"]),
            ("Smart Hubs (Home Assistant, Hubitat)", "high", ["home assistant", "automation", "integrations"]),
            ("Access Control & Smart Locks Configuration", "high", ["smart locks", "door access", "keypads"])
        ], ["Low Voltage Wiring", "Alarm System Certification", "Battery Backup"]),

        ("Wireless Network Engineer", "Conducts RF heatmaps, designs Wi-Fi 6/7 architectures, and tunes enterprise wireless.", [
            ("Wi-Fi Standards (802.11ax/be - Wi-Fi 6/7)", "critical", ["wi-fi 6", "wi-fi 7", "802.11", "wlan", "wireless"]),
            ("RF Site Surveys & Heatmapping (Ekahau)", "critical", ["ekahau", "site survey", "heatmaps", "rf spectrum"]),
            ("Wireless LAN Controllers (Aruba, Cisco, UniFi)", "high", ["wireless controller", "aruba", "cisco wlc", "unifi", "access points"]),
            ("RF Interference & Channel Tuning", "high", ["channel bonding", "spectrum analysis", "roaming optimization", "rssi"]),
            ("WPA3 Enterprise & 802.1X Authentication", "high", ["wpa3", "802.1x", "radius", "eap-tls"])
        ], ["Outdoor Wireless PTP Links", "Cellular 5G Private Networks", "CWNA Certification"]),

        ("Disaster Recovery Specialist", "Formulates business continuity plans, replication strategies, and emergency recovery drills.", [
            ("Business Impact Analysis (BIA) & RPO/RTO", "critical", ["rpo", "rto", "bia", "business continuity", "disaster recovery"]),
            ("Backup Technologies & Immutable Storage", "critical", ["veeam", "immutable backup", "air-gapped", "cloud replication"]),
            ("High Availability & Failover Orchestration", "high", ["failover", "clustering", "site recovery manager", "dr testing"]),
            ("Crisis Communication & Runbook Authoring", "high", ["dr runbooks", "emergency response", "call trees"]),
            ("Annual DR Simulation Drills", "high", ["tabletop drill", "dr drill", "simulation", "post-test review"])
        ], ["Multi-Cloud Resiliency", "Cold/Warm/Hot Site Logistics", "Regulatory Compliance"])
    ],

    "Design, UI/UX & Creative Arts": [
        ("UI (User Interface) Designer", "Designs high-fidelity visual interfaces, responsive layouts, and interactive design systems.", [
            ("Figma Mastery (Components, Auto-Layout, Variants)", "critical", ["figma", "components", "auto-layout", "variants", "design system"]),
            ("Visual Design Principles (Typography, Spacing, Color)", "critical", ["typography", "color theory", "spacing", "visual hierarchy"]),
            ("Responsive Web & Mobile UI Patterns", "high", ["responsive design", "mobile ui", "desktop ui", "ui patterns"]),
            ("Interactive Prototyping & Micro-interactions", "high", ["prototyping", "figma prototypes", "micro-interactions"]),
            ("Developer Handoff & Design Tokens", "high", ["design tokens", "developer handoff", "specs", "assets"])
        ], ["Design Systems Architecture", "Tailwind Integration", "Accessibility Contrast"]),

        ("UX (User Experience) Researcher", "Uncovers user behaviors, pain points, mental models, and validates product flows.", [
            ("User Interviewing & Usability Testing", "critical", ["user interviews", "usability testing", "moderated testing", "think aloud"]),
            ("Survey Design & Quantitative Analysis", "critical", ["surveys", "quantitative research", "sus score", "data synthesis"]),
            ("User Journey Mapping & Personas", "high", ["user journey", "personas", "empathy map", "service blueprint"]),
            ("Information Architecture & Card Sorting", "high", ["information architecture", "card sorting", "tree testing"]),
            ("Synthesizing Research Insights & Presentation", "high", ["research report", "stakeholder presentations", "affinity mapping"])
        ], ["Eye Tracking", "A/B Testing Methodologies", "Diary Studies"]),

        ("Product Designer (Digital)", "Merges user research, UX architecture, business goals, and visual UI into cohesive products.", [
            ("End-to-End Product Design Lifecycle", "critical", ["product design", "ux design", "ui design", "double diamond"]),
            ("Figma Advanced Workflows", "critical", ["figma", "design systems", "prototyping"]),
            ("Design Strategy & Business Alignment", "high", ["product strategy", "kpis", "user onboarding", "conversion"]),
            ("Wireframing & Rapid Iteration", "high", ["wireframing", "low fidelity", "rapid prototyping"]),
            ("Cross-Functional Collaboration with Engineers", "high", ["agile", "developer handoff", "scrum", "qa review"])
        ], ["User Metrics Tracking", "Growth Design", "Design Systems Maintenance"]),

        ("Graphic Designer", "Creates compelling visual brand communications, posters, marketing assets, and illustrations.", [
            ("Adobe Illustrator & Vector Artwork", "critical", ["illustrator", "vector graphics", "pen tool", "logos"]),
            ("Adobe Photoshop & Raster Editing", "critical", ["photoshop", "photo manipulation", "masking", "compositing"]),
            ("Typography, Hierarchy & Layout Composition", "high", ["typography", "layout design", "hierarchy", "grids"]),
            ("Branding Collateral & Social Media Creatives", "high", ["branding", "marketing assets", "social media posts", "banners"]),
            ("Color Theory & Print vs Digital Standards", "high", ["cmyk", "rgb", "pantone", "resolution", "dpi"])
        ], ["InDesign", "Motion Design Basics", "Pre-Press Production"]),

        ("Brand Identity Designer", "Crafts comprehensive brand identity guidelines, logos, color palettes, and brand books.", [
            ("Logo Design & Vector Craftsmanship", "critical", ["logo design", "brand mark", "vector", "illustrator"]),
            ("Brand Guidelines & Style Guides", "critical", ["brand guidelines", "style guide", "brand book", "typography system"]),
            ("Brand Archetypes & Strategic Positioning", "high", ["brand strategy", "positioning", "moodboards", "archetypes"]),
            ("Collateral Mockups (Signage, Stationery, Packaging)", "high", ["mockups", "stationery", "packaging design"]),
            ("Color Systems & Pantone Matching", "high", ["pantone", "color palette", "brand colors"])
        ], ["Custom Lettering", "Motion Branding", "Rebranding Audits"]),

        ("Motion Graphics Designer", "Brings typography, vectors, and brand assets to life with cinematic animation.", [
            ("Adobe After Effects & Keyframe Animation", "critical", ["after effects", "motion design", "keyframes", "graph editor"]),
            ("Animation Principles (Easing, Anticipation, Timing)", "critical", ["12 principles of animation", "easing", "timing", "motion curves"]),
            ("Motion for UI & Lottie Exports", "high", ["lottie", "bodymovin", "ui animation", "micro-animations"]),
            ("Vector Preparation in Illustrator", "high", ["illustrator", "vector assets", "layer separation"]),
            ("Sound Design & Music Synchronization", "high", ["audio sync", "sound effects", "sound design"])
        ], ["Cinema 4D Basics", "Spline 3D", "Character Rigging"]),

        ("3D Modeler & Sculptor (Blender/ZBrush)", "Sculpts organic characters, hard-surface props, and game-ready 3D assets.", [
            ("Blender or ZBrush High-Poly Sculpting", "critical", ["blender", "zbrush", "3d modeling", "digital sculpting"]),
            ("Topology, Retopology & UV Unwrapping", "critical", ["retopology", "uv unwrapping", "quad topology", "edge loops"]),
            ("PBR Texturing (Substance Painter)", "high", ["substance painter", "pbr texturing", "normal maps", "baking"]),
            ("Hard Surface vs Organic Modeling Techniques", "high", ["hard surface", "organic modeling", "subdivision"]),
            ("Export Pipelines for Engines (FBX, OBJ, glTF)", "high", ["fbx", "gltf", "game assets", "scale"])
        ], ["Rigging Basics", "Lighting & Rendering (Cycles/Marmoset)", "3D Printing Preparation"]),

        ("3D Environment & Asset Artist", "Constructs immersive 3D landscapes, architectural environments, and game worlds.", [
            ("Modular Environment Asset Creation", "critical", ["modular environment", "3d assets", "blender", "maya"]),
            ("Level Dressing & Unreal Engine / Unity Worldbuilding", "critical", ["unreal engine", "unity", "level design", "foliage"]),
            ("PBR Materials & Shader Graphs", "high", ["substance designer", "pbr materials", "material graph"]),
            ("Photogrammetry & Scan Clean-Up", "high", ["photogrammetry", "realitycapture", "scan cleanup"]),
            ("Optimization (LODs, Draw Calls, Collision Meshes)", "high", ["lods", "draw calls", "light baking", "collision"])
        ], ["Nanite & Lumen", "Houdini Procedural Environments", "Terrain Generation"]),

        ("Packaging Designer", "Engineers functional, aesthetic, and regulatory compliant physical product packaging.", [
            ("Dieline Creation & Structural Packaging", "critical", ["dielines", "structural packaging", "folding cartons", "corrugated"]),
            ("Adobe Illustrator for Packaging Art", "critical", ["illustrator", "vector art", "packaging design"]),
            ("Materials, Finishes & Printing Techniques (Emboss, Foil)", "high", ["foil stamping", "embossing", "spot uv", "substrates"]),
            ("Regulatory Labeling & Barcode Placement", "high", ["nutrition facts", "barcodes", "fda labeling", "compliance"]),
            ("3D Packaging Renders & Mockups", "high", ["3d mockups", "keyshot", "dimensions", "product visualization"])
        ], ["Sustainable Packaging Materials", "Pre-Press Proofing", "Industrial Blister Packs"]),

        ("Print & Editorial Layout Designer", "Designs magazines, multi-page books, annual reports, and brochures.", [
            ("Adobe InDesign Mastery", "critical", ["indesign", "editorial design", "master pages", "paragraph styles"]),
            ("Grid Systems & Editorial Hierarchy", "critical", ["grid systems", "column layout", "editorial hierarchy", "leading"]),
            ("Pre-Press Preparation & Color Management", "high", ["bleed", "slug", "cmyk", "preflight", "color profiles"]),
            ("Long-Form Typesetting & Micro-Typography", "high", ["typesetting", "kerning", "orphans", "widows", "hyphenation"]),
            ("Binding Styles & Paper Stock Selection", "high", ["saddle stitch", "perfect bound", "paper stocks", "finishing"])
        ], ["Interactive Digital PDFs", "ePub Publishing", "Large Format Print"]),

        ("Typography & Custom Lettering Artist", "Draws bespoke letterforms, custom typefaces, and expressive typographic logos.", [
            ("Bespoke Letterform Construction & Bézier Curves", "critical", ["lettering", "bezier curves", "calligraphy", "vector curves"]),
            ("Font Creation Software (Glyphs, FontLab)", "critical", ["glyphs", "fontlab", "font creation", "typography"]),
            ("Kerning Pairs, Metrics & OpenType Features", "high", ["kerning", "opentype", "ligatures", "spacing"]),
            ("Historical Type Classifications & Anatomy", "high", ["serif", "sans serif", "type anatomy", "ascenders"]),
            ("Custom Typographic Logotypes & Badges", "high", ["logotypes", "hand lettering", "branding"])
        ], ["Variable Fonts", "Monogram Design", "Sign Painting Heritage"]),

        ("Digital Illustrator", "Creates original digital paintings, editorial illustrations, and conceptual visual art.", [
            ("Digital Drawing Software (Photoshop, Procreate)", "critical", ["procreate", "photoshop", "digital illustration", "brushwork"]),
            ("Anatomy, Perspective & Composition", "critical", ["anatomy", "perspective", "composition", "vanishing point"]),
            ("Light, Shadow & Color Shading", "high", ["shading", "lighting", "color palettes", "rendering"]),
            ("Stylistic Versatility (Flat, Realistic, Isometric)", "high", ["isometric", "flat illustration", "character drawing"]),
            ("Editorial & Commercial Brief Execution", "high", ["client briefs", "thumbnails", "revisions", "storytelling"])
        ], ["Vector Illustration", "Clip Studio Paint", "NFT Art Creation"]),

        ("Concept Artist (Games/Film)", "Visualizes early conceptual characters, environments, vehicles, and creatures for entertainment.", [
            ("Speed Painting & Rapid Visual Ideation", "critical", ["concept art", "speed painting", "photobashing", "visual development"]),
            ("Worldbuilding, Mood & Atmospheric Lighting", "critical", ["mood", "lighting", "worldbuilding", "cinematic"]),
            ("Character & Creature Design Sheets", "high", ["character design", "turnaround", "creature design", "costume"]),
            ("3D Block-Out for 2D Paint-Over (Blender)", "high", ["blender", "blockout", "paintover", "3d coat"]),
            ("Production Art Bible Documentation", "high", ["art bible", "callout sheets", "film/game pipelines"])
        ], ["Keyframe Art", "Vehicle Design", "VR Conceptual Sketching"]),

        ("Storyboard Artist", "Translates scripts into sequential illustrated panels for films, commercials, and animations.", [
            ("Visual Storytelling & Shot Composition", "critical", ["storyboarding", "shot composition", "camera angles", "framing"]),
            ("Camera Movement & Continuity Direction", "critical", ["camera moves", "panning", "zooms", "continuity", "180 rule"]),
            ("Rapid Gesture Sketching & Character Poses", "high", ["gesture drawing", "posing", "expression", "quick sketching"]),
            ("Storyboard Software (Storyboard Pro, Photoshop)", "high", ["storyboard pro", "photoshop", "animatic"]),
            ("Pacing, Timing & Animatic Generation", "high", ["animatic", "pacing", "scene transitions", "beat boards"])
        ], ["Script Breakdown", "Action Sequence Choreography", "Directorial Vision"]),

        ("Character Designer", "Develops distinctive characters with expressive anatomy, silhouettes, and wardrobe.", [
            ("Silhouette, Shape Language & Readability", "critical", ["shape language", "silhouette", "character design", "appeal"]),
            ("Facial Expressions & Emotional Range", "critical", ["facial expressions", "model sheets", "mouth shapes"]),
            ("Turnaround Sheets & Costume Design", "high", ["turnarounds", "costume design", "props", "color palettes"]),
            ("Anatomy & Proportion Stylization", "high", ["stylized anatomy", "exaggeration", "proportions"]),
            ("Digital Drawing & Inking Craftsmanship", "high", ["inking", "clean lines", "digital drawing"])
        ], ["3D Sculpting for Reference", "Rigging Awareness", "Animation Preparation"]),

        ("Architectural Visualizer (3D Rendering)", "Produces photorealistic renders of buildings, interiors, and architectural spaces.", [
            ("3D Architecture Software (3ds Max, Revit, SketchUp)", "critical", ["3ds max", "sketchup", "revit", "archviz"]),
            ("Rendering Engines (V-Ray, Corona, Lumion, D5)", "critical", ["v-ray", "corona renderer", "lumion", "d5 render", "photorealism"]),
            ("Architectural Lighting & Sun Studies", "high", ["hdri lighting", "interior lighting", "sun study", "ies lights"]),
            ("PBR Architectural Materials (Glass, Concrete, Wood)", "high", ["architectural materials", "shaders", "textures"]),
            ("Photoshop Post-Production & Color Grading", "high", ["post-production", "photoshop", "compositing", "entourage"])
        ], ["Twinmotion", "Unreal Engine ArchViz", "Virtual Tour Creation"]),

        ("CAD Drafter (AutoCAD/SolidWorks)", "Produces technical engineering drawings, blueprints, and tolerance specifications.", [
            ("AutoCAD or SolidWorks 2D/3D Drafting", "critical", ["autocad", "solidworks", "cad drafting", "technical drawings"]),
            ("GD&T (Geometric Dimensioning & Tolerancing)", "critical", ["gd&t", "tolerances", "dimensions", "orthographic projection"]),
            ("BOM (Bill of Materials) & Part Callouts", "high", ["bill of materials", "bom", "assembly drawings", "part details"]),
            ("Engineering Standards (ASME, ISO)", "high", ["asme", "iso standards", "drawing sheets"]),
            ("Parametric Modeling & Assembly Verification", "high", ["parametric modeling", "interference check", "mating"])
        ], ["Revit MEP", "CNC Export Files (DXF/STEP)", "Sheet Metal Drafting"]),

        ("Industrial / Product Prototype Designer", "Designs tangible consumer products from ergonomics to physical prototypes.", [
            ("Form Giving, Styling & Ergonomics", "critical", ["industrial design", "ergonomics", "form development", "product styling"]),
            ("CAD Modeling (Rhino, Fusion 360)", "critical", ["fusion 360", "rhino", "surface modeling", "cad"]),
            ("Rapid Prototyping & 3D Printing", "high", ["3d printing", "prototyping", "foam modeling", "cnc milling"]),
            ("Design for Manufacturing (DFM - Injection Molding)", "high", ["dfm", "injection molding", "draft angles", "tooling"]),
            ("Keyshot Photorealistic Product Renders", "high", ["keyshot", "product rendering", "cbr", "finishes"])
        ], ["Design Thinking", "User Physical Testing", "Patenting Drawings"]),

        ("Interior Space Planner", "Plans interior layouts, furniture arrangements, flow of movement, and spatial utility.", [
            ("Floor Plans, Space Planning & Circulation", "critical", ["space planning", "floor plans", "circulation", "scale"]),
            ("AutoCAD / SketchUp for Interiors", "critical", ["sketchup", "autocad", "elevation drawings"]),
            ("Building Codes & ADA Accessibility Requirements", "high", ["building codes", "ada compliance", "egress", "clearances"]),
            ("Furniture, Fixtures & Equipment (FF&E) Schedules", "high", ["ff&e", "material specification", "furniture sourcing"]),
            ("Lighting Plans & Finish Palettes", "high", ["lighting design", "materials", "swatches", "color schemes"])
        ], ["3D Walkthrough Renders", "Kitchen & Bath Standards", "Sustainable LEED Design"]),

        ("Fashion & Apparel Technical Designer", "Creates tech packs, garment measurement specs, grading, and pattern modifications.", [
            ("Tech Pack Creation & Garment Specifications", "critical", ["tech pack", "garment specs", "apparel design", "bill of materials"]),
            ("Flat Technical Drawings (Adobe Illustrator)", "critical", ["technical flats", "illustrator", "garment sketches"]),
            ("Patternmaking & Grading Rules", "high", ["patternmaking", "grading", "fit evaluation", "seam construction"]),
            ("Fabric Properties & Sourcing Knowledge", "high", ["textiles", "knits", "wovens", "fabric testing"]),
            ("Sample Review & Factory Quality Control", "high", ["fit comments", "sample review", "factory communication", "tolerances"])
        ], ["CLO 3D Virtual Fitting", "Optitex", "Sustainable Garment Dyeing"]),

        ("Textile & Surface Pattern Designer", "Draws repeating patterns for textiles, wallpapers, packaging, and home furnishings.", [
            ("Seamless Repeat Patterns (Half-Drop, Block)", "critical", ["repeat patterns", "half-drop", "seamless pattern", "surface design"]),
            ("Adobe Illustrator & Photoshop for Textiles", "critical", ["illustrator", "photoshop", "pattern tool", "vector patterns"]),
            ("Color Separations & Screen Printing Specs", "high", ["color separation", "screen printing", "rotary print", "colorways"]),
            ("Textile Printing Methods (Digital, Dye-Sub, Jacquard)", "high", ["digital textile printing", "jacquard", "fabric printing"]),
            ("Trend Forecasting & Moodboard Curation", "high", ["trend forecasting", "moodboards", "fashion color trends"])
        ], ["Weaving Basics", "Packaging Surface Applications", "Licensing Art Portfolios"]),

        ("Tattoo Artist", "Designs custom flash art and implements safe sterile body ink application.", [
            ("Flash Drawing & Custom Linework", "critical", ["tattoo design", "flash art", "linework", "procreate tattoo"]),
            ("Sterilization, Bloodborne Pathogen & Sanitation", "critical", ["bloodborne pathogens", "autoclave", "cross-contamination", "hygiene"]),
            ("Tattoo Machine Operation (Rotary / Coil)", "high", ["tattoo machine", "needle configurations", "voltage", "depth"]),
            ("Skin Anatomy & Healing Dynamics", "high", ["skin layers", "ink saturation", "aftercare instructions"]),
            ("Stencil Application & Body Placement", "high", ["stencil application", "anatomical placement", "shading techniques"])
        ], ["Color Realism", "Black & Grey Shading", "Cover-up Artistry"]),

        ("Muralist & Sign Painter", "Paints large-scale wall installations, hand-lettered signs, and urban public art.", [
            ("Large-Scale Grid Scaling & Projector Transfer", "critical", ["mural painting", "grid scaling", "doodle grid", "wall art"]),
            ("Exterior Paint Chemistry & Weather Sealing", "critical", ["exterior paint", "masonry primer", "uv varnish", "anti-graffiti"]),
            ("Hand Lettering & Pinstriping Brushes", "high", ["sign painting", "mahl stick", "lettering brushes", "enamel paint"]),
            ("Scaffolding, Lift Safety & Surface Prep", "high", ["surface prep", "scaffolding safety", "ladder safety", "power washing"]),
            ("Client Site Proposals & Digital Mockups", "high", ["site proposals", "photoshop mockup", "scaling"])
        ], ["Spray Paint / Aerosol Technique", "Gold Leaf Gilding", "Community Art Organizing"]),

        ("Infographics Designer", "Visualizes intricate statistics, chronologies, and workflows into clear graphic formats.", [
            ("Information Architecture & Data Simplification", "critical", ["infographics", "data simplification", "visual breakdown", "diagrams"]),
            ("Adobe Illustrator Vector Graphics", "critical", ["illustrator", "icons", "vector illustrations", "charts"]),
            ("Statistical Chart Selection & Accuracy", "high", ["chart selection", "data accuracy", "proportions", "visual hierarchy"]),
            ("Iconography & Visual Metaphor Design", "high", ["icon design", "visual metaphors", "styling"]),
            ("Typography & Color Coding Systems", "high", ["typography", "color coding", "editorial styling"])
        ], ["Interactive Infographics", "Motion Infographics", "Report Layouts"]),

        ("Presentation / Pitch Deck Designer", "Designs high-stakes investor pitch decks, keynote slides, and corporate decks.", [
            ("Presentation Tools (PowerPoint, Keynote, Figma)", "critical", ["powerpoint", "keynote", "figma", "slide design", "pitch deck"]),
            ("Storytelling & Narrative Structuring", "critical", ["pitch narrative", "investor deck", "problem solution", "storytelling"]),
            ("Data Slides, Financial Tables & Chart Redesigns", "high", ["financial charts", "data slides", "metrics presentation"]),
            ("Slide Master & Template Systems", "high", ["slide master", "custom templates", "branding guidelines"]),
            ("High-Impact Typography & Layout Polish", "high", ["typography", "clean layout", "visual impact"])
        ], ["Speaker Notes Coaching", "Fundraising Deck Formats", "Animation Transitions"]),

        ("Thumbnail & Social Visual Designer", "Creates high-CTR YouTube thumbnails, hook banners, and viral social assets.", [
            ("High-CTR Visual Composition & Expressions", "critical", ["youtube thumbnail", "ctr optimization", "focal point", "eye-catching"]),
            ("Photoshop Retouching, Cutouts & Lighting Effects", "critical", ["photoshop", "cutouts", "glow effects", "color pop", "face enhancement"]),
            ("Bold Readable Typography at Small Scale", "high", ["thumbnail text", "bold fonts", "mobile readability"]),
            ("Visual Storytelling & Curated Curiosity Gaps", "high", ["curiosity gap", "visual hooks", "click intent"]),
            ("A/B Testing Thumbnail Analytics", "high", ["a/b testing", "ctr metrics", "youtube studio"])
        ], ["3D Render Integration", "Branded Series Templates", "Shorts Covers"]),

        ("Book Cover Designer", "Designs genre-defining front, spine, and back book jackets for print and digital.", [
            ("Genre Tropes & Market Positioning", "critical", ["book cover design", "genre tropes", "commercial appeal", "amazon thumbnail"]),
            ("Full Jacket Layout & Spine Width Calculation", "critical", ["spine calculation", "page count", "print jacket", "bleed"]),
            ("Photoshop Compositing & Typography Integration", "high", ["compositing", "title typography", "photo manipulation"]),
            ("Barcode, Blurb & Title Hierarchy", "high", ["hierarchy", "isbn barcode", "blurb placement"]),
            ("Ebook & Audiobook Cover Adaptation", "high", ["ebook cover", "acx specs", "audible cover"])
        ], ["Custom Illustration", "Spot UV & Foil Prep", "Series Branding"]),

        ("Exhibition & Booth Designer", "Creates trade show displays, experiential retail pop-ups, and interactive exhibition spaces.", [
            ("Spatial Flow & Trade Show Booth Planning", "critical", ["booth design", "exhibition design", "trade show", "foot traffic"]),
            ("3D Modeling & Rendering (SketchUp / 3ds Max)", "critical", ["sketchup", "3ds max", "booth renders", "materials"]),
            ("Large Format Graphic Panels & Backdrop Specs", "high", ["large format graphics", "trade show banners", "print specs"]),
            ("Lighting, AV Integration & Truss Systems", "high", ["booth lighting", "truss systems", "video walls"]),
            ("Modular Fabrication & Assembly Logistics", "high", ["modular systems", "fabrication", "knockdown display"])
        ], ["Interactive Kiosks", "Brand Experience Staging", "Electrical Layouts"]),

        ("Set & Prop Designer", "Conceives physical movie, theater, and television set environments and period props.", [
            ("Set Drafting, Elevations & Floor Plans", "critical", ["set design", "elevations", "floor plans", "scenic drafting"]),
            ("Period Research, Texture & Scenic Painting", "critical", ["period accuracy", "scenic art", "aging techniques", "materials"]),
            ("Prop Fabrication & Material Sourcing", "high", ["prop making", "fabrication", "casting", "3d printing"]),
            ("Camera Angle Awareness & Lighting Practicalities", "high", ["camera sightlines", "wild walls", "lighting access"]),
            ("Set Construction Budgeting & Safety", "high", ["construction materials", "stage safety", "breakaway props"])
        ], ["Scale Model Making", "Theatrical Fly Systems", "Costume Integration"]),

        ("Colorist (Photo/Print)", "Calibrates tonal curves, skin tones, and color reproduction across photographic shoots.", [
            ("Color Grading Software (Photoshop, Capture One)", "critical", ["capture one", "photoshop", "color grading", "curves"]),
            ("Monitor Calibration & Color Management (ICC Profiles)", "critical", ["icc profiles", "monitor calibration", "colorimeter", "x-rite"]),
            ("Advanced Skin Tone Neutralization & Retouching", "high", ["skin tones", "color balance", "frequency separation"]),
            ("Mood Tone Mapping & Look Development", "high", ["look creation", "lut development", "color harmonies"]),
            ("Print Proofing & Soft Proofing Validation", "high", ["soft proofing", "gamut check", "fine art printing"])
        ], ["Film Emulation", "Batch Matching", "High-Volume Catalog Work"])
    ],

    "Video, Audio & Multimedia Production": [
        ("Video Editor (Long-Form / Documentary)", "Edits narrative pacing, interviews, and multi-track timelines for feature formats.", [
            ("NLE Software (Premiere Pro / DaVinci Resolve / Final Cut)", "critical", ["premiere pro", "davinci resolve", "final cut pro", "video editing"]),
            ("Narrative Pacing, Story Structure & A/B Roll", "critical", ["story structure", "b-roll", "pacing", "assembly cut"]),
            ("Audio Track Mixing & Dialogue Cleaning", "high", ["audio cleaning", "dialogue leveling", "eq", "noise reduction"]),
            ("Basic Color Correction & Shot Matching", "high", ["color correction", "shot matching", "lumetri"]),
            ("Export Settings, Codecs & Archival Workflows", "high", ["codecs", "prores", "h.264", "bitrates", "project archiving"])
        ], ["Multicam Editing", "Proxy Workflows", "Subtitle Timing"]),

        ("Short-Form Video Editor (Reels/Shorts/TikTok)", "Edits fast-paced viral mobile video content with captions and kinetic rhythm.", [
            ("Fast-Paced Mobile Editing (Premiere / CapCut)", "critical", ["capcut", "premiere pro", "short form", "reels", "tiktok"]),
            ("Hook Creation & Retention Pacing", "critical", ["hook", "retention rate", "pacing", "jump cuts"]),
            ("Dynamic Kinetic Subtitles & Typography", "high", ["kinetic captions", "animated subtitles", "emojis"]),
            ("Sound Effects & Audio Trend Syncing", "high", ["sound design", "sfx", "tiktok trends", "audio sync"]),
            ("Motion Tracking, Zoom Ins & Visual Hooks", "high", ["motion tracking", "keyframing", "speed ramps", "b-roll overlays"])
        ], ["A/B Thumbnail Frames", "Viral Formats", "After Effects Micro-Transitions"]),

        ("YouTube Channel Producer", "Directs editorial calendars, titles, thumbnails, workflows, and channel analytics.", [
            ("YouTube Analytics & Retention Auditing", "critical", ["youtube studio", "retention graph", "ctr", "analytics", "audience"]),
            ("Packaging Strategy (Title & Thumbnail Synergy)", "critical", ["title optimization", "packaging", "curiosity hook"]),
            ("Video Script Breakdown & Shooting Direction", "high", ["scripting", "b-roll planning", "production coordination"]),
            ("Workflow Management & Team Delegation (Editors, Designers)", "high", ["trello", "notion", "production pipeline", "deadlines"]),
            ("Sponsorship & Mid-Roll Ad Placements", "high", ["sponsor integration", "ad placement", "brand deals"])
        ], ["Community Tab Strategy", "Merch Shelf", "YouTube SEO"]),

        ("Cinematographer / Camera Operator", "Operates camera systems, lenses, stabilizers, and lighting gear for cinematic shots.", [
            ("Cinema Camera Operation (Sony FX, RED, Blackmagic)", "critical", ["camera operation", "exposure", "cinema cameras", "shutter angle"]),
            ("Lens Selection, Depth of Field & Focus Pulling", "critical", ["lenses", "focal length", "depth of field", "focus pulling"]),
            ("Gimbal, Dolly & Handheld Camera Movement", "high", ["gimbal", "ronin", "dolly", "camera movement", "tripod"]),
            ("Log Color Profiles (S-Log, C-Log, ProRes)", "high", ["log profile", "white balance", "histogram", "false color"]),
            ("Camera Rigging, Audio Feeds & Monitors", "high", ["cage rigging", "wireless video", "matte box", "timecode"])
        ], ["Anamorphic Lenses", "Drone Cinematography", "High-Speed Cameras"]),

        ("Drone Pilot & Aerial Videographer", "Pilots UAVs safely to capture high-altitude cinematic footage and surveys.", [
            ("Drone Flight Operations (DJI Enterprise/Mavic)", "critical", ["drone piloting", "dji", "flight control", "uav"]),
            ("Airspace Regulations & FAA Part 107 Compliance", "critical", ["part 107", "airspace authorization", "faa regulations", "safety"]),
            ("Cinematic Aerial Flight Movements", "high", ["cinematic moves", "orbit", "reveal shot", "smooth flight"]),
            ("ND Filters & Exposure Management", "high", ["nd filters", "polarizers", "aerial exposure", "d-log"]),
            ("Emergency Procedures & Weather Assessment", "high", ["weather assessment", "failsafe rth", "battery management"])
        ], ["FPV Drone Piloting", "Aerial Mapping / Photogrammetry", "Night Flight Waivers"]),

        ("Video Colorist (DaVinci Resolve)", "Grades cinematic films, balances exposure, and creates distinct aesthetic looks.", [
            ("DaVinci Resolve Color Page Mastery", "critical", ["davinci resolve", "color grading", "node tree", "colorist"]),
            ("Scopes Analysis (Waveform, Vectorscope, Parade)", "critical", ["waveform", "vectorscope", "parade", "false color"]),
            ("Color Management (ACES, DaVinci YRGB Color Managed)", "high", ["aces", "color management", "color space transform"]),
            ("Shot Matching & Secondary Color Corrections", "high", ["shot matching", "qualifiers", "power windows", "skin tones"]),
            ("Look Development & Show LUT Creation", "high", ["look development", "film look", "lut creation", "halation"])
        ], ["HDR Grading (Dolby Vision)", "Color Control Surfaces", "Conform Workflows"]),

        ("VFX (Visual Effects) Compositor", "Blends CGI, live-action footage, matte paintings, and pyrotechnics seamlessly.", [
            ("Node-Based Compositing (Nuke / Fusion / After Effects)", "critical", ["nuke", "fusion", "after effects", "compositing"]),
            ("Rotoscoping & Paint Clean-Up", "critical", ["rotoscoping", "paint cleanup", "wire removal", "clean plate"]),
            ("Green Screen & Blue Screen Keying", "high", ["chroma key", "spill suppression", "edge blending", "primatte"]),
            ("3D Camera Tracking & Matchmoving", "high", ["camera tracking", "matchmoving", "point tracking", "planar tracking"]),
            ("Lighting Matching, Grain & Lens Distortion", "high", ["color matching", "film grain", "lens distortion", "depth of field"])
        ], ["Deep Compositing", "CG Multipass Compositing", "Matte Painting"]),

        ("Sound Designer", "Synthesizes custom sound effects, cinematic ambiences, and audio environments.", [
            ("DAW Software (Pro Tools / Ableton Live / Reaper)", "critical", ["pro tools", "ableton", "reaper", "daw", "sound design"]),
            ("Synthesizing SFX & Audio Manipulation", "critical", ["synthesizers", "pitch shifting", "audio effects", "sfx creation"]),
            ("Foley, Ambience & Layering Techniques", "high", ["foley", "room tone", "ambience", "audio layering"]),
            ("Audio Restoration (iZotope RX)", "high", ["izotope rx", "spectral repair", "noise reduction", "de-click"]),
            ("Syncing Sound to Picture with Frame Accuracy", "high", ["audio sync", "sync to picture", "spotting sessions"])
        ], ["Wwise / FMOD for Games", "Spatial Audio / Dolby Atmos", "Field Recording"]),

        ("Audio Mixing & Mastering Engineer", "Balances multi-track audio recordings into balanced, release-ready masters.", [
            ("Gain Staging & Multi-Track Leveling", "critical", ["gain staging", "audio mixing", "headroom", "fader balance"]),
            ("Parametric EQ & Dynamic Frequency Carving", "critical", ["parametric eq", "eq curves", "frequency masking", "high-pass"]),
            ("Compression & Dynamic Control (VCA, FET, Opto)", "high", ["compression", "multiband", "sidechain", "limiter"]),
            ("Spatial Reverbs, Delays & Stereo Imaging", "high", ["reverb", "delay", "stereo widening", "panning"]),
            ("Mastering Loudness Standards (LUFS, True Peak)", "high", ["mastering", "lufs", "true peak", "dithering", "streaming delivery"])
        ], ["Analog Hardware Outboard", "Stem Mastering", "Dolby Atmos Music"]),

        ("Podcast Producer & Editor", "Oversees recording sessions, audio cleaning, narrative pacing, and episode hosting.", [
            ("Podcast Audio Editing (Descript, Audition, Audacity)", "critical", ["descript", "adobe audition", "audacity", "podcast editing"]),
            ("Dialogue Editing (Umms, Gaps, Pacing)", "critical", ["dialogue editing", "filler words", "pacing", "breath control"]),
            ("Mic Technique, Gain & Room Acoustic Setup", "high", ["microphone selection", "shure sm7b", "audio interface", "acoustics"]),
            ("Show Notes, Chapter Markers & ID3 Metadata", "high", ["show notes", "chapter markers", "id3 tags", "transcripts"]),
            ("Podcast Hosting & RSS Distribution (Spotify, Apple)", "high", ["rss feed", "libsyn", "transistor", "distribution"])
        ], ["Video Podcast Setup", "Guest Prep & Interviewing", "Sponsorship Insertion"]),

        ("Voiceover Artist", "Delivers vocal performances for commercials, narration, animations, and audiobooks.", [
            ("Vocal Delivery, Diction & Tone Modulation", "critical", ["voiceover", "voice acting", "diction", "pacing", "inflection"]),
            ("Home Studio Acoustic Treatment & Sound Booth", "critical", ["acoustic treatment", "sound booth", "noise floor", "pop filter"]),
            ("Microphone Technique & Mic Proximity", "high", ["condenser microphone", "proximity effect", "mic technique"]),
            ("Audio Editing & Punch-and-Roll Recording", "high", ["punch and roll", "reaper", "audacity", "breath editing"]),
            ("Script Cold Reading & Character Development", "high", ["cold reading", "character voices", "commercial reads"])
        ], ["Audiobook Mastering Standards (ACX)", "Dialects and Accents", "Live Directed Sessions (Source-Connect)"]),

        ("Foley Artist", "Performs physical sound effects synchronized live to film projections in studio.", [
            ("Physical Prop Performance & Timing", "critical", ["foley", "prop performance", "sync to picture", "timing"]),
            ("Footsteps Performance Across Diverse Surfaces", "critical", ["footstep foley", "shoe types", "foley pit", "surfaces"]),
            ("Microphone Placement & Preamps for Delicate Sounds", "high", ["mic placement", "shotgun mics", "low noise preamps"]),
            ("Cloth Rustle & Texture Manipulation", "high", ["cloth movement", "garment rustle", "textures"]),
            ("Foley Studio Organization & Prop Sourcing", "high", ["prop sourcing", "foley studio", "materials"])
        ], ["Outdoor Foley Recording", "DAW Recording Track Layouts"]),

        ("Live Stream & Broadcast Technician", "Manages video switchers, multi-camera feeds, and RTMP encoders for live broadcasts.", [
            ("Live Video Switching (ATEM / vMix / OBS Studio)", "critical", ["obs studio", "vmix", "atem mini", "video switcher", "live streaming"]),
            ("Streaming Protocols (RTMP, SRT, NDI)", "critical", ["rtmp", "srt", "ndi", "bitrate", "encoding"]),
            ("Audio Mixer & Multi-Mic Setup for Live", "high", ["digital mixer", "behringer x32", "wireless lavaliers", "audio sync"]),
            ("Network Bandwidth Bonding & Backup Streams", "high", ["bandwidth management", "network bonding", "redundancy"]),
            ("Lower Thirds, Graphics Overlays & Stinger Transitions", "high", ["lower thirds", "graphics", "stinger transitions", "scoreboards"])
        ], ["Satellite / Cellular Bonding (LiveU)", "Broadcast Engineering", "PTZ Camera Control"]),

        ("Lighting Technician (Gaffer)", "Designs and shapes light on set using fixtures, diffusion, flags, and color gels.", [
            ("Lighting Fixtures (LED, HMI, Tungsten, RGB)", "critical", ["gaffer", "lighting", "aputure", "arri", "cinematography lighting"]),
            ("Light Shaping (Diffusion, Flags, Scrims, Grids)", "critical", ["c-stands", "diffusion", "flags", "softboxes", "light shaping"]),
            ("3-Point Lighting & Key-to-Fill Ratios", "high", ["key light", "fill light", "backlight", "contrast ratios"]),
            ("Color Temperature (Kelvin) & Green/Magenta Tint", "high", ["color temperature", "kelvin", "cri", "gels", "rgb control"]),
            ("Electrical Power Distribution & On-Set Safety", "high", ["power distribution", "amperage", "cable runs", "set safety"])
        ], ["DMX & Wireless Lighting (Sidus Link)", "Day-for-Night Techniques", "Generator Operation"]),

        ("Commercial Photographer", "Photographs campaigns, models, and advertising concepts for corporate brands.", [
            ("Commercial Studio Lighting (Strobe & Flash)", "critical", ["studio lighting", "strobes", "profoto", "softboxes", "lighting ratios"]),
            ("Professional Camera Systems (Full Frame & Medium Format)", "critical", ["camera settings", "full frame", "shutter speed", "aperture", "iso"]),
            ("Tethered Shooting (Capture One)", "high", ["tethered shooting", "capture one", "live client review"]),
            ("Commercial Creative Direction & Moodboards", "high", ["art direction", "moodboards", "call sheets", "location scouting"]),
            ("High-End Retouching Coordination", "high", ["retouching", "color grading", "compositing"])
        ], ["Commercial Licensing Contracts", "Model Casting", "Location Scouting"]),

        ("Product & E-Commerce Photographer", "Captures crisp catalog imagery, 360 spins, and lifestyle shots of physical products.", [
            ("Reflective Surface Lighting (Jewelry, Glass, Metal)", "critical", ["product photography", "reflective surfaces", "light tent", "polarizers"]),
            ("Seamless White Background & Shadow Consistency", "critical", ["pure white background", "clipping path", "shadows", "infinity cove"]),
            ("Focus Stacking for Crisp Product Sharpness", "high", ["focus stacking", "macro lens", "helicon focus", "sharpness"]),
            ("Color Accuracy & Product Fidelity", "high", ["color checker", "color accuracy", "white balance"]),
            ("Batch Shooting Workflows & Metadata Management", "high", ["batch processing", "file naming", "cataloging"])
        ], ["360 Degree Turntable Photography", "Stop Motion Animations", "Props Styling"]),

        ("Event & Wedding Photographer", "Photographs dynamic emotional milestones, low-light receptions, and fast-moving events.", [
            ("Fast Run-and-Gun Camera Handling in Variable Light", "critical", ["event photography", "low light", "fast autofocus", "iso management"]),
            ("On-Camera & Off-Camera Bounce Flash", "critical", ["speedlights", "bounce flash", "ttl", "diffusers"]),
            ("Candid Human Interaction & Shot List Execution", "high", ["candid photography", "shot list", "timeline management"]),
            ("High-Volume Batch Culling & Lightroom Editing", "high", ["lightroom", "photo culling", "batch editing", "presets"]),
            ("Client Gallery Delivery & Print Album Design", "high", ["gallery delivery", "pixieset", "print albums", "backup redundant cards"])
        ], ["Dual Card Slot Security", "Wedding Day Scheduling", "Posing Direction"]),

        ("Photo Retoucher & Photo Restorer", "Cleans blemishes, reconstructs vintage damaged photos, and retouches high-fashion skin.", [
            ("High-End Frequency Separation & Dodge & Burn", "critical", ["frequency separation", "dodge and burn", "skin texture", "photoshop"]),
            ("Photo Restoration & Tear / Scratch Removal", "critical", ["photo restoration", "clone stamp", "healing brush", "scratch removal"]),
            ("Color Reconstruction & Vintage Tinting", "high", ["colorization", "vintage photos", "faded ink recovery"]),
            ("Body Reshaping, Liquify & Silhouette Polish", "high", ["liquify", "silhouette", "stray hairs removal"]),
            ("Masking, Clipping Paths & Background Compositing", "high", ["pen tool", "layer masking", "background replacement"])
        ], ["AI Assisted Inpainting Tools", "High-Volume Fashion Retouching", "Print Color Proofing"]),

        ("Music Producer / Beatmaker", "Produces instrumentals, arranges song structures, and programs melodic hooks.", [
            ("DAW Workflow (FL Studio / Ableton / Logic Pro)", "critical", ["fl studio", "ableton live", "logic pro", "music production"]),
            ("Music Theory (Scales, Chord Progressions, Basslines)", "critical", ["chord progressions", "music theory", "melody", "chords"]),
            ("Drum Programming, 808s & Groove Quantization", "high", ["drum programming", "808s", "groove", "swing", "quantization"]),
            ("VST Instruments, Plugins & Audio Sampling", "high", ["vst", "serum", "omnisphere", "sampling", "sample flipping"]),
            ("Song Arrangement & Pre-Mix Leveling", "high", ["arrangement", "transitions", "pre-mixing", "instrumentation"])
        ], ["Beat Licensing & Type Beat SEO", "Vocal Production", "MIDI Keyboards"]),

        ("Session Musician", "Records professional instrumental tracks for producers, bands, and studio sessions.", [
            ("Instrument Mastery (Guitar / Bass / Keys / Drums)", "critical", ["instrument performance", "guitar", "piano", "drums", "sight reading"]),
            ("Playing to a Metronome / Click Track", "critical", ["click track", "timing", "groove", "rhythm"]),
            ("Improvisation & Genre Adaptability", "high", ["improvisation", "genre adaptability", "solos", "tone crafting"]),
            ("Studio Instrument Mic Placement & Tone Settings", "high", ["tone dialing", "pedals", "amplifiers", "mic placement"]),
            ("Direct Injection (DI) & Recording Audio Interfaces", "high", ["di box", "audio interface", "daw recording"])
        ], ["Remote Session File Delivery", "Sheet Music Sight Reading", "Arrangement Harmonization"]),

        ("Audiobook Narrator & Producer", "Performs long-form book narration, voice acting, and formats master files for ACX.", [
            ("Long-Form Narration Stamina & Character Accents", "critical", ["narration", "audiobook", "character voices", "pacing", "stamina"]),
            ("ACX Technical Standards Compliance (RMS, Peak)", "critical", ["acx standards", "rms levels", "peak levels", "-60db noise floor"]),
            ("Punch-and-Roll Recording & Flub Editing", "high", ["punch and roll", "error editing", "room tone matching"]),
            ("Mouth Click & Breath Control Processing", "high", ["breath reduction", "de-click", "de-esser", "eq"]),
            ("Mastering & Chapter File Organization", "high", ["chapter splitting", "id3 tags", "audible submission"])
        ], ["Dialect Research", "Voice Preservation Techniques", "Directing Home Studio Sessions"]),

        ("Subtitle & Closed-Captioning Specialist", "Generates timed caption files (SRT, VTT) adhering to accessibility standards.", [
            ("Time-Synced Captions (SRT, VTT, SCC)", "critical", ["srt", "vtt", "caption timing", "subtitle synchronization"]),
            ("Transcription Accuracy & Punctuation Nuance", "critical", ["transcription", "grammar", "phonetic spelling", "homophones"]),
            ("Caption Standards (Reading Speed, Line Breaks)", "high", ["reading speed", "cps", "line limits", "caption guidelines"]),
            ("Non-Speech Sound Identification (SFX, Music Cues)", "high", ["sound description", "music cues", "speaker identification"]),
            ("Translation & Subtitle Burn-In Workflows", "high", ["hardcoding subtitles", "subtitle burn-in", "multilingual subs"])
        ], ["Automated Captioning AI Clean-Up", "Broadcast Closed-Captioning Compliance"]),

        ("Dubbing & ADR Technician", "Records and synchronizes replacement dialogue for foreign films and on-set audio fixes.", [
            ("Automated Dialogue Replacement (ADR) Setup", "critical", ["adr", "dialogue replacement", "lip sync", "beeps"]),
            ("Audio-to-Lip-Movement Synchronization", "critical", ["lip sync", "timing", "rhythm matching"]),
            ("Matching On-Set Acoustic Ambience & Reverbs", "high", ["reverb matching", "eq matching", "mic placement matching"]),
            ("Actor Direction & Voice Guidance", "high", ["voice direction", "pacing", "energy matching"]),
            ("Dialogue Editing & Clean Edits", "high", ["dialogue editing", "crossfades", "noise reduction"])
        ], ["Foreign Language Dubbing Pipelines", "Source-Connect Remote ADR"]),

        ("AV (Audio-Visual) Systems Installer", "Mounts, connects, and programs presentation hardware in corporate and venue spaces.", [
            ("Commercial Display & Projector Installation", "critical", ["projector mounts", "commercial displays", "video walls", "av installation"]),
            ("Cable Pulling & Termination (HDMI, HDBaseT, Cat6)", "critical", ["cable termination", "hdbaset", "hdmi extenders", "crimping"]),
            ("Audio Amplifiers, Ceiling Speakers & Microphones", "high", ["ceiling speakers", "70v audio", "wireless mics", "dsp"]),
            ("Control Systems Setup (Crestron, Extron)", "high", ["crestron", "extron", "control panels", "touchscreens"]),
            ("Rack Building & System Commissioning", "high", ["av rack", "wire lacing", "testing", "signal flow"])
        ], ["Video Conferencing Integration (Zoom Rooms / Teams)", "Acoustic Room Tuning"]),

        ("Virtual Event Technical Director", "Operates live streaming switches, attendee feeds, remote speakers, and Q&A panels.", [
            ("Virtual Platforms (Zoom Events, Hopin, Teams Live)", "critical", ["zoom events", "hopin", "virtual events", "teams live"]),
            ("Remote Speaker Green Room & Tech Checks", "critical", ["tech check", "audio/video checks", "speaker coordination"]),
            ("Switching Video Feeds & Screen Sharing Runs", "high", ["slide switching", "obs", "vmix", "broadcast runs"]),
            ("Q&A, Polling & Engagement Tool Orchestration", "high", ["slido", "mentimeter", "chat moderation", "polling"]),
            ("Live Trouble Mitigation & Backup Feeds", "high", ["redundant connections", "contingency plans", "recording backup"])
        ], ["Simulive Broadcast Execution", "Post-Event Video Cutdowns"])
    ],

    "Digital Marketing, Growth & Content": [
        ("SEO (Search Engine Optimization) Specialist", "Drives organic search traffic through keyword research, on-page optimization, and links.", [
            ("Keyword Research & Search Intent Mapping", "critical", ["keyword research", "search intent", "semrush", "ahrefs"]),
            ("On-Page SEO (Meta Tags, Headers, Content Optimization)", "critical", ["on-page seo", "meta tags", "h1-h6", "internal linking"]),
            ("Link Building & Digital PR Strategies", "high", ["backlinks", "link building", "outreach", "domain authority"]),
            ("Google Search Console & Organic Performance", "high", ["google search console", "impressions", "rank tracking"]),
            ("Content Strategy for Organic Rankings", "high", ["content briefs", "topic clusters", "pillar pages"])
        ], ["Schema Markup", "Local SEO", "AI Content Optimization"]),

        ("Technical SEO Auditor", "Optimizes crawl budgets, XML sitemaps, indexation, schema architecture, and site speed.", [
            ("Crawl Analysis & Auditing (Screaming Frog)", "critical", ["screaming frog", "site crawl", "technical seo", "crawl budget"]),
            ("Robots.txt, Canonical Tags & Indexation", "critical", ["robots.txt", "canonical tags", "noindex", "sitemaps", "status codes"]),
            ("Structured Data & Schema.org JSON-LD", "high", ["schema markup", "json-ld", "rich snippets", "structured data"]),
            ("Core Web Vitals & Technical Speed Diagnostics", "high", ["core web vitals", "lighthouse", "javascript rendering"]),
            ("Site Migration & 301 Redirect Mapping", "high", ["301 redirects", "site migration", "broken link fixes"])
        ], ["Log File Analysis", "International SEO (Hreflang)", "Headless CMS SEO"]),

        ("PPC / Paid Search Specialist (Google Ads)", "Builds, manages, and optimizes profitable Google search and shopping campaigns.", [
            ("Google Ads Campaign Architecture & Bidding", "critical", ["google ads", "search ads", "bidding strategies", "cpc", "roas"]),
            ("Keyword Match Types & Negative Keyword Lists", "critical", ["exact match", "phrase match", "negative keywords", "search terms"]),
            ("Ad Copywriting & Responsive Search Ads (RSA)", "high", ["ad copy", "responsive search ads", "ad extensions"]),
            ("Conversion Tracking & Google Tag Manager", "high", ["conversion tracking", "gtm", "offline conversions"]),
            ("Landing Page Alignment & Quality Score Optimization", "high", ["quality score", "landing page relevance", "ctr"])
        ], ["Google Shopping / Performance Max", "Remarketing Campaigns", "A/B Copy Testing"]),

        ("Paid Social Media Buyer (Meta/TikTok/LinkedIn)", "Scales paid acquisition on Facebook, Instagram, TikTok, and B2B LinkedIn.", [
            ("Meta Ads Manager / TikTok Ads Manager", "critical", ["meta ads", "facebook ads", "tiktok ads", "ads manager"]),
            ("Audience Targeting, Lookalikes & Retargeting", "critical", ["lookalike audiences", "custom audiences", "retargeting", "pixel"]),
            ("Creative Testing Frameworks & Ad Fatigue Cycling", "high", ["creative testing", "ad fatigue", "hooks", "ugc creatives"]),
            ("Metrics Analysis (CPA, ROAS, CPM, Thumb-Stop Rate)", "high", ["roas", "cpa", "cpm", "ctr", "thumb-stop rate"]),
            ("Conversion API (CAPI) & Privacy Attribution", "high", ["conversions api", "capi", "ios 14 tracking", "attribution"])
        ], ["LinkedIn Campaign Manager", "Budget Scaling Tactics", "UGC Sourcing"]),

        ("Conversion Rate Optimization (CRO) Specialist", "Conducts A/B experiments to boost landing page and checkout conversion percentages.", [
            ("A/B Testing Methodologies & Significance", "critical", ["a/b testing", "split testing", "statistical significance", "vwo", "optimizely"]),
            ("Heatmaps & User Session Recordings (Hotjar, Clarity)", "critical", ["hotjar", "microsoft clarity", "heatmaps", "session recordings"]),
            ("Landing Page Heuristic Audits & UX Friction Identification", "high", ["heuristic evaluation", "friction points", "funnel analysis"]),
            ("Copy & Value Proposition Optimization", "high", ["copywriting", "value proposition", "call to action"]),
            ("Form & Checkout Drop-Off Remediation", "high", ["checkout optimization", "form friction", "cart abandonment"])
        ], ["Personalization Strategies", "Mobile CRO", "Wireframing Fixes"]),

        ("Email Marketing & Lifecycle Automation Specialist", "Builds automated welcome series, nurture funnels, and retention newsletters.", [
            ("Email Platforms (Klaviyo, Mailchimp, ActiveCampaign)", "critical", ["klaviyo", "mailchimp", "activecampaign", "email marketing"]),
            ("Lifecycle Automations (Welcome, Abandoned Cart, Win-Back)", "critical", ["email flows", "abandoned cart", "welcome series", "lifecycle"]),
            ("List Segmentation & Audience Hygiene", "high", ["segmentation", "list cleaning", "unengaged subscribers"]),
            ("Deliverability, SPF, DKIM & DMARC Protocols", "high", ["email deliverability", "spf", "dkim", "dmarc", "bounce rate"]),
            ("A/B Testing Subject Lines & Open/Click Metrics", "high", ["subject lines", "open rate", "ctr", "a/b testing"])
        ], ["HTML Email Coding", "SMS Marketing Integration", "Predictive Analytics"]),

        ("Direct-Response Copywriter", "Writes sales pages, VSLs, emails, and ads engineered to trigger immediate purchase action.", [
            ("Direct-Response Principles & Psychological Triggers", "critical", ["direct response", "copywriting", "scarcity", "urgency", "social proof"]),
            ("Long-Form Sales Letters & Landing Page Copy", "critical", ["sales pages", "long-form copy", "vsl", "lead capture"]),
            ("Headlines, Hooks & Fascination Bullets", "high", ["headlines", "hooks", "bullet points", "fascinations"]),
            ("Customer Research & Voice-of-Customer Mining", "high", ["voice of customer", "review mining", "avatar research"]),
            ("Offer Structuring & Guarantee Framing", "high", ["irresistible offer", "bonuses", "guarantees", "risk reversal"])
        ], ["Email Sequence Copy", "Ad Scriptwriting", "Conversion Audits"]),

        ("Technical Writer", "Authorizes developer documentation, API guides, architecture overviews, and tutorials.", [
            ("Developer Documentation & API References", "critical", ["technical writing", "api documentation", "developer guides", "swagger"]),
            ("Docs-as-Code Workflows (Markdown, Git, Static Site Generators)", "critical", ["markdown", "git", "docusaurus", "docs as code"]),
            ("Information Architecture & Complex Topic Simplification", "high", ["information architecture", "clarity", "diagramming"]),
            ("Code Samples & SDK Verification", "high", ["code samples", "curl", "python examples", "sdk testing"]),
            ("Style Guides & Editorial Consistency (Google/Microsoft Style)", "high", ["style guides", "editorial standards", "grammar"])
        ], ["Release Notes Automation", "Interactive API Playgrounds", "Video Documentation"]),

        ("UX Writer / Microcopy Specialist", "Writes intuitive button labels, error states, onboarding flows, and product copy.", [
            ("Microcopy (Button CTAs, Error Messages, Empty States)", "critical", ["microcopy", "ux writing", "button copy", "error states"]),
            ("Product Onboarding & Progressive Disclosure", "critical", ["onboarding", "walkthroughs", "tooltips", "progressive disclosure"]),
            ("Brand Voice & Product Tone Frameworks", "high", ["brand voice", "product tone", "content guidelines"]),
            ("Figma Collaborative Design Integration", "high", ["figma", "content design", "component text"]),
            ("Usability & Comprehension Testing for Copy", "high", ["copy testing", "comprehension", "user feedback"])
        ], ["Localization Preparation", "Accessibility Screen Reader Copy", "Design Systems Copy Rules"]),

        ("Content Strategist", "Maps brand content pillars, customer journey touchpoints, and omnichannel themes.", [
            ("Content Audit & Gap Analysis", "critical", ["content strategy", "content audit", "gap analysis", "content pillars"]),
            ("Customer Journey Content Mapping", "critical", ["buyer journey", "awareness", "consideration", "decision stage"]),
            ("Editorial Calendar Governance", "high", ["editorial calendar", "workflow", "deadlines", "publishing cadence"]),
            ("Brand Messaging Architecture & Tone Guidelines", "high", ["messaging hierarchy", "tone of voice", "brand positioning"]),
            ("Content KPI Measurement & ROI Reporting", "high", ["content analytics", "roi", "engagement metrics", "traffic attribution"])
        ], ["Repurposing Frameworks", "Thought Leadership Strategy", "Content Ops Tools"]),

        ("Ghostwriter (Books/Thought Leadership)", "Writes memoirs, business books, and executive LinkedIn thought leadership in the client's voice.", [
            ("Interviewing Executives & Voice Emulation", "critical", ["ghostwriting", "interviewing", "voice matching", "tone emulation"]),
            ("Book Outlining, Chapter Architecture & Pacing", "critical", ["book outline", "table of contents", "chapter structure"]),
            ("Deep Research & Narrative Non-Fiction Storytelling", "high", ["research", "storytelling", "case studies", "anecdotes"]),
            ("LinkedIn Thought Leadership & Executive Essays", "high", ["thought leadership", "executive posts", "op-eds", "articles"]),
            ("Manuscript Revisions & Editorial Turnaround", "high", ["manuscript editing", "revisions", "pacing", "publishing prep"])
        ], ["Publishing Proposal Writing", "Ghostwriting Contracts", "Keynote Scriptwriting"]),

        ("Scriptwriter (YouTube/Commercials/Podcasts)", "Writes hooks, pacing, visual cues, and narratives for screen and audio.", [
            ("YouTube Video Scripting & Retention Hooks", "critical", ["youtube scriptwriting", "hooks", "visual cues", "pacing", "retention"]),
            ("Commercial Storyboard Scripts (Audio/Video Split)", "critical", ["commercial script", "two-column script", "voiceover cues"]),
            ("Character Dialogue & Authentic Conversational Voice", "high", ["dialogue", "conversational tone", "authenticity"]),
            ("Narrative Arcs & Story Frameworks (Hero's Journey)", "high", ["story arcs", "three-act structure", "tension", "payoff"]),
            ("Researching Topics & Fact-Checking Assertions", "high", ["research", "fact-checking", "citing sources"])
        ], ["Humor & Comedy Timing", "Educational Explainers", "Documentary Scripting"]),

        ("Social Media Manager", "Builds organic audience engagement, publishes content, and tracks engagement metrics.", [
            ("Social Platform Algorithms (Instagram, X, LinkedIn, TikTok)", "critical", ["social media management", "algorithms", "instagram", "linkedin", "tiktok"]),
            ("Content Creation, Caption Writing & Asset Assembly", "critical", ["caption writing", "canva", "creative design", "scheduling"]),
            ("Publishing Platforms (Buffer, Hootsuite, Later)", "high", ["scheduling tools", "buffer", "later", "sprout social"]),
            ("Community Engagement & Direct Message Management", "high", ["community engagement", "comment replies", "reputation management"]),
            ("Analytics Tracking & Monthly Performance Audits", "high", ["engagement rate", "follower growth", "reach", "impressions"])
        ], ["Crisis Communications", "Trend Jacking", "Influencer Collaborations"]),

        ("Community Manager (Discord/Circle/Slack)", "Cultivates thriving, safe, and active brand membership communities.", [
            ("Community Platforms (Discord, Circle, Slack)", "critical", ["discord", "circle.so", "slack", "community management"]),
            ("Member Onboarding, Roles & Welcome Sequences", "critical", ["member onboarding", "roles", "permissions", "welcome flows"]),
            ("Moderation Guidelines, Bot Configuration & Safety", "high", ["moderation", "automod", "community safety", "bots"]),
            ("Virtual Events, AMAs & Member Activation", "high", ["amas", "community events", "challenges", "rituals"]),
            ("Community Health Metrics (DAU, Retention, Sentiment)", "high", ["community metrics", "engagement", "sentiment analysis"])
        ], ["Super-User Programs", "Web3 Community Management", "Crisis De-escalation"]),

        ("Influencer Marketing Coordinator", "Identifies, negotiates, and coordinates sponsored campaigns with online creators.", [
            ("Influencer Discovery & Audience Vetting", "critical", ["influencer marketing", "creator discovery", "fake follower vetting", "engagement rate"]),
            ("Contract Negotiation, Deliverables & Usage Rights", "critical", ["contract negotiation", "usage rights", "deliverables", "pricing"]),
            ("Creative Briefs & Campaign Execution", "high", ["creative briefs", "talking points", "compliance guidelines"]),
            ("FTC Ad Disclosure & Legal Compliance", "high", ["ftc compliance", "ad disclosure", "sponsored guidelines"]),
            ("Campaign ROI Tracking (UTMs, Promo Codes)", "high", ["promo codes", "utm links", "influencer roas", "attribution"])
        ], ["Micro-Influencer Gifting", "Creator Relationship Management Platforms (Aspire/Grin)"]),

        ("Affiliate Marketing Manager", "Recruits partners, structures commission models, and tracks affiliate revenue networks.", [
            ("Affiliate Networks (Impact, ShareASale, CJ)", "critical", ["affiliate marketing", "impact.com", "shareasale", "cj affiliate"]),
            ("Partner Recruitment & Relationship Building", "critical", ["partner outreach", "publisher recruitment", "relationship management"]),
            ("Commission Tiers, Terms & Fraud Prevention", "high", ["commission structures", "affiliate terms", "cookie windows", "fraud detection"]),
            ("Promotional Asset Delivery & Newsletter Updates", "high", ["banners", "copy snippets", "partner communication"]),
            ("Tracking Pixel Verification & Conversion Reporting", "high", ["pixel tracking", "sub-id tracking", "epc", "revenue reporting"])
        ], ["Co-Marketing Bundles", "Brand Ambassador Programs"]),

        ("App Store Optimization (ASO) Specialist", "Improves organic mobile discovery and keyword ranking on Apple App Store & Google Play.", [
            ("App Title, Subtitle & Keyword Field Architecture", "critical", ["aso", "app store optimization", "keyword rankings", "app store"]),
            ("App Icon & Screenshot Conversion Rate Testing", "critical", ["screenshot optimization", "app icon", "custom product pages", "a/b testing"]),
            ("Apple App Store vs Google Play Ranking Signals", "high", ["google play console", "apple app store", "app indexing"]),
            ("Ratings & Reviews Sentiment Strategy", "high", ["app ratings", "review management", "in-app prompt timing"]),
            ("Localization for Global App Stores", "high", ["app store localization", "keyword translation", "cultural adaptation"])
        ], ["Search Ads (Apple Search Ads)", "Competitor ASO Monitoring (AppTweak)"]),

        ("E-Commerce Marketplace Manager (Amazon/Flipkart)", "Optimizes product listings, Buy Box share, inventory, and PPC on marketplaces.", [
            ("Amazon Seller Central / Flipkart Operations", "critical", ["amazon seller central", "flipkart", "marketplace management", "buy box"]),
            ("Listing Optimization (Title, Bullets, A+ Content)", "critical", ["a+ content", "listing optimization", "backend search terms"]),
            ("Amazon PPC Advertising (Sponsored Products/Brands)", "high", ["amazon ppc", "sponsored products", "acos", "tacos"]),
            ("Inventory Replenishment & FBA Logistics", "high", ["fba", "inventory planning", "stranded inventory"]),
            ("Brand Registry, Reviews & IP Protection", "high", ["brand registry", "vine reviews", "hijacker removal"])
        ], ["Walmart Marketplace", "International Amazon Expansion", "Profitability Analytics"]),

        ("Landing Page Funnel Builder", "Designs and builds high-converting click funnels, opt-ins, and upsell steps.", [
            ("Funnel Builders (ClickFunnels, Unbounce, GoHighLevel)", "critical", ["clickfunnels", "unbounce", "gohighlevel", "leadpages", "funnels"]),
            ("High-Converting Layouts & Mobile Responsiveness", "critical", ["landing page design", "mobile responsive", "visual hierarchy"]),
            ("Form Integrations, Webhooks & CRM Sync", "high", ["webhooks", "crm sync", "form captures"]),
            ("Upsell, Downsell & Order Bump Logic", "high", ["order bumps", "upsells", "downsells", "checkout flows"]),
            ("Page Speed Tuning & Tracking Scripts Integration", "high", ["page speed", "gtm tags", "facebook pixel", "scripts"])
        ], ["Custom CSS/JS", "Quiz Funnel Logic", "Webflow Funnels"]),

        ("Public Relations (PR) & Media Outreach Specialist", "Secures press coverage, journalist mentions, and brand features in media.", [
            ("Media Pitching & Journalist Relationships", "critical", ["media relations", "press pitching", "journalists", "press coverage"]),
            ("Press Releases (Writing & Newswire Distribution)", "critical", ["press release", "pr writing", "pr newswire", "pr distribution"]),
            ("HARO / Connectively & Reactive Media Opportunities", "high", ["haro", "connectively", "reactive pr", "expert commentary"]),
            ("Media Kit & Spokesperson Executive Prep", "high", ["press kit", "media training", "talking points"]),
            ("Coverage Tracking & Earned Media Value (EMV)", "high", ["media monitoring", "clippings", "earned media value"])
        ], ["Crisis PR Management", "Podcast Guest Booking", "Press Conference Coordination"]),

        ("Brand Partnerships Manager", "Architects joint ventures, brand collaborations, and co-marketed commercial alliances.", [
            ("Partnership Deal Sourcing & Outreach", "critical", ["brand partnerships", "business development", "deal sourcing", "alliances"]),
            ("Value Proposition Framing & Pitch Presentations", "critical", ["pitch decks", "partnership proposals", "shared value"]),
            ("Contract Terms, Co-Branding & Revenue Share Models", "high", ["contracts", "revenue share", "co-branding", "mou"]),
            ("Cross-Promotional Campaign Execution", "high", ["cross-promotion", "campaign coordination", "deliverable tracking"]),
            ("Post-Campaign ROI & Relationship Cultivation", "high", ["partnership roi", "relationship management", "renewals"])
        ], ["Event Sponsorships", "Licensing Deals", "Influencer Brand Merges"]),

        ("Local SEO & Google Business Profile Specialist", "Optimizes Google Maps rankings, local citations, and regional organic visibility.", [
            ("Google Business Profile (GBP) Optimization", "critical", ["google business profile", "gbp", "google maps", "local seo"]),
            ("Local Citation Building (NAP Consistency)", "critical", ["citations", "nap consistency", "name address phone", "directories"]),
            ("Review Generation & Reputation Management", "high", ["review management", "review generation", "customer responses"]),
            ("Local Keyword Research & Geo-Targeted Landing Pages", "high", ["local keywords", "geo-targeted pages", "near me searches"]),
            ("Local Pack Tracking & Geogrid Rankings", "high", ["local pack", "geogrid ranking", "local falcon"])
        ], ["Apple Maps & Bing Places", "Multi-Location Enterprise SEO", "Local Schema"]),

        ("Newsletter Publisher / Curator", "Writes, curates, monetizes, and scales loyal email newsletter subscriptions.", [
            ("Newsletter Platforms (Substack, Beehiiv, ConvertKit)", "critical", ["beehiiv", "substack", "convertkit", "newsletter"]),
            ("Curation, Editorial Voice & Digest Formats", "critical", ["content curation", "editorial voice", "digest writing"]),
            ("Sponsor Outreach & Native Ad Placements", "high", ["newsletter sponsors", "native advertising", "cpm pricing"]),
            ("Subscriber Acquisition (Referrals, Boosts, Lead Magnets)", "high", ["referral program", "lead magnets", "subscriber growth"]),
            ("Deliverability & Open Rate Optimization", "high", ["open rates", "deliverability", "inbox placement"])
        ], ["Paid Subscription Tiers", "Web Archives", "Cross-Promotions"]),

        ("Grant Writer", "Researches, writes, and coordinates funding proposals for non-profits and institutions.", [
            ("Grant Prospect Research & Eligibility Vetting", "critical", ["grant writing", "prospect research", "grant eligibility", "foundations"]),
            ("Narrative Proposal Writing & Project Description", "critical", ["proposal writing", "narrative", "needs statement", "program design"]),
            ("Budget Preparation & Justification Worksheets", "high", ["grant budget", "financial justification", "matching funds"]),
            ("Compliance, Reporting & Deliverable Tracking", "high", ["compliance", "grant reporting", "deliverables", "outcomes"]),
            ("Funder Relationship Management & Letters of Inquiry (LOI)", "high", ["loi", "funder relations", "letters of inquiry"])
        ], ["Federal Grants (Grants.gov)", "501(c)(3) Documentation", "Institutional Partnerships"]),

        ("Proposal & Tender Writer", "Engineers persuasive RFP responses, commercial bids, and government tender submissions.", [
            ("RFP / RFI / RFQ Analysis & Compliance Matrix", "critical", ["rfp", "rfi", "rfq", "compliance matrix", "tender writing"]),
            ("Persuasive Bid Writing & Executive Summaries", "critical", ["bid writing", "executive summary", "win themes", "value proposition"]),
            ("Collaborative Subject Matter Expert (SME) Interviews", "high", ["sme interviews", "technical input", "coordination"]),
            ("Pricing Schedules & Commercial Packaging", "high", ["pricing proposals", "packaging", "tender formats"]),
            ("Proposal Management & Deadline Execution", "high", ["proposal management", "submission deadlines", "shipley methodology"])
        ], ["Government Procurement Protocols", "Contract Knowledge", "Graphics for Proposals"]),

        ("Bilingual / Multilingual Translator", "Translates texts with cultural fidelity, nuance, and terminology precision.", [
            ("Source and Target Language Fluency", "critical", ["translation", "bilingual", "multilingual", "linguistics"]),
            ("Cultural Nuance & Idiomatic Adaptation", "critical", ["cultural adaptation", "idioms", "localization", "semantics"]),
            ("CAT Tools (Trados, MemoQ, Smartcat)", "high", ["cat tools", "trados", "memoq", "translation memory"]),
            ("Terminology Glossaries & Consistency Management", "high", ["glossaries", "termbases", "style guides"]),
            ("Proofreading, Editing & Certified Translation Standards", "high", ["proofreading", "editing", "translation accuracy"])
        ], ["Legal / Medical Translation", "Subtitling Translation", "Machine Translation Post-Editing (MTPE)"]),

        ("Localization Specialist", "Adapts software, websites, and marketing materials for international target regions.", [
            ("Software & Web Localization Workflows", "critical", ["localization", "l10n", "internationalization", "i18n"]),
            ("TMS Platforms (Lokalise, Phrase, Crowdin)", "critical", ["lokalise", "phrase", "crowdin", "translation management"]),
            ("String Extraction, Key Management & Formatting (JSON/PO)", "high", ["po files", "json strings", "string extraction", "placeholders"]),
            ("Pseudo-Localization & UI Expansion Testing", "high", ["pseudo-localization", "ui testing", "character truncation"]),
            ("Cultural Tone & Imagery Regionalization", "high", ["cultural review", "regional imagery", "date/currency formatting"])
        ], ["Multilingual SEO", "App Store Localization", "Right-to-Left (RTL) Layouts"]),

        ("Proofreader & Developmental Editor", "Refines grammar, structural narrative, clarity, and voice in written manuscripts.", [
            ("Copyediting & Proofreading Standards (Chicago Manual, AP Style)", "critical", ["proofreading", "copyediting", "chicago manual of style", "ap style"]),
            ("Developmental Editing (Structure, Pacing, Continuity)", "critical", ["developmental editing", "structure", "pacing", "narrative flow"]),
            ("Grammar, Syntax & Punctuation Precision", "high", ["grammar", "syntax", "punctuation", "consistency"]),
            ("Track Changes & Editorial Query Management", "high", ["track changes", "editor queries", "word", "google docs"]),
            ("Style Sheets & Character/Terminology Indexing", "high", ["style sheet", "terminology consistency", "fact-checking"])
        ], ["Line Editing", "Academic Editing", "Publishing Submissions"]),

        ("Growth Hacker / Experimentation Lead", "Runs rapid high-tempo marketing experiments across product and acquisition channels.", [
            ("Rapid Experimentation Framework & Ice Scoring", "critical", ["growth hacking", "rapid experimentation", "ice score", "growth sprints"]),
            ("Funnel Analytics & Viral Loop Engineering", "critical", ["viral loops", "referral systems", "pirate metrics", "aarrr"]),
            ("Cross-Channel Scrappy Growth Tactics", "high", ["scrappy marketing", "scraping", "automation", "outbound"]),
            ("A/B Landing Page & Offer Testing", "high", ["conversion testing", "messaging experiments", "hooks"]),
            ("Product-Led Growth (PLG) & User Activation", "high", ["plg", "user activation", "time to value", "retention"])
        ], ["Data Querying (SQL/Mixpanel)", "No-Code Prototypes", "API Automations"]),

        ("Programmatic Advertising Specialist", "Executes automated real-time ad bidding across DSPs and ad exchanges.", [
            ("DSP Platforms (Display & Video 360, The Trade Desk)", "critical", ["dv360", "the trade desk", "dsp", "programmatic advertising"]),
            ("Real-Time Bidding (RTB) & SSP Mechanics", "critical", ["rtb", "ssp", "ad exchanges", "bidding logic"]),
            ("Audience Segments & 3rd-Party Data Integration", "high", ["dmp", "audience segments", "data onboarding", "cookieless"]),
            ("Brand Safety, Verification (DoubleVerify, IAS) & Fraud Prevention", "high", ["brand safety", "doubleverify", "ias", "ad fraud"]),
            ("Deal IDs & Private Marketplace (PMP) Management", "high", ["pmp", "deal ids", "programmatic guaranteed", "inventory"])
        ], ["Connected TV (CTV) Ads", "Audio Ads", "Dynamic Creative Optimization (DCO)"])
    ],

    "Business Operations, Sales & Finance": [
        ("B2B Sales Development Representative (SDR)", "Conducts cold outbound prospect research, email sequencing, and qualifies leads.", [
            ("Outbound Prospecting & Lead Generation", "critical", ["outbound sales", "prospecting", "lead gen", "cold calling"]),
            ("Sales Engagement Tools (Apollo, Outreach, Salesloft)", "critical", ["apollo", "outreach", "salesloft", "cold email"]),
            ("LinkedIn Sales Navigator & Boolean Search", "high", ["sales navigator", "boolean search", "social selling"]),
            ("Qualification Frameworks (BANT, MEDDIC)", "high", ["bant", "meddic", "lead qualification", "discovery calls"]),
            ("CRM Pipeline Hygiene (Salesforce / HubSpot)", "high", ["salesforce", "hubspot", "crm data", "pipeline tracking"])
        ], ["Objection Handling", "Cold Calling Scripts", "Video Prospecting"]),

        ("High-Ticket Closer / Account Executive", "Leads discovery, product demonstrations, negotiation, and closes enterprise contracts.", [
            ("Discovery Calls & Pain Point Diagnosis", "critical", ["discovery calls", "consultative selling", "pain points", "account executive"]),
            ("Value-Based Product Demonstrations", "critical", ["product demo", "value selling", "solution presentation"]),
            ("Objection Handling & High-Stakes Negotiation", "high", ["negotiation", "objection handling", "closing", "pricing"]),
            ("Enterprise Contract & Proposal Closures", "high", ["proposals", "contracts", "msa", "procurement"]),
            ("Pipeline Management & Accurate Forecasting", "high", ["pipeline management", "forecast accuracy", "sales cycle"])
        ], ["Multi-Stakeholder Consensus", "Enterprise Procurement Navigation", "Challenger Sale"]),

        ("Customer Success Manager", "Drives customer retention, product adoption, onboarding satisfaction, and renewals.", [
            ("Customer Onboarding & Time-to-Value", "critical", ["customer success", "onboarding", "product adoption", "time to value"]),
            ("Churn Prevention & Health Score Monitoring", "critical", ["churn prevention", "health scores", "customer retention"]),
            ("Quarterly Business Reviews (QBRs) & Executive Check-Ins", "high", ["qbr", "executive reviews", "relationship management"]),
            ("Upsell & Expansion Identification", "high", ["expansion revenue", "upsells", "cross-sells"]),
            ("Customer Advocacy & Case Studies", "high", ["advocacy", "case studies", "nps", "csat"])
        ], ["Gainsight Platform", "Product Feedback Loops", "Renewal Contract Management"]),

        ("RevOps (Revenue Operations) Specialist", "Aligns sales, marketing, and customer success data, systems, and processes.", [
            ("Revenue Tech Stack Architecture", "critical", ["revops", "revenue operations", "sales tech", "tech stack alignment"]),
            ("Cross-Functional Pipeline Data Modeling", "critical", ["funnel analytics", "pipeline velocity", "data modeling"]),
            ("CRM Administration & Workflow Automations", "high", ["salesforce administration", "hubspot operations", "workflow rules"]),
            ("Sales Commission & Territory Planning", "high", ["commission plans", "territory design", "quotas"]),
            ("Revenue Reporting & Executive Forecasting Dashboards", "high", ["revenue reporting", "bi dashboards", "forecasting"])
        ], ["Attribution Modeling", "Data Warehouse Integration", "Deal Desk Guidance"]),

        ("CRM Administrator (Salesforce/HubSpot)", "Configures custom objects, permission sets, validation rules, and business automations.", [
            ("Salesforce or HubSpot Certified Administration", "critical", ["salesforce admin", "hubspot admin", "custom objects", "crm"]),
            ("Automation Flows & Process Builder Logic", "critical", ["flow builder", "workflows", "validation rules", "triggers"]),
            ("User Security, Profiles & Permission Sets", "high", ["permission sets", "profiles", "role hierarchy", "sharing rules"]),
            ("Data Import, Deduplication & Cleansing (Data Loader)", "high", ["data loader", "data cleaning", "import/export"]),
            ("Custom Reports & Executive Dashboards", "high", ["reports", "dashboards", "analytics", "kpi tracking"])
        ], ["AppExchange Integrations", "Apex Basics", "API Syncs"]),

        ("Project Manager (Agile/Scrum)", "Orchestrates project timelines, cross-functional sprints, deliverables, and resource allocation.", [
            ("Project Management Methodologies (Agile, Waterfall, Hybrid)", "critical", ["project management", "agile", "waterfall", "pmp"]),
            ("Sprint Planning, Roadmaps & Milestone Tracking", "critical", ["sprint planning", "roadmaps", "milestones", "gantt charts"]),
            ("Project Tools (Jira, Asana, Monday.com)", "high", ["jira", "asana", "monday.com", "confluence"]),
            ("Risk Assessment & Scope Creep Management", "high", ["risk mitigation", "scope creep", "change control"]),
            ("Stakeholder Communication & Budget Oversight", "high", ["stakeholder management", "status reports", "budget tracking"])
        ], ["Scrum Master Certification (CSM)", "Resource Capacity Planning", "Vendor Management"]),

        ("Scrum Master", "Facilitates Agile ceremonies, removes team blockers, and fosters self-organizing engineering squads.", [
            ("Scrum Ceremonies (Standups, Retros, Planning, Reviews)", "critical", ["scrum master", "daily standup", "sprint retrospective", "sprint review"]),
            ("Blocker Removal & Impediment Resolution", "critical", ["impediment removal", "blockers", "servant leadership"]),
            ("Sprint Metrics (Velocity, Burndown Charts)", "high", ["velocity", "burndown charts", "capacity tracking"]),
            ("Agile Coaching & Continuous Improvement", "high", ["agile coaching", "team psychological safety", "continuous improvement"]),
            ("Jira / Confluence Agile Board Administration", "high", ["jira boards", "backlog grooming", "confluence"])
        ], ["SAFe Framework", "Kanban Methodology", "Team Conflict Resolution"]),

        ("Product Operations Manager", "Streamlines product data, user feedback loops, feature launches, and internal product tooling.", [
            ("Product Feedback Loops & Voice of Customer Centralization", "critical", ["product operations", "feedback loops", "voc", "feature requests"]),
            ("Product Analytics (Mixpanel, Amplitude, Pendo)", "critical", ["amplitude", "mixpanel", "pendo", "product analytics"]),
            ("Go-to-Market (GTM) Launch Alignment", "high", ["gtm launch", "release management", "internal enablement"]),
            ("Product Tooling & Template Governance", "high", ["notion", "jira product discovery", "roadmapping tools"]),
            ("Feature Experimentation & Beta Testing Programs", "high", ["beta programs", "feature flags", "early access"])
        ], ["Cross-Team Alignment", "Product Roadmap Operations", "Product Ops Strategy"]),

        ("Executive Virtual Assistant", "Manages high-level executive schedules, email inboxes, complex travel, and confidential operations.", [
            ("Executive Calendar & Schedule Optimization", "critical", ["calendar management", "executive assistant", "time blocking", "scheduling"]),
            ("Inbox Triage & Professional Correspondence", "critical", ["inbox zero", "email triage", "business correspondence"]),
            ("Complex Travel Logistics & Itinerary Planning", "high", ["travel booking", "itineraries", "flight logistics", "visas"]),
            ("Confidential Documentation & Expense Reports", "high", ["confidentiality", "expense reports", "expensify", "receipts"]),
            ("Meeting Minutes & Action Item Follow-Through", "high", ["meeting minutes", "action items", "task tracking"])
        ], ["Presentation Preparation", "Event Coordination", "Basic Bookkeeping"]),

        ("Bookkeeper (QuickBooks/Xero/Tally)", "Maintains financial ledgers, bank reconciliations, accounts, and financial statements.", [
            ("Accounting Software (QuickBooks Online, Xero, Tally)", "critical", ["quickbooks", "xero", "tally", "bookkeeping"]),
            ("Bank Reconciliation & General Ledger Journal Entries", "critical", ["bank reconciliation", "general ledger", "journal entries"]),
            ("Accounts Payable & Accounts Receivable Tracking", "high", ["accounts payable", "accounts receivable", "invoicing", "bills"]),
            ("Chart of Accounts Organization", "high", ["chart of accounts", "categorization", "accrual accounting"]),
            ("Monthly Financial Statements (P&L, Balance Sheet)", "high", ["profit and loss", "balance sheet", "financial statements"])
        ], ["Payroll Processing", "Sales Tax Filing", "Year-End 1099s"]),

        ("Payroll Specialist", "Processes accurate employee wages, tax withholdings, benefits deductions, and direct deposits.", [
            ("Payroll Systems (Gusto, ADP, Paychex, Rippling)", "critical", ["payroll", "gusto", "adp", "paychex", "rippling"]),
            ("Wage Calculations, Overtime & Deductions", "critical", ["overtime calculation", "benefits deductions", "wage garnishment"]),
            ("Payroll Tax Withholding (Federal, State, Local)", "high", ["payroll tax", "w-2", "w-4", "941 filing", "withholdings"]),
            ("Direct Deposit & Disbursement Compliance", "high", ["direct deposit", "pay stubs", "ach batches"]),
            ("Time and Attendance Tracking Audits", "high", ["timecards", "attendance", "paid time off", "audit"])
        ], ["Multi-State Payroll", "Contractor 1099 Setup", "Year-End Tax Reconciliation"]),

        ("Accounts Payable / Receivable Specialist", "Handles outgoing supplier payments, invoices, collections, and vendor accounts.", [
            ("Three-Way Matching (PO, Receipt, Invoice)", "critical", ["three-way match", "accounts payable", "purchase orders", "invoices"]),
            ("Vendor Payment Processing (ACH, Check, Wire)", "critical", ["ach payments", "wire transfers", "check runs", "payment terms"]),
            ("Invoicing & Billing Generation", "high", ["invoicing", "accounts receivable", "billing", "collections"]),
            ("Aging Reports & Overdue Follow-Up", "high", ["aging reports", "collections", "dso", "bad debt"]),
            ("Vendor Inquiries & Account Reconciliation", "high", ["vendor reconciliation", "statement review", "dispute resolution"])
        ], ["ERP Accounting (NetSuite)", "Credit Verification", "Expense Auditing"]),

        ("Financial Analyst (FP&A)", "Develops financial forecasts, variance analysis, annual budgets, and corporate models.", [
            ("Budgeting, Forecasting & Long-Range Planning", "critical", ["fp&a", "financial planning", "budgeting", "forecasting"]),
            ("Variance Analysis (Actual vs Budget)", "critical", ["variance analysis", "budget vs actual", "financial analysis"]),
            ("Advanced Excel (Financial Modeling, Lookups, Modeling)", "high", ["excel modeling", "financial modeling", "scenarios"]),
            ("KPI Dashboards & Business Performance Reporting", "high", ["financial kpis", "ebitda", "gross margin", "dashboards"]),
            ("Cross-Functional Departmental Cost Control", "high", ["cost analysis", "department spend", "headcount modeling"])
        ], ["Hyperion / Adaptive Insights", "SQL for Finance", "Capital Expenditure Planning"]),

        ("Tax Preparer", "Prepares compliant individual and business tax filings, deductions, and tax schedules.", [
            ("Tax Preparation Software (Drake, TurboTax, ProConnect)", "critical", ["tax preparation", "drake tax", "tax software", "filing"]),
            ("Individual & Corporate Tax Code (Form 1040, 1120, 1065)", "critical", ["form 1040", "schedule c", "1120s", "tax deductions"]),
            ("Deduction Optimization & Tax Credits", "high", ["tax credits", "depreciation", "business deductions"]),
            ("Tax Document Verification (W-2, 1099, K-1)", "high", ["w-2", "1099-misc", "schedule k-1", "records review"]),
            ("IRS Compliance & Filing Procedures", "high", ["irs guidelines", "e-file", "tax extensions", "ptin"])
        ], ["State Tax Returns", "IRS Notice Resolution", "Enrolled Agent Certification"]),

        ("Supply Chain & Logistics Coordinator", "Coordinates freight shipments, customs documentation, inventory levels, and logistics.", [
            ("Freight Management (Ocean, Air, Domestic Trucking)", "critical", ["freight forwarding", "logistics", "shipping", "inbound/outbound"]),
            ("Customs Documentation & Incoterms", "critical", ["incoterms", "bill of lading", "commercial invoice", "customs clearance"]),
            ("Inventory Tracking & Purchase Order Fulfillment", "high", ["po tracking", "inventory tracking", "warehouse coordination"]),
            ("Carrier Rate Negotiation & Transit Optimization", "high", ["carrier negotiation", "rates", "transit times", "freight quotes"]),
            ("Logistics Disruption Mitigation & Tracking", "high", ["delay management", "shipment tracking", "claims", "traceability"])
        ], ["TMS Software", "Dangerous Goods (Hazmat)", "Reverse Logistics"]),

        ("Procurement & Vendor Negotiator", "Sources suppliers, executes RFPs, negotiates pricing contracts, and monitors vendor SLAs.", [
            ("Supplier Sourcing & Vendor Vetting", "critical", ["procurement", "supplier sourcing", "vendor vetting", "purchasing"]),
            ("Contract Negotiation (Pricing, Terms, SLAs)", "critical", ["contract negotiation", "payment terms", "slas", "cost reduction"]),
            ("Purchase Order Issuance & Approval Workflows", "high", ["purchase orders", "procurement workflows", "approval processes"]),
            ("Vendor Performance & Scorecard Management", "high", ["vendor scorecards", "supplier audits", "performance tracking"]),
            ("Category Spend Analysis & Cost Savings", "high", ["spend analysis", "cost savings", "strategic sourcing"])
        ], ["ERP Procurement (SAP/Oracle)", "E-Procurement Platforms", "Sustainable Sourcing"]),

        ("Inventory Control Specialist", "Conducts cycle counts, minimizes shrinkage, tracks stock levels, and audits warehouses.", [
            ("Inventory Management Systems (WMS / ERP)", "critical", ["inventory control", "wms", "stock tracking", "sku management"]),
            ("Cycle Counting & Physical Stock Audits", "critical", ["cycle counting", "physical inventory", "stock reconciliation"]),
            ("Shrinkage & Loss Prevention Analysis", "high", ["shrinkage", "loss prevention", "discrepancy investigation"]),
            ("Reorder Points, Safety Stock & Lead Times", "high", ["reorder points", "safety stock", "lead time calculation", "min-max"]),
            ("Damaged Goods & RMA Processing", "high", ["damaged inventory", "rma", "quarantine stock"])
        ], ["Barcode / RFID Scanning", "ABC Inventory Classification", "Forklift Certified"]),

        ("Technical Recruiter / Sourcer", "Sources, screens, interviews, and closes candidates for technical engineering roles.", [
            ("Technical Candidate Sourcing (LinkedIn Recruiter, GitHub)", "critical", ["technical recruiting", "sourcing", "linkedin recruiter", "github sourcing"]),
            ("Candidate Screening & Technical Competency Vetting", "critical", ["phone screening", "candidate vetting", "resume review"]),
            ("Applicant Tracking Systems (Greenhouse, Lever, Ashby)", "high", ["ats", "greenhouse", "lever", "ashby"]),
            ("Offer Negotiation & Closing Candidates", "high", ["offer negotiation", "candidate closing", "compensation packages"]),
            ("Hiring Manager Collaboration & Intake Meetings", "high", ["intake meetings", "job descriptions", "pipeline updates"])
        ], ["Diversity Hiring", "Talent Market Mapping", "Employer Branding"]),

        ("People Operations / HR Generalist", "Directs employee onboarding, workplace culture, benefits administration, and HR policies.", [
            ("HR Policies & Employee Handbooks", "critical", ["people operations", "hr policies", "employee handbook", "labor law"]),
            ("Employee Onboarding & Offboarding Lifecycle", "critical", ["onboarding", "offboarding", "exit interviews"]),
            ("Benefits Administration & Open Enrollment", "high", ["health insurance", "401k", "benefits administration", "open enrollment"]),
            ("Employee Relations & Conflict Resolution", "high", ["employee relations", "conflict resolution", "workplace culture"]),
            ("HR Information Systems (BambooHR, Workday)", "high", ["hris", "bamboohr", "workday", "employee records"])
        ], ["Performance Review Cycles", "Compliance Auditing (EEOC)", "Remote Culture Building"]),

        ("Notion / Workspace Systems Architect", "Constructs relational databases, automated company wikis, and project hubs.", [
            ("Advanced Notion Relational Databases & Rollups", "critical", ["notion", "relations", "rollups", "formulas 2.0", "database architecture"]),
            ("Company Wiki & Knowledge Base Architecture", "critical", ["company wiki", "knowledge base", "information architecture"]),
            ("Notion Automations & Third-Party Sync (Make / Zapier)", "high", ["notion api", "make.com", "zapier", "automations"]),
            ("Custom Dashboard Design & Permissions Hierarchy", "high", ["dashboard design", "workspace permissions", "guest access"]),
            ("Template Creation & Internal Team Onboarding", "high", ["notion templates", "team documentation", "standard operating procedures"])
        ], ["Coda Workspace", "Airtable Systems", "Portal Security"]),

        ("Fractional Operations Manager", "Optimizes operations, standardizes SOPs, and removes business bottlenecks for growth.", [
            ("Business Process Mapping & Bottleneck Diagnosis", "critical", ["process mapping", "operations management", "bottlenecks", "sop"]),
            ("Standard Operating Procedure (SOP) Authoring", "critical", ["sop authoring", "process documentation", "checklists"]),
            ("Software Tool Consolidation & Streamlining", "high", ["tech stack consolidation", "tool auditing", "cost saving"]),
            ("Team Accountability & KPI Tracking", "high", ["kpis", "okrs", "team accountability", "scorecards"]),
            ("Cross-Departmental Workflow Optimization", "high", ["workflow optimization", "cross-functional operations"])
        ], ["Financial Oversight", "Agile Operations", "Change Management"]),

        ("E-Commerce Fulfillment Coordinator", "Supervises pick, pack, ship operations, order routing, and returns in warehouses.", [
            ("Order Management Systems (ShipStation, ShipBob)", "critical", ["order fulfillment", "shipstation", "shipbob", "pick pack ship"]),
            ("Warehouse Pick and Pack Accuracy", "critical", ["order picking", "packing lists", "barcode scanning", "fulfillment"]),
            ("Shipping Carrier Logistics (USPS, FedEx, UPS)", "high", ["shipping labels", "carrier rates", "manifests", "couriers"]),
            ("Returns Management & Restocking (Reverse Logistics)", "high", ["returns processing", "restocking", "reverse logistics"]),
            ("Packaging Materials & Box Dimension Optimization", "high", ["dimensional weight", "box optimization", "packing materials"])
        ], ["Same-Day Fulfillment SLAs", "Inventory Accuracy", "Warehouse Safety"]),

        ("Freight Broker", "Negotiates freight rates, matches shippers with motor carriers, and tracks loads.", [
            ("Carrier Sourcing & Load Board Matching (DAT, Truckstop)", "critical", ["freight broker", "dat load board", "truckstop", "carrier sourcing"]),
            ("Freight Rate Negotiation & Margin Calculation", "critical", ["rate negotiation", "freight rates", "gross margin", "bidding"]),
            ("Carrier Vetting & Safety Rating Audits (FMCSA)", "high", ["carrier vetting", "fmcsa", "safety rating", "insurance certificates"]),
            ("Load Dispatch & Real-Time Tracking Check Calls", "high", ["dispatch", "check calls", "tracking", "detention tracking"]),
            ("Bill of Lading (BOL) & Proof of Delivery (POD) Audits", "high", ["bol", "pod", "rate confirmation", "invoicing"])
        ], ["TMS Platforms", "Reefer & Flatbed Specialized Cargo", "Cross-Border Shipping"]),

        ("Real Estate Transaction Coordinator", "Manages contracts, escrow deadlines, disclosures, and documents through closing.", [
            ("Real Estate Purchase Contracts & Addendums", "critical", ["transaction coordinator", "purchase agreements", "addendums", "contracts"]),
            ("Escrow, Title & Inspection Deadline Management", "critical", ["escrow timelines", "title company", "inspection contingencies"]),
            ("Disclosure Compliance & Document Verification", "high", ["disclosures", "compliance", "docusign", "dotloop"]),
            ("Liaison Between Buyers, Sellers, Agents & Lenders", "high", ["client coordination", "agent communication", "lender follow-up"]),
            ("Closing File Archiving & Commission Disbursements", "high", ["closing packets", "broker review", "commission paperwork"])
        ], ["MLS Coordination", "Property Disclosures", "State Real Estate Regulations"]),

        ("Insurance Claims Adjuster", "Investigates property and casualty claims, inspects damages, and negotiates settlements.", [
            ("Claims Investigation & Coverage Verification", "critical", ["claims adjuster", "insurance claims", "coverage verification", "policy terms"]),
            ("Physical Damage Inspection & Repair Estimating", "critical", ["damage inspection", "repair estimates", "xactimate", "estimating"]),
            ("Claimant & Witness Interviewing", "high", ["witness interviews", "recorded statements", "liability determination"]),
            ("Settlement Negotiation & Payout Authorization", "high", ["settlement negotiation", "claim payout", "releases"]),
            ("Detailed Claims Report & File Documentation", "high", ["claims documentation", "file notes", "subrogation identification"])
        ], ["Catastrophe Claims Response", "State Adjuster Licensing", "Fraud Detection"])
    ],

    "Skilled Trades, Construction & Manufacturing": [
        ("Electrician (Residential/Commercial)", "Installs wiring, circuit breakers, conduit, and troubleshoots electrical systems.", [
            ("National Electrical Code (NEC) Compliance", "critical", ["nec code", "electrical code", "grounding", "safety standards"]),
            ("Conduit Bending & Wire Pulling (EMT, Romex)", "critical", ["conduit bending", "emt", "romex", "wire pulling"]),
            ("Circuit Breaker Panels, Outlets & Switch Installation", "high", ["breaker panel", "outlets", "switches", "junction boxes"]),
            ("Troubleshooting Circuits with Multimeters", "high", ["multimeter", "voltage testing", "short circuits", "continuity"]),
            ("Blueprint & Electrical Schematic Reading", "high", ["electrical schematics", "blueprints", "one-line diagrams"])
        ], ["Three-Phase Power", "Lighting Retrofits", "Generator Transfer Switches"]),

        ("Industrial Electrician", "Maintains heavy machinery power distribution, motors, drives, and plant automation.", [
            ("Three-Phase Power & High Voltage Systems (480V)", "critical", ["480v", "three-phase", "industrial electrical", "high voltage"]),
            ("Electric Motors, Transformers & Variable Frequency Drives (VFDs)", "critical", ["electric motors", "vfd", "transformers", "motor controls"]),
            ("PLC Troubleshooting & Relay Logic", "high", ["plc troubleshooting", "relay logic", "control panels"]),
            ("Lockout/Tagout (LOTO) & Arc Flash Safety", "high", ["lockout tagout", "loto", "arc flash", "nfpa 70e"]),
            ("Industrial Sensor Wiring & Calibration", "high", ["proximity sensors", "thermocouples", "limit switches"])
        ], ["Industrial Switchgear", "Preventative Maintenance", "Motor Rewinding"]),

        ("Plumber & Pipefitter", "Installs, repairs, and inspects water, gas, and drainage piping systems.", [
            ("Plumbing Code & Drainage System Standards", "critical", ["plumbing code", "dwv", "drainage", "venting"]),
            ("Pipe Joining & Soldering (Copper, PEX, PVC, Cast Iron)", "critical", ["copper soldering", "pex", "pvc", "pipe fitting", "threading"]),
            ("Fixture Installation (Sinks, Toilets, Showers, Heaters)", "high", ["water heaters", "fixtures", "faucets", "rough-in"]),
            ("Drain Cleaning, Augers & Camera Inspection", "high", ["drain cleaning", "snaking", "camera inspection", "hydro-jetting"]),
            ("Pressure Testing & Leak Diagnostics", "high", ["pressure testing", "leak detection", "gas line testing"])
        ], ["Backflow Prevention Certification", "Tankless Water Heaters", "Commercial Boiler Piping"]),

        ("HVAC (Heating, Ventilation, Air Conditioning) Technician", "Installs and repairs air conditioning units, heat pumps, furnaces, and ducts.", [
            ("Refrigeration Cycle Diagnostics & Manifold Gauges", "critical", ["refrigeration cycle", "manifold gauges", "superheat", "subcooling"]),
            ("EPA 608 Certification & Refrigerant Handling", "critical", ["epa 608", "r-410a", "freon", "refrigerant recovery"]),
            ("Furnace & Heat Pump Electrical Troubleshooting", "high", ["furnace repair", "heat pump", "contactors", "capacitors", "flame sensors"]),
            ("Airflow, Ductwork Sizing & Static Pressure", "high", ["ductwork", "static pressure", "airflow", "balancing"]),
            ("Thermostats & Smart Control Wiring", "high", ["smart thermostats", "24v wiring", "zone dampers"])
        ], ["Gas Piping for Furnaces", "Variable Refrigerant Flow (VRF)", "Commercial Chillers"]),

        ("Welder (MIG/TIG/Stick)", "Fuses metal structures and fabrications using arc welding techniques and blueprints.", [
            ("Welding Processes (MIG, TIG, Stick / SMAW, GMAW, GTAW)", "critical", ["mig welding", "tig welding", "stick welding", "arc welding"]),
            ("Blueprint Reading & Welding Symbols (AWS)", "critical", ["welding symbols", "blueprints", "weld specs"]),
            ("Metal Prep, Fit-Up, Clamping & Grinding", "high", ["fit-up", "angle grinders", "beveling", "joint preparation"]),
            ("Material Metallurgy (Steel, Aluminum, Stainless)", "high", ["carbon steel", "aluminum", "stainless steel", "heat distortion"]),
            ("Weld Quality Inspection & Defect Remediation", "high", ["visual inspection", "porosity", "undercut", "penetration"])
        ], ["Pipe Welding 6G", "Plasma Cutting", "Structural Certification (AWS D1.1)"]),

        ("CNC Machinist", "Programs and operates computer numerical control mills and lathes to craft metal parts.", [
            ("CNC Machine Setup & Operation (Mills & Lathes)", "critical", ["cnc mill", "cnc lathe", "machining", "spindle", "fixtures"]),
            ("G-Code and M-Code Interpretation & Editing", "critical", ["g-code", "m-code", "cnc programming"]),
            ("Precision Measuring Tools (Micrometers, Calipers, Dial Indicators)", "high", ["micrometers", "calipers", "dial indicator", "tolerances"]),
            ("Tooling Selection, Speeds & Feeds Calculation", "high", ["speeds and feeds", "carbide tooling", "end mills", "coolant"]),
            ("CAM Software Basics (Mastercam, Fusion 360)", "high", ["cam", "mastercam", "toolpaths"])
        ], ["5-Axis Machining", "CMM Inspection", "Geometric Tolerancing"]),

        ("Finish Carpenter & Cabinetmaker", "Builds precision cabinetry, trim, moldings, custom furniture, and wooden joinery.", [
            ("Trim Carpentry & Crown Molding Installation", "critical", ["finish carpentry", "trim", "crown molding", "baseboards", "casing"]),
            ("Cabinet Construction & Joinery (Dovetail, Mortise & Tenon)", "critical", ["cabinetry", "joinery", "pocket holes", "dovetail"]),
            ("Table Saws, Miter Saws & Router Precision", "high", ["table saw", "miter saw", "router table", "planer"]),
            ("Hardware Installation (Concealed Hinges, Drawer Slides)", "high", ["hinges", "drawer slides", "cabinet hardware"]),
            ("Wood Sanding, Staining & Clear Finish Application", "high", ["sanding", "wood staining", "polyurethane", "lacquer"])
        ], ["Custom Architectural Millwork", "Laminate Countertops", "Veneering"]),

        ("Structural Framer", "Erects wooden and steel skeletons, load-bearing walls, floor joists, and roof trusses.", [
            ("Framing Walls, Floors & Ceiling Joists", "critical", ["framing", "studs", "joists", "headers", "structural carpentry"]),
            ("Roof Rafters & Truss Installation", "critical", ["roof framing", "rafters", "trusses", "pitch"]),
            ("Blueprint Reading & Framing Layout Specifications", "high", ["blueprints", "layout", "chalk lines", "rough opening"]),
            ("Pneumatic Nail Guns & Framing Saws", "high", ["nail gun", "circular saw", "framing hammer"]),
            ("Level, Plumb & Square Verification", "high", ["plumb", "level", "square", "bracing", "sheathing"])
        ], ["Light-Gauge Steel Framing", "Engineered Lumber (LVL)", "Stair Framing"]),

        ("Solar PV Installer & Technician", "Mounts solar panels, connects inverters, runs conduit, and commissions clean energy systems.", [
            ("Solar Panel Roof Mounting & Racking Systems", "critical", ["solar panels", "racking", "flashing", "roof attachments"]),
            ("Inverter & Microinverter Wiring (Enphase, SolarEdge)", "critical", ["inverters", "microinverters", "dc wiring", "string inverter"]),
            ("Electrical AC/DC Disconnect & Junction Box Connections", "high", ["ac disconnect", "dc disconnect", "junction boxes", "conduit"]),
            ("Roof Fall Protection & OSHA Ladder Safety", "high", ["fall protection", "harness", "roof safety", "osha"]),
            ("System Commissioning & Monitoring Setup", "high", ["system commissioning", "solar monitoring", "rapid shutdown"])
        ], ["Battery Storage (Tesla Powerwall)", "Ground Mount Systems", "NABCEP Certification"]),

        ("EV Charging Station Technician", "Installs, wires, and commissions Level 2 and Level 3 DC fast-charging stations.", [
            ("Level 2 & DC Fast Charging Hardware", "critical", ["ev charger", "level 2", "dc fast charger", "evse"]),
            ("High Amperage Electrical Service & Breaker Panels", "critical", ["high amperage", "subpanel", "240v", "480v", "load calculation"]),
            ("Conduit Bending & Underground Trench Wiring", "high", ["conduit runs", "trenching", "feeder wires"]),
            ("EV Charger Networking & OCPP Protocol", "high", ["ocpp", "networking", "cellular gateway", "station commissioning"]),
            ("Safety Testing, Grounding & Commissioning", "high", ["grounding", "gfci", "ev simulator testing"])
        ], ["Fleet Depots Charging", "Commercial Microgrids", "EVITP Certification"]),

        ("Automotive Diagnostic Technician", "Diagnoses OBD-II trouble codes, engine issues, sensors, and electronic vehicle faults.", [
            ("OBD-II Scanners & Live Sensor Data Interpretation", "critical", ["obd-ii", "scan tool", "trouble codes", "live data", "diagnostics"]),
            ("Automotive Electrical Troubleshooting & Wire Schematics", "critical", ["wiring schematics", "multimeter", "relays", "short circuits"]),
            ("Engine Mechanical Diagnostics (Compression, Leak-Down)", "high", ["compression test", "cylinder leak-down", "timing", "fuel pressure"]),
            ("Brake, Suspension & Steering Repair", "high", ["brakes", "suspension", "alignment", "calipers"]),
            ("Automotive Computer Networks (CAN Bus)", "high", ["can bus", "ecm", "bcm", "modules"])
        ], ["ASE Certifications", "Emissions Diagnostics", "Air Conditioning Repair (MACS)"]),

        ("Electric Vehicle (EV) Mechanic", "Services high-voltage battery packs, electric motors, power electronics, and regenerative brakes.", [
            ("High-Voltage Safety & Personal Protective Equipment (PPE)", "critical", ["high voltage", "ev safety", "insulated tools", "1000v ppe"]),
            ("High-Voltage Battery Pack Diagnostics & Cell Balancing", "critical", ["battery pack", "bms", "lithium-ion", "cell degradation"]),
            ("Electric Drive Motors & Inverter Troubleshooting", "high", ["electric motor", "inverter", "regen braking", "resolver"]),
            ("Thermal Management & Battery Cooling Loops", "high", ["thermal management", "coolant loops", "chiller", "heat pump"]),
            ("EV Firmware Updates & Sensor Calibration", "high", ["flashing", "software updates", "adas calibration"])
        ], ["Solid-State Battery Systems", "Motor Phase Testing", "Charging Port Replacement"]),

        ("Diesel & Heavy Equipment Mechanic", "Maintains heavy diesel engines, hydraulic systems, bulldozers, and tractor-trailers.", [
            ("Diesel Engine Diagnostics & Fuel Injection (Common Rail)", "critical", ["diesel engine", "common rail", "fuel injectors", "turbocharger"]),
            ("Hydraulic Systems Troubleshooting (Cylinders, Pumps, Valves)", "critical", ["hydraulics", "hydraulic pumps", "cylinders", "spool valves"]),
            ("Heavy Truck Brake Systems (Air Brakes)", "high", ["air brakes", "compressor", "slack adjusters", "abs"]),
            ("Diesel Exhaust Aftertreatment (DEF, DPF, SCR)", "high", ["dpf", "def", "scr", "aftertreatment regeneration"]),
            ("Heavy Equipment Undercarriage & Transmission Repair", "high", ["tracks", "undercarriage", "powershift transmission"])
        ], ["DOT Inspection Certification", "Heavy Crane Hydraulics", "Diagnostic Software (Cat ET, Cummins Insite)"]),

        ("Aviation Maintenance Technician (A&P)", "Services aircraft airframes, turbine engines, avionics, and FAA flight control systems.", [
            ("FAA Federal Aviation Regulations & Logbook Compliance", "critical", ["faa", "a&p license", "logbook entries", "airworthiness"]),
            ("Airframe Structural Inspection & Sheet Metal Riveting", "critical", ["airframe", "sheet metal", "riveting", "structural repair"]),
            ("Aircraft Powerplant (Turbine & Piston Engine) Overhaul", "high", ["turbine engine", "piston engine", "magnetos", "propeller"]),
            ("Avionics & Electrical Bus Troubleshooting", "high", ["avionics", "wiring", "instruments", "pitot-static"]),
            ("Hydraulic Landing Gear & Flight Control Rigging", "high", ["landing gear", "flight controls", "cables", "rigging"])
        ], ["Composite Aircraft Materials", "Non-Destructive Testing (NDT)", "Turbofan Borescope Inspection"]),

        ("Robotics & Industrial Automation Technician", "Programs, teaches, and repairs robotic arms and automated factory assembly cells.", [
            ("Industrial Robotic Arm Programming (FANUC, KUKA, ABB)", "critical", ["fanuc", "kuka", "abb", "robotic arm", "teach pendant"]),
            ("End-of-Arm Tooling (EOAT) & Pneumatics", "critical", ["eoat", "grippers", "pneumatics", "solenoids"]),
            ("Safety Interlocks, Light Curtains & Area Scanners", "high", ["light curtains", "safety relays", "e-stop", "interlocks"]),
            ("Robot Calibration & Tool Center Point (TCP) Setup", "high", ["tcp", "robot calibration", "path optimization"]),
            ("Robotics Preventative Maintenance & Joint Lubrication", "high", ["preventative maintenance", "greasing", "harness check"])
        ], ["Machine Vision Integration (Cognex)", "Collaborative Robots (Cobots)", "PLC Handshaking"]),

        ("PLC (Programmable Logic Controller) Programmer", "Writes Ladder Logic, Function Blocks, and oversees industrial plant processes.", [
            ("PLC Programming (Ladder Logic, Structured Text)", "critical", ["ladder logic", "structured text", "allen-bradley", "siemens s7", "plc"]),
            ("HMI & SCADA Development (Ignition, FactoryTalk)", "critical", ["hmi", "scada", "ignition", "factorytalk"]),
            ("Industrial Communication Protocols (EtherNet/IP, Modbus)", "high", ["ethernet/ip", "modbus", "profibus", "industrial networking"]),
            ("I/O Wiring, Digital/Analog Modules & Schematics", "high", ["analog inputs", "digital outputs", "i/o modules", "wiring"]),
            ("Machine Commissioning & Debugging on Factory Floors", "high", ["commissioning", "debugging", "loop checks", "safety plcs"])
        ], ["Batch Control (ISA-88)", "DCS Systems", "OPC-UA Integration"]),

        ("3D Printing & Additive Manufacturing Technician", "Operates, calibrates, and post-processes industrial SLA, SLS, and FDM printers.", [
            ("Industrial 3D Printers (FDM, SLA, SLS, Metal DMLS)", "critical", ["3d printing", "fdm", "sla", "sls", "additive manufacturing"]),
            ("Slicing Software & Print Parameter Tuning", "critical", ["slicer", "cura", "prusaslicer", "support structures", "infill"]),
            ("Printer Calibration (Bed Leveling, Extruder, Laser Power)", "high", ["bed leveling", "z-offset", "extrusion calibration"]),
            ("Post-Processing & Support Removal (Curing, Sandblasting)", "high", ["support removal", "uv curing", "sandblasting", "vapor smoothing"]),
            ("Filament, Resin & Powder Material Handling", "high", ["photopolymer resin", "powder handling", "drying filament", "safety"])
        ], ["Topology Optimization", "3D Scanner Operation", "Metal Sintering"]),

        ("Elevator & Escalator Mechanic", "Installs, inspects, and repairs passenger elevators, cables, motors, and safety brakes.", [
            ("Elevator Safety Codes (ASME A17.1)", "critical", ["asme a17.1", "elevator code", "safety circuits", "inspections"]),
            ("Traction & Hydraulic Elevator Drive Systems", "critical", ["traction elevator", "hydraulic elevator", "hoist ropes", "pumps"]),
            ("Door Operators, Interlocks & Hall Stations", "high", ["door interlocks", "door operator", "hall lanterns"]),
            ("Relay & Microprocessor Elevator Controllers", "high", ["elevator controller", "troubleshooting", "schematics"]),
            ("Governor & Emergency Safety Brake Testing", "high", ["overspeed governor", "safety brake", "counterweights"])
        ], ["Escalator Step Chain Maintenance", "Modernization Overhauls", "Cab Interior Upgrades"]),

        ("Locksmith & Physical Security Installer", "Installs high-security locks, master key systems, and electronic access strikes.", [
            ("Pin Tumbler & High-Security Lock Rekeying", "critical", ["locksmith", "rekeying", "pin tumbler", "master keying"]),
            ("Lock Picking & Non-Destructive Entry Techniques", "critical", ["lock picking", "impressioning", "bumping", "bypass"]),
            ("Commercial Hardware Installation (Mortise, Panic Bars)", "high", ["mortise lock", "panic exit device", "door closers"]),
            ("Electronic Access Control (Electric Strikes, Maglocks)", "high", ["electric strike", "magnetic lock", "keypad", "card readers"]),
            ("Automotive Key Generation & Transponder Programming", "high", ["car key programming", "transponder", "key cutting machines"])
        ], ["Safe Cracking & Combination Dialing", "Master Key System Design", "Detention Hardware"]),

        ("Glazier (Architectural Glass Installer)", "Cuts, fits, and secures structural glass, storefronts, and curtain walls.", [
            ("Glass Cutting, Edging & Safe Handling", "critical", ["glass cutting", "glass handling", "suction cups", "edging"]),
            ("Storefront Aluminum Framing & Curtain Wall Systems", "critical", ["storefront", "curtain wall", "aluminum framing"]),
            ("Commercial & Residential Glazing (Tempered, Laminated, Insulated)", "high", ["tempered glass", "laminated glass", "insulated units"]),
            ("Sealants, Gaskets & Weatherproofing (Structural Silicone)", "high", ["silicone sealant", "gaskets", "weatherproofing", "glazing tape"]),
            ("Glass Railings, Mirrors & Shower Enclosures", "high", ["glass railings", "mirrors", "frameless showers", "hardware"])
        ], ["Crane & Spider Crane Glass Lifts", "Bullet-Resistant Glass", "Skylight Installation"]),

        ("Mason & Bricklayer", "Lays bricks, concrete blocks, stone, and pours mortar for structural foundations and facades.", [
            ("Bricklaying & Concrete Masonry Unit (CMU) Blockwork", "critical", ["bricklaying", "cmu blocks", "masonry", "trowel"]),
            ("Mortar Mixing & Joint Finishing (Concave, Raked)", "critical", ["mortar mixing", "joint tooling", "portland cement", "sand ratio"]),
            ("Plumb, Level & Line String Mastery", "high", ["line blocks", "masonry line", "plumb level", "leads"]),
            ("Stone Masonry (Natural Stone, Veneer, Flagstone)", "high", ["stone masonry", "stone veneer", "chiseling", "dry stack"]),
            ("Wall Ties, Flashing & Rebar Reinforcement", "high", ["wall ties", "rebar", "grouting", "weep holes"])
        ], ["Restoration & Tuckpointing", "Fireplace Construction", "Retaining Walls"]),

        ("Tiler & Flooring Specialist", "Installs ceramic tile, hardwood, luxury vinyl plank, and ensures level subfloors.", [
            ("Subfloor Preparation & Self-Leveling Underlayment", "critical", ["subfloor prep", "self-leveling", "cement board", "un叶"]),
            ("Tile Cutting, Layout & Pattern Spacing (Porcelain, Marble)", "critical", ["tile cutter", "wet saw", "tile spacers", "layout"]),
            ("Thin-Set Mortar Application & Trowel Sizing", "high", ["thin-set", "mortar coverage", "notched trowel"]),
            ("Grouting (Cementitious, Epoxy) & Caulk Expansion Joints", "high", ["grouting", "epoxy grout", "silicone caulk"]),
            ("Waterproofing Membrane Systems (Schluter Kerdi)", "high", ["waterproofing membrane", "shower pan", "schluter kerdi"])
        ], ["Hardwood Nail-Down & Sanding", "LVP Click-Lock Flooring", "Mosaic Intricate Inlays"]),

        ("Heavy Crane & Excavator Operator", "Operates hydraulic excavators, mobile cranes, and earthmovers on construction sites.", [
            ("Excavator Operation (Trenching, Grading, Digging)", "critical", ["excavator", "earthmoving", "trenching", "grading", "bucket control"]),
            ("Mobile Crane Operation & Rigging Signals", "critical", ["crane operator", "rigging", "hand signals", "load charts"]),
            ("Site Safety, Soil Stability & Utility Call-Before-You-Dig", "high", ["811 locate", "soil stability", "trench boxes", "overhead lines"]),
            ("Pre-Operation Equipment Inspection & Daily Greasing", "high", ["equipment inspection", "fluids", "greasing", "tracks"]),
            ("GPS Laser Grading & Elevation Control", "high", ["laser level", "gps grade control", "elevation"])
        ], ["NCCCO Crane Certification", "Bulldozer Slope Work", "Demolition Attachments"]),

        ("Home Inspector", "Inspects foundations, roofs, electrical, plumbing, and compiles pre-purchase home reports.", [
            ("Home Inspection Standards of Practice (InterNACHI / ASHI)", "critical", ["home inspection", "internachi", "ashi", "inspection report"]),
            ("Roofing, Flashing & Attic Ventilation Inspection", "critical", ["roof inspection", "shingles", "attic insulation", "ventilation"]),
            ("Electrical Panel & Safety Hazard Identification", "high", ["electrical panel", "gfci", "knob and tube", "aluminum wiring"]),
            ("Plumbing, Water Heater & Drainage Checks", "high", ["plumbing inspection", "water heater", "drainage slope"]),
            ("Foundation, Structural Cracks & Moisture Diagnostics", "high", ["foundation cracks", "moisture meter", "thermal imaging", "crawlspace"])
        ], ["Radon Testing", "Termite / Wood-Destroying Organisms", "Sewer Scope Camera"]),

        ("Building Energy Auditor", "Conducts blower door depressurization tests, thermal scans, and audits energy efficiency.", [
            ("Blower Door Depressurization Testing (ACH50)", "critical", ["blower door", "ach50", "air leakage", "building envelope"]),
            ("Thermal Imaging & Infrared Heat Loss Scanning", "critical", ["thermal camera", "infrared", "thermal bridge", "insulation gaps"]),
            ("HVAC Efficiency & Duct Blaster Testing", "high", ["duct blaster", "duct leakage", "seer rating"]),
            ("Energy Modeling Software (REM/Rate, BEopt)", "high", ["energy modeling", "rem/rate", "hes score", "rebates"]),
            ("Combustion Safety & Carbon Monoxide Testing", "high", ["combustion safety", "draft test", "carbon monoxide"])
        ], ["BPI Building Analyst Certification", "HERS Rater Standards", "Solar Feasibility Analysis"]),

        ("Marine / Boat Mechanic", "Maintains inboard and outboard marine boat engines, electrical, and propeller drives.", [
            ("Outboard & Inboard Marine Engines (Yamaha, Mercury)", "critical", ["marine engine", "outboard motor", "inboard", "mercury", "yamaha"]),
            ("Marine Fuel Systems & Water Ingress Remediation", "critical", ["fuel filters", "carburetors", "water separator", "fuel injection"]),
            ("Boat 12V DC Electrical & Bilge Pump Systems", "high", ["marine wiring", "bilge pumps", "dual battery switches", "gauges"]),
            ("Sterndrive, Lower Unit & Propeller Maintenance", "high", ["lower unit", "impeller", "gear lube", "propeller pitch"]),
            ("Winterization & Shrink Wrap Preservation", "high", ["winterization", "antifreeze", "fogging oil", "shrink wrap"])
        ], ["ABYC Marine Electrical Certification", "Marine Diesel Inboards", "Fiberglass Hull Repair"]),

        ("Refrigeration Technician", "Services commercial walk-in freezers, supermarket display cases, and ice machines.", [
            ("Commercial Refrigeration Systems (Walk-in Coolers, Freezers)", "critical", ["commercial refrigeration", "walk-in freezer", "cooler", "evaporator"]),
            ("Defrost Cycles & Defrost Timers / Heaters", "critical", ["defrost cycle", "defrost timer", "electric defrost", "hot gas defrost"]),
            ("Thermostatic Expansion Valves (TXV) Adjustment", "high", ["txv", "expansion valve", "superheat adjustment"]),
            ("Leak Detection & Nitrogen Pressure Testing", "high", ["nitrogen pressure test", "electronic leak detector", "soap bubbles"]),
            ("Commercial Ice Machine Cleaning & Diagnostics", "high", ["ice machine", "water filters", "harvest cycle"])
        ], ["Supermarket Rack Systems", "CO2 / Ammonia Refrigerants", "EPA Universal Certification"]),

        ("Sheet Metal Worker", "Fabricates and installs custom metal ducts, architectural flashings, and hoods.", [
            ("Sheet Metal Layout & Geometric Pattern Development", "critical", ["sheet metal", "layout", "duct fabrication", "transitions"]),
            ("Brakes, Shears, Rolls & Metal Forming Tools", "critical", ["sheet metal brake", "shear", "slip rolls", "pittsburgh lock"]),
            ("HVAC Ductwork Assembly & S-Cleat / Drive Installation", "high", ["ductwork", "s-cleat", "drive slips", "hangers"]),
            ("Architectural Metal Flashing & Standing Seam Trim", "high", ["flashing", "standing seam", "fascia", "metal roofing"]),
            ("Spot Welding & Riveting of Ductwork", "high", ["spot welding", "riveting", "sheet metal screws"])
        ], ["CNC Plasma Table Operation", "Stainless Commercial Kitchen Hoods", "Exhaust Ducting"]),

        ("Tool and Die Maker", "Precision machines specialized dies, stamping molds, gauges, and manufacturing jigs.", [
            ("Die Construction (Stamping, Punching, Progressive Dies)", "critical", ["tool and die", "stamping die", "progressive die", "punch"]),
            ("Precision Surface Grinding to Tenths (.0001\")", "critical", ["surface grinder", "tolerances", "gauge blocks", "grinding"]),
            ("EDM (Electrical Discharge Machining - Wire & Sinker)", "high", ["edm", "wire edm", "sinker edm"]),
            ("Heat Treatment of Tool Steels (A2, D2, O1)", "high", ["heat treatment", "hardening", "tempering", "rockwell hardness"]),
            ("Tool Assembly, Tryout & Troubleshooting", "high", ["die tryout", "clearance", "alignment", "shimming"])
        ], ["Jig and Fixture Design", "Optical Comparator Inspection", "Micro-Machining"]),

        ("Non-Destructive Testing (NDT) Technician", "Inspects welds, aerospace structures, and pipelines without causing damage.", [
            ("Ultrasonic Testing (UT) & Thickness Gauging", "critical", ["ultrasonic testing", "ut", "flaw detector", "thickness gauge"]),
            ("Magnetic Particle Testing (MT) & Liquid Penetrant (PT)", "critical", ["magnetic particle", "mt", "liquid penetrant", "pt", "dye"]),
            ("Radiographic Testing (RT / X-Ray) Interpretation", "high", ["radiographic testing", "x-ray inspection", "film interpretation"]),
            ("Welding & Aerospace Defect Identification", "high", ["cracks", "inclusions", "lack of fusion", "corrosion"]),
            ("ASNT Level II Standards & Documentation Reports", "high", ["asnt", "ndt certification", "inspection reporting", "standards"])
        ], ["Eddy Current Testing (ET)", "Phased Array Ultrasonic (PAUT)", "Pipeline Integrity Audits"])
    ],

    "Healthcare, Wellness & Personal Services": [
        ("Emergency Medical Technician (EMT) / Paramedic", "Provides pre-hospital emergency medical treatment, airway management, and triage.", [
            ("Patient Assessment & Vital Signs Monitoring", "critical", ["patient assessment", "vital signs", "triage", "trauma"]),
            ("CPR, AED & Basic / Advanced Life Support", "critical", ["cpr", "aed", "bls", "als", "cardiac arrest"]),
            ("Airway Management & Oxygen Delivery (BVM, Suction)", "high", ["airway management", "bvm", "oxygen therapy", "intubation"]),
            ("Bandaging, Splinting & Spinal Immobilization", "high", ["splinting", "hemorrhage control", "tourniquet", "c-spine"]),
            ("Radio Communications & Patient Care Reports (ePCR)", "high", ["epcr", "patient care report", "radio turnover", "hand-off"])
        ], ["Paramedic Pharmacology", "Emergency Vehicle Operations (EVOC)", "IV Therapy"]),

        ("Phlebotomist", "Performs venipuncture, collects blood specimens, and ensures sterile laboratory handling.", [
            ("Venipuncture Technique & Vacutainer Blood Draw", "critical", ["phlebotomy", "venipuncture", "butterfly needle", "blood draw"]),
            ("Order of Draw & Tube Additive Knowledge", "critical", ["order of draw", "vacutainer", "anticoagulants", "edta", "clot activator"]),
            ("Patient Identification, Safety & Vein Palpation", "high", ["vein palpation", "patient verification", "median cubital"]),
            ("Specimen Labeling, Centrifugation & Processing", "high", ["specimen labeling", "centrifuge", "lab processing"]),
            ("Sterile Technique, Sharps Disposal & Biohazard Safety", "high", ["sharps disposal", "biohazard", "infection control"])
        ], ["Pediatric Phlebotomy", "Dermal Punctures (Fingersticks)", "Blood Culture Collection"]),

        ("Medical Coder & Biller", "Translates clinical diagnoses and healthcare procedures into standardized codes.", [
            ("ICD-10-CM Diagnosis Coding", "critical", ["icd-10", "icd-10-cm", "diagnosis coding", "medical coding"]),
            ("CPT & HCPCS Procedure Coding", "critical", ["cpt codes", "hcpcs", "procedure coding", "modifiers"]),
            ("Medical Terminology & Human Anatomy", "high", ["medical terminology", "anatomy", "pathology"]),
            ("Health Insurance Claims Processing (CMS-1500, UB-04)", "high", ["claims submission", "cms-1500", "denial management"]),
            ("HIPAA Compliance & Clinical Documentation Improvement", "high", ["hipaa", "documentation review", "audit"])
        ], ["AAPC CPC Certification", "EHR Billing Modules", "Appeals Management"]),

        ("Dental Assistant", "Prepares operatories, assists chairside during procedures, and takes dental radiographs.", [
            ("Chairside Dental Assisting & Four-Handed Dentistry", "critical", ["dental assistant", "chairside assisting", "four-handed dentistry", "suctioning"]),
            ("Dental X-Rays (Bitewings, Periapical, Panoramic)", "critical", ["dental x-rays", "radiography", "sensor positioning"]),
            ("Instrument Sterilization & Autoclave Operation", "high", ["autoclave", "instrument sterilization", "disinfection"]),
            ("Impression Taking & Model Pouring (Alginate)", "high", ["alginate impressions", "stone models", "bite registration"]),
            ("Dental Terminology & Tooth Charting", "high", ["tooth numbering", "charting", "periodontal charting"])
        ], ["Coronal Polishing Certification", "Temporary Crown Fabrication", "Rubber Dam Placement"]),

        ("Pharmacy Technician", "Fills prescription orders, calculates dosages, and manages pharmacy retail dispensing.", [
            ("Prescription Processing & Pharmacy Software Systems", "critical", ["pharmacy technician", "prescription filling", "dispensing"]),
            ("Pharmaceutical Calculations & Dosage Measurements", "critical", ["pharmaceutical math", "dosage calculation", "metric conversions"]),
            ("Generic and Brand Medication Name Knowledge", "high", ["brand and generic", "drug classes", "indications"]),
            ("Pill Counting, Bottle Labeling & Compounding", "high", ["pill counting", "labeling", "non-sterile compounding"]),
            ("Insurance Adjudication & Prior Authorization", "high", ["adjudication", "copays", "prior authorization", "insurance"])
        ], ["PTCB Certification", "Sterile IV Compounding", "Controlled Substance Logging"]),

        ("Radiologic / Ultrasound Technologist", "Operates medical imaging equipment to capture diagnostic scans of internal anatomy.", [
            ("Diagnostic Imaging Operation (X-Ray / Ultrasound Probe)", "critical", ["x-ray", "ultrasound", "radiologic technologist", "sonography"]),
            ("Patient Positioning & Anatomical Landmarks", "critical", ["patient positioning", "anatomy", "centering", "views"]),
            ("Radiation Safety, ALARA Principles & Shielding", "high", ["radiation safety", "alara", "lead apron", "collimation"]),
            ("Image Quality Assessment & Exposure Factors (kVp, mAs)", "high", ["kvp", "mas", "image contrast", "artifacts"]),
            ("PACS & RIS Medical Imaging Systems", "high", ["pacs", "ris", "dicom", "radiology orders"])
        ], ["ARRT / ARDMS Certification", "CT Scan Cross-Training", "Doppler Ultrasound"]),

        ("Surgical Technologist", "Prepares sterile surgical suites, passes instruments to surgeons, and maintains asepsis.", [
            ("Aseptic Technique & Operating Room Sterility", "critical", ["aseptic technique", "sterile field", "surgical technologist", "scrubbing"]),
            ("Surgical Instrumentation Knowledge & Setup", "critical", ["surgical instruments", "scalpels", "forceps", "clamps", "retractors"]),
            ("Surgical Sponge, Needle & Instrument Counts", "high", ["surgical counts", "sponge count", "patient safety"]),
            ("Anticipating Surgeon Needs During Procedures", "high", ["passing instruments", "tissue retraction", "suction"]),
            ("Draping Patients & Mayo Stand Preparation", "high", ["mayo stand", "sterile draping", "prep table"])
        ], ["CST Certification", "Laparoscopic Instrumentation", "Robotic Surgery Setup (da Vinci)"]),

        ("Optician (Eyewear Dispensing & Fitting)", "Interprets optical prescriptions, fits eyeglass frames, and selects corrective lenses.", [
            ("Optical Prescription Interpretation (Sphere, Cylinder, Axis)", "critical", ["optical prescription", "optician", "sphere", "cylinder", "axis"]),
            ("Pupillary Distance (PD) & Segment Height Measurement", "critical", ["pupillary distance", "pupillometer", "segment height"]),
            ("Lens Material Selection (Polycarbonate, High-Index, Progressive)", "high", ["progressive lenses", "high-index", "anti-reflective"]),
            ("Frame Fitting, Temple Bending & Nosepad Adjustment", "high", ["frame adjustments", "temple bending", "optical pliers"]),
            ("Lensometer Operation & Verification", "high", ["lensometer", "focimeter", "lens verification"])
        ], ["Contact Lens Dispensing", "Edging Machine Operation", "ABO Certification"]),

        ("Certified Personal Trainer", "Designs customized exercise routines, coaches biomechanics, and motivates clients.", [
            ("Exercise Programming & Periodization Cycles", "critical", ["personal training", "exercise programming", "periodization", "hypertrophy"]),
            ("Biomechanics, Movement Screening & Form Correction", "critical", ["biomechanics", "form correction", "movement screen", "posture"]),
            ("Cardiovascular & Resistance Training Principles", "high", ["resistance training", "cardio", "progressive overload"]),
            ("Fitness Assessments & Goal Setting (Body Fat, Strength)", "high", ["fitness assessment", "body composition", "vo2 max"]),
            ("Client Motivation & Accountability Coaching", "high", ["client coaching", "habit formation", "adherence"])
        ], ["NASM / ACE Certified", "Corrective Exercise", "Small Group Training"]),

        ("Strength & Conditioning Coach", "Develops power, athletic speed, agility, and injury prevention in competitive athletes.", [
            ("Olympic Weightlifting & Compound Lifts (Squat, Clean, Snatch)", "critical", ["strength and conditioning", "olympic lifting", "squat", "deadlift"]),
            ("Speed, Agility & Quickness (SAQ) Drills", "critical", ["saq", "sprint mechanics", "change of direction", "plyometrics"]),
            ("Periodization for Sports Seasons (In-Season, Off-Season)", "high", ["annual plan", "tapering", "peak performance", "volume/intensity"]),
            ("Velocity-Based Training & Force Plate Telemetry", "high", ["vbt", "force plates", "power output", "jump testing"]),
            ("Athlete Workload Management & Injury Mitigation", "high", ["workload monitoring", "readiness", "return to play"])
        ], ["CSCS Certification", "GPS Athlete Tracking", "Nutrition for Athletes"]),

        ("Sports Massage Therapist", "Applies deep tissue therapy, trigger point release, and assisted stretching on athletes.", [
            ("Deep Tissue & Sports Massage Techniques", "critical", ["sports massage", "deep tissue", "myofascial release", "effleurage"]),
            ("Trigger Point Therapy & Muscle Spasm Relief", "critical", ["trigger points", "neuromuscular therapy", "ischemic pressure"]),
            ("Musculoskeletal Anatomy & Kinesiology", "high", ["musculoskeletal anatomy", "origin and insertion", "kinesiology"]),
            ("Assisted Stretching & Proprioceptive Neuromuscular Facilitation (PNF)", "high", ["pnf stretching", "range of motion", "mobility"]),
            ("Pre-Event & Post-Event Treatment Protocols", "high", ["pre-event massage", "flush massage", "recovery"])
        ], ["Kinesiology Taping", "Cupping Therapy", "State Massage License"]),

        ("Yoga / Pilates Instructor", "Guides mindful breathing, postural alignment, core stabilization, and flow sequences.", [
            ("Yoga Asanas / Pilates Mat & Reformer Exercises", "critical", ["yoga instructor", "pilates", "asanas", "reformer", "vinyasa"]),
            ("Verbal Cueing & Safe Hands-On Adjustments", "critical", ["cueing", "alignment", "posture adjustments"]),
            ("Pranayama Breathing & Breath-to-Movement Sync", "high", ["pranayama", "breathwork", "ujjayi"]),
            ("Class Sequencing & Modification for Injuries", "high", ["sequencing", "modifications", "props", "inclusivity"]),
            ("Mindfulness, Meditation & Savasana Facilitation", "high", ["meditation", "mindfulness", "relaxation", "savasana"])
        ], ["RYT-200 / RYT-500 Certification", "Prenatal Yoga", "Sound Bath Experience"]),

        ("Nutrition & Wellness Coach", "Assists clients with macronutrient meal planning, dietary habits, and lifestyle coaching.", [
            ("Macronutrient & Caloric Energy Balance", "critical", ["nutrition coach", "macronutrients", "calories", "protein", "energy balance"]),
            ("Meal Planning & Dietary Protocols (Mediterranean, Plant-Based)", "critical", ["meal planning", "grocery guides", "dietary patterns"]),
            ("Behavior Change Psychology & Habit Coaching", "high", ["behavior change", "motivational interviewing", "habit stacking"]),
            ("Reading Nutrition Labels & Ingredient Quality", "high", ["nutrition facts", "food labels", "micronutrients"]),
            ("Hydration, Sleep & Stress Optimization Guidance", "high", ["hydration", "sleep hygiene", "wellness coaching"])
        ], ["Precision Nutrition Certified", "Sports Nutrition", "Gut Health Fundamentals"]),

        ("Esthetician / Skincare Specialist", "Performs facials, skin barrier evaluations, chemical peels, and waxing treatments.", [
            ("Skin Type Analysis & Dermatological Conditions", "critical", ["esthetician", "skin analysis", "fitzpatrick scale", "acne", "hyperpigmentation"]),
            ("Facial Protocols, Steam & Manual Extractions", "critical", ["facials", "extractions", "facial massage", "skin cleansing"]),
            ("Chemical Peels & Exfoliation (AHA, BHA, Enzymes)", "high", ["chemical peels", "glycolic acid", "salicylic acid", "exfoliation"]),
            ("Body Waxing & Hair Removal Techniques", "high", ["waxing", "hard wax", "soft wax", "brow shaping"]),
            ("Sanitation, Disinfection & Esthetic Licensing", "high", ["sanitation", "barbicide", "state board licensing", "sterilization"])
        ], ["Microdermabrasion", "LED Light Therapy", "Dermaplaning"]),

        ("Hair Stylist & Colorist", "Cuts, sculpts, bleaches, tones, and styles hair across diverse textures and lengths.", [
            ("Haircutting Techniques (Shears, Razors, Clippers)", "critical", ["haircut", "shears", "sectioning", "angles", "elevation", "layers"]),
            ("Hair Color Formulations & Color Wheel Chemistry", "critical", ["hair color", "formulation", "color wheel", "developer", "toner"]),
            ("Balayage, Foiling & Lightening Processes", "high", ["balayage", "highlights", "foiling", "bleach"]),
            ("Blowouts, Thermal Styling & Finishing", "high", ["blowout", "round brush", "curling iron", "styling products"]),
            ("Client Consultation & Hair Texture Analysis", "high", ["consultation", "hair porosity", "curl patterns", "scalp health"])
        ], ["Cosmetology License", "Keratin Smoothing Treatments", "Extension Installation"]),

        ("Barber", "Specializes in men's fades, straight razor shaves, beard sculpting, and hair texturizing.", [
            ("Clipper Fades (Skin Fades, Tapers, Blends)", "critical", ["barber", "skin fade", "taper fade", "clipper guards", "blending"]),
            ("Straight Razor Shaves & Hot Towel Treatment", "critical", ["straight razor", "hot towel", "lather", "shaving"]),
            ("Beard Trimming, Sculpting & Lineups", "high", ["beard sculpting", "lineup", "edge up", "trimmers"]),
            ("Scissor-Over-Comb & Texturizing Shears", "high", ["scissor over comb", "shear work", "texturizing"]),
            ("Sanitation & Disinfection (Barbicide, Clippercide)", "high", ["barbicide", "clippercide", "blade maintenance", "hygiene"])
        ], ["Master Barber License", "Hair Designs & Patterns", "Pomade & Product Styling"]),

        ("Makeup Artist (Editorial/Bridal/SFX)", "Applies cosmetics, contouring, bridal aesthetics, and special effects makeup.", [
            ("Face Shaping, Contouring & Color Matching Foundation", "critical", ["makeup artist", "contouring", "foundation matching", "undertones"]),
            ("Eye Makeup Artistry (Blends, Cut Crease, Liner)", "critical", ["eyeshadow", "cut crease", "eyeliner", "false lashes"]),
            ("Long-Wear Bridal & Photography Makeup", "high", ["bridal makeup", "setting spray", "hd makeup", "flash photography"]),
            ("Hygiene, Spatulas & Disposable Applicator Safety", "high", ["sanitation", "palette", "disposables", "brush cleaning"]),
            ("Skin Prep, Primers & Complexion Finishing", "high", ["skin prep", "primers", "setting powder", "highlighter"])
        ], ["Special Effects SFX (Prosthetics/Latex)", "Airbrush Makeup", "Editorial Fashion Styling"]),

        ("Nail Technician", "Provides manicures, pedicures, acrylic extensions, gel overlays, and nail art.", [
            ("Manicure & Pedicure Nail Care (Cuticles, Shaping)", "critical", ["manicure", "pedicure", "nail tech", "cuticle care", "shaping"]),
            ("Gel Polish Application & UV/LED Lamp Curing", "critical", ["gel polish", "uv lamp", "led curing", "top coat"]),
            ("Acrylic & Hard Gel Nail Extensions", "high", ["acrylic nails", "monomer", "polymer powder", "forms", "tips"]),
            ("Electric Nail File (E-File) Operation & Bits", "high", ["e-file", "drill bits", "callus removal", "debulking"]),
            ("Nail Art, French Tips & Chrome Finishes", "high", ["nail art", "french tip", "chrome powder", "rhinestones"])
        ], ["Nail Sanitation Standards", "Dip Powder Techniques", "Pedicure Massage"]),

        ("Veterinary Technician", "Assists veterinarians with animal restraint, clinical medications, IVs, and surgical prep.", [
            ("Animal Restraint & Low-Stress Handling", "critical", ["animal restraint", "veterinary technician", "handling", "canine", "feline"]),
            ("Venipuncture & IV Catheter Placement in Animals", "critical", ["iv catheter", "blood draw", "jugular venipuncture", "cephalic"]),
            ("Administering Medications (Oral, Subcutaneous, IM, IV)", "high", ["medication administration", "dosage calculations", "injections"]),
            ("Anesthesia Monitoring & Vital Signs during Surgery", "high", ["anesthesia monitoring", "spO2", "end-tidal co2", "extubation"]),
            ("Veterinary Laboratory Diagnostics (Fecals, Urinalysis, Smears)", "high", ["urinalysis", "fecal float", "blood smears", "cytology"])
        ], ["Vet Tech Certification (CVT/RVT)", "Veterinary Dental Scaling", "Radiograph Positioning"]),

        ("Dog Trainer & Behaviorist", "Teaches obedience commands, corrects behavioral issues, and modifies canine aggression.", [
            ("Operant Conditioning & Positive Reinforcement", "critical", ["dog training", "positive reinforcement", "clicker training", "operant conditioning"]),
            ("Basic & Advanced Obedience (Sit, Stay, Recall, Heel)", "critical", ["obedience training", "recall", "loose leash walking"]),
            ("Canine Body Language & Stress Signals", "high", ["dog body language", "calming signals", "bite prevention"]),
            ("Behavior Modification (Reactivity, Separation Anxiety)", "high", ["reactivity", "desensitization", "counter-conditioning"]),
            ("Human Client Coaching & Consistency Training", "high", ["client coaching", "handler mechanics", "homework plans"])
        ], ["CPDT-KA Certification", "Agility Training", "Service Dog Task Training"])
    ],

    "Culinary, Hospitality & Specialized Craft": [
        ("Line Cook / Sous Chef", "Executes high-volume station prep, knife cuts, pan cooking, and kitchen service.", [
            ("Knife Skills (Julienne, Brunoise, Chiffonade)", "critical", ["knife skills", "knife cuts", "chef knife", "mise en place"]),
            ("Cooking Techniques (Sauté, Grill, Braise, Roast, Fry)", "critical", ["saute", "grilling", "braising", "roasting", "cooking techniques"]),
            ("Kitchen Station Management & Mise en Place", "high", ["station management", "mise en place", "prep list", "ticket timing"]),
            ("Food Safety, Temp Checks & HACCP Sanitation (ServSafe)", "high", ["servsafe", "haccp", "internal temperature", "cross-contamination"]),
            ("Sauces, Stocks & Seasoning Balances", "high", ["mother sauces", "pan sauces", "stocks", "tasting", "seasoning"])
        ], ["Expediting the Pass", "Kitchen Leadership", "Cost of Goods Kitchen Waste Reduction"]),

        ("Pastry Chef & Chocolatier", "Crafts baked pastries, laminated doughs, chocolate tempering, and plated desserts.", [
            ("Baking Science & Baker's Percentages", "critical", ["pastry chef", "baking science", "bakers percentages", "scaling"]),
            ("Laminated Doughs (Croissants, Puff Pastry, Danish)", "critical", ["laminated dough", "croissants", "puff pastry", "butter block"]),
            ("Chocolate Tempering & Confections", "high", ["chocolate tempering", "seeding method", "bonbons", "ganache"]),
            ("Custards, Creams & Mousse (Pastry Cream, Bavarian)", "high", ["custard", "pastry cream", "mousse", "meringue"]),
            ("Plated Dessert Composition & Presentation", "high", ["plated desserts", "garnishes", "sugar work", "piping"])
        ], ["Wedding Cake Construction", "Artisan Gelato", "Sourdough Fermentation"]),

        ("Artisan Baker", "Bakes sourdough breads, hearth loaves, and manages natural fermentation processes.", [
            ("Wild Yeast Sourdough Starter Maintenance & Fermentation", "critical", ["sourdough", "starter", "wild yeast", "fermentation"]),
            ("Flour Types, Hydration Levels & Gluten Development", "critical", ["hydration", "gluten development", "autolyse", "flour proteins"]),
            ("Dough Mixing, Bulk Fermentation, Stretch-and-Fold", "high", ["bulk fermentation", "stretch and fold", "proofing"]),
            ("Dough Shaping (Batards, Boules, Baguettes)", "high", ["shaping", "boules", "batards", "baguettes"]),
            ("Deck Oven Baking, Steam Injection & Scoring (Lame)", "high", ["scoring", "bread lame", "deck oven", "steam injection"])
        ], ["Wood-Fired Brick Ovens", "Ancient Grains", "Commercial Bread Production"]),

        ("Specialty Coffee Barista & Roaster", "Dials in espresso grinders, steams silky microfoam, and roasts coffee beans.", [
            ("Espresso Extraction & Grinder Dialing (Yield, Time)", "critical", ["espresso extraction", "barista", "grinder dialing", "ratio", "tamping"]),
            ("Milk Steaming & Latte Art Microfoam Pouring", "critical", ["milk steaming", "microfoam", "latte art", "pitcher control"]),
            ("Manual Brew Methods (V60, Chemex, Aeropress)", "high", ["pour over", "v60", "chemex", "aeropress", "bloom"]),
            ("Coffee Bean Origin Characteristics & Sensory Cupping", "high", ["coffee origins", "cupping", "tasting notes", "specialty coffee"]),
            ("Commercial Espresso Machine Maintenance (Backflushing)", "high", ["backflushing", "group head cleaning", "steam wand maintenance"])
        ], ["Coffee Roasting Curves", "SCA Barista Certification", "Water Chemistry for Coffee"]),

        ("Mixologist / Craft Bartender", "Mixes balanced craft cocktails, house syrups, and delivers hospitality.", [
            ("Cocktail Families & Ratios (Sours, Highballs, Stirred)", "critical", ["craft cocktails", "mixology", "cocktail ratios", "jigger"]),
            ("Spirits Knowledge (Whiskey, Gin, Rum, Tequila, Agave)", "critical", ["spirits", "bourbon", "mezcal", "liqueurs"]),
            ("Shaking, Stirring, Straining & Ice Carving Techniques", "high", ["shaking", "stirring", "hawthorne strainer", "ice carving"]),
            ("House Syrups, Shrubs & Garnish Crafting", "high", ["simple syrup", "shrubs", "bitters", "garnishes", "infusions"]),
            ("High-Volume Bar Speed, TABS & TIPS Certification", "high", ["bar speed", "pos operation", "responsible serving", "tips certified"])
        ], ["Clarified Cocktails", "Smoked Cocktails", "Bar Inventory Control"]),

        ("Sommelier", "Curates fine wine lists, advises wine pairings, and stores wine collections.", [
            ("Global Wine Regions & Terroir (Old World / New World)", "critical", ["sommelier", "wine regions", "bordeaux", "napa", "terroir"]),
            ("Grape Varieties & Viticulture Characteristics", "critical", ["grape varietals", "cabernet", "pinot noir", "chardonnay"]),
            ("Blind Tasting & Systematic Sensory Evaluation (Court of Master Sommeliers)", "high", ["blind tasting", "acid", "tannin", "aromas"]),
            ("Food & Wine Pairing Chemistry", "high", ["food and wine pairing", "flavor balance", "acidity match"]),
            ("Wine Cellar Storage, Decanting & Formal Service", "high", ["decanting", "corkage", "cellar temperature", "glassware"])
        ], ["CMS / WSET Level 3 Certification", "Champagne & Sparkling Methods", "Fortified Wines (Port, Sherry)"]),

        ("Butcher / Meat Cutter", "Breaks down whole animal carcasses, trims cuts, and crafts house sausages.", [
            ("Whole Animal Seam Butchery & Primal Cuts", "critical", ["butcher", "primal cuts", "seam butchery", "carcass breakdown"]),
            ("Boning Knife Skills & Precision Trimming", "critical", ["boning knife", "meat trimming", "yield optimization", "knife sharpening"]),
            ("Meat Grinding & Sausage Making (Casing, Seasoning)", "high", ["sausage making", "meat grinder", "casings", "emulsification"]),
            ("Bandsaw, Meat Slicer & Heavy Meat Processing Machinery", "high", ["bandsaw", "meat slicer", "cubing machine"]),
            ("Cold Chain Meat Storage & USDA / Health Guidelines", "high", ["usda guidelines", "cold storage", "dry aging", "sanitation"])
        ], ["Dry-Aging Steaks", "Charcuterie Curing", "Kosher / Halal Butchery"]),

        ("Florist & Floral Event Designer", "Arranges fresh flower compositions, bridal bouquets, and large floral installations.", [
            ("Floral Design Principles (Focal Point, Rhythm, Scale)", "critical", ["floral design", "flower arrangement", "color balance", "focal point"]),
            ("Flower Processing, Stem Cutting & Hydration Conditioning", "critical", ["flower conditioning", "hydration", "stem stripping", "preservation"]),
            ("Bouquet Construction (Spiral Hand-Tied, Foam Arrangements)", "high", ["hand-tied bouquet", "oasis foam", "boutonniere", "corsage"]),
            ("Large Installations (Arches, Hanging Clouds, Centerpieces)", "high", ["floral arch", "installations", "centerpieces", "wire mechanics"]),
            ("Flower Sourcing, Cold Storage & Seasonal Availability", "high", ["flower market", "cold room", "perishables", "seasonality"])
        ], ["Bridal Consultation", "Eco-Friendly Foam-Free Mechanics", "Pressed Dried Floral Preservation"]),

        ("Tailor & Bespoke Garment Maker", "Alters, cuts, fits, and sews bespoke suiting and tailored clothing.", [
            ("Fitting Alterations (Hemming, Tapering, Taking In/Out)", "critical", ["tailoring", "alterations", "hemming", "taking in seams", "fittings"]),
            ("Industrial Sewing Machine & Serger Operation", "critical", ["industrial sewing machine", "serger", "overlock", "presser foot"]),
            ("Bespoke Pattern Drafting & Body Measurements", "high", ["pattern drafting", "body measurements", "muslin mockups"]),
            ("Hand Stitching (Basting, Blind Hem, Pad Stitching)", "high", ["hand stitching", "blind hem", "pad stitching", "buttonholes"]),
            ("Fabric Pressing, Ironing & Interfacing Shaping", "high", ["steam pressing", "tailor ham", "interfacing", "canvas"])
        ], ["Suit Jacket Canvas Construction", "Tuxedo Details", "Leather Sewing"]),

        ("Cobbler & Leatherworker", "Repairs shoes, resoles footwear, and crafts handmade leather goods.", [
            ("Shoe Resoling & Heel Replacement (Goodyear Welt, Blake Stitch)", "critical", ["cobbler", "shoe repair", "goodyear welt", "resole", "heels"]),
            ("Leather Stitching (Saddle Stitching & Leather Sewing Machines)", "critical", ["saddle stitch", "leather sewing", "awl", "waxed thread"]),
            ("Leather Types & Tannages (Vegetable Tanned, Chrome Tanned)", "high", ["leather craft", "vegetable tanned", "leather thickness", "grain"]),
            ("Edge Finishing, Burnishing & Skiving", "high", ["edge burnishing", "tokonole", "skiving", "beveling"]),
            ("Shoe Lasting, Stretching & Leather Polishing", "high", ["shoe stretching", "saphir polish", "patina", "conditioning"])
        ], ["Custom Boot Making", "Bag Construction", "Hardware Riveting"]),

        ("Watchmaker & Horology Technician", "Disassembles, cleans, oils, and calibrates mechanical watch movements.", [
            ("Mechanical Watch Movement Disassembly & Assembly", "critical", ["watchmaker", "horology", "movement disassembly", "escapement", "mainspring"]),
            ("Micro-Tweezers & Screwdriver Precision Handling", "critical", ["watch tweezers", "loupe", "micro screwdrivers", "parts handling"]),
            ("Ultrasonic Cleaning & Synthetic Lubricant Oiling", "high", ["ultrasonic cleaning", "oiling", "moebius oil", "jewels"]),
            ("Timing Machine Calibration (Timegrapher, Beat Error, Rate)", "high", ["timegrapher", "beat error", "amplitude", "rate regulation"]),
            ("Case Refinishing, Waterproof Pressure Testing & Gaskets", "high", ["pressure testing", "gaskets", "case polishing", "crystal replacement"])
        ], ["WOSTEP Certification", "Complications (Chronograph)", "Hairspring Truing"]),

        ("Bench Jeweler & Goldsmith", "Fabricates, solders, casts, and sets precious stones into fine jewelry.", [
            ("Jewelry Soldering & Torch Flame Control", "critical", ["jewelry soldering", "micro torch", "flux", "solder pick"]),
            ("Stone Setting (Prong, Bezel, Pave)", "critical", ["stone setting", "prong setting", "bezel", "gemstones", "diamonds"]),
            ("Metal Piercing with Jeweler's Saw & Filing", "high", ["jewelers saw", "precision files", "clean cuts"]),
            ("Lost-Wax Casting & Rubber Mold Making", "high", ["lost wax casting", "investment casting", "centrifugal casting"]),
            ("Precious Metal Finishing, Polishing & Ultrasonic Cleaning", "high", ["buffing wheel", "rouge", "gold", "platinum", "ultrasonic"])
        ], ["Laser Welding for Jewelry", "Ring Sizing", "CAD Jewelry Design (MatrixGold)"]),

        ("Luthier (String Instrument Maker/Repairer)", "Builds, sets up, refrets, and restores acoustic and electric guitars and violins.", [
            ("Guitar / Violin Setup (Intonation, Action, Truss Rod)", "critical", ["luthier", "guitar setup", "truss rod", "action", "intonation"]),
            ("Fretwork (Leveling, Crowning, Dressing, Refretting)", "critical", ["fret leveling", "crowning", "refretting", "fret wire"]),
            ("Nut & Saddle Carving (Bone, Tusq)", "high", ["nut carving", "saddle", "string slots", "radius gauge"]),
            ("Tonewood Selection & Acoustic Bracing", "high", ["tonewoods", "spruce", "rosewood", "bracing", "tap tone"]),
            ("Electronics Wiring (Pickups, Pots, Switches)", "high", ["pickup wiring", "soldering", "potentiometers", "shielding"])
        ], ["French Polish Shellac Application", "Neck Resets", "Crack Repair & Splines"]),

        ("Scuba Diving Instructor", "Trains divers in underwater physics, physiology, dive tables, and emergency open water skills.", [
            ("PADI / SSI Dive Instructor Certification Standards", "critical", ["padi instructor", "ssi", "dive instruction", "dive standards"]),
            ("Underwater Dive Physics, Decompression & Tables", "critical", ["dive tables", "decompression sickness", "boyles law", "nitrox"]),
            ("Open Water Skills (Regulator Recovery, Mask Clearing, Buoyancy)", "high", ["neutral buoyancy", "mask clearing", "regulator recovery", "safety stops"]),
            ("Emergency Rescue Procedures & Out-of-Air Ascents", "high", ["rescue diver", "csea", "emergency ascent", "oxygen administration"]),
            ("Scuba Gear Maintenance (Regulators, BCD, Cylinders)", "high", ["regulator servicing", "bcd", "tanks", "hydrostatic test"])
        ], ["Night Diving Specialty", "Deep Diver Certification", "Marine Ecology Teaching"]),

        ("Wilderness & Adventure Guide", "Leads expeditions through backcountry trails, navigates terrain, and oversees safety.", [
            ("Wilderness First Responder (WFR) & Emergency Triage", "critical", ["wilderness first responder", "wfr", "backcountry first aid", "evacuation"]),
            ("Topographic Map, Compass & GPS Navigation", "critical", ["topographic map", "orienteering", "compass", "backcountry navigation"]),
            ("Leave No Trace (LNT) Ethics & Outdoor Camping Logistics", "high", ["leave no trace", "lnt", "campsite selection", "camp cooking"]),
            ("Weather Interpretation & Mountain Hazard Assessment", "high", ["weather assessment", "avalanche safety", "hypothermia", "river crossings"]),
            ("Group Leadership & Wilderness Risk Management", "high", ["group management", "expedition planning", "risk mitigation"])
        ], ["Rock Climbing Anchor Building", "Whitewater Raft Guiding", "Survival Shelter Construction"])
    ]
}

def generate_catalog():
    roles = []
    total_count = 0
    for cat_name, role_list in ROLES_BY_CATEGORY.items():
        for item in role_list:
            title = item[0]
            desc = item[1]
            req_skills = item[2]
            opt_skills = item[3] if len(item) > 3 else []
            role_id = slugify(title)
            
            structured_req = []
            for s in req_skills:
                s_name = s[0]
                s_imp = s[1]
                s_aliases = s[2]
                structured_req.append({
                    "name": s_name,
                    "importance": s_imp,
                    "description": f"Demonstrated proficiency in {s_name} with practical execution and domain standards.",
                    "aliases": s_aliases
                })
                
            roles.append({
                "id": role_id,
                "title": title,
                "category": cat_name,
                "description": desc,
                "required_skills": structured_req,
                "optional_skills": opt_skills
            })
            total_count += 1
            
    print(f"Generated {total_count} roles across {len(ROLES_BY_CATEGORY)} categories.")
    catalog = {"roles": roles}
    
    with open("roles.json", "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)
    print("Saved roles.json successfully.")

if __name__ == "__main__":
    generate_catalog()
