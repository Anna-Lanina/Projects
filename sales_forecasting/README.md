# Описание проекта

**Задача:** Спрогнозировать продажи в разрезе id товаров на август, сентябрь 2021 года.

Заполнить и направить для проверки таблицу на вкладке result, а также notebook с алгоритмом и его кратким описанием.

Проверка будет производиться на уровне id товаров и family по MAPE, MdAPE.

# Результаты исследования

1. были проведены анализ временных рядов и обработка данных.

2. для прогнозирования рядов были вбраны модели: линейная регрессия, дерево решени, случайный лес и градиентный бустинг - catboost. Из них наилучшее качество по MAPE и MDAPE показал Catboost

mape на тестовой выборке 20.57

mdape на тестовой выборке 16.71

3. подготовлены ряд выгрузок с предсказаниями для листов data (test и train) и result

4. в ходе данного исследования был построен бейзлайн как в плане подготовки данных, так и в плане выбора моделей. Помимо подбора моделей машинного обучения и их гиперпараметро также стоит попробовать аддитивные модели, вроде модели Хольта и др., а также модели вроде SARIMA (в данном исследовании не рассматривается, так как требует значительно больше времени на подгтовку данных и подбор параметров)