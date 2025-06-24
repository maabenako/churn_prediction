# 📉 Churn Prediction com Big Data & PySpark

Este projeto implementa uma pipeline de previsão de **churn (cancelamento de clientes)** utilizando **Kedro**, **PySpark**, e **Streamlit**, com foco em organização modular, escalabilidade e visualizações avançadas.

---

## 🚀 Tecnologias Utilizadas

- [Kedro](https://kedro.org/)
- [Apache Spark](https://spark.apache.org/)
- [MLlib](https://spark.apache.org/mllib/)
- [Streamlit](https://streamlit.io/)
- Scikit-learn, Pandas, Seaborn, Matplotlib

---

## 📁 Estrutura do Projeto
```bash
churn_spark/
├── conf/ # Configurações do projeto Kedro
├── data/
│ ├── 01_raw/ # Dados brutos
│ ├── 02_intermediate/ # Pré-processamento inicial
│ ├── 03_primary/ # Dados limpos
│ ├── 04_feature/ # Features tratadas
│ ├── 05_model_input/ # Dados balanceados prontos para modelar
│ ├── 06_models/ # Modelos salvos
│ ├── 08_reporting/ # Métricas e outputs
│ └── 09_visuals/ # Gráficos para Streamlit
├── notebooks/ # Notebooks de apoio
├── src/
│ └── churn_analytics/
│ ├── pipelines/ # Módulos: ingestion, eda, modeling, inferência, dataviz
├── streamlit_app/ # Aplicação de dashboard
├── requirements.txt
└── README.md
```
---

## ⚙️ Como Executar

### 1. Crie e ative o ambiente
```bash
conda create -n churn python=3.10 -y
conda activate churn
```
### 2. Instale as dependências
```bash
pip install -r requirements.txt
```
> Certifique-se de que o Java está instalado para rodar o Spark.

### 3. Execute a pipeline
```bash
kedro run
```
> Isso irá processar os dados, treinar o modelo e gerar gráficos.

### 4. Inicie o dashboard
```bash
streamlit run streamlit_app/app.py
```
---

## 📊 Funcionalidades

### 🔎 EDA + Visualizações
- Mapa de correlação
- Distribuições por variável
- Boxplots por Churn

### 🧠 Modelagem
- Regressão Logística com Spark MLlib
- Métricas avançadas: AUC, Precision, Recall, F1-score, Confusion Matrix

### 📉 Dashboard Interativo
- Desenvolvido com Streamlit
- Visualização simples e funcional para stakeholders
- Gráficos salvos em "data/09_visuals"

---

## 💡 Insights

- Identificação de padrões de cancelamento de clientes
- Correlações entre variáveis críticas e churn
- Visualização clara da performance do modelo

---

## 🌐 Acesso ao Dashboard

Acesse via navegador:
```bash
http://localhost:8501
```
---

## 🧑‍💻 Autoria

Desenvolvido com 💜 por [@maabenako](https://github.com/maabenako)
