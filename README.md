# 🏥 Système Intelligent de Triage des Patients RAG + Automatisation

**Auteur :** Wael Etteyeb  
**École :** ENIT (École Nationale d’Ingénieurs de Tunis)  
**Entreprise :** Technozor 

## 🎯 Objectif du projet

Ce projet met en œuvre un **système intelligent de triage médical** basé sur l’**Intelligence Artificielle** et l’**automatisation**, permettant d’analyser les symptômes des patients et de leur attribuer un **niveau de priorité médicale**.

L’application combine :
- un **backend FastAPI** pour l’orchestration,
- une architecture **RAG (Retrieval-Augmented Generation)** pour la compréhension contextuelle,
- et une intégration **automatisée (n8n)** pour déclencher des actions (notifications, rendez-vous, etc.).

## ⚙️ Stack technique

| Domaine | Technologies utilisées |
|----------|------------------------|
| **Langage principal** | Python ≥ 3.10 |
| **Framework Backend** | FastAPI |
| **IA & NLP** |  Groq API, embeddings vectoriels |
| **Automatisation** | n8n (webhooks, e-mails, planification) |
| **Base de données** | ChromaDB  |
| **Visualisation** | Streamlit / Interface de triage |


| Fonction                             | Description                                                                  |
| ------------------------------------ | ---------------------------------------------------------------------------- |
| 🩺 **Triage IA**                     | Analyse des symptômes patients et classification automatique (niveau 1–5)    |
| 🧾 **Extraction de guidelines**      | Lecture et indexation de documents médicaux (PDF, JSON)                      |
| 🔍 **Recherche contextuelle (RAG)**  | Utilisation d’embeddings  pour fournir des recommandations précises   |
| 🤖 **Agents IA spécialisés**         | Dialogue entre “Médecin” et “Réceptionniste” pour prise de décision          |
| 🔗 **Automatisation n8n**            | Envoi automatique de mails / réservations / suivi patient                    |

