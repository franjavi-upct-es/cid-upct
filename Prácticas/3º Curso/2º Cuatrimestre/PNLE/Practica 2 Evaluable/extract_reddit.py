import os                       # Operaciones con archivos y directorios
import json                     # Leer y escribir archivos JSON
import re                       # Expresiones regulares para procesamiento de texto
import praw                     # PRAW: API de Reddit
import numpy as np              # Cálculos numéricos y vectores
from datetime import datetime   # Manejo de fechas
import warnings

os.chdir(os.path.abspath(os.path.dirname(__file__)))

# scikit-learn: clasificadores, métricas y transformadores de texto
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

# FastTexT embeddings con gensim
from gensim.models import FastText

# Hugging Face: modelos, entrenador (Trainer) y pipelines
from transformers import (
    AutoTokenizer,                          # Tokenizador para modelos HF
    AutoModelForSequenceClassification,     # Modelo para clasificación de texto
    Trainer,                                # Entrenador de Hugging Face
    TrainingArguments,                      # Argumentos para el entrenamiento
    DataCollatorWithPadding,                # Collator para batches dinámicos
    pipeline                                # Para pipelines rápidos (sentimiento, zero-shot)
)
from datasets import Dataset    # Para preparar datasets en fine-tuning

# Sentece Transformers (SBERT) para similitud de sentencias
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity # Para calcular similitud de vectores

# ---------------------------------------------
# Configuración global (subreddits de tecnología)
# ---------------------------------------------
SUBREDDITS = [
    'technology',       # Subreddit general de tecnología
    'programming',      # Programación y desarrollo de software
    'machinelearning',  # Aprendizaje automático e IA
    'datascience',      # Ciencia de datos y análisis
    'computerscience',  # Teoría y práctica de la informática
    'gadgets'           # Dispositivos, hardware y electrónica
]
THREADS_PER_SUB = 20     # Número de hilos a extraer por subreddit
COMMENTS_PER_THREAD = 50 # Número máximo de comentarios por hilo
JSON_DIR = 'data'        # Carpeta para guardar los archivos JSON
os.makedirs(JSON_DIR, exist_ok=True) # Crear carpeta si no existe

# Stopwords y stemmer para limpieza léxica
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
STOPWORDS = set(stopwords.words('english')) | set(stopwords.words('spanish'))
STEMMER = SnowballStemmer('spanish') # Snowball para español

# Inicializar cliente de Reddit y suprimir advertencias irrelevantes
warnings.filterwarnings('ignore')
reddit = praw.Reddit(
    client_id='ShOBXaW1U-PMc1hhr88znw',
    client_secret='o12KLkUR18D5wZqnPxG5lp8jQFszgg',
    user_agent='pln-practica-2025'
)

# ----------------------------------------------
# Funciones de preprocesamiento de texto
# ----------------------------------------------
def convertir_fecha(utc_timestamp):
    """
    Convierte un timestamp UNIX a una cadena legible 'YYYY-MM-DD HH:MM:SS'.
    """
    return datetime.fromtimestamp(utc_timestamp).strftime('%Y-%m-%d %H:%M:%S')

# Regex para eliminar URLs, menciones y enlaces markdown
LEXICAL_PATTERN = re.compile(r"http\S+|www\.\S+|\[.*?\]\(.*?\)|@[A-Za-z0-9_]+")

def limpiar_texto(texto):
    """
    - Elimina URLs, menciones y markdown.
    - Tokeniza, filtra stopwords y tokens muy cortos.
    - Aplica stemming para normalizar palabras.
    """
    # Eliminar patrones no deseados
    texto_limpio = LEXICAL_PATTERN.sub('', texto)
    # Tokenizar en palabras y pasar a minúsculas
    tokens = re.findall(r"\b\w+\b", texto_limpio.lower())
    # Filtrar y stemizar
    procesados = [STEMMER.stem(tok) for tok in tokens if tok not in STOPWORDS and len(tok) > 2]
    return " ".join(procesados)

# ----------------------------------
# Paso 1: Extracción y guardado del corpus
# ----------------------------------
def extraer_y_guardar_corpus():
    """
    Extrae hilos 'hot' y comentarios de subreddits.
    Preprocesa el texto, guarda un JSON por subreddit y devuelve un diccionario.
    """
    corpus = {}
    for sr in SUBREDDITS:
        hilos = []
        # Recorrer hilos más populares
        for post in reddit.subreddit(sr).hot(limit=THREADS_PER_SUB):
            hilo = {
                'title': post.title,
                'flair': post.link_flair_text,
                'author': str(post.author),
                'date': convertir_fecha(post.created_utc),
                'score': post.score,
                'description': limpiar_texto(post.selftext),
                'comments': []
            }
            # Cargar comentarios evitando 'MoreComments'
            post.comments.replace_more(limit=0)
            for c in post.comments.list()[:COMMENTS_PER_THREAD]:
                hilo['comments'].append({
                    'user': str(c.author),
                    'comment': limpiar_texto(c.body),
                    'score': c.score,
                    'date': convertir_fecha(c.created_utc)
                })
            hilos.append(hilo)
        # Guardar JSON individual para este subreddit
        ruta = os.path.join(JSON_DIR, f'corpus_{sr}.json')
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(hilos, f, ensure_ascii=False, indent=4)
        corpus[sr] = hilos
    return corpus

# ----------------------------------
# Paso 2: Clasificación de comentarios
# ----------------------------------

def split_by_thread(corpus):
    """
    Divide hilos en 14 para entrenamiento y 6 para validación.
    Evita fugas de información al separar por hilo.
    """
    X_train, y_train, X_val, y_val = [], [], [], []
    for sr, threads in corpus.items():
        train_threads, val_threads = threads[:14], threads[14:]
        # Extraer comentarios de entrenamiento
        for th in train_threads:
            for c in th['comments']:
                X_train.append(c['comment'])
                y_train.append(sr)
        for th in val_threads:
            for c in th['comments']:
                X_val.append(c['comment'])
                y_val.append(sr)
    return X_train, y_train, X_val, y_val

def train_baselines(X_train, y_train, X_val, y_val):
    """
    Entrena dos modelos base:
        1) TF-IDF + Random Forest
        2) FastText + SVM lineal
    Muestra métricas y matrices de confusión.
    """
    # TF-IDF + Random Forest
    vec = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
    X_train_vec = vec.fit_transform(X_train)
    X_val_vec = vec.transform(X_val)
    rf = RandomForestClassifier(n_estimators=200, random_state=0)
    rf.fit(X_train_vec, y_train)
    preds_rf = rf.predict(X_val_vec)
    print("--- TF-IDF + Random Forest ---")
    print(classification_report(y_val, preds_rf))
    print(confusion_matrix(y_val, preds_rf))

    # FastText + SVM
    ft_model = FastText(
        sentences=[doc.split() for doc in X_train],
        vector_size=100, window=5, min_count=2, workers=4
    )
    def embed_docs(docs):
        embeddings = []
        for doc in docs:
            vectors = [ft_model.wv[w] for w in doc.split() if w in ft_model.wv]
            embeddings.append(np.mean(vectors, axis=0) if vectors else np.zeros(100))
        return np.vstack(embeddings)
    X_train_ft = embed_docs(X_train)
    X_val_ft = embed_docs(X_val)
    svm = SVC(kernel='linear', probability=True)
    svm.fit(X_train_ft, y_train)
    preds_svm = svm.predict(X_val_ft)
    print("--- FastText + SVM ---")
    print(classification_report(y_val, preds_svm))
    print(confusion_matrix(y_val, preds_svm))

def train_transformer(X_train, y_train, X_val, y_val):
    """
    Fine-tuning de BERT multilingüe para clasificación.
    Si el modelo ya está entrenado en la carpeta 'finetune', lo carga directamente.
    """
    from pathlib import Path

    # Ruta del modelo entrenado
    finetune_dir = 'finetune'
    if Path(finetune_dir).exists():
        print("Cargando modelo ya entrenado desde la carpeta 'finetune'...")
        model = AutoModelForSequenceClassification.from_pretrained(finetune_dir)
        tokenizer = AutoTokenizer.from_pretrained(finetune_dir)
    else:
        print("Entrenando modelo desde cero...")
        datos = {'text': X_train + X_val, 'label': y_train + y_val}
        ds = Dataset.from_dict(datos).class_encode_column('label')
        train_ds, val_ds = ds.train_test_split(test_size=len(X_val)/len(ds)).values()

        tokenizer = AutoTokenizer.from_pretrained('bert-base-multilingual-uncased')
        def tokenize_fn(batch):
            return tokenizer(batch['text'], padding='max_length', truncation=True, max_length=128)
        train_ds = train_ds.map(tokenize_fn, batched=True).rename_column('label', 'labels')
        val_ds = val_ds.map(tokenize_fn, batched=True).rename_column('label', 'labels')

        collator = DataCollatorWithPadding(tokenizer)
        model = AutoModelForSequenceClassification.from_pretrained(
            'bert-base-multilingual-uncased', num_labels=len(set(y_train))
        )
        args = TrainingArguments(
            output_dir=finetune_dir, num_train_epochs=3,
            per_device_train_batch_size=16, per_gpu_eval_batch_size=16,
            eval_strategy='epoch', save_strategy='epoch',
            load_best_model_at_end=True
        )
        trainer = Trainer(
            model=model, args=args,
            train_dataset=train_ds, eval_dataset=val_ds,
            tokenizer=tokenizer, data_collator=collator
        )
        trainer.train()
        
        # Guardar el modelo y tokenizador
        model.save_pretrained(finetune_dir)
        tokenizer.save_pretrained(finetune_dir)

    # Evaluar el modelo
    datos = {'text': X_val, 'label': y_val}
    val_ds = Dataset.from_dict(datos).class_encode_column('label')
    val_ds = val_ds.map(lambda batch: tokenizer(batch['text'], padding='max_length', truncation=True, max_length=128), batched=True).rename_column('label', 'labels')
    res = Trainer(model=model).predict(val_ds)
    preds = np.argmax(res.predictions, axis=1)
    print('--- BERT Fine-Tuning ---')
    print(classification_report(val_ds['labels'], preds))
    print(confusion_matrix(val_ds['labels'], preds))

# ---------------------------------
# Paso 3: Similitud de hilos con FastText y SBERT
# ---------------------------------

def buscar_hilos_similares_fasttext(corpus, top_k=5):
    """
    Calcula embedding promedio de cada hilo con FastText y obtiene top_k similares.
    """
    ids, vectors = [], []
    ft = FastText(
        sentences=[c['comment'].split() for threads in corpus.values() for c in threads['comments']],
        vector_size=100, window=5, min_count=2, workers=4
    )
    for sr, threads in corpus.items():
        for idx, hilo in enumerate(threads):
            ids.append((sr, idx))
            doc_vecs = [ft.wv[w] for c in hilo['comments'] for w in c['comment'].split() if w in ft.wv]
            vectors.append(np.mean(doc_vecs, axis=0) if doc_vecs else np.zeros(100))
    sims = cosine_similarity(vectors)
    similares = {ids[i]: [(ids[j], float(sims[i][j])) for j in np.argsort(sims[i])[-top_k-1:-1][::-1]] for i in range(len(ids))}
    return similares

def buscar_hilos_similares_sbert(corpus, model_name='all-MiniLM-L6-v2', top_k=5):
    """
    Similitud de hilos usando embeddings SBERT (SentenceTransformer).
    """
    model = SentenceTransformer(model_name)
    ids, texts = [], []
    for sr, threads in corpus.items():
        for idx, hilo in enumerate(threads):
            ids.append((sr, idx))
            combined = hilo['title'] + ' ' + ' '.join(c['comment'] for c in hilo['comments'])
            texts.append(combined)
    embs = model.encode(texts)
    sims = cosine_similarity(embs)
    similares = {ids[i]: [(ids[j], float(sims[i][j])) for j in np.argsort(sims[i])[-top_k-1:-1][::-1]] for i in range(len(ids))}
    return similares

# ---------------------------------------------
# Paso 4: Análisis de subjetividad (sentimiento/emoción)
# ---------------------------------------------

def analisis_sentimiento(corpus):
    """
    Pipeline de Hugging Face para sentimiento y clasificación de emociones.
    Añade campos `sentiment`, `sentiment_score` y `emotion`.
    """
    sent_pipe = pipeline('sentiment-analysis', model='finiteautomata/beto-sentiment-analysis', truncation=True, max_length=128)
    emo_pipe = pipeline('text-classification', model='pysentimiento/robertuito-emotion-analysis', return_all_scores=True, truncation=True, max_length=128)
    for threads in corpus.values():
        for hilo in threads:
            for c in hilo['comments']:
                text = c['comment'][:512]
                s = sent_pipe(text)[0]
                e = emo_pipe(text)[0]
                c['sentiment'] = s['label']
                c['sentiment_score'] = s['score']
                c['emotion'] = {item['label']: item['score'] for item in e}
    return corpus

# ---------------------------------------------
# Paso 5: Resumen automático abstractivo
# ---------------------------------------------
def resumen_preentrenado(corpus, model_name='csebuetnlp/mT5_multilingual_XLSum'):
    """
    Genera resúmenes con modelo seq2seq preentrenado.
    Guarda en campo `summary_pretrained`.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    for threads in corpus.values():
        for hilo in threads:
            inp = hilo['title'] + ": " + hilo['description']
            tokens = tokenizer(inp, return_tensors='pt', truncation=True, max_length=512)
            out = model.generate(**tokens, max_length=100, num_beams=4)
            hilo['summary_pretrained'] = tokenizer.decode(out[0], skip_special_tokens=True)
    return corpus

def resumen_zero_shot(corpus, model_name='google/flan-t5-small'):
    """
    Genera resúmenes en zero-shot con Flan-T5 y guarda en campo `summary_zero_shot`.
    """
    zsl_pipe = pipeline('text2text-generation', model=model_name)
    for threads in corpus.values():
        for hilo in threads:
            prompt = f"Resume: {hilo['title']}. {hilo['description']}"
            generated = zsl_pipe(prompt, max_length=100)[0]
            hilo['summary_zero_shot'] = generated['generated_text']
    return corpus

# ---------------------------------------------
# Paso 6: Detección de contenido inapropiado
# ---------------------------------------------

def deteccion_inapropiado(corpus):
    """
    Zero-shot + Chain-of-thought con Hugging Face para detectar lenguaje inapropiado.
    Añade `zsl_label`, `zs_score` y `cot_output` a cada comentario.
    """
    zsl_cls = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')
    cot_pipe = pipeline('text2text-generation', model='google/flan-t5-small')
    labels = ['apropiado', 'inapropiado']
    for threads in corpus.values():
        for hilo in threads:
            for c in hilo['comments']:
                res = zsl_cls(c['comment'], labels)
                c['zs_label'] = res['labels'][0]
                c['zs_score'] = res['scores'][0]
                prompt = f"Evalúa si este comentario contiene lenguaje inapropiado. Primero explica tu razonamiento y luego clasifica. Comentario: {c['comment']}"
                c['cot_output'] = cot_pipe(prompt, max_new_tokens=50)[0]['generated_text']
    return corpus

# Few-Shot ejemplos para r/OpcionesPolemicas
FEW_SHOT_EXAMPLES = [
    ('Este comentario es ofensivo y soez', 'inapropiado'),
    ('¡Me encanta esta publicación!', 'apropiado'),
    ('Qué horror, no soporto esto.', 'apropiado'),
]

def deteccion_inapropiado_fsl(corpus):
    """
    Few-Shot en r/OpinionesPolemicas inyectando ejemplos en el prompt.
    """
    zsl_pipe = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')
    prompt_fsl = 'Clasifica como apropiado o inapropiado:\n' + "".join([
        f'Ejemplo: {ex[0]} -> {ex[1]}.\n' for ex in FEW_SHOT_EXAMPLES
    ])
    results = {}
    for sr, threads in corpus.items():
        if sr != 'OpinionesPolemicas':
            continue
        for idx, hilo in enumerate(threads[:10]):
            for c in hilo['comments']:
                text = f"{prompt_fsl}Comentario: {c['comment']} ->"
                r = zsl_pipe(text, candidate_labels=['apropiado', 'inapropiado'])
                results[(sr, idx, c['date'])] = {'label_zsl': r['labels'][0], 'score': r['scores'][0]}
    return results

# ---------------------------------------------
# Ejecución completa del pipeline
# ---------------------------------------------
if __name__ == '__main__':
    # 1) Extraer y guardar el corpus preprocesado
    corpus = extraer_y_guardar_corpus()
    # 2) Preparar datos y entrenar clasificadores
    X_train, y_train, X_val, y_val = split_by_thread(corpus)
    train_baselines(X_train, y_train, X_val, y_val)
    train_transformer(X_train, y_train, X_val, y_val)
    # 3) Calcular similitud de hilos
    sims_ft = buscar_hilos_similares_fasttext(corpus)
    sims_sbert = buscar_hilos_similares_sbert(corpus)
    # 4) Análisis de sentimiento y emoción
    corpus = analisis_sentimiento(corpus)
    # 5) Generar resúmenes preentrenados y zero-shot
    corpus = resumen_preentrenado(corpus)
    corpus = resumen_zero_shot(corpus)
    # 6) Detección de contenido inapropiado (ZSL, CoT y FSL)
    corpus = deteccion_inapropiado(corpus)
    inap_fsl = deteccion_inapropiado_fsl(corpus)
    # Guardar resultados adicionales en JSON
    with open(os.path.join(JSON_DIR, 'analysis_extras.json'), 'w', encoding='utf-8') as f:
        json.dump({'sims_ft': sims_ft, 'sims_sbert': sims_sbert, 'inap_fsl': inap_fsl}, f, ensure_ascii=False, indent=4)