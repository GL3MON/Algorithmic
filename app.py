from Algorithmic.pipeline.graph import Graph
from typing import List
import gradio as gr
        

def main(question: str, test_cases: str, required_output: str):
    graph = Graph()
    app = graph.app()
    inputs = {"question": question, "error":"", "test_cases": test_cases, "required_output": required_output, "regenerate_count":0}
    for output in app.stream(inputs, {"recursion_limit": 50}):
        for key, value in output.items():
            print(f"Finished running: {key}:")
    
    return {final_code: value["final_code"], logic_code: value["logic_code"], terminal_output: value['terminal_output'], error: value["error"], math_analysis: value['math_analysis'], question_analysis: value['question_analysis']}      

with gr.Blocks() as gradio_app:        
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("# Algorithmic")
    
    with gr.Row():
        question = gr.Textbox(label="Question", lines=5, max_lines=5, show_label=True)
        test_cases = gr.Textbox(label="Test Cases", lines=5, max_lines=5, show_label= True)
        required_output = gr.Textbox(label="True Values", lines=5, max_lines=5, show_label= True)
    
    with gr.Row():
        final_code = gr.Code(language="python", lines=7, show_label=True, interactive=False)
        logic_code = gr.Code(language="python", lines=7, show_label=True, interactive=False)
    
    with gr.Row():
        math_analysis = gr.Textbox(label="Math Analysis", lines=7, max_lines=7, show_label= True, interactive=False)
        question_analysis = gr.Textbox(label="Question Analysis", lines=7, max_lines=7, show_label= True, interactive=False)
    
    with gr.Row():
        terminal_output = gr.Code(language="shell", lines=3, show_label=True, interactive=False)
        error = gr.Code(language="shell", lines=3, show_label=True, interactive=False)
        with gr.Column():
            generate_btn = gr.Button("Generate")
            generate_btn.click(main, inputs=[question, test_cases, required_output], outputs=[final_code, logic_code, terminal_output, error, math_analysis, question_analysis])
    


if __name__ == "__main__":
    gradio_app.launch()