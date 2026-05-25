from flask import Flask, render_template, request, send_from_directory
import datetime
import os

app = Flask(__name__)

# ── Internationalized Site Data ──────────────────────────────────────
SITE_DATA = {
    "en": {
        "ui": {
            "title_suffix": "SRE & AI Platform Engineer",
            "nav_bio": "Bio",
            "nav_projects": "Projects",
            "nav_skills": "Stack",
            "nav_cv": "📄 Resume",
            "hero_badge": "☁️ SRE & AI Platform Engineer",
            "hero_greeting": "I'm",
            "btn_cv": "📄 Download Resume",
            "projects_title": "Featured Projects",
            "projects_subtitle": "Production architectures, intelligent agents, and cloud-native labs",
            "btn_project": "View Project",
            "skills_title": "Tech Stack",
            "skills_subtitle": "Tools and platforms I use daily in production",
            "footer_made_with": "Made with ❤️ in Mexico City",
            "lang_toggle_url": "?lang=es",
            "lang_toggle_text": "🇪🇸 ES"
        },
        "profile": {
            "name": "Miguel Angel Carvajal",
            "title": "SRE & AI Platform Engineer",
            "bio": "I build and operate cloud-native platforms at scale. "
                   "8+ years shipping production infrastructure — from EKS clusters serving AI workloads "
                   "to CI/CD pipelines, observability stacks, and incident response. "
                   "Currently focused on AI platform reliability and automation.",
            "location": "Mexico City",
            "email": "krva@ciencias.unam.mx",
            "social": {
                "linkedin": "https://www.linkedin.com/in/miguel-carvajal",
                "github": "https://github.com/krvax",
            }
        },
        "projects": [
            {
                "id": 1,
                "title": "AI Platform on EKS",
                "category": "AI & Cloud",
                "description": "Generative platform in production on EKS integrating AWS Bedrock "
                               "(Claude, Titan), MCP Gateway as a Helm chart, and Redis/PostgreSQL "
                               "for persistence — serving 500+ internal users.",
                "link": "https://github.com/krvax/epam-aws-devops-prep",
                "icon": "🤖"
            },
            {
                "id": 2,
                "title": "Cóatl Finance Agent",
                "category": "AI Agents",
                "description": "Advanced reasoning agent deployed on Vertex AI for "
                               "financial market analysis using Gemini Enterprise.",
                "link": "https://vertexaisearch.cloud.google.com/home/cid/947f744a-0690-499b-82a5-22d91d67b103/r/agent/8544371628222189320",
                "icon": "🐍"
            },
            {
                "id": 3,
                "title": "Cloud Native Labs",
                "category": "Kubernetes & SRE",
                "description": "Comprehensive sandbox for Kubernetes troubleshooting, "
                               "ArgoCD GitOps pipelines, and Istio Service Mesh configurations.",
                "link": "https://github.com/krvax/AI-Club-Condesa-Workshops/tree/main/workshops",
                "icon": "☁️"
            },
            {
                "id": 4,
                "title": "Conference Site Generator",
                "category": "Backend",
                "description": "Dynamic web app deployment framework using Flask and Cloud Run, "
                               "built as part of the AI Condesa engineering workshops.",
                "link": "https://github.com/krvax/AI-Club-Condesa-Workshops/tree/main/projects",
                "icon": "🚀"
            }
        ],
        "skills": {
            "AI & LLM": ["AWS Bedrock", "Vertex AI", "Gemini", "LangChain", "Vector DBs"],
            "Cloud & Infra": ["AWS", "GCP", "Kubernetes (EKS/GKE)", "Terraform", "Docker"],
            "SRE & DevOps": ["GitHub Actions", "ArgoCD", "Prometheus", "Grafana", "Linux"],
            "Dev": ["Python", "Flask", "Bash", "Node.js", "Git"]
        }
    },
    "es": {
        "ui": {
            "title_suffix": "SRE & AI Platform Engineer",
            "nav_bio": "Bio",
            "nav_projects": "Proyectos",
            "nav_skills": "Stack",
            "nav_cv": "📄 CV",
            "hero_badge": "☁️ SRE & AI Platform Engineer",
            "hero_greeting": "Soy",
            "btn_cv": "📄 Descargar CV",
            "projects_title": "Proyectos Destacados",
            "projects_subtitle": "Arquitecturas en producción, agentes inteligentes y laboratorios cloud-native",
            "btn_project": "Ver Proyecto",
            "skills_title": "Stack Tecnológico",
            "skills_subtitle": "Herramientas y plataformas que uso a diario en producción",
            "footer_made_with": "Hecho con ❤️ en Ciudad de México",
            "lang_toggle_url": "?lang=en",
            "lang_toggle_text": "🇺🇸 EN"
        },
        "profile": {
            "name": "Miguel Angel Carvajal",
            "title": "SRE & AI Platform Engineer",
            "bio": "Construyo y opero plataformas cloud-native a escala. "
                   "8+ años llevando infraestructura a producción — desde clusters EKS sirviendo workloads de AI "
                   "hasta pipelines CI/CD, stacks de observabilidad e incident response. "
                   "Actualmente enfocado en reliability de plataformas AI y automatización.",
            "location": "Ciudad de México",
            "email": "krva@ciencias.unam.mx",
            "social": {
                "linkedin": "https://www.linkedin.com/in/miguel-carvajal",
                "github": "https://github.com/krvax",
            }
        },
        "projects": [
            {
                "id": 1,
                "title": "AI Platform on EKS",
                "category": "AI & Cloud",
                "description": "Plataforma generativa en producción sobre EKS integrando AWS Bedrock "
                               "(Claude, Titan), MCP Gateway como Helm chart, y Redis/PostgreSQL "
                               "para persistencia — sirviendo 500+ usuarios internos.",
                "link": "https://github.com/krvax/epam-aws-devops-prep",
                "icon": "🤖"
            },
            {
                "id": 2,
                "title": "Agente Cóatl Finanzas",
                "category": "AI Agents",
                "description": "Agente de razonamiento avanzado desplegado en Vertex AI para "
                               "análisis de mercados financieros con Gemini Enterprise.",
                "link": "https://vertexaisearch.cloud.google.com/home/cid/947f744a-0690-499b-82a5-22d91d67b103/r/agent/8544371628222189320",
                "icon": "🐍"
            },
            {
                "id": 3,
                "title": "Cloud Native Labs",
                "category": "Kubernetes & SRE",
                "description": "Entorno completo de experimentación para troubleshooting en Kubernetes, "
                               "pipelines GitOps con ArgoCD y configuración de Istio Service Mesh.",
                "link": "https://github.com/krvax/AI-Club-Condesa-Workshops/tree/main/workshops",
                "icon": "☁️"
            },
            {
                "id": 4,
                "title": "Conference Site Generator",
                "category": "Backend",
                "description": "Framework de despliegue dinámico de aplicaciones web usando Flask "
                               "y Cloud Run, construido como parte de los workshops de AI Condesa.",
                "link": "https://github.com/krvax/AI-Club-Condesa-Workshops/tree/main/projects",
                "icon": "🚀"
            }
        ],
        "skills": {
            "AI & LLM": ["AWS Bedrock", "Vertex AI", "Gemini", "LangChain", "Vector DBs"],
            "Cloud & Infra": ["AWS", "GCP", "Kubernetes (EKS/GKE)", "Terraform", "Docker"],
            "SRE & DevOps": ["GitHub Actions", "ArgoCD", "Prometheus", "Grafana", "Linux"],
            "Dev": ["Python", "Flask", "Bash", "Node.js", "Git"]
        }
    }
}

# ── Rutas ───────────────────────────────────────────────────────────
@app.route("/")
def home():
    # Detect language from query parameter, default to "en"
    lang = request.args.get("lang", "en")
    if lang not in ["en", "es"]:
        lang = "en"
        
    data = SITE_DATA[lang]
    return render_template(
        "index.html", 
        lang=lang,
        ui=data["ui"],
        profile=data["profile"],
        projects=data["projects"],
        skills=data["skills"],
        datetime=datetime
    )

@app.route("/download-cv")
def download_cv():
    # Since the PDF is already in English, we just serve the existing file.
    # If a Spanish version is added later, we can use the 'lang' parameter to serve different files.
    filename = "CV-Miguel-Carvajal.pdf"
    assets_dir = os.path.join(app.root_path, 'static', 'assets')
    return send_from_directory(assets_dir, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
