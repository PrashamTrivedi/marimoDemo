import marimo

__generated_with = "0.11.2"
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

    form = (
        mo.md(
            r"""
        # Prompt Testing
        {prompt}
        {model}
        {multi_model}

        """
        )
        .batch(
            prompt=prompt_text_area,
            model=models_dropdown,
            multi_model=multi_model_checkbox,
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

    print(models_to_run)

    with mo.status.spinner(title="Running prompts on all models...") as spinner:
        for model in models_to_run:
            spinner.update(f"Running prompt on {model}...")
            response = prompt(form.value["prompt"], model)
            prompt_responses.append(
                {
                    "model_id": model,
                    "output": mo.md(response),
                }
            )
    prompt_responses
    return model, models_to_run, prompt_responses, response, spinner


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
