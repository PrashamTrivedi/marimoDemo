import marimo

__generated_with = "0.11.9"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    from aiUtils import prompt, listModels

    model_list = listModels()
    return listModels, mo, model_list, prompt


@app.cell
def form(mo, model_list):
    # Convert tuple (provider, model) to "model (provider)" format
    formatted_models = {
        f"{model}({provider})": f"{model}" for provider, model in model_list
    }

    print(formatted_models)
    models_dropdown = mo.ui.multiselect(
        options=formatted_models,
        label="select model",
    )
    multi_model_checkbox = mo.ui.checkbox(label="Run on All Models", value=False)

    prompt_text_area = mo.ui.text_area(label="Prompt", full_width=True)
    reasoning_checkbox = mo.ui.checkbox(
        label="Select Reasoning Models",
        value=False,
    )
    reasoning_effort=mo.ui.dropdown(label="Reasoning efforts for o series models", options=["low", "medium", "high"], value="low")
    reasoning_tokens=mo.ui.number(label="Number of tokens for reasoning, Anthropic 3-7 model.", value=1024)
    form = (
        mo.md(
            r"""
        # Prompt Testing
        {prompt}
        {model}
        {multi_model}
        {reasoning_effort}
        {reasoning_tokens}
        """
        )
        .batch(
            prompt=prompt_text_area,
            model=models_dropdown,
            multi_model=multi_model_checkbox,
            reasoning_effort=reasoning_effort,
            reasoning_tokens=reasoning_tokens
        )
        .form()
    )

    form
    return (
        form,
        formatted_models,
        models_dropdown,
        multi_model_checkbox,
        prompt_text_area,
        reasoning_checkbox,
        reasoning_effort,
        reasoning_tokens,
    )


@app.cell
def _(form, mo):
    print(form.value.items())
    mo.stop(not form.value or not len(form.value), "")

    # Format the form data for the table
    formatted_data = {}
    for key, value in form.value.items():
        print(value)
        if isinstance(value, list):
            formatted_data[key] = ",\n".join(value)
        else:
            formatted_data[key] = value

    # Create and display the table
    table = mo.ui.table(
        [formatted_data],  # Wrap in a list to create a single-row table
        label="Input",
        selection=None,
    )

    mo.md(f"# Form Values\n\n{table}")
    table
    return formatted_data, key, table, value


@app.cell
def _(form, listModels, mo, prompt):
    prompt_responses = []

    models_to_run = form.value["model"]
    if form.value["multi_model"]:
        models_to_run = listModels()

    reasoning_effort_value=form.value['reasoning_effort']
    reasoning_tokens_value=form.value['reasoning_tokens']

    print(models_to_run,reasoning_effort_value,reasoning_tokens_value)
    extra_args={}
    with mo.status.spinner(title="Running prompts on all models...") as spinner:
        for model in models_to_run:
            spinner.update(f"Running prompt on {model}...")
            if model.startswith(("o1", "o3")):
                extra_args['reasoning_effort']=reasoning_effort_value
            elif "reasoning" in model and reasoning_tokens_value>=1024:
                extra_args["thinking"]={
                    "type": "enabled",
                    "budget_tokens": reasoning_tokens_value
                }
            else:
                extra_args={}
            response = prompt(form.value["prompt"], model, extra_args)
            prompt_responses.append(
                {
                    "model_id": model,
                    "output": mo.md(response),
                }
            )
    prompt_responses
    return (
        extra_args,
        model,
        models_to_run,
        prompt_responses,
        reasoning_effort_value,
        reasoning_tokens_value,
        response,
        spinner,
    )


@app.cell
def _(mo, prompt_responses):
    mo.stop(not len(prompt_responses), "")

    # We need to create tabs from prompt_responses using below example
    # tabs = mo.ui.tabs(
        # {"Heading 1": tab1, "Heading 2": tab2}, value="Heading 2"
    # )
    tabs = mo.ui.tabs(
        {
            f"{response['model_id']}": response["output"]
            for response in prompt_responses
        },
        value=f"{prompt_responses[0]['model_id']}",
    )
    tabs
    return (tabs,)


if __name__ == "__main__":
    app.run()
