"""Reproduz o experimento supervisionado publicado, a partir dos insumos congelados.

Uso: python reproduzir.py --verificar | --selecionados | --completo
Não faz rede, não altera referências, não carrega objetos pickle.
"""
import argparse
import gzip
import hashlib
import json
import pathlib

import numpy as np
from sklearn.ensemble import (RandomForestClassifier, RandomForestRegressor,
    ExtraTreesClassifier, ExtraTreesRegressor,
    HistGradientBoostingClassifier, HistGradientBoostingRegressor)
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import roc_auc_score, brier_score_loss, mean_absolute_error, mean_squared_log_error
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = pathlib.Path(__file__).resolve().parent


def estimadores(familia):
    """Parâmetros idênticos aos usados no experimento V2; semente fixa."""
    if familia == 'rf':
        return (RandomForestClassifier(n_estimators=180, max_depth=12, min_samples_leaf=20,
                    max_features=.7, n_jobs=4, random_state=42),
                RandomForestRegressor(n_estimators=180, max_depth=12, min_samples_leaf=12,
                    max_features=.7, n_jobs=4, random_state=42))
    if familia == 'extra':
        return (ExtraTreesClassifier(n_estimators=180, max_depth=16, min_samples_leaf=15,
                    max_features=.8, n_jobs=4, random_state=42),
                ExtraTreesRegressor(n_estimators=180, max_depth=16, min_samples_leaf=12,
                    max_features=.8, n_jobs=4, random_state=42))
    if familia == 'hgb':
        return (HistGradientBoostingClassifier(max_iter=150, max_leaf_nodes=15,
                    l2_regularization=10, random_state=42),
                HistGradientBoostingRegressor(max_iter=150, max_leaf_nodes=15,
                    l2_regularization=10, random_state=42))
    return (make_pipeline(StandardScaler(), LogisticRegression(C=.1, max_iter=1500)),
            make_pipeline(StandardScaler(), Ridge(alpha=100)))


def carregar():
    manifesto = json.loads((ROOT / 'manifesto.json').read_text(encoding='utf-8'))
    for nome, esperado in manifesto['sha256'].items():
        atual = hashlib.sha256((ROOT / nome).read_bytes()).hexdigest()
        assert atual == esperado, f'Integridade inválida: {nome}'
    with gzip.open(ROOT / 'dados/experimento_congelado.json.gz', 'rt', encoding='utf-8') as f:
        dados = json.load(f)
    return dados


def executar(modo):
    dados = carregar()
    rows, sets = dados['rows'], dados['features']
    y = np.array([r['alvo_arrematada'] for r in rows])
    lance = np.array([r['lance_reais'] for r in rows])
    assert np.all((lance > 0) == (y == 1))
    assert len({(r['rodada'], r['area'], r['processo']) for r in rows}) == len(rows)

    def indices(rodadas):
        return np.array([i for i, r in enumerate(rows) if r['rodada'] in rodadas])

    def sem_sobreposicao(treino, avaliacao):
        processos = {rows[i]['processo'] for i in avaliacao}
        return np.array([i for i in treino if rows[i]['processo'] not in processos])

    validacao, teste = indices([5]), indices([8])
    treino_escolha = sem_sobreposicao(indices([1, 2, 3]), validacao)
    treino_final = sem_sobreposicao(indices([1, 2, 3, 4, 5]), teste)
    assert treino_final.tolist() == dados['final_train_indices']
    assert teste.tolist() == dados['test_indices']
    assert (len(treino_escolha), len(validacao), len(treino_final), len(teste)) == (10110, 4465, 16223, 4950)
    referencia = json.loads((ROOT / 'resultados_referencia/experimento_ml_v2.json').read_text(encoding='utf-8'))
    saida = {'integridade': 'verificada', 'observacoes': len(rows), 'modo': modo}
    if modo == 'verificar':
        print(json.dumps(saida, ensure_ascii=False))
        return

    def matrizes(conjunto, treino, avaliacao):
        vetor = DictVectorizer(sparse=False)
        # Aprende categorias somente no treino; categorias novas são ignoradas.
        return (vetor.fit_transform([sets[conjunto][i] for i in treino]),
                vetor.transform([sets[conjunto][i] for i in avaliacao]))

    escolhido = referencia['chosen'].copy()
    if modo == 'completo':
        candidatos = [('rf', 'historico'), ('extra', 'historico'), ('hgb', 'basico'),
                      ('hgb', 'historico'), ('linear', 'historico'), ('hgb', 'territorial')]
        selecao = {}
        for familia, conjunto in candidatos:
            a, b = matrizes(conjunto, treino_escolha, validacao)
            clf, reg = estimadores(familia)
            clf.fit(a, y[treino_escolha])
            prob = clf.predict_proba(b)[:, 1]
            reg.fit(a[y[treino_escolha] == 1], np.log1p(lance[treino_escolha][y[treino_escolha] == 1]))
            pos = y[validacao] == 1
            pred = np.maximum(0, np.expm1(reg.predict(b[pos])))
            selecao[familia + '_' + conjunto] = {
                'auc': float(roc_auc_score(y[validacao], prob)),
                'brier': float(brier_score_loss(y[validacao], prob)),
                'rmsle': float(np.sqrt(mean_squared_log_error(lance[validacao][pos], pred))),
                'mae': float(mean_absolute_error(lance[validacao][pos], pred))}
            print('Concluído:', familia, conjunto, flush=True)
        escolhido = {'classifier': min(selecao, key=lambda k: selecao[k]['brier']),
                     'regressor': min(selecao, key=lambda k: selecao[k]['rmsle'])}
        assert escolhido == referencia['chosen'], 'Seleção difere do relatório publicado'
        saida['selecao'] = selecao

    previsoes = {}
    for tarefa, nome in escolhido.items():
        familia, conjunto = nome.split('_', 1)
        a, b = matrizes(conjunto, treino_final, teste)
        clf, reg = estimadores(familia)
        if tarefa == 'classifier':
            clf.fit(a, y[treino_final])
            previsoes['p'] = clf.predict_proba(b)[:, 1]
        else:
            pos = y[treino_final] == 1
            reg.fit(a[pos], np.log1p(lance[treino_final][pos]))
            previsoes['valor'] = np.maximum(0, np.expm1(reg.predict(b)))
        print('Reestimado:', nome, flush=True)
    pos = y[teste] == 1
    med = {'auc': float(roc_auc_score(y[teste], previsoes['p'])),
           'brier': float(brier_score_loss(y[teste], previsoes['p'])),
           'rmsle': float(np.sqrt(mean_squared_log_error(lance[teste][pos], previsoes['valor'][pos]))),
           'mae': float(mean_absolute_error(lance[teste][pos], previsoes['valor'][pos]))}
    for nome, valor in med.items():
        assert np.isclose(valor, referencia['test'][nome], rtol=1e-6, atol=1e-7), f'Métrica diferente: {nome}'
    saida.update({'escolhidos': escolhido, 'teste': med, 'comparacao_referencia': 'passou'})
    if modo == 'completo':
        a, b = matrizes('territorial', treino_final, teste)
        bandas = []
        for quantil in [.1, .9]:
            reg = HistGradientBoostingRegressor(loss='quantile', quantile=quantil,
                max_iter=150, max_leaf_nodes=15, l2_regularization=10, random_state=42)
            positivos = y[treino_final] == 1
            reg.fit(a[positivos], np.log1p(lance[treino_final][positivos]))
            bandas.append(np.maximum(0, np.expm1(reg.predict(b))))
        inferior, superior = np.minimum(*bandas), np.maximum(*bandas)
        cobertura = float(np.mean((lance[teste][pos] >= inferior[pos]) & (lance[teste][pos] <= superior[pos])))
        assert np.isclose(cobertura, referencia['interval']['observed_coverage'])
        saida['cobertura_retrospectiva'] = cobertura
    (ROOT / 'reproducao_resultado.json').write_text(json.dumps(saida, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(saida, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    grupo = parser.add_mutually_exclusive_group(required=True)
    for modo in ['verificar', 'selecionados', 'completo']:
        grupo.add_argument('--' + modo, action='store_const', const=modo, dest='modo')
    executar(parser.parse_args().modo)
