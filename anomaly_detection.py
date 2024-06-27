import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import LocalOutlierFactor
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.cluster import KMeans
import warnings

class AnomalyDetection:
    def __init__(self, time_series, params):
        self.time_series = time_series
        self.params = params

    # Método IQR
    def detect_iqr(self):
        q25, q75 = np.percentile(
            self.time_series, 25), np.percentile(self.time_series, 75)
        iqr = q75 - q25
        lower_bound = q25 - 1.5 * iqr
        upper_bound = q75 + 1.5 * iqr
        anomalies = [(i, x) for i, x in enumerate(self.time_series)
                     if x < lower_bound or x > upper_bound]
        return anomalies

    # Método Z-Score
    def detect_z_score(self):
        threshold = float(self.params["Z-Score"]["threshold"])
        mean = np.mean(self.time_series)
        std_dev = np.std(self.time_series)
        anomalies = [(i, x) for i, x in enumerate(self.time_series)
                     if abs((x - mean) / std_dev) > threshold]
        return anomalies

    # Método Média Móvel
    def detect_moving_average(self):
        window = int(self.params["Média Móvel"]["window"])
        threshold = float(self.params["Média Móvel"]["threshold"])
        moving_avg = pd.Series(self.time_series).rolling(window=window).mean()
        anomalies = [(i, x) for i, x in enumerate(self.time_series) if abs(
            x - moving_avg[i]) > threshold * np.std(self.time_series)]
        return anomalies

    # Método LOF
    def detect_lof(self):
        n_neighbors = int(self.params["LOF"]["n_neighbors"])
        threshold = float(self.params["LOF"]["threshold"])
        lof = LocalOutlierFactor(n_neighbors=n_neighbors)
        y_pred = lof.fit_predict(np.array(self.time_series).reshape(-1, 1))
        anomalies = [(i, x) for i, (x, pred) in enumerate(
            zip(self.time_series, y_pred)) if pred == -1]
        return anomalies

    # Método Decomposição Sazonal
    def detect_seasonal_decompose(self):
        model = self.params["Decomposição Sazonal"]["model"]
        period = int(self.params["Decomposição Sazonal"]["period"])
        decomposition = seasonal_decompose(
            self.time_series, model=model, period=period)
        residual = decomposition.resid
        mean_residual = np.nanmean(residual)
        std_residual = np.nanstd(residual)
        anomalies = [(i, self.time_series[i]) for i, x in enumerate(
            residual) if abs(x - mean_residual) > 3 * std_residual]
        return anomalies

    # Método K-Means
    def detect_kmeans(self):
        n_clusters = int(self.params["K-Means"]["n_clusters"])
        threshold = float(self.params["K-Means"]["threshold"])
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", FutureWarning)
            reshaped_data = np.array(self.time_series).reshape(-1, 1)
            kmeans = KMeans(n_clusters=n_clusters, n_init=10)
            kmeans.fit(reshaped_data)
            centers = kmeans.cluster_centers_
            labels = kmeans.labels_
            distances = [np.linalg.norm(x - centers[labels[i]])
                         for i, x in enumerate(reshaped_data)]
            mean_distance = np.mean(distances)
            std_distance = np.std(distances)
            anomalies = [(i, self.time_series[i]) for i, x in enumerate(
                reshaped_data) if distances[i] > mean_distance + threshold * std_distance]
        return anomalies

    # Método para plotar as anomalias
    def plot_anomalies(self, anomalies):
        plt.figure(figsize=(10, 6))
        plt.plot(self.time_series, label='Série Temporal')
        if anomalies:
            indices, values = zip(*anomalies)
            plt.scatter(indices, values, color='red', label='Anomalias')
        plt.legend()
        plt.xlabel('Índice')
        plt.ylabel('Valor')
        plt.title('Detecção de Anomalias na Série Temporal')
        plt.show()

    # Método para selecionar o método
    def detect_method(self, method):
        return {
            "IQR": self.detect_iqr,
            "Z-Score": self.detect_z_score,
            "Média Móvel": self.detect_moving_average,
            "LOF": self.detect_lof,
            "Decomposição Sazonal": self.detect_seasonal_decompose,
            "K-Means": self.detect_kmeans,
        }[method]()

    # Método para comparar os métodos
    def compare_methods(self, selected_methods):
        methods = {
            "IQR": self.detect_iqr,
            "Z-Score": self.detect_z_score,
            "Média Móvel": self.detect_moving_average,
            "LOF": self.detect_lof,
            "Decomposição Sazonal": self.detect_seasonal_decompose,
            "K-Means": self.detect_kmeans,
        }

        total_data_points = len(self.time_series)
        comparison_results = []
        for method_name in selected_methods:
            anomalies = methods[method_name]()
            num_anomalies = len(anomalies)
            proportion_anomalies = num_anomalies / total_data_points
            comparison_results.append({
                "Método": method_name,
                "Número de anomalias": num_anomalies,
                "Proporção de anomalias na base": f"{proportion_anomalies:.2%}"
            })

        return pd.DataFrame(comparison_results)
