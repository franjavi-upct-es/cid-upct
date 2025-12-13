"""# 1. Importaciones y configuración global

**Descripción**

Se importan las librerías necesarias para:
- Operaciones con archivos, JSON y expresiones regulares.
- Acceso a la API de Reddit (`praw`).
- Procesamiento numérico (`numpy`).
- Manejo de fechas.
- Modelos y utilidades de `scikit-learn`, `fasttext`, `Hugging Face` y `SentenceTransformers`.
- Stopwords y stemmer con `nltk`.
Además, se definen subreddits, número de hilos/comentarios a extraer, y se crea la carpeta `data` para guardar los JSON.
"""

import os
import json
import re
import praw
import numpy as np
from datetime import datetime
import fasttext
import warnings
import tempfile

# scikit-learn
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

# Hugging Face
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    DataCollatorWithPadding,
    pipeline
)
from datasets import Dataset

# SBERT y similitud
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# NLTK para limpieza léxica
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

import nltk
nltk.download('stopwords')

# Configuración básica
SUBREDDITS = ['technology', 'programming', 'machinelearning',
              'datascience', 'computerscience', 'gadgets']
THREADS_PER_SUB = 20
COMMENTS_PER_THREAD = 50
JSON_DIR = 'data'
os.makedirs(JSON_DIR, exist_ok=True)

STOPWORDS = set(stopwords.words('english')) | set(stopwords.words('spanish'))
STEMMER = SnowballStemmer('spanish')

warnings.filterwarnings('ignore')
reddit = praw.Reddit(
    client_id='ShOBXaW1U-PMc1hhr88znw',
    client_secret='o12KLkUR18D5wZqnPxG5lp8jQFszgg',
    user_agent='pln-practica-2025',
    check_for_async=False
)

"""# 2. Funciones de preprocesamiento de texto
## 2.1 Conversión de timestamps

Convierte segundos UNIX a formato legible.
"""

def convertir_fecha(utc_timestamp):
    """
    Convierte un timestamp UNIX a 'YYYY-MM-DD HH:MM:SS'.
    """
    return datetime.fromtimestamp(utc_timestamp).strftime('%Y-%m-%d %H:%M:%S')

"""## 2.2 Limpieza léxica
- Elimina URLs, meciones y enlaces Markdown.
- Tokeniza, filtra stopwords y tokens muy cortos.
- Aplica stemming.
"""

LEXICAL_PATTERN = re.compile(r"http\S+|www\.\S+|\[.*?\]\(.*?\)|@[A-Za-z0-9_]+")

def limpiar_texto(texto):
    """
    - Elimina URLs, menciones y markdown.
    - Tokeniza en palabras, pasa a minúsculas.
    - Filtra stopwords y tokens < 3 caracteres.
    - Aplica stemming.
    """
    texto_limpio = LEXICAL_PATTERN.sub('', texto)
    tokens = re.findall(r"\b\w+\b", texto_limpio.lower())
    procesados = [
        STEMMER.stem(tok)
        for tok in tokens
        if tok not in STOPWORDS and len(tok) > 2
    ]
    return " ".join(procesados)

"""# 3. Extracción y guardado del corpus
Recorre cada subreddit, extrae los hilos "hot" y hasta 50 comentarios por hilo, los preprocesa y guarda un JSON por subreddit en `data/corpus_<sr>.json`.
"""

def extraer_y_guardar_corpus():
    corpus = {}
    for sr in SUBREDDITS:
        hilos = []
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
            post.comments.replace_more(limit=0)
            for c in post.comments.list()[:COMMENTS_PER_THREAD]:
                hilo['comments'].append({
                    'user': str(c.author),
                    'comment': limpiar_texto(c.body),
                    'score': c.score,
                    'date': convertir_fecha(c.created_utc)
                })
            hilos.append(hilo)
        ruta = os.path.join(JSON_DIR, f'corpus_{sr}.json')
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(hilos, f, ensure_ascii=False, indent=4)
        corpus[sr] = hilos
    return corpus

"""# 4. Prepraración de datos y clasificación
## 4.1 Separación por hilo
Evita fugas de información: 14 hilos para entrenamiento y 6 para validación.
"""

def split_by_thread(corpus):
    X_train, y_train, X_val, y_val = [], [], [], []
    for sr, threads in corpus.items():
        train_threads, val_threads = threads[:14], threads[14:]
        for th in train_threads:
            for c in th['comments']:
                X_train.append(c['comment']); y_train.append(sr)
        for th in val_threads:
            for c in th['comments']:
                X_val.append(c['comment']); y_val.append(sr)
    return X_train, y_train, X_val, y_val

"""## 4.2 Modelos baseline
1. **TF-IDF + RandomForest**
2. **FastText embeddings + SVM lineal**
"""

def train_baselines(X_train, y_train, X_val, y_val):
    # TF-IDF + Random Forest
    vec = TfidfVectorizer(ngram_range=(1,2), max_features=5000)
    X_tr_vec = vec.fit_transform(X_train)
    X_val_vec = vec.transform(X_val)
    rf = RandomForestClassifier(n_estimators=200, random_state=0)
    rf.fit(X_tr_vec, y_train)
    preds_rf = rf.predict(X_val_vec)
    print("--- TF-IDF + Random Forest ---")
    print(classification_report(y_val, preds_rf))
    print(confusion_matrix(y_val, preds_rf))

    # fastText oficial + SVM
    with tempfile.NamedTemporaryFile('w+', delete=False, encoding='utf-8') as tmp:
        for doc in X_train:
            tmp.write(doc + '\n')
        tmp_path = tmp.name
    ft_model = fasttext.train_unsupervised(tmp_path, model='skipgram', dim=100, ws=5, minCount=2)

    def embed_docs(docs):
        return np.vstack([ft_model.get_sentence_vector(doc) for doc in docs])

    X_tr_ft = embed_docs(X_train)
    X_val_ft = embed_docs(X_val)
    svm = SVC(kernel='linear', probability=True)
    svm.fit(X_tr_ft, y_train)
    preds_svm = svm.predict(X_val_ft)
    print("--- fastText oficial + SVM ---")
    print(classification_report(y_val, preds_svm))
    print(confusion_matrix(y_val, preds_svm))

"""## 4.3 Fine-tuning con Transformers

Utiliza BERT multilingüe para clasificación. Carga el modelo pre-entrenado si existe, si no lo entrena y guarda en `finetune/`.
"""

def train_transformer(X_train, y_train, X_val, y_val):
    from pathlib import Path
    finetune_dir = 'finetune'
    if Path(finetune_dir).exists():
        print("Cargando modelo ya entrenado…")
        model = AutoModelForSequenceClassification.from_pretrained(finetune_dir)
        tokenizer = AutoTokenizer.from_pretrained(finetune_dir)
    else:
        print("Entrenando modelo desde cero…")
        datos = {'text': X_train + X_val, 'label': y_train + y_val}
        ds = Dataset.from_dict(datos).class_encode_column('label')
        train_ds, val_ds = ds.train_test_split(
            test_size=len(X_val)/len(ds)
        ).values()

        tokenizer = AutoTokenizer.from_pretrained('bert-base-multilingual-uncased')
        def tokenize_fn(batch):
            return tokenizer(
                batch['text'], padding='max_length',
                truncation=True, max_length=128
            )
        train_ds = train_ds.map(tokenize_fn, batched=True) \
                         .rename_column('label','labels')
        val_ds   = val_ds.map(tokenize_fn, batched=True)   \
                         .rename_column('label','labels')

        collator = DataCollatorWithPadding(tokenizer)
        model = AutoModelForSequenceClassification.from_pretrained(
            'bert-base-multilingual-uncased',
            num_labels=len(set(y_train))
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
        model.save_pretrained(finetune_dir)
        tokenizer.save_pretrained(finetune_dir)

    # Evaluación
    datos = {'text': X_val, 'label': y_val}
    val_ds = Dataset.from_dict(datos).class_encode_column('label')
    val_ds = val_ds.map(
        lambda b: tokenizer(
            b['text'], padding='max_length',
            truncation=True, max_length=128
        ), batched=True
    ).rename_column('label','labels')
    res = Trainer(model=model).predict(val_ds)
    preds = np.argmax(res.predictions, axis=1)
    print('--- BERT Fine-Tuning ---')
    print(classification_report(val_ds['labels'], preds))
    print(confusion_matrix(val_ds['labels'], preds))

"""# 5. Similitud de hilos
## 5.1 FastText
Embedding promedio de comentarios por cada hilo y similitud coseno.
"""

def buscar_hilos_similares_fasttext(corpus, top_k=5):
    # Prepara un archivo temporal con cada hilo como línea
    with tempfile.NamedTemporaryFile('w+', delete=False, encoding='utf-8') as tmp:
        for threads in corpus.values():
            for hilo in threads:
                comments_text = ' '.join(c['comment'] for c in hilo['comments'])
                tmp.write(comments_text + '\n')
        tmp_path = tmp.name

    ft_model = fasttext.train_unsupervised(tmp_path, model='skipgram', dim=100, ws=5, minCount=2)
    ids, vectors = [], []
    for sr, threads in corpus.items():
        for idx, hilo in enumerate(threads):
            ids.append((sr, idx))
            text = ' '.join(c['comment'] for c in hilo['comments'])
            vectors.append(ft_model.get_sentence_vector(text))
    sims = cosine_similarity(vectors)
    similares = {
        ids[i]: [
            (ids[j], float(sims[i][j]))
            for j in np.argsort(sims[i])[-top_k-1:-1][::-1]
        ]
        for i in range(len(ids))
    }
    return similares

"""## 5.2 SBERT
Embeddings de título + comentarios con SentenceTransformers.
"""

def buscar_hilos_similares_sbert(corpus, model_name='all-MiniLM-L6-v2', top_k=5):
    model = SentenceTransformer(model_name)
    ids, texts = [], []
    for sr, threads in corpus.items():
        for idx, hilo in enumerate(threads):
            ids.append((sr, idx))
            combined = hilo['title'] + ' ' + ' '.join(
                c['comment'] for c in hilo['comments']
            )
            texts.append(combined)
    embs = model.encode(texts)
    sims = cosine_similarity(embs)
    similares = {
        ids[i]: [
            (ids[j], float(sims[i][j]))
            for j in np.argsort(sims[i])[-top_k-1:-1][::-1]
        ]
        for i in range(len(ids))
    }
    return similares

"""# 6. Análisis de sentimiento y resumen automático
## 6.1 Sentimiento y emoción
Pipelines de Hugging Face para sentimiento (`finiteautomata/beto-sentiment-analysis`) y emoción (`pysentimiento/robertuito-emotion-analysis`).
"""

def analisis_sentimiento(corpus):
    sent_pipe = pipeline(
        'sentiment-analysis',
        model='finiteautomata/beto-sentiment-analysis',
        truncation=True, max_length=128
    )
    emo_pipe = pipeline(
        'text-classification',
        model='pysentimiento/robertuito-emotion-analysis',
        return_all_scores=True,
        truncation=True, max_length=128
    )
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

"""## 6.2 Resumen preentrenado y zero-shot
- **mT5 multilingual XLSum**
- **Flan-T5 small**
"""

def resumen_preentrenado(corpus, model_name='csebuetnlp/mT5_multilingual_XLSum'):
    from transformers import AutoModelForSeq2SeqLM
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    for threads in corpus.values():
        for hilo in threads:
            inp = hilo['title'] + ": " + hilo['description']
            tokens = tokenizer(inp, return_tensors='pt',
                               truncation=True, max_length=512)
            out = model.generate(**tokens, max_length=100, num_beams=4)
            hilo['summary_pretrained'] = tokenizer.decode(
                out[0], skip_special_tokens=True
            )
    return corpus

def resumen_zero_shot(corpus, model_name='google/flan-t5-small'):
    zsl_pipe = pipeline('text2text-generation', model=model_name)
    for threads in corpus.values():
        for hilo in threads:
            prompt = f"Resume: {hilo['title']}. {hilo['description']}"
            gen = zsl_pipe(prompt, max_length=100)[0]
            hilo['summary_zero_shot'] = gen['generated_text']
    return corpus

"""# 7. Detección de contenido inapropiado
## 7.1 Zero-shot + Chain-of-thought
Utiliza BART-MNLI para clasificación y Flan-T5 para explicar razonamiento.
"""

def deteccion_inapropiado(corpus, zsl_batch_size=32, cot_batch_size=16):
    import torch

    # ── 1. Aceleradores PyTorch ───────────────────────────────
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32    = True
    torch.backends.cudnn.benchmark     = True

    # ── 2. Inicializa pipelines en GPU con FP16 ───────────────
    zsl_cls = pipeline(
        'zero-shot-classification',
        model='facebook/bart-large-mnli',
        device=0,
        torch_dtype=torch.float16,
        batch_size=zsl_batch_size
    )
    cot_pipe = pipeline(
        'text2text-generation',
        model='google/flan-t5-small',
        device=0,
        torch_dtype=torch.float16,
        batch_size=cot_batch_size
    )
    labels = ['apropiado', 'inapropiado']

    # ── 3. Recolecta y preasigna comentarios vacíos ──────────
    pending_texts = []
    metadata = []   # tuplas (sr, hilo_idx, comment_idx)
    for sr, threads in corpus.items():
        for hilo_idx, hilo in enumerate(threads):
            for c_idx, c in enumerate(hilo['comments']):
                txt = c['comment'].strip()
                if not txt:
                    c['zs_label']  = 'apropiado'
                    c['zs_score']  = 1.0
                    c['cot_output']= "Comentario vacío, asumido como apropiado."
                else:
                    pending_texts.append(txt)
                    metadata.append((sr, hilo_idx, c_idx))

    # ── 4. Zero-shot clasificación por lotes ───────────────────
    if pending_texts:
        zsl_outs = zsl_cls(pending_texts, candidate_labels=labels)
        if isinstance(zsl_outs, dict):
            zsl_outs = [zsl_outs]
        for out, (sr, hi, ci) in zip(zsl_outs, metadata):
            c = corpus[sr][hi]['comments'][ci]
            c['zs_label'] = out['labels'][0]
            c['zs_score'] = out['scores'][0]

    # ── 5. Chain-of-thought generación por lotes ──────────────
    cot_prompts = [
        f"Evalúa si este comentario contiene lenguaje inapropiado. "
        f"Primero explica tu razonamiento y luego clasifica. Comentario: {text}"
        for text in pending_texts
    ]
    if cot_prompts:
        cot_outs = cot_pipe(cot_prompts, max_new_tokens=50)
        for out, (sr, hi, ci) in zip(cot_outs, metadata):
            corpus[sr][hi]['comments'][ci]['cot_output'] = out['generated_text']

    return corpus

"""## 7.2 Few-Shot para r/OpinionesPolemicas
Inyecta ejemplos manuales en el prompt.
"""

FEW_SHOT_EXAMPLES = [
    ('Este comentario es ofensivo y soez','inapropiado'),
    ('¡Me encanta esta publicación!','apropiado'),
    ('Qué horror, no soporto esto.','apropiado'),
]

def deteccion_inapropiado_fsl(corpus):
    zsl_pipe = pipeline('zero-shot-classification',
                       model='facebook/bart-large-mnli')
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
                r = zsl_pipe(text, candidate_labels=['apropiado','inapropiado'])
                results[(sr, idx, c['date'])] = {
                    'label_zsl': r['labels'][0],
                    'score': r['scores'][0]
                }
    return results

if __name__ == "__main__":
    """# 8. Ejecución del código"""

    # 1) Extracción
    corpus = extraer_y_guardar_corpus()

    # 2) Clasificación
    import wandb
    X_train, y_train, X_val, y_val = split_by_thread(corpus)
    train_baselines(X_train, y_train, X_val, y_val)
    # Wandb API_KEY: 2d75120400b77d01fafd28db25130420fb4cac8f
    train_transformer(X_train, y_train, X_val, y_val)

    # 3) Similitud
    sims_ft = buscar_hilos_similares_fasttext(corpus)
    sims_sbert = buscar_hilos_similares_sbert(corpus)

    # 4) Sentimiento y emoción
    corpus = analisis_sentimiento(corpus)

    # 5) Resúmenes
    corpus = resumen_preentrenado(corpus)
    corpus = resumen_zero_shot(corpus)

    # 6) Detección inapropiado
    corpus = deteccion_inapropiado(corpus)
    inap_fsl = deteccion_inapropiado_fsl(corpus)

    # Guardar análisis extra
    with open(os.path.join(JSON_DIR,'analysis_extras.json'),
            'w', encoding='utf-8') as f:
        sims_ft_str_keys = {str(key): value for key, value in sims_ft.items()}
        sims_sbert_str_keys = {str(key): value for key, value in sims_sbert.items()}
        json.dump({
            'sims_ft': sims_ft_str_keys,
            'sims_sbert': sims_sbert_str_keys,
            'inap_fsl': inap_fsl
        }, f, ensure_ascii=False, indent=4)
