import pandas as pd
import numpy as np
import plotly.graph_objs as go
from models.HN_Model import HNGarch


class backt_predict:

    def __init__(self, ts):
        self.ts = ts

    def backtesting(self, n_reps=1000, n_teps=1):

        ts = self.ts

        # Inicializar la instancia de la clase HNGarch con los primeros 3 valores de la serie
        model = HNGarch(ts)
        model.GARCH_fit()
        vec1 = model.hist_simulation()

        x = np.arange(-5, np.log(7000), 0.01)
        x[x == 0] = 1e-10

        pdf = model.pdf_func(x, 90)
        cdf = model.cdf_func(x, 90)

        std_errs = model.get_std_errors()

        model.lr_vol()

        # vector of variances of the estimated model
        vec = model.ts_var(vec=True)
        # Lista para almacenar las predicciones del siguiente precio
        predictions = []

        # Realizar backtesting para cada valor de la serie, comenzando desde el segundo valor
        for i in range(len(ts)-1):

            # Predecir el siguiente precio y agregarlo a la lista de predicciones
            predictions.append(model.montecarlo_sim2(n_reps, n_teps))

            model.timeseries = ts.iloc[i:]

        # Crear un DataFrame con los precios reales y las predicciones
        backtest_results = pd.DataFrame({
            # Ignoramos el primer valor ya que no hay una predicción para él
            'Real Price': ts.iloc[1:].values,
            'Predicted Price': predictions
        }, index=ts.index[1:])  # Ignoramos el primer índice ya que no hay una predicción para él

        return backtest_results

    def prediction(self, number_scenarios=1000, n_steps=252, vec=True):

        ts = self.ts

        # init of the class
        model = HNGarch(ts)

        # fitting the model
        model.GARCH_fit()

        vec1 = model.hist_simulation()

        x = np.arange(-5, np.log(7000), 0.01)
        x[x == 0] = 1e-10

        pdf = model.pdf_func(x, 90)
        cdf = model.cdf_func(x, 90)

        model.lr_vol()

        # vector of variances of the estimated model
        vec = model.ts_var(vec)

        # # plot the simulated garch model over a 252d future interval
        j = pd.DataFrame()
        # how many simulations to plot
        number_scenarios = 10000
        for i in range(number_scenarios):
            y = pd.DataFrame(model.GARCH_single_fc(n_steps, True))
            j = pd.concat([j, y], axis=1)

        j['Promedio'] = j.mean(axis=1)
        j['Desviacion'] = j.std(axis=1)

        # Calcula el límite superior e inferior ajustado
        limite_superior = j['Promedio'] + j['Desviacion']
        limite_inferior = j['Promedio'] - j['Desviacion']

        # Agrega estas columnas al DataFrame
        j['Limite_Superior'] = limite_superior
        j['Limite_Inferior'] = limite_inferior

        # Asignar nombres a los índices de los DataFrames
        # ts.index.name = 'Date'
        # j.index.name = 'Date'

        # # Concatenar los DataFrames
        # df2 = pd.concat([ts, j], axis=1)

        # # Resetear el índice para convertirlo en una columna
        # df2 = df2.reset_index()

        # # Eliminar la columna 'index' si es que se creó al resetear el índice
        # if 'index' in df2.columns:
        #     df2 = df2.drop(['index'], axis=1)

        # # Mostrar las primeras filas del DataFrame resultante
        # df2.drop('Date', axis=1, inplace=True)
        # df2 = df2[['']]

        j = j[['Promedio', 'Desviacion', 'Limite_Superior', 'Limite_Inferior']]

        return j


def data(ts):

    model = backt_predict(ts)
    backtest_results = model.backtesting()
    predict = model.prediction()

    # Asignar nombres a los índices de los DataFrames
    predict.index.name = 'Date'
    backtest_results.index.name = 'Date'

    # Concatenar los DataFrames
    data = pd.concat([backtest_results, predict], axis=1)

    # Resetear el índice para convertirlo en una columna
    data = data.reset_index()

    # Eliminar la columna 'index' si es que se creó al resetear el índice
    if 'index' in data.columns:
        data = data.drop(['index'], axis=1)

    # Mostrar las primeras filas del DataFrame resultante
    data.drop('Date', axis=1, inplace=True)
    data['media'] = data.iloc[:, 1:].mean(axis=1)

    return data


def graph(data):

    # Create traces
    trace1 = go.Scatter(
        x=data.index, y=data['Real Price'], mode='lines', name='Real Price', line=dict(color='blue'))
    trace2 = go.Scatter(x=data.index, y=data['Predicted Price'],
                        mode='lines', name='Predicted Price', line=dict(color='red'))
    trace3 = go.Scatter(x=data.index, y=data['Promedio'], mode='lines',
                        name='Valor esperado Heston', line=dict(color='white', dash='dash'))
    trace4 = go.Scatter(x=data.index, y=data['Limite_Superior'], mode='lines',
                        name='limites Heston', line=dict(color='orange', dash='dash'))
    trace5 = go.Scatter(x=data.index, y=data['Limite_Inferior'], mode='lines', line=dict(
        color='orange', dash='dash'))

    # Create layout
    layout = go.Layout(
        width=1000,
        height=450,
        legend=dict(font=dict(color='white')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',

        xaxis=dict(title='Periodo', showgrid=True, linecolor='white',
                   ticks='outside', gridcolor='rgba(255, 255, 255, 0.1)'),
        yaxis=dict(title='Precio', showgrid=True, linecolor='white',
                   ticks='outside', gridcolor='rgba(255, 255, 255, 0.1)'),
        margin=dict(l=0, r=50, b=50, t=50),

    )

    # Combine traces into data list
    data_plotly = [trace1, trace2, trace3, trace4, trace5]

    # Create figure
    fig = go.Figure(data=data_plotly, layout=layout)

    # Show figure
    return fig
