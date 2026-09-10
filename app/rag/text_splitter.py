from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text(
        text: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
) -> list[str]:


    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks = splitter.split_text(text)

    return chunks