import os
import pandas as pd
import json
import kagglehub
from sklearn.ensemble import RandomForestClassifier
import joblib

try:
    print("Cargando y uniendo ambos datasets de KaggleHub y el archivo local RT_IOT2022.csv...")
    from kagglehub import KaggleDatasetAdapter
    # --- Dataset alternativo ---
    path_alt = kagglehub.dataset_download("michellevp/dataset-phishing-domain-detection-cybersecurity")
    files_alt = [f for f in os.listdir(path_alt) if f.endswith(('.csv', '.tsv', '.json', '.jsonl', '.xml', '.parquet', '.feather', '.sqlite', '.sqlite3', '.db', '.db3', '.s3db', '.dl3', '.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods', '.odt'))]
    if not files_alt:
        print("No se encontraron archivos de datos soportados en el dataset alternativo.")
        exit()
    file_path_alt = os.path.join(path_alt, files_alt[0])
    if file_path_alt.endswith('.csv'):
        df_alt = pd.read_csv(file_path_alt)
    elif file_path_alt.endswith('.tsv'):
        df_alt = pd.read_csv(file_path_alt, sep='\t')
    elif file_path_alt.endswith('.json'):
        df_alt = pd.read_json(file_path_alt)
    elif file_path_alt.endswith('.xlsx'):
        df_alt = pd.read_excel(file_path_alt)
    else:
        print("Tipo de archivo no soportado automáticamente en alternativo. Cárgalo manualmente.")
        exit()
    # Detecta columna objetivo
    if 'phishing' in df_alt.columns:
        target_col_alt = 'phishing'
    elif 'Result' in df_alt.columns:
        target_col_alt = 'Result'
    else:
        print("No se encontró una columna objetivo reconocida en alternativo ('phishing' o 'Result').")
        print(f"Columnas disponibles: {df_alt.columns.tolist()}")
        exit()
    df_alt = df_alt.rename(columns={target_col_alt: 'target'})
    print(f"Dataset alternativo: {df_alt.shape[0]} filas, {df_alt.shape[1]} columnas")
    # --- Dataset original ---
    path_orig = kagglehub.dataset_download("hasibur013/phishing-data")
    files_orig = [f for f in os.listdir(path_orig) if f.endswith('.csv')]
    if not files_orig:
        print("No se encontró ningún archivo CSV en el dataset original.")
        exit()
    file_path_orig = os.path.join(path_orig, files_orig[0])
    df_orig = pd.read_csv(file_path_orig, encoding='latin-1')
    if 'index' in df_orig.columns:
        df_orig = df_orig.drop(columns=['index'])
    if 'Result' in df_orig.columns:
        target_col_orig = 'Result'
    elif 'phishing' in df_orig.columns:
        target_col_orig = 'phishing'
    else:
        print("No se encontró una columna objetivo reconocida en original ('Result' o 'phishing').")
        print(f"Columnas disponibles: {df_orig.columns.tolist()}")
        exit()
    df_orig = df_orig.rename(columns={target_col_orig: 'target'})
    print(f"Dataset original: {df_orig.shape[0]} filas, {df_orig.shape[1]} columnas")
    # --- Dataset local: buscar cualquier archivo que empiece por RT_IOT y termine en .csv en subcarpetas ---
    local_files = []
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.startswith('RT_IOT') and f.endswith('.csv'):
                local_files.append(os.path.join(root, f))
    if local_files:
        for local_file in local_files:
            print(f"Cargando archivo local: {local_file}")
            df_local_tmp = pd.read_csv(local_file)
            # Detecta columna objetivo
            if 'phishing' in df_local_tmp.columns:
                target_col_local = 'phishing'
            elif 'Result' in df_local_tmp.columns:
                target_col_local = 'Result'
            elif 'target' in df_local_tmp.columns:
                target_col_local = 'target'
            elif 'Attack_type' in df_local_tmp.columns:
                target_col_local = 'Attack_type'
                # Convertir Attack_type a binario: 0 para Normal, 1 para otro
                df_local_tmp['target'] = (df_local_tmp['Attack_type'] != 'Normal').astype(int)
                df_local_tmp = df_local_tmp.drop(columns=['Attack_type'])
            else:
                print(f"No se encontró una columna objetivo reconocida en {local_file} ('phishing', 'Result', 'target' o 'Attack_type').")
                print(f"Columnas disponibles: {df_local_tmp.columns.tolist()}")
                continue
            if target_col_local != 'Attack_type':
                df_local_tmp = df_local_tmp.rename(columns={target_col_local: 'target'})
            print(f"Dataset local {local_file}: {df_local_tmp.shape[0]} filas, {df_local_tmp.shape[1]} columnas")
            if 'df_local' in locals() and df_local is not None:
                df_local = pd.concat([df_local, df_local_tmp], ignore_index=True)
            else:
                df_local = df_local_tmp
    else:
        print("No se encontró ningún archivo local RT_IOT*.csv en la carpeta ni subcarpetas. Solo se usarán los datasets de Kaggle.")
        df_local = None
    # --- Dataset local: agregar archivo específico 'RT_IOT2022.csv' si existe ---
    specific_file = 'RT_IOT2022.csv'
    if os.path.exists(specific_file):
        print(f"Cargando archivo local específico: {specific_file}")
        df_specific = pd.read_csv(specific_file)
        # Detecta columna objetivo
        if 'phishing' in df_specific.columns:
            target_col_specific = 'phishing'
        elif 'Result' in df_specific.columns:
            target_col_specific = 'Result'
        elif 'target' in df_specific.columns:
            target_col_specific = 'target'
        elif 'Attack_type' in df_specific.columns:
            target_col_specific = 'Attack_type'
            df_specific['target'] = (df_specific['Attack_type'] != 'Normal').astype(int)
            df_specific = df_specific.drop(columns=['Attack_type'])
        else:
            print(f"No se encontró una columna objetivo reconocida en {specific_file} ('phishing', 'Result', 'target' o 'Attack_type').")
            print(f"Columnas disponibles: {df_specific.columns.tolist()}")
            df_specific = None
        if df_specific is not None:
            if target_col_specific != 'Attack_type':
                df_specific = df_specific.rename(columns={target_col_specific: 'target'})
            print(f"Dataset local {specific_file}: {df_specific.shape[0]} filas, {df_specific.shape[1]} columnas")
            if 'df_local' in locals() and df_local is not None:
                df_local = pd.concat([df_local, df_specific], ignore_index=True)
            else:
                df_local = df_specific
    # --- Unir todos los datasets ---
    all_columns = sorted(set(df_alt.columns) | set(df_orig.columns) | (set(df_local.columns) if df_local is not None else set()))
    df_alt = df_alt.reindex(columns=all_columns)
    df_orig = df_orig.reindex(columns=all_columns)
    if df_local is not None:
        df_local = df_local.reindex(columns=all_columns)
        df_total = pd.concat([df_orig, df_alt, df_local], ignore_index=True)
    else:
        df_total = pd.concat([df_orig, df_alt], ignore_index=True)
    print(f"Dataset combinado: {df_total.shape[0]} filas, {df_total.shape[1]} columnas")
    print("Columnas disponibles en df_total:", df_total.columns.tolist())

    # Define SOLO los features que ya existen en tu DataFrame y que puedes usar para el modelo
    FEATURES = [
        'Abnormal_URL ',
        'Prefix_Suffix ',
        'SSLfinal_State ',
        'Shortining_Service ',
        'having_At_Symbol ',
        'having_Sub_Domain '
    ]

    # Manejo de valores nulos antes de seleccionar features
    df_total = df_total.fillna(0)  # O usa df_total.dropna() si prefieres eliminar filas

    # Filtra el DataFrame solo con los features seleccionados
    X = df_total[FEATURES]
    y = df_total['target']

    # División en train/test para evaluación
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, classification_report
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    model = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
    print("Entrenando el modelo Random Forest SOLO con los features seleccionados...")
    model.fit(X_train, y_train)
    print("Entrenamiento completado.")

    # Evaluación
    y_pred = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # Guarda el modelo en la ruta que usa el backend
    os.makedirs('social engineer/model', exist_ok=True)
    joblib.dump(model, 'social engineer/model/phishing_model_rf.joblib')
    print("Modelo Random Forest guardado en: social engineer/model/phishing_model_rf.joblib")

    # Guarda la lista de features
    with open('social engineer/model/features.json', 'w') as f:
        json.dump(FEATURES, f)
    print("Características usadas guardadas en: social engineer/model/features.json")

    # Verifica las columnas del modelo entrenado
    print("\n--- VERIFICACIÓN DEL MODELO GUARDADO ---")
    loaded_model = joblib.load('social engineer/model/phishing_model_rf.joblib')
    try:
        print("n_features_in_:", loaded_model.n_features_in_)
        print("feature_names_in_:", getattr(loaded_model, 'feature_names_in_', 'No disponible'))
    except Exception as e:
        print(f"No se pudo obtener información de features del modelo: {e}")

    # --- Verificación de archivos exportados ---
    print("\n--- Verificación de archivos exportados ---")
    for fname in ['model/features.json', 'model/phishing_model_rf.joblib']:
        if os.path.exists(fname):
            size = os.path.getsize(fname)
            print(f"{fname}: {size} bytes")
            if fname.endswith('.json'):
                with open(fname, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                        print(f"Primeros 200 caracteres: {str(data)[:200]}")
                    except Exception as e:
                        print(f"Error al leer {fname} como JSON: {e}")
        else:
            print(f"{fname} NO existe")
except Exception as e:
    print(f"Error general en el procesamiento: {e}")