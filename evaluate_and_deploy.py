import joblib
import os


change_sentiment = 0
change_topic = 0


def read_stored_model_description():
    previous_description = joblib.load('./trained_models/trainedModelsData.jl')
    new_description = joblib.load('./trained_models/newtrainedModelsData.jl')

    return (previous_description, new_description)


def compare_sentiment_models(prev_desc, new_desc):
    global change_sentiment
    if(new_desc['sentiment_analysis']['score'] > prev_desc['sentiment_analysis']['score']):
        change_sentiment == 1
        return (new_desc['sentiment_analysis']['name'], new_desc['sentiment_analysis']['score'])

    else:
        return (prev_desc['sentiment_analysis']['name'], prev_desc['sentiment_analysis']['score'])


def compare_topic_models(prev_desc, new_desc):
    global change_topic
    if(new_desc['topic_modeling']['coherence_score'] > prev_desc['topic_modeling']['coherence_score']):
        if(new_desc['topic_modeling']['perplexity_score'] < prev_desc['topic_modeling']['perplexity_score']):
            change_topic == 1
            return (new_desc['topic_modeling']['perplexity_score'], new_desc['topic_modeling']['coherence_score'])

    else:
        return (prev_desc['topic_modeling']['perplexity_score'], prev_desc['topic_modeling']['coherence_score'])


def deploy_better_models():
    try:
        prev_desc, new_desc = read_stored_model_description()
        validated_description = prev_desc.copy()

        validated_description['sentiment_analysis']['name'],
        validated_description['sentiment_analysis']['score'] = compare_sentiment_models(
            prev_desc, new_desc)
        validated_description['topic_modeling']['perplexity_score'], validated_description[
            'sentiment_analysis']['coherence_score'] = compare_topic_models(prev_desc, new_desc)

        global change_sentiment
        global change_topic
        if(change_sentiment == 1):
            sentiment_model = joblib.load(
                './trained_models/newsentimentSGDmodel.jl')
            os.remove('./trained_models/sentimentSGDmodel.jl')
            joblib.dump(sentiment_model, './trained_models/sentimentSGDmodel.jl')

        if(change_topic == 1):
            topic_model = joblib.load('./trained_models/newtopicLDAmodel.jl')
            os.remove('./trained_models/topicLDAmodel.jl')
            joblib.dump(topic_model, './trained_models/topicLDAmodel.jl')

        os.remove('./trained_models/trainedModelsData.jl')
        os.remove('./trained_models/newtrainedModelsData.jl')
        os.remove('./trained_models/newsentimentSGDmodel.jl')
        os.remove('./trained_models/newtopicLDAmodel.jl')

        joblib.dump(validated_description, './trained_models/trainedModelsData.jl')

    except FileNotFoundError:
        pass


if __name__ == '__main__':
    deploy_better_models()
