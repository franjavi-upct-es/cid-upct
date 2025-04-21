import numpy as np
import praw
import json 
import re
from datetime import datetime
import os
import warnings
warnings.filterwarnings("ignore")

from sklearn.ensemble import RandomForestClassifier

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def cargar_corpus(ruta_json):
    """
    Carga un archivo JSON que contiene un diccionario de subreddits a hilos.

    :param ruta_json: Ruta al archivo JSON.
    :return: Diccionario con estructura { subreddit: [hilos, ...], ... }.
    """
    with open(ruta_json, 'r', encoding='utf-8') as f:
        return json.load(f)

# ---------------------------------------------
# Ejercicio 1: Compilación del corpus y procesamiento léxico
# ---------------------------------------------
reddit = praw.Reddit(
    client_id='ShOBXaW1U-PMc1hhr88znw',
    client_secret='o12KLkUR18D5wZqnPxG5lp8jQFszgg',
    user_agent='pln-practica-2025'
)

def convertir_fecha(utc):
    """
    Convierte un timestamp UTC (float) a una cadena legible "YYYY-MM-DD HH:MM:SS".

    :param utc: tiempo en formato UNIX UTC.
    :return: Cadena con fecha y hora en UTC.
    """
    return datetime.fromtimestamp(utc).strftime('%Y-%m-%d %H:%M:%S')

def extraer_corpus_raw(subreddit_nombre, limite_hilos=20, limite_comentarios=None):
    """
    Extrae hilos y comentarios de un subreddit, sin filtrado temático.

    :param subreddit_nombre: nombre del subreddit (`str`)
    :param limite_hilos: número máximo de hilos a extraer
    :param limite_comentarios: máximo de comentarios por hilo (`None` = todos)
    :return: lista de dicts con campos:
        `title`, `flair`, `author`, `date`, `score`, `description`, `comments`.
    """
    subreddit = reddit.subreddit(subreddit_nombre)
    resultados = [] # Lista donde almacenamos la información de cada hilo

    # Recorremos los hilos 'hot' del subreddit hasta el límite indicado
    for post in subreddit.hot(limit=limite_hilos):
        # Creamos el diccionario base con información del hilo
        hilo = {
            'title': post.title,
            'flair': post.link_flair_text,
            'author': str(post.author),
            'date': convertir_fecha(post.created_utc),
            'score': post.score,
            'description': post.selftext,
            'comments': [] #Lista para comentarios
        }
        # Cargamos todos los comentarios
        post.comments.replace_more(limit=0) # Evita objetos "MoreComments"
        comentarios = post.comments.list()

        # Si hay un límite de comentarios, recortamos la lista
        if limite_comentarios:
            comentarios = comentarios[:limite_comentarios]

        # Procesar cada comentario
        for c in comentarios:
            # Eliminamos URLs para limpiar el texto
            texto = re.sub(r'http\S+', '', c.body)
            # Añadimos el comentario al hilo
            hilo['comments'].append({
                'user': str(c.author),
                'comment': texto,
                'score': c.score,
                'date': convertir_fecha(c.created_utc)
            })
        resultados.append(hilo)
        print(f"[Ej1] Hilo '{post.title}' -> {len(hilo['comments'])} comentarios extraídos.")
    return resultados

# ---------------------------------------------
# Ejercicio 2: Clasificador de comentarios en subreddits
# ---------------------------------------------
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix
# Transformers para el fine-tuning
from transformers import (
    AutoTokenizer, AutoModelForSequenceClassification,
    Trainer, TrainingArguments,
    DataCollatorWithPadding
)
from datasets import Dataset

def preparar_datos_clasificacion(corpus):
    """
    Construye un dataset para clasificación a partir del corpus

    :param corpus: diccionario con clave=subreddit y valor=lista de hilos.
    :return: datasets.Dataset con columnas `text` (comentario) y `label` (subreddit).
    """
    texts, labels = [], []
    for subreddit, threads in corpus.items():
        for th in threads:
            for c in th['comments']:
                texts.append(c['comment']) # Texto del comentario
                labels.append(subreddit) # Etiqueta: nombre del subreddit
    # Creamos un Dataset de la librería 'datasets' para facilitar el fine-tuning
    return Dataset.from_dict({'text': texts, 'label': labels})

def baseline_tfidf_rf(X_train, y_train, X_val, y_val):
    """
    Entrena y evalúa un clasificador básico usando TF-IDF y Random Forest

    :param X_train, y_train: Datos de entrenamiento.
    :param X_val, y_val: Datos de validación.
    :return: Vectorizador TF-IDF y modelo RandomForest entrenado.
    """
    # Vectorización TF-IDF con unigramas y bigramas
    vect = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
    X_tr = vect.fit_transform(X_train)
    X_vl = vect.transform(X_val)

    # Entrenamos el RandomForest
    clf = RandomForestClassifier(n_estimators=200, random_state=0)
    clf.fit(X_tr, y_train)

    # Predicción y métricas
    preds = clf.predict(X_vl)
    print("=== Baseline TF-IDF + RandomForest ===")
    print(classification_report(y_val, preds))
    print(f"Confusion Matrix:\n{confusion_matrix(y_val, preds)}")
    return vect, clf

def finetune_transformer(train_ds, val_ds,
                         model_name='bert-base-multilingual-uncased',
                         output_dir='./finetuned-model'):
    """
    Fine-tuning de un modelo Transformer (BERT multilingüe) para clasificación.

    :param train_ds, val_ds: datasets.Dataset con columnas `text` y `label`.
    :param model_name: Identificador del modelo en Hugging Face.
    :param output_dir: Carpeta para guardar el modelo entrenado.
    :return: modelo y tokenizer entrenados.
    """
    # Cargamos el tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Función para tokenizar y truncar
    def tokenize(batch):
        return tokenizer(batch['text'], padding='max_length', truncation=True, max_length=128)

    # Aplicamos tokenización a los datasets
    train_tok = train_ds.map(tokenize, batched=True)
    val_tok = val_ds.map(tokenize, batched=True)

    # Renombramos la columna de etiquetas a 'labels' por convención
    if 'label' in train_tok.column_names:
        train_tok = train_tok.rename_column('label', 'labels')
    if 'label' in val_tok.column_names:
        val_tok = val_tok.rename_column('label', 'labels')

    # Preparador de batch con padding dinámico
    data_collator = DataCollatorWithPadding(tokenizer)

    # Cargamos el modelo preentrenado para clasificación con el número de clases adecuado
    num_labels = len(set(train_tok['labels'])) # Calculamos cuántas etiquetas únicas hay
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)

    # Definimos los argumentos de entrenamiento
    args = TrainingArguments(
        output_dir=output_dir,
        eval_strategy="steps",        # Evalúa en intervalos de pasos
        save_strategy="steps",        # Guarda el modelo en intervalos de pasos
        logging_steps=500,            # Registra métricas cada 500 pasos
        eval_steps=500,               # Evalúa cada 500 pasos
        save_steps=500,               # Guarda el modelo cada 500 pasos
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
        load_best_model_at_end=True,   # Carga el mejor modelo al final
    )

    # Creamos el Trainer
    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_tok,
        eval_dataset=val_tok,
        tokenizer=tokenizer,
        data_collator=data_collator
    )

    # Entrenamos y evaluamos
    trainer.train()
    trainer.evaluate()

    # Predicción sore el set de validación
    preds = trainer.predict(val_tok)
    y_true = val_tok['labels']
    y_pred = np.argmax(preds.predictions, axis=1)
    print("=== Reporte Fine-Tuning ===")
    print(classification_report(y_true, y_pred))

    return model, tokenizer

# ---------------------------------------------
# Ejercicio 3: Búsqueda de hilos similares
# ---------------------------------------------
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def buscar_hilos_similares(corpus, modelo_name='all-MiniLM-L6-v2', top_k=5):
    """
    Encuentra los hilos más similares entre sí usando embeddings

    :param corpus: Diccionario con datos extraídos
    :param modelo_name: Identificador de modelo SentenceTransformer
    :param top_k: Cuántos vecinos similares devolver
    :return: Diccionario con `clave`=(subreddit, índice del hilo), `valor`=listado de top_k similares
    """
    # Cargamos el modelo de embeddings
    model = SentenceTransformer(modelo_name)
    ids, textos = [], []

    # Construimos una lista de textos por hilo
    for sr, threads in corpus.items():
        for idx, th in enumerate(threads):
            ids.append((sr, idx))
            # Concatenamos título y comentarios para representar el hilo completo
            textos.append(th['title'] + ' ' + ' '.join(c['comment'] for c in th['comments']))

    # Calculamos embeddings y matriz de similitud
    embs = model.encode(textos)
    sims = cosine_similarity(embs)

    similares = {}
    for i, key in enumerate(ids):
        # Obtenemos índices de los top_k más similares (excluyendo el propio hilo)
        orden = np.argsort(sims[i])[-top_k-1:-1][::-1]
        similares[key] = [(ids[j], float(sims[i][j])) for j in orden]

    return similares

# ---------------------------------------------
# Ejercicio 4: Análisis de subjetividad
# ---------------------------------------------
from transformers import pipeline

def analisis_sentimiento(corpus):
    """
    Añade análisis de sentimiento y emoción a cada comentario.

    :param corpus: Diccionario con hilos y comentarios.
    :return: Corpus modificado con nuevos campos en cada comentario.
    """
    # Pipeline para sentimiento (positivo/negativo/neutro)
    sent_pipe = pipeline('sentiment-analysis', model='finiteautomata/beto-sentiment-analysis', truncation=True, max_length=128)
    # Pipeline para emociones múltiples con puntuaciones
    emo_pipe = pipeline('text-classification', model='pysentimiento/robertuito-emotion-analysis', return_all_scores=True, truncation=True, max_length=128)

    # Iteramos sobre todos los comentarios
    for threads in corpus.values():
        for th in threads:
            for c in th['comments']:
                # Truncamos el comentario si excede el límite
                texto = c['comment'][:512]  # Ajusta el límite según sea necesario
                try:
                    # Obtenemos etiqueta y puntuación de sentimiento
                    s = sent_pipe(texto)[0]
                    # Obtenemos distribución de emociones
                    e = emo_pipe(texto)[0]
                    # Guardamos resultados en el diccionario del comentario
                    c['sentiment'] = s['label']
                    c['sentiment_score'] = s['score']
                    c['emotion'] = {x['label']: x['score'] for x in e}
                except Exception as ex:
                    print(f"Error procesando comentario: {texto[:50]}... - {ex}")
                    c['sentiment'] = None
                    c['sentiment_score'] = None
                    c['emotion'] = None

    return corpus

# ---------------------------------------------
# Ejercicio 5: Resumen automático abstractivo
# ---------------------------------------------
from transformers import AutoTokenizer as SumTokenizer, AutoModelForSeq2SeqLM

def resumen_preentrenado(corpus, model_name='csebuetnlp/mT5_multilingual_XLSum'):
    """
    Genera resúmenes abtractivos con un modelo seq2seq preentrenado.

    :param corpus: Diccionario con hilos.
    :param model_name: Modelo de Hugging Face para resumen.
    :return: Corpus con campo `summary_pretrained` en cada hilo.
    """
    tokenizer = SumTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    for threads in corpus.values():
        for th in threads:
            # Creamos la entrada: título + descripción
            inp = th['title'] + ': ' + th['description']
            tokens = tokenizer(inp, return_tensors='pt', truncation=True, max_length=512)
            # Generamos el resumen
            out = model.generate(**tokens, max_length=100, num_beams=4)
            th['summary_pretrained'] = tokenizer.decode(out[0], skip_special_tokens=True)

    return corpus

def resumen_zero_shot(corpus, model_name='google/flan-t5-small'):
    """
    Usa un modelo causal (Flan-T5) en zero-shot para generar resúmenes.

    :param corpus: Diccionario con hilos.
    :param model_name: Identificador de modelo causal.
    :return: Corpus con campo 'summary_zero_shot' en cada hilo.
    """
    from transformers import pipeline as zsl_pipeline
    zsl = zsl_pipeline('text2text-generation', model=model_name)

    for threads in corpus.values():
        for th in threads:
            prompt = f"Resume: {th['title']}. {th['description']}"
            th['summary_zero_shot'] = zsl(prompt, max_length=100)[0]['generated_text']

    return corpus

# ---------------------------------------------
# Ejercicio 6: Detección de contenido inapropiado
# ---------------------------------------------
from transformers import pipeline as hf_pipeline

def deteccion_inapropiado(corpus):
    """
    Detecta lenguaje inapropiado con enfoques ZSL y Chain-of-Thought.

    :param corpus: Diccionario con hilos y comentarios.
    :return: Corpus con campos 'zsl_label', 'zsl_score' y 'cot_output' en cada comentario.
    """
    # Clasificador Zero-Shot para etiquetar 'apropiado' vs 'inapropiado'
    classifier = hf_pipeline('zero-shot-classification', model='facebook/bart-large-mnli')
    labels = ['apropiado', 'inapropiado']

    for threads in corpus.values():
        for th in threads:
            for c in th['comments']:
                # Zero-shot classification
                res = classifier(c['comment'], labels)
                c['zs_label'] = res['labels'][0]
                c['zs_score'] = res['scores'][0]
                # Chain-of-Thought: solicitamos razonamiento intermedio
                prompt_coh = (
                    f"Evalúa si este comentario contiene lenguaje inapropiado. "
                    f"Primero explica tu razonamiento y luego clasifica. Comentario: {c['comment']}"
                )
                cot = hf_pipeline('text2text-generation', model='gpt2')(prompt_coh, max_length=200)[0]['generated_text']
                c['cot_output'] = cot

    return corpus

# Ejecutar todo el pipeline
if __name__ == '__main__':
    # Nombre de los archivos JSON
    raw_json_path = 'raw_technology.json'
    processed_corpus_path = 'tech_debate_corpus_total.json'
    full_analysis_path = 'tech_debate_full_analysis.json'

    # Paso 1: Extracción básica del subreddit 'technology'
    if os.path.exists(raw_json_path):
        print(f"Cargando datos desde {raw_json_path}...")
        with open(raw_json_path, 'r', encoding='utf-8') as f:
            raw = json.load(f)
    else:
        print("Extrayendo datos del subreddit 'technology'...")
        raw = extraer_corpus_raw('technology', limite_hilos=20)
        # Guardamos la extracción inicial en JSON
        with open(raw_json_path, 'w', encoding='utf-8') as f:
            json.dump(raw, f, ensure_ascii=False, indent=4)

    # Paso 2: Cargar o procesar el corpus
    if os.path.exists(processed_corpus_path):
        print(f"Cargando corpus procesado desde {processed_corpus_path}...")
        corpus = cargar_corpus(processed_corpus_path)
    else:
        print("Procesando el corpus...")
        corpus = preparar_datos_clasificacion(raw)
        # Guardamos el corpus procesado
        with open(processed_corpus_path, 'w', encoding='utf-8') as f:
            json.dump(corpus, f, ensure_ascii=False, indent=4)

    # Paso 3: Clasificación de comentarios
    ds = preparar_datos_clasificacion(corpus)
    ds = ds.class_encode_column('label')  # Convertir la columna 'label' a ClassLabel
    train_ds, val_ds = ds.train_test_split(test_size=0.3, stratify_by_column='label').values()
    baseline_tfidf_rf(train_ds['text'], train_ds['label'], val_ds['text'], val_ds['label'])
    finetune_transformer(train_ds, val_ds)

    # Paso 4: Búsqueda de hilos similares
    similares = buscar_hilos_similares(corpus)
    print("Ejemplo hilos similares:", list(similares.items())[:1])

    # Paso 5: Análisis de sentimiento y emoción
    corpus = analisis_sentimiento(corpus)

    # Paso 6: Generación de resúmenes
    corpus = resumen_preentrenado(corpus)
    corpus = resumen_zero_shot(corpus)

    # Paso 7: Detección de contenido inapropiado
    corpus = deteccion_inapropiado(corpus)

    # Guardamos el análisis completo en un solo JSON
    with open(full_analysis_path, 'w', encoding='utf-8') as f:
        json.dump(corpus, f, ensure_ascii=False, indent=4)
    print(f"Análisis completo guardado en '{full_analysis_path}'.")