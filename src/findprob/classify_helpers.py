
from rich.progress import track

from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

import json
import os


PROMPT_TEMPLATE_TOPICS_GIVEN = """You are an experienced professor in {field} who is an expert at teaching.
You will be given a problem from a {field} course, and you should be able to identify the topic the problem
is trying to assess. Here are some sections of the textbook that might be related:
{context}

Here is a list of the topics that are included in this course, along with a short
description in parentheses:
{topics}

Your task is to identify which of the above topics the problem below is trying to assess:
{input}

Before you give a final answer, you may think about which concepts might be required
to solve the problem. Afterwards, pick one or more of the topics from the above list,
following these rules:

1. All the topic(s) you pick must come from the list given above. The topic names
should match exactly, except you must not include the information in parentheses.
2. If none of the topics apply, use "other".
3. The order of topic(s) chosen does not matter.

Only output valid json, and do not include any other information. Respond in the format below:
{{
    "topics": ["topic choice(s) here"]
}}
"""


def get_vectorstore_retriever(vec_dir, k):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(
        vec_dir,
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": k})


def topics_given_classify(in_dir, field, retriever, topics_file):
    # setup LLM + RAG
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        max_tokens=256,
    )
    prompt_template = PromptTemplate(
        template=PROMPT_TEMPLATE_TOPICS_GIVEN,
        input_variables=["field", "context", "topics", "input"],
    )
    docs_chain = create_stuff_documents_chain(llm, prompt_template)
    retrieval_chain = create_retrieval_chain(retriever, docs_chain)

    # read topics file
    with open(topics_file) as f:
        topics = f.read()

    # traverse in_dir and classify problems as you go
    classifications = {}
    for dir_path, dir_names, file_names in track(os.walk(in_dir)):
        for fname in file_names:
            problem_path = os.path.join(dir_path, fname) 

            with open(problem_path) as f:
                problem_text = f.read()

            response = retrieval_chain.invoke({
                "field": field,
                "input": problem_text, # TODO fix_curly_brace?
                "topics": topics
            })
            answer = response["answer"]

            try:
                answer_json = json.loads(answer)
                predicted_topics = answer_json['topics']
            except Exception as e:
                print(f"Classification for problem {problem_path} errored:", e)
                predicted_topics = []
            
            classifications[problem_path] = predicted_topics
    
    return classifications


def no_topics_classify():
    pass


def feedback_classify():
    pass


def save_classifications(classifications, out_file):
    with open(out_file, 'w') as f:
        json.dump(classifications, f, indent=4)
