from rich.progress import track
from rich import print

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


PROMPT_TEMPLATE_NO_TOPICS = """You are an experienced professor in {field} who is an expert at teaching.
You will be given a problem from a {field} course, and you should be able to identify the topic the problem
is trying to assess. Here are some sections of the textbook that might be related:
{context}

Your task is to identify which of the above topics the problem below is trying to assess:
{input}

Before you give a final answer, you may think about which concepts might be required
to solve the problem. Afterwards, make a list of the topics that you believe this problem covers. 

Only output valid json, and do not include any other information. Respond in the format below:
{{
    "topics": ["topic choice(s) here"]
}}
"""


PROMPT_TEMPLATE_FEEDBACK = """You are an experienced professor in {field} who is an expert at teaching.
You will be given a problem from a {field} course, and you should be able to identify the topic the problem
is trying to assess. Here are some sections of the textbook that might be related:
{context}

Here is a list of the topics that are included in this course, along with a short
description in parentheses:
{topics}

Your task is to identify which of the above topics the problem below is trying to assess:
{input}

Before you give a final answer, you may think about which concepts might be required
to solve the problem. Afterwards, make a list of the topics that you believe this problem covers,
following these rules:

1. You can use any topics, including those outside of the ones given in the list above. If you 
use topic names given in the list above, they should match exactly except you must not include the 
information in parentheses.
2. The order of topic(s) chosen does not matter.

Only output valid json, and do not include any other information. Respond in the format below:
{{
    "topics": ["topic choice(s) here"]
}}
"""


def get_vectorstore_retriever(vec_dir, k):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(
        vec_dir, embeddings, allow_dangerous_deserialization=True
    )
    return vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": k})


def get_retrieval_chain(retriever, prompt_template):
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        max_tokens=256,
    )
    docs_chain = create_stuff_documents_chain(llm, prompt_template)
    return create_retrieval_chain(retriever, docs_chain)


def run_classifier(retrieval_chain, prompt_vars, in_dir):
    # traverse in_dir and classify problems as you go
    classifications = {}
    for dir_path, dir_names, file_names in track(
        os.walk(in_dir), description="Classifying problems..."
    ):
        for fname in file_names:
            problem_path = os.path.join(dir_path, fname)

            with open(problem_path) as f:
                problem_text = fix_curly_brace(f.read())

            curr_vars = prompt_vars | {"input": problem_text}  # merge dictionaries
            response = retrieval_chain.invoke(curr_vars)
            answer = response["answer"]

            try:
                answer_json = json.loads(answer)
                predicted_topics = answer_json["topics"]
            except Exception as e:
                print(f"[orange]Classification for problem {problem_path} errored, setting topics to empty array. Stack trace below:[/orange]")
                print(e)
                predicted_topics = []

            classifications[problem_path] = predicted_topics

    return classifications


def fix_curly_brace(s):
    # If the problem text includes curly braces, it is interpreted as a prompt template variable
    # so we want to replace them with {{ and }}
    return s.replace("{", "{{").replace("}", "}}")


def topics_given_classify(in_dir, field, retriever, topics_file):
    prompt_template = PromptTemplate(
        template=PROMPT_TEMPLATE_TOPICS_GIVEN,
        input_variables=["field", "context", "topics", "input"],
    )
    retrieval_chain = get_retrieval_chain(retriever, prompt_template)

    with open(topics_file) as f:
        topics = f.read()

    prompt_vars = {
        "field": field,
        "topics": topics,
    }
    return run_classifier(retrieval_chain, prompt_vars, in_dir)


def no_topics_classify(in_dir, field, retriever):
    prompt_template = PromptTemplate(
        template=PROMPT_TEMPLATE_NO_TOPICS,
        input_variables=["field", "context", "input"],
    )
    retrieval_chain = get_retrieval_chain(retriever, prompt_template)

    prompt_vars = {"field": field}
    return run_classifier(retrieval_chain, prompt_vars, in_dir)


def feedback_classify(in_dir, field, retriever, topics_file):
    prompt_template = PromptTemplate(
        template=PROMPT_TEMPLATE_FEEDBACK,
        input_variables=["field", "context", "topics", "input"],
    )
    retrieval_chain = get_retrieval_chain(retriever, prompt_template)

    with open(topics_file) as f:
        topics = f.read()

    prompt_vars = {
        "field": field,
        "topics": topics,
    }
    return run_classifier(retrieval_chain, prompt_vars, in_dir)


def save_classifications(classifications, out_file):
    with open(out_file, "w") as f:
        json.dump(classifications, f, indent=4)
