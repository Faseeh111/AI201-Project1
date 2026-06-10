import gradio as gr
from query import ask


def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""

    result = ask(question)

    answer = result["answer"]

    sources = "\n".join(f"• {source}" for source in result["sources"])

    return answer, sources


with gr.Blocks() as demo:
    gr.Markdown("# Beginner Rock Climbing Guide")
    gr.Markdown("Ask a question about beginner climbing, gear, grades, training, injury prevention, or etiquette.")

    question = gr.Textbox(label="Your question", placeholder="Example: What does 5.12a mean?")
    ask_button = gr.Button("Ask")

    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=5)

    ask_button.click(handle_query, inputs=question, outputs=[answer, sources])
    question.submit(handle_query, inputs=question, outputs=[answer, sources])


if __name__ == "__main__":
    demo.launch()