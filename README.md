# 🏥 Système Intelligent de Triage des Patients — FastAPI + RAG + Automatisation

**Auteur :** Wael Etteyeb  
**École :** ENIT (École Nationale d’Ingénieurs de Tunis)  
**Entreprise :** Technozor 
**Contact :** [wael.etteyeb@etudiant-enit.utm.tn](mailto:wael.etteyeb@etudiant-enit.utm.tn) 

## 🎯 Objectif du projet

Ce projet met en œuvre un **système intelligent de triage médical** basé sur l’**Intelligence Artificielle** et l’**automatisation**, permettant d’analyser les symptômes des patients et de leur attribuer un **niveau de priorité médicale**.

L’application combine :
- un **backend FastAPI** pour l’orchestration,
- une architecture **RAG (Retrieval-Augmented Generation)** pour la compréhension contextuelle,
- et une intégration **automatisée (n8n)** pour déclencher des actions (notifications, rendez-vous, etc.).

Ce projet illustre la capacité à **industrialiser une IA appliquée**, du prétraitement à la mise en production — compétences directement alignées avec les missions **Prime Analytics / Prime IA**.

---

## ⚙️ Stack technique

| Domaine | Technologies utilisées |
|----------|------------------------|
| **Langage principal** | Python ≥ 3.10 |
| **Framework Backend** | FastAPI |
| **IA & NLP** | LangChain, FAISS, Groq API, embeddings vectoriels |
| **Automatisation** | n8n (webhooks, e-mails, planification) |
| **Base de données** | ChromaDB (SQLite vector store) |
| **Infrastructure** | Docker, .env configuration |
| **Tests & CI/CD** | Pytest, GitHub Actions (prévu) |
| **Visualisation** | Streamlit / Interface de triage |
| **Documentation** | Markdown, PDF (`/docs/Rapport Technozor FINAL.pdf`) |

---

## 🧩 Structure du projet


---

## 🚀 Installation et exécution

### 🧱 Prérequis
- Python ≥ 3.10  
- pip / virtualenv  
- (Optionnel) Docker / docker-compose  
- Variables d’environnement dans `.env` (ex : clés API Groq / n8n)

### 🔧 Installation locale



# Cloner le projet
git clone https://github.com/waeletteyeb/triage-ia-fastapi-rag.git
cd triage-ia-fastapi-rag

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate   # ou .\venv\Scripts\activate sous Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer l’API
uvicorn app.main:app --reload


| Fonction                             | Description                                                                  |
| ------------------------------------ | ---------------------------------------------------------------------------- |
| 🩺 **Triage IA**                     | Analyse des symptômes patients et classification automatique (niveau 1–5)    |
| 🧾 **Extraction de guidelines**      | Lecture et indexation de documents médicaux (PDF, JSON)                      |
| 🔍 **Recherche contextuelle (RAG)**  | Utilisation d’embeddings + FAISS pour fournir des recommandations précises   |
| 🤖 **Agents IA spécialisés**         | Dialogue entre “Médecin” et “Réceptionniste” pour prise de décision          |
| 🔗 **Automatisation n8n**            | Envoi automatique de mails / réservations / suivi patient                    |
| 📊 **Documentation & visualisation** | Schémas, architecture, et métriques dans `/Images de rapport et soutenances` |
