from sklearn.metrics.pairwise import cosine_similarity

def find_best_chunk(question_embedding, chunk_embeddings, chunks):

    similarities = cosine_similarity(
        [question_embedding],
        chunk_embeddings
    )[0]

    best_index = similarities.argmax()

    return chunks[best_index], similarities[best_index]