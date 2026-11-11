def pipeline(question: str) -> str:

    """
    Main PlantIQ query pipeline.

    Future steps:
    1. Process the question.
    2. Generate question embeddings.
    3. Retrieve relevant document chunks.
    4. Retrieve related equipment information.
    5. Build context.
    6. Generate an answer using an LLM.
    """

    answer = (
        f"PlantIQ received your question: {question}. "
        "The query pipeline is working. "
        "AI processing will be integrated next."
    )

    return answer