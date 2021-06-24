import joblib


models_description = joblib.load('./trained_models/trainedModelsData.jl')
sentiment_model = joblib.load('./trained_models/sentimentSGDmodel.jl')
topic_model = joblib.load('./trained_models/topicLDAmodel.jl')

if __name__ == '__main__':
    print("Sentiment Model: ")
    print('Type: {}\nScore: {}'.format(
        models_description['sentiment_analysis']['name'], models_description['sentiment_analysis']['score']))
    print("\nTopic Model: ")
    print('Perplexity Score: {}\nCoherence Score: {}'.format(
        models_description['topic_modeling']['perplexity_score'], models_description['topic_modeling']['coherence_score']))

    print('''\nModels Ready For Use !!!''')
